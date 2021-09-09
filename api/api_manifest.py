import os
import json

from flask_restful import Resource
class ManifestApi(Resource):
    def get(self):
        try:
            with open(os.environ['MANIFEST_FILE_PATH']) as manifest_file:
                manifest = json.load(manifest_file)
                return manifest
        except IOError as err:
            return 500, {'status': 'error', 'reason': err}
