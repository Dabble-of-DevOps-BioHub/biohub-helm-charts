from email.policy import default
from flask import (
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_api import status
import json
import logging
import os
import urllib.parse
from threading import Lock, Thread
from cellxgene_gateway import env, flask_util
from cellxgene_gateway.backend_cache import BackendCache
from cellxgene_gateway.cache_entry import CacheEntryStatus
from cellxgene_gateway.cache_key import CacheKey
from cellxgene_gateway.cellxgene_exception import CellxgeneException
from cellxgene_gateway.extra_scripts import get_extra_scripts
from cellxgene_gateway.filecrawl import render_item_source
from cellxgene_gateway.process_exception import ProcessException
from cellxgene_gateway.prune_process_cache import PruneProcessCache
from cellxgene_gateway.util import current_time_stamp

from cellxgene_gateway.gateway import app, cache, item_sources, default_item_source

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
)

def launch():
    env.validate()
    if not item_sources or not len(item_sources):
        raise Exception("No data sources specified for Cellxgene Gateway")

    global default_item_source
    if default_item_source is None:
        default_item_source = item_sources[0]

    logging.info('Item Sources')
    logging.info(default_item_source)
    from pprint import pprint
    logging.info(pprint(item_sources))

    pruner = PruneProcessCache(cache)

    background_thread = Thread(target=pruner)
    background_thread.start()

    app.launchtime = current_time_stamp()


def main():
    cellxgene_data = os.environ.get("CELLXGENE_DATA", None)
    cellxgene_bucket = os.environ.get("CELLXGENE_BUCKET", None)

    global default_item_source

    if cellxgene_bucket is not None:
        from cellxgene_gateway.items.s3.s3item_source import S3ItemSource

        item_sources.append(S3ItemSource(cellxgene_bucket, name="s3"))
        logging.info(item_sources)
        default_item_source = "s3"

    if cellxgene_data is not None:
        from cellxgene_gateway.items.file.fileitem_source import FileItemSource

        item_sources.append(FileItemSource(cellxgene_data, name="local"))
        default_item_source = "local"
    if len(item_sources) == 0:
        raise Exception("Please specify CELLXGENE_DATA or CELLXGENE_BUCKET")

    flask_util.include_source_in_url = len(item_sources) > 1

    launch()

main()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(5005), debug=True)
