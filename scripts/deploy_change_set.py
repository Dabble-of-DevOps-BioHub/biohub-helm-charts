#!/usr/bin/env python3

import boto3
import json
import os
import typing
from copy import deepcopy
import time
from pprint import pprint
import argparse

REGISTRY_ID = os.environ.get("REGISTERY_ID", "709825985650")
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

marketplace_client = boto3.client("marketplace-catalog")
ecr_client = boto3.client("ecr")


class Error(Exception):
    """Base class for other exceptions"""

    pass


class NoTagFoundECRError(Error):
    """Raised when a tag is not found in the ECR Container URI"""

    pass


class InvalidEcrRepoNameError(Error):
    """Raised when the ecr repo name is invalid"""

    pass


class ContainerNotFoundError(Error):
    """Raised when a tag is not found in the ECR Container URI"""

    pass


class HelmChartNotSuppliedError(Error):
    """Raised when a helm chart is not passed to the change set"""

    pass


class ParameterKeyError(Error):
    """Raised when an override key contains [ or -"""

    pass


def search_ecr_images(images, tag):
    found = False
    image = None
    for t_image in images:
        if tag in t_image["imageTags"]:
            found = True
            image = deepcopy(t_image)
    return found, image


def validate_ecr_repo_name(container_image):
    container_l = container_image.split(":")
    if len(container_l) == 0:
        print("No tag found in container")
        raise NoTagFoundECRError
    elif len(container_l) == 2:
        container_name = container_l[0].split("/")
        repository_name = (f"{container_name[1]}/{container_name[2]}",)
        tag = container_l[1]
    else:
        raise InvalidEcrRepoNameError
    return repository_name, tag


def update_helm_uri_version(data, helm_chart_version):
    for changeset in data.get("ChangeSet"):
        details_data = changeset["Details"]
        if isinstance(details_data, str):
            details_data = json.loads(details_data)
        for delivery_options in details_data.get("DeliveryOptions", []):
            delivery_options_details = delivery_options.get(
                "Details", {"HelmDeliverOptionDetails": []}
            )
            helm_delivery_options = delivery_options_details.get(
                "HelmDeliveryOptionDetails", []
            )
            helm_chart = helm_delivery_options.get("HelmChartUri", None)
            if helm_chart:
                repository_name, tag = validate_ecr_repo_name(helm_chart)
                helm_delivery_options['HelmChartUri'] = f"{repository_name}:{helm_chart_version}"



def convert_details_to_json(data, version_title, release_notes):
    for changeset in data.get("ChangeSet"):
        details = changeset.get("Details")
        details["Version"] = {
            "ReleaseNotes": release_notes,
            "VersionTitle": version_title,
        }
        details = json.dumps(details)
        changeset["Details"] = details
    return data


def read_changeset_file(file: str, version_title, release_notes, helm_chart_version) -> dict:
    assert os.path.exists(file) == True
    fh = open(file)
    data = json.load(fh)
    assert "ChangeSet" in data.keys()
    assert "Catalog" in data.keys()
    return data


def validate_ecr_repo(container_image):
    repository_name, tag = validate_ecr_repo_name(container_image)
    found = False
    ecr_check = ecr_client.describe_images(
        registryId=REGISTRY_ID,
        repositoryName=repository_name,
    )
    images = ecr_check["imageDetails"]
    found, image = search_ecr_images(images, tag)
    while "NextToken" in ecr_check["ResponseMetadata"].keys() or not found:
        ecr_check = ecr_client.describe_images(
            registryId=REGISTRY_ID,
            repositoryName=repository_name,
        )
        images = ecr_check["imageDetails"]
        found, image = search_ecr_images(images, tag)
    if not found:
        raise ContainerNotFoundError
    # TODO add in security check
    return image


def sanity_check_helm_chart(helm_delivery_options):
    helm_chart = helm_delivery_options.get("HelmChartUri", None)
    if helm_chart:
        repository_name, tag = validate_ecr_repo_name(helm_chart)
        image = validate_ecr_repo(helm_chart)
    else:
        raise HelmChartNotSuppliedError
    return image


def sanity_check_container_images(helm_delivery_options):
    container_images = helm_delivery_options.get("ContainerImages", [])
    images = []
    for container_image in container_images:
        image = validate_ecr_repo(container_image)
        images.append(image)
    return images


