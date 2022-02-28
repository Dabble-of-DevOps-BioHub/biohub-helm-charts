#!/usr/bin/env python3

import boto3
import json
import os
import typing

client = boto3.client('marketplace-catalog')

def read_changset_file(file: str) -> dict:
    assert os.path.exists(file)
    fh = open(file)
    data =  json.load(fh)
    assert 'ChangeSet' in data.keys()
    assert 'Catalog' in data.keys()
    for changeset in data.get('ChangeSet'):
        details = changeset.get('Details')
        details = json.dumps(details)
        changeset['Details'] = details
    return data

def start_change_set(data):
    response = client.start_change_set(
        Catalog = "AWSMarketplace",
        ChangeSet= data.get('ChangeSet'),
        ChangeSetName='internal-release-0.0.1',
        # ClientRequestToken='string'
    )