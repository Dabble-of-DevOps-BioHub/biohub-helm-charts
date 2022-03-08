import yaml
import argparse
import os
import json
from copy import deepcopy
from pprint import pprint


specs_dict = {
    "type": "array",
    "description": "List of ShinyProxy application specs",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string", "description": "application id"},
            "port": {
                "type": "number",
                "description": "port the internal application is running on",
            },
            "displayName": {
                "type": "string",
                "description": "Name displayed on the landing page",
            },
            "containerImage": {"type": "string", "description": "Docker image"},
            "containerWaitTime": {"type": "number", "description": ""},
            "heartbeatEnabled": {"type": "boolean", "description": ""},
            "heartbeatTimeout": {"type": "number", "description": ""},
            "containerMemoryRequest": {"type": "string", "description": ""},
            "containerMemoryLimit": {"type": "string", "description": ""},
            "containerCpuRequest": {"type": "number", "description": ""},
            "containerCpuLimit": {"type": "number", "description": ""},
            "serviceAccount": {
                "type": "string",
                "description": "The service account used to access the S3 buckets. Please see the docs for more details.",
            },
            "targetPath": {"type": "string", "description": ""},
            "containerEnv": {
                # any containerEnv
                "type": "object",
            },
            "kubernetesPodPatches": {
                "type": "string",
                "description": "Add some file mounts and env vars",
            },
        },
    },
}

specs_any_of_dict = {
    "anyOf": [
        deepcopy(specs_dict),
        {
            "type": "object",
            "description": "Dict of ShinyProxy Application Specs",
            "properties": deepcopy(specs_dict["items"]["properties"]),
        },
    ]
}
users_any_of_dict = {
    "anyOf": [
        {
            "type": "array",
            "description": "List of ShinyProxy Application Simple Auth Users",
        },
        {
            "type": "object",
            "description": "Dict of ShinyProxy Application Simple Auth Users",
        },
    ]
}

parser = argparse.ArgumentParser()
parser.add_argument("values_schema")
args = parser.parse_args()

assert os.path.exists(args.values_schema)
with open(args.values_schema) as json_file:
    values_data = json.load(json_file)

if "shinyproxy" in values_data["properties"].keys():
    print("Using helm chart extending shiny proxy")
    # replace the specs
    replace_this = values_data["properties"]["shinyproxy"]["properties"]["proxy"]["properties"]["specs"]
    if "type" in replace_this.keys():
        del replace_this["type"]
        replace_this["anyOf"] = specs_any_of_dict["anyOf"]
        values_data["properties"]["shinyproxy"]["properties"]["proxy"]["properties"]["specs"] = replace_this

    # replace the users
    try:
        replace_this = values_data["properties"]["shinyproxy"]["properties"]["auth"]["properties"]["users"]
    except:

        properties = values_data["properties"]["shinyproxy"]["properties"]
        properties['auth'] = {'properties': {'users': {}}}
    replace_this = values_data["properties"]["shinyproxy"]["properties"]["auth"]["properties"]["users"]

    if "type" in replace_this.keys():
        del replace_this["type"]
    replace_this["anyOf"] = users_any_of_dict["anyOf"]
    values_data["properties"]["shinyproxy"]["properties"]["auth"]["properties"]["users"] = users_any_of_dict

    values_json = json.dumps(values_data, indent=4)
    with open(args.values_schema, 'w') as outfile:
        outfile.write(values_json)
else:
    print("Using default shinyproxy chart")

    # replace the specs
    replace_this = values_data["properties"]["proxy"]["properties"]["specs"]
    if "type" in replace_this.keys():
        del replace_this["type"]
    replace_this["anyOf"] = specs_any_of_dict["anyOf"]
    values_data["properties"]["proxy"]["properties"]["specs"] = replace_this

    # replace the users
    replace_this = values_data["properties"]["auth"]["properties"]["users"]
    if "type" in replace_this.keys():
        del replace_this["type"]
    replace_this["anyOf"] = users_any_of_dict["anyOf"]
    values_data["properties"]["auth"]["properties"]["users"] = users_any_of_dict


    values_json = json.dumps(values_data, indent=4)
    with open(args.values_schema, 'w') as outfile:
        outfile.write(values_json)