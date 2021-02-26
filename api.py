from flask import Flask, request
from flask_restful import Resource, Api

from subprocess import check_output
from multiprocessing import Process
import os
import json
import sys
import re

app = Flask(__name__)
api = Api(app)

def get_script_output (cmd):
    print("[get_script_output] cmd = {}".format(cmd))
    try:
        return check_output(cmd, shell=True, text=True)
    except:
        return check_output(cmd, shell=True, universal_newlines=True)

def is_not_empty (var):
    return var is not None and "" != var and "null" != var and "nil" != var

def is_empty (var):
    return not is_not_empty(var)

def is_empty_request_field (name):
    body = request.get_json(force=True)
    return not name in body or is_empty(body[name])

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def is_not_ok(body):
    return not "status" in body or body["status"] != "ok"

def check_mandatory_param(name):
    if is_empty_request_field(name):
        eprint("[check_mandatory_param] bad request : missing argument = {}, body = {}".format(name, request.data))
        return {
            "status": "bad_request",
            "reason": "missing {} argument".format(name)
        }
    else:
        return {
            "status": "ok"
        }

class KomposeVersionsApi(Resource):
    def get(self):
        return {
            'status': 'ok',
            'available_pipelines': json.loads(get_script_output("/kompose_versions.sh"))
        }

class KomposeApi(Resource):
    def post(self):
        return {
            'status': 'to develop',
            'executed': True
        }

class RootEndPoint(Resource):
    def get(self):
        return {
            'status': 'ok',
            'alive': True
        }

class ManifestEndPoint(Resource):
    def get(self):
        try:
            with open(os.environ['MANIFEST_FILE_PATH']) as manifest_file:
                manifest = json.load(manifest_file)
                return manifest
        except IOError as err:
            return 500, {'status': 'error', 'reason': err}

health_check_routes = ['/', '/health', '/health/']
kompose_versions_routes = ['/kompose/versions', '/kompose-api/versions', '/kompose/versions/', '/kompose-api/versions/']
kompose_routes = ['/kompose', '/kompose-api', '/kompose/', '/kompose-api/']
manifest_routes = ['/manifest', '/manifest/']

api.add_resource(RootEndPoint, *health_check_routes)
api.add_resource(KomposeVersionsApi, *kompose_versions_routes)
api.add_resource(KomposeApi, *kompose_routes)
api.add_resource(ManifestEndPoint, *manifest_routes)

if __name__ == '__main__':
    app.run()
