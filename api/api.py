import os
import json
import uuid 
import markdown

from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from kompose_api_utils import *

app = Flask(__name__)
api = Api(app)

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
