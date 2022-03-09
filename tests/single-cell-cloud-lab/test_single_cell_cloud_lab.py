import yaml
import subprocess
import os
import tempfile
import shutil
import json
import base64
import typing
from pprint import pprint

# TODO Add jsonschema validation


def read_yaml(file: str):
    assert os.path.exists(file)
    with open(file, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            # read in the data as a string
            data = stream.read()
    return data


def read_json_encoded(encoded_str):
    decoded_data = base64.b64decode(encoded_str)
    return json.loads(decoded_data)


class HelmChart(object):
    def __init__(self, chart_name: str, helm_dir: str, values_file: str):
        self.chart_name = chart_name
        self.helm_dir = helm_dir
        self.values_file = values_file
        self.values_data = read_yaml(values_file)
        self.rendered_data = {}
        self.application_data = ""
        assert os.path.exists(helm_dir)
        assert os.path.exists(values_file)

    def read_application_data(self):
        configmap_data = self.rendered_data["configmap.yaml"]
        application_yaml_str = configmap_data["data"]["application.yml"]
        application_data = yaml.load(application_yaml_str, Loader=yaml.FullLoader)
        self.application_data = application_data

    def render_helm_template_command(self, temp_dir: str):
        helm_command = f"""
        helm template \
            --output-dir {temp_dir} \
            --values {self.values_file} \
            {self.helm_dir}
        """
        helm_command = helm_command.strip()
        return helm_command

    def run_helm_template(self, files):
        self.rendered_data = {}
        with tempfile.TemporaryDirectory() as tmpdirname:
            helm_command = self.render_helm_template_command(temp_dir=tmpdirname)
            subprocess.run(["bash", "-c", helm_command])
            template_dir = os.path.join(tmpdirname, self.chart_name, "charts", "shinyproxy", "templates")
            for base_file in os.listdir(template_dir):
                file = os.path.join(template_dir, base_file)
                if (
                    os.path.isfile(file)
                    and base_file in files
                    or base_file == "configmap.yaml"
                ):
                    file_data = read_yaml(file)
                    base = os.path.basename(base_file)
                    self.rendered_data[base] = file_data
            self.read_application_data()


def test_values_auth_simple():

    chart_name = "single-cell-cloud-lab"
    sub_chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "single-cell-cloud-lab"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-auth-simple.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml", "configmap.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    secrets_json = read_json_encoded(secrets_data["data"]["secrets.json"])

    # pprint(secrets_json)
    # pprint(chart.application_data)
    assert "proxy" in secrets_json.keys()
    assert "users" in secrets_json["proxy"]
    assert secrets_json["proxy"]["users"][0]["groups"] == "scientists, users"
    assert secrets_json["proxy"]["users"][0]["name"] == "user01"
    assert secrets_json["proxy"]["users"][0]["password"] == "password"
    assert "containerBackend" not in chart.application_data["proxy"].keys()
    assert "landingPage" not in chart.application_data["proxy"].keys()
    assert "podWaitTime" not in chart.application_data["proxy"]["kubernetes"].keys()
    assert len(chart.application_data["proxy"]["specs"]) == 1
    assert "container-memory-limit" in chart.application_data["proxy"]["specs"][0]
    # pprint(chart.values_data)

    rendered_bucket = chart.application_data["proxy"]["specs"][0]["container-env"]["BUCKET"]
    values_bucket = chart.values_data["shinyproxy"]["proxy"]["specs"][0]["containerEnv"]["BUCKET"]
    assert rendered_bucket == values_bucket
