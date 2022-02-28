#!/usr/bin/env python3

import boto3
import json
import os
import typing

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
            elif  len(container_l) == 2:
                container_name = container_l[0].split('/')
                ecr_check = ecr_client.describe_images(
                    registryId=REGISTRY_ID,
                    repositoryName=f"{container_name[1]}/{container_name[2]}",
                )


def sanity_checks(details_data):
    pass

def describe_change_set(change_set_id: str):
    response = marketplace_client.describe_change_set(
        Catalog = "AWSMarketplace",
        ChangeSetId=change_set_id,
        # ClientRequestToken='string'
    )
    for changeset in response['ChangeSet']:
        details = changeset['Details']
        details_data = json.loads(details)
        changeset['Details'] = details_data

def start_change_set(data):
    response = marketplace_client.start_change_set(
        Catalog = "AWSMarketplace",
        ChangeSet= data.get('ChangeSet'),
        ChangeSetName='internal-release-0.0.1',
        # ClientRequestToken='string'
    )