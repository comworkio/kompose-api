from flask import Flask, request, Response

## https://github.com/flask-restful/flask-restful/pull/913
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from subprocess import check_output
from multiprocessing import Process
import os
import json
import uuid 
import markdown

app = Flask(__name__)
api = Api(app)

def get_script_output (cmd):
    try:
        return check_output(cmd, shell=True, text=True)
    except:
        return check_output(cmd, shell=True, universal_newlines=True)

def is_forbidden (var):
    forbidden_chars = ["'" , "\"", "&", ";", "|", "\\"]
    return any(char in var for char in forbidden_chars)

def is_not_empty (var):
    if (isinstance(var, bool)):
        return var
    elif (isinstance(var, int)):
        return False
    empty_chars = ["", "null", "nil", "false", "none"]
    return var is not None and not any(c == var.lower() for c in empty_chars)

def is_empty (var):
    return not is_not_empty(var)

def is_empty_request_field (name):
    body = request.get_json(force=True)
    return not name in body or is_empty(body[name])

def get_available_versions(var):
    return json.loads(get_script_output("/versions.sh {}".format(var)))

def get_kompose_available_versions():
    return get_available_versions("KOMPOSE_VERSION")

def konvert (filename, version, provider, namespace, apply):
    return get_script_output("/konvert.sh {} {} {} {} {}".format(filename, version, provider, namespace, apply))

class VersionsApi(Resource):
    def get(self):
        return {
            'status': 'ok',
            'kompose_versions': get_kompose_available_versions(),
            'kubectl_versions': get_available_versions("K8S_VERSION"),
            'help': "Go see the documentation here: {}".format(os.environ['KOMPOSE_DOC_URL'])
        }

class KomposeApi(Resource):
    def get(self):
        return {
            'status': 'ok',
            'alive': True,
            'help': "Go see the documentation here: {}".format(os.environ['KOMPOSE_DOC_URL']) 
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
            provider = "null"

        namespace = request.headers.get('X-K8S-NS')
        if is_empty(namespace):
            namespace = "null"

        apply = request.headers.get('X-K8S-Apply')        
        if is_empty(namespace) or is_empty(os.environ['ENABLE_KUBECTL_APPLY']):
            apply = "null"

        if any(is_forbidden(arg) for arg in [provider, namespace, apply]):
            return {
                'status': 'forbidden',
                'reason': 'forbidden character in the headers' 
            }, 403

        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage, location='files')
        args = parse.parse_args()
        tmp_file = args['file']
        filename = "docker-compose-{}.yml".format(uuid.uuid1())
        tmp_file.save(filename)
        return Response(konvert(filename, requested_version, provider, namespace, apply), mimetype='application/x-yaml')    

class ManifestEndPoint(Resource):
    def get(self):
        try:
            with open(os.environ['MANIFEST_FILE_PATH']) as manifest_file:
                manifest = json.load(manifest_file)
                return manifest
        except IOError as err:
            return {
                'status': 'error', 
                'reason': err
            }, 500

class DocEndPoint(Resource):
    def get(self):
        try:
            with open(os.environ['README_FILE_PATH'], 'r') as doc:
                html = markdown.markdown(doc.read())
                return Response(html, mimetype='text/html')
        except IOError as err:
            return {'status': 'error', 'reason': err}, 500


kompose_routes = ['/', '/v1', '/v1/']
versions_routes = ['/versions', '/versions/', '/v1/versions', '/v1/versions/']
manifest_routes = ['/manifest', '/manifest/', '/v1/manifest', '/v1/manifest/']
doc_routes = ['/doc', '/doc/', '/v1/doc', '/v1/doc/']

api.add_resource(KomposeApi, *kompose_routes)
api.add_resource(VersionsApi, *versions_routes)
api.add_resource(ManifestEndPoint, *manifest_routes)
api.add_resource(DocEndPoint, *doc_routes)

if __name__ == '__main__':
    app.run()
