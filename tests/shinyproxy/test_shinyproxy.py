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
            template_dir = os.path.join(tmpdirname, self.chart_name, "templates")
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


def test_values_not_exists():
    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-auth-NOT-EXIST.yaml")
    try:
        chart = HelmChart(
            chart_name=chart_name, helm_dir=helm_dir, values_file=values_file
        )
    except AssertionError as e:
        pass


def test_values_auth_simple():

    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-auth-simple.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml", "configmap.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    secrets_json = read_json_encoded(secrets_data["data"]["secrets.json"])

    assert "proxy" in secrets_json.keys()
    assert "users" in secrets_json["proxy"]
    assert secrets_json["proxy"]["users"][0]["groups"] == "scientists, users"
    assert secrets_json["proxy"]["users"][0]["name"] == "user01"
    assert secrets_json["proxy"]["users"][0]["password"] == "password"

def test_values_auth_simple_dict():

    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-auth-simple-dict.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml", "configmap.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    secrets_json = read_json_encoded(secrets_data["data"]["secrets.json"])

    assert "proxy" in secrets_json.keys()
    assert "users" in secrets_json["proxy"]
    assert secrets_json["proxy"]["users"][0]["groups"] == "scientists, users"
    assert secrets_json["proxy"]["users"][0]["name"] == "user01"
    assert secrets_json["proxy"]["users"][0]["password"] == "password"

def test_values_ldap():

    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-auth-ldap.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    secrets_json = read_json_encoded(secrets_data["data"]["secrets.json"])

    assert "proxy" in secrets_json.keys()
    assert "ldap" in secrets_json["proxy"]
    assert secrets_json["proxy"]["ldap"]["group-search-base"] == "my-group-search-base"
    assert chart.application_data["proxy"]["authentication"] == "ldap"


def test_values_none():

    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-auth-none.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    secrets_json = read_json_encoded(secrets_data["data"]["secrets.json"])

    assert "proxy" in secrets_json.keys()
    assert chart.application_data["proxy"]["authentication"] == "none"


def test_values_social():

    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-auth-social.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    secrets_json = read_json_encoded(secrets_data["data"]["secrets.json"])

    assert "proxy" in secrets_json.keys()
    assert "social" in secrets_json["proxy"]
    assert secrets_json["proxy"]["social"]["facebook"]["app-id"] == "yourfacebookappid"
    assert (
        secrets_json["proxy"]["social"]["facebook"]["app-secret"]
        == "yourfacebookappsecret"
    )
    assert "github" not in secrets_json["proxy"]["social"]

    assert chart.application_data["proxy"]["authentication"] == "social"


def test_values_none():

    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-auth-none.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    secrets_json = read_json_encoded(secrets_data["data"]["secrets.json"])

    assert "proxy" in secrets_json.keys()
    assert chart.application_data["proxy"]["authentication"] == "none"


def test_values_specs():

    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-specs.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    secrets_json = read_json_encoded(secrets_data["data"]["secrets.json"])

    assert "proxy" in secrets_json.keys()
    assert chart.application_data["proxy"]["authentication"] == "simple"
    assert len(chart.application_data["proxy"]["specs"]) >= 1

    # Test that conversion to kebab case works properly
    assert "container-image" in chart.application_data["proxy"]["specs"][0].keys()
    assert "containerImage" in chart.values_data["proxy"]["specs"][0].keys()
    assert "service-account" in chart.application_data["proxy"]["specs"][0].keys()
    assert "serviceAccount" in chart.values_data["proxy"]["specs"][0].keys()

    assert chart.application_data["proxy"]["kubernetes"]["internal-networking"]
    assert chart.application_data["proxy"]["kubernetes"]["namespace"] == "default"


def test_values_specs_service_account():

    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-specs.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    assert "service-account" in chart.application_data["proxy"]["specs"][0].keys()
    assert "serviceAccount" in chart.values_data["proxy"]["specs"][0].keys()

    k8s_pod_patches = chart.application_data["proxy"]["specs"][0][
        "kubernetes-pod-patches"
    ]
    k8s_pod_patches_data = yaml.load(k8s_pod_patches, Loader=yaml.FullLoader)
    assert "/spec/serviceAccountName" == k8s_pod_patches_data[0]["path"]
    assert (
        chart.application_data["proxy"]["specs"][0]["service-account"]
        == k8s_pod_patches_data[0]["value"]
    )

def test_values_specs_dict():
    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-specs-dict.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    secrets_json = read_json_encoded(secrets_data["data"]["secrets.json"])

    assert "proxy" in secrets_json.keys()
    assert chart.application_data["proxy"]["authentication"] == "simple"
    assert len(chart.application_data["proxy"]["specs"]) >= 1


    # Test that conversion to kebab case works properly
    assert "container-image" in chart.application_data["proxy"]["specs"][0].keys()
    assert "containerImage" in chart.values_data["proxy"]["specs"].keys()
    assert "service-account" in chart.application_data["proxy"]["specs"][0].keys()
    assert "serviceAccount" in chart.values_data["proxy"]["specs"].keys()

    assert chart.application_data["proxy"]["kubernetes"]["internal-networking"]
    assert chart.application_data["proxy"]["kubernetes"]["namespace"] == "default"


def test_values_specs_service_account():

    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-specs.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["secrets.yaml"])

    secrets_data = chart.rendered_data["secrets.yaml"]
    assert "data" in secrets_data.keys()
    assert "service-account" in chart.application_data["proxy"]["specs"][0].keys()
    assert "serviceAccount" in chart.values_data["proxy"]["specs"][0].keys()

    k8s_pod_patches = chart.application_data["proxy"]["specs"][0][
        "kubernetes-pod-patches"
    ]
    k8s_pod_patches_data = yaml.load(k8s_pod_patches, Loader=yaml.FullLoader)
    assert "/spec/serviceAccountName" == k8s_pod_patches_data[0]["path"]
    assert (
        chart.application_data["proxy"]["specs"][0]["service-account"]
        == k8s_pod_patches_data[0]["value"]
    )

def test_auth_existing_secret():

    chart_name = "shinyproxy"
    helm_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "charts", "shinyproxy"
    )
    values_file = os.path.join(os.path.dirname(__file__), "values-auth-existing-secret.yaml")
    chart = HelmChart(chart_name=chart_name, helm_dir=helm_dir, values_file=values_file)
    chart.run_helm_template(files=["deployment.yaml"])
    secret_name = chart.values_data['authExistingSecret']['secretKeyRef']['name']
    secret_key = chart.values_data['authExistingSecret']['secretKeyRef']['key']

    deployment_data = chart.rendered_data["deployment.yaml"]
    container_env = deployment_data['spec']['template']['spec']['containers'][0]['env']
    assert secret_name == container_env[0]['valueFrom']['secretKeyRef']['name']
    assert secret_key == container_env[0]['valueFrom']['secretKeyRef']['key']