from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from subprocess import check_output
from multiprocessing import Process
import os
import json
import sys
import re
import uuid 

app = Flask(__name__)
api = Api(app)

def get_script_output (cmd):
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

def get_kompose_available_versions():
    return json.loads(get_script_output("/kompose_versions.sh"))

def konvert (filname, version, provider):
    return get_script_output("/konvert.sh {} {} {}".format(filname, version, provider))

class KomposeVersionsApi(Resource):
    def get(self):
        return {
            'status': 'ok',
            'available_versions': get_kompose_available_versions()
        }

class KomposeApi(Resource):
    def get(self):
        return {
            'status': 'ok',
            'alive': True
        }
    def post(self):
        available_versions = get_kompose_available_versions()
        requested_version = request.headers.get('X-Kompose-Version')
        
        if is_empty(requested_version):
            requested_version = os.environ['KOMPOSE_VERSION_N']

        if not requested_version in available_versions:
            return {
                'status': 'not_implemented',
                'reason': "{} version of kompose is not available!".format(requested_version)
            }, 405

        provider = request.headers.get('X-K8S-Provider')
        if is_empty(provider):
            provider = ""

        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage, location='files')
        args = parse.parse_args()
        tmp_file = args['file']
        filename = "docker-compose-{}.yml".format(uuid.uuid1())
        tmp_file.save(filename)
        return Response(konvert(filename, requested_version, provider), mimetype='application/x-yaml')    

class ManifestEndPoint(Resource):
    def get(self):
        try:
            with open(os.environ['MANIFEST_FILE_PATH']) as manifest_file:
                manifest = json.load(manifest_file)
                return manifest
        except IOError as err:
            return 500, {'status': 'error', 'reason': err}

kompose_routes = ['/', '/kompose', '/kompose-api', '/kompose/', '/kompose-api/']
kompose_versions_routes = ['/versions', '/versions/', '/kompose/versions', '/kompose-api/versions', '/kompose/versions/', '/kompose-api/versions/']
manifest_routes = ['/manifest', '/manifest/']

api.add_resource(KomposeVersionsApi, *kompose_versions_routes)
api.add_resource(KomposeApi, *kompose_routes)
api.add_resource(ManifestEndPoint, *manifest_routes)

if __name__ == '__main__':
    app.run()
