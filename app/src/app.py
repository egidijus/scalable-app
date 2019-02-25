#!/usr/bin/env python

from flask import jsonify
from flask import Flask, render_template, make_response
from flask import request
import os, sys, logging

logger = logging.getLogger(__name__)

s3_static_asset_bucket = os.environ['s3_static_asset_bucket']

def setup_logging(verbose=False):
    '''
    Setup logging
    :param verbose: bool - Enable verbose debug mode
    '''

    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    if verbose:
        logger.setLevel(logging.DEBUG)

app = Flask(__name__)

setup_logging()

@app.route('/')
def home():
    return render_template('index.html', s3_static_asset_bucket=s3_static_asset_bucket)


@app.route('/_health')
def mock():
    return jsonify(
        env=dict(**os.environ),
        request=dict(request.headers))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8448)
