from flask import Flask
from flask_restful import Api

from api_manifest import ManifestApi
from api_versions import VersionsApi
from api_doc import DocApi
from api_kompose import KomposeApi

app = Flask(__name__)
api = Api(app)

kompose_routes = ['/', '/v1', '/v1/']
versions_routes = ['/versions', '/versions/', '/v1/versions', '/v1/versions/']
manifest_routes = ['/manifest', '/manifest/', '/v1/manifest', '/v1/manifest/']
doc_routes = ['/doc', '/doc/', '/v1/doc', '/v1/doc/']

api.add_resource(KomposeApi, *kompose_routes)
api.add_resource(VersionsApi, *versions_routes)
api.add_resource(ManifestApi, *manifest_routes)
api.add_resource(DocApi, *doc_routes)

if __name__ == '__main__':
    app.run()
