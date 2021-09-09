import os

from flask_restful import Resource
from kompose_api_utils import *

class VersionsApi(Resource):
    def get(self):
        return {
            'status': 'ok',
            'kompose_versions': get_kompose_available_versions(),
            'kubectl_versions': get_available_versions("K8S_VERSION"),
            'help': "Go see the documentation here: {}".format(os.environ['KOMPOSE_DOC_URL'])
        }