def sanity_check_override_keys(helm_delivery_options):
    key_length_error = {}
    key_character_error = {}
    raise_error = False
    override_parameters = helm_delivery_options.get("OverrideParameters", [])
    for parameter in override_parameters:
        key = parameter["Key"]
        if len(key) >= 50:
            key_length_error[key] = True
            raise_error = True
        if "[" in key:
            key_character_error[key] = True
            raise_error = True
        if "-" in key:
            key_character_error[key] = True
            raise_error = True
    if raise_error:
        print("One or more errors was found with the overrides keys")
        pprint(key_character_error.keys())
        pprint(key_length_error.keys())
        raise ParameterKeyError


def sanity_check_helm_chart_delivery_options(details_data):
    for delivery_options in details_data.get("DeliveryOptions", []):
        delivery_options_details = delivery_options.get(
            "Details", {"HelmDeliverOptionDetails": []}
        )
        helm_delivery_options = delivery_options_details.get(
            "HelmDeliveryOptionDetails", []
        )
        helm_delivery_options = deepcopy(helm_delivery_options)
        sanity_check_container_images(helm_delivery_options)
        sanity_check_helm_chart(helm_delivery_options)
        sanity_check_override_keys(helm_delivery_options)


def sanity_checks(data):
    for changeset in data["ChangeSet"]:
        details_data = changeset["Details"]
        if isinstance(details_data, str):
            details_data = json.loads(details_data)
            sanity_check_helm_chart_delivery_options(details_data)


def describe_change_set(change_set_id: str):
    describe_change_set_response = marketplace_client.describe_change_set(
        Catalog="AWSMarketplace",
        ChangeSetId=change_set_id,
    )
    return describe_change_set_response


def get_change_set_status(change_set_id):

    describe_change_set_response = describe_change_set(change_set_id)
    in_complete_statuses = ["PREPARING", "APPLYING"]
    complete_statuses = ["SUCCEEDED", "CANCELLED", "FAILED"]
    status = describe_change_set_response["Status"]

    while status not in complete_statuses:
        describe_change_set_response = describe_change_set(change_set_id)
        status = describe_change_set_response["Status"]
        time.sleep(60)

    failure_code = describe_change_set_response.get("FailureCode", None)

    print(f"Change set complete with status: {status}")
    if failure_code:
        print(f"Failure Code: {failure_code}")

    for changeset in describe_change_set_response["ChangeSet"]:
        details = changeset["Details"]
        if isinstance(details, str):
            details_data = json.loads(details)
            changeset["Details"] = details_data
        error_detail_list = changeset["ErrorDetailList"]
        print("---------------------------")
        pprint(error_detail_list)
    return describe_change_set_response


def start_change_set(data, change_set_name):
    start_change_set_response = marketplace_client.start_change_set(
        Catalog="AWSMarketplace",
        ChangeSet=data.get("ChangeSet"),
        ChangeSetName=change_set_name,
    )
    change_set_id = start_change_set_response["ChangeSetId"]
    return change_set_id


def run(
    changeset_file, changeset_name, version_title, release_notes, helm_chart_version
):
    data = read_changeset_file(changeset_file, version_title, release_notes, helm_chart_version)
    sanity_checks(data)
    convert_details_to_json(data, version_title, release_notes)
    change_set_id = start_change_set(data, changeset_name)
    print(f"Successfuly submitted changeset with id: {change_set_id}")
    describe_change_set_response = get_change_set_status(change_set_id)
    pprint(describe_change_set_response)


if __name__ == "__main__":
    # TODO add dry-run, sanity check
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--changeset-file",
        "-c",
        default="changesets/single-cell-cloud-lab/changeset.json",
        help="Path to the changesets file",
    )
    parser.add_argument(
        "--helm-chart-version", required=True, help="Helm Chart Version"
    )
    parser.add_argument("--changeset-name", required=True, help="Changeset Name")
    parser.add_argument("--version-title", required=True, help="Version Title")
    parser.add_argument("--release-notes", required=True, help="Version Release Notes")
    args = parser.parse_args()

    assert os.path.exists(args.changeset_file)
    if not args.version_title:
        args.version_title = args.changeset_name
    if not args.release_notes:
        args.release_notes = args.changeset_name
    run(
        changeset_file=args.changeset_file,
        changeset_name=args.changeset_name,
        version_title=args.version_title,
        release_notes=args.release_notes,
        helm_chart_version=args.helm_chart_version,
    )
