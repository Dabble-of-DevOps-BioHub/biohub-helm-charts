# Copyright 2019 Novartis Institutes for BioMedical Research Inc. Licensed
# under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0. Unless
# required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.

from __future__ import annotations
import logging
import subprocess

from flask_api import status

from cellxgene_gateway.cache_entry import CacheEntryStatus
from cellxgene_gateway.dir_util import make_annotations
from cellxgene_gateway.env import cellxgene_args, enable_annotations, enable_backed_mode
from cellxgene_gateway.process_exception import ProcessException

import os
ANNOTATION_DIR = os.environ.get('ANNOTATION_DIR', os.path.abspath('annotations'))

logger = logging.getLogger("cellxgene_gateway")

class SubprocessBackend:
    def __init__(self):
        pass

    def create_cmd(self, cellxgene_loc, file_path, port, scripts, annotation_file_path):
        logger.info(f"Creating CMD")
        logger.info(f"File path: {file_path}")
        logger.info(f"Annotations file path: {annotation_file_path}")

        bucket = os.environ.get('CELLXGENE_BUCKET', '')
        clean_file_path = file_path

        if 's3://' in clean_file_path:
            clean_file_path  = clean_file_path.replace('s3://', '')
            if f"{bucket}/" in clean_file_path:
                clean_file_path = clean_file_path.replace(f"{bucket}/", '')
            elif f"{bucket}" in clean_file_path:
                clean_file_path = clean_file_path.replace(f"{bucket}", '')

        dataset_file = clean_file_path
        if "s3://" in clean_file_path:
            annotations_dir = os.path.join(ANNOTATION_DIR, bucket, f"{dataset_file}_annotations")
        else:
            annotations_dir = os.path.join(ANNOTATION_DIR, f"{dataset_file}_annotations")
        logger.info(f'Annotations dir: {annotations_dir}')
        os.makedirs(annotations_dir, exist_ok=True)

        extra_args = ""
        #if enable_annotations and not annotation_file_path is None:
        extra_args = f" --annotations-dir {annotations_dir}"

        if enable_annotations:
            if annotation_file_path == None or annotation_file_path == "":
                logger.info(f"No annotations file path")
                extra_args = f" --annotations-dir {annotations_dir}"
            else:
                logger.info(f"Using existing annotations file")
                extra_args = f" --annotations-file {annotation_file_path}"
        else:
            extra_args = " --disable-annotations"
        if enable_backed_mode:
            extra_args += " --backed"
        if not cellxgene_args is None:
            extra_args += f" {cellxgene_args}"

        cmd = (
            f"yes | {cellxgene_loc} launch {file_path}"
            + f" --port {port}"
            + " --host 127.0.0.1"
            + extra_args
        )

        for s in scripts:
            cmd += f" --scripts {s}"

        return cmd

    def launch(self, cellxgene_loc, scripts, cache_entry):
        cmd = self.create_cmd(
            cellxgene_loc,
            cache_entry.key.file_path,
            cache_entry.port,
            scripts,
            cache_entry.key.annotation_file_path,
        )
        logging.getLogger("cellxgene_gateway").info(f"launching {cmd}")
        process = subprocess.Popen(
            [cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        while True:
            output = process.stdout.readline().decode()
            if output == "[cellxgene] Type CTRL-C at any time to exit.\n":
                break
            elif output == "":
                stderr = process.stderr.read().decode()
                if (
                    "Error while loading file" in stderr
                    or "Could not open file" in stderr
                ):
                    message = "File was invalid."
                    http_status = status.HTTP_400_BAD_REQUEST
                else:
                    message = "Cellxgene failed to launch dataset."
                    http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

                cache_entry.status = CacheEntryStatus.error
                cache_entry.set_error(message, stderr, http_status)

                raise ProcessException.from_cache_entry(cache_entry)
            else:
                cache_entry.append_output(output)

        cache_entry.set_loaded(process.pid)

        return
