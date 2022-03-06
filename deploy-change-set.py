#!/usr/bin/env python3

from pydoc import describe
import boto3
import json
import os
import typing
import time
from pprint import pprint

REGISTRY_ID = os.environ.get('REGISTERY_ID', '709825985650')
SELLER_NAME = os.environ.get('SELLER_NAME', 'dabble-of-devops')
REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

marketplace_client = boto3.client('marketplace-catalog')
ecr_client =  boto3.client('ecr')

def read_changeset_file(file: str) -> dict:
    assert os.path.exists(file) == True
    fh = open(file)
    data =  json.load(fh)
    assert 'ChangeSet' in data.keys()
    assert 'Catalog' in data.keys()
    for changeset in data.get('ChangeSet'):
        details = changeset.get('Details')
        details = json.dumps(details)
        changeset['Details'] = details
    return data

class Error(Exception):
    """Base class for other exceptions"""
    pass

class NoTagFoundECR(Error):
    """Raised when a tag is not found in the ECR Container URI"""
    pass

def sanity_check_container_images(details_data):
    for delivery_options in details_data['DeliveryOptions']:
        helm_delivery_options = delivery_options['Details']['HelmDeliveryOptionDetails']
        container_images = helm_delivery_options['ContainerImages']
        for container_image in container_images:
            container_l = container_image.split(':')
            if len(container_l) == 0:
                print('No tag found in container')
                raise NoTagFoundECR
            elif len(container_l) == 2:
                container_name = container_l[0].split('/')
                ecr_check = ecr_client.describe_images(
                    registryId=REGISTRY_ID,
                    repositoryName=f"{container_name[1]}/{container_name[2]}",
                )

def sanity_checks_key_length(details_data):
    pass

def sanity_checks(details_data):
    pass

def describe_change_set(change_set_id: str):
    describe_change_set_response = marketplace_client.describe_change_set(
        Catalog = "AWSMarketplace",
        ChangeSetId=change_set_id,
        # ClientRequestToken='string'
    )
    return describe_change_set_response

def get_change_set_status(change_set_id):

    describe_change_set_response=describe_change_set(change_set_id)
    in_complete_statuses = ['PREPARING','APPLYING']
    complete_statuses = [ 'SUCCEEDED','CANCELLED','FAILED']
    status = describe_change_set_response['Status']

    while status not in complete_statuses:
        describe_change_set_response=describe_change_set(change_set_id)
        status = describe_change_set_response['Status']
        time.sleep(60)

    failure_code = describe_change_set_response['FailureCode']

    print(f"Change set complete with status: {status}")
    print(f"Failure Code: {failure_code}")

    for changeset in describe_change_set_response['ChangeSet']:
        details = changeset['Details']
        if isinstance(details, str):
            details_data = json.loads(details)
            changeset['Details'] = details_data
        # title = changeset['Details']['DeliveryOptionTitle']
        # print(f"Error Detail List:")
        error_detail_list = changeset['ErrorDetailList']
        print('---------------------------')
        pprint(error_detail_list)
    return describe_change_set_response


def start_change_set(data):
    start_change_set_response = marketplace_client.start_change_set(
        Catalog = "AWSMarketplace",
        ChangeSet= data.get('ChangeSet'),
        ChangeSetName='internal-release-0.0.1',
    )
    change_set_id = start_change_set_response['ChangeSetId']
    return change_set_id

def run():
    file = ''
    data = {}
    change_set_id = start_change_set(data)
    describe_change_set_response = get_change_set_status(change_set_id)