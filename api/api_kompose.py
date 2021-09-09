import os
import uuid

from flask import request, Response
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from kompose_api_utils import *

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
