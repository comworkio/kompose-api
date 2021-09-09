import os
import markdown

from flask import Response
from flask_restful import Resource

class DocApi(Resource):
    def get(self):
        try:
            with open(os.environ['README_FILE_PATH'], 'r') as doc:
                html = markdown.markdown(doc.read())
                return Response(html, mimetype='text/html')
        except IOError as err:
            return {'status': 'error', 'reason': err}, 500
