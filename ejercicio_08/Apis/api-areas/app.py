import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from extensions import db
from flask_migrate import Migrate
from resources.AreaResources import AreaListResource
from resources.AreaResources import AreaResource


def create_app():
    env = os.environ.get('FLASK_ENV', 'Development')
    if env == 'Production':
        config_str = 'config.ProductionConfig'
    elif env == 'Staging':
        config_str = 'config.StagingConfig'
    else:
        config_str = 'config.DevelopmentConfig'

    app = Flask(__name__)
    app.config.from_object(config_str)

    register_extensions(app)
    register_resources(app)

    context_path = os.environ.get('CONTEXT_PATH', '')
    CORS(app, resources = {
         f"/{context_path}/*": {
                "origins": "*",
                "Access-Control-Allow-Origin": "*"
             }
         })

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    context_path = os.environ.get('CONTEXT_PATH', '')
    api = Api(app, prefix=f"/{context_path}")

    # Seccion de catalogos.
    api.add_resource(AreaListResource, '/area')
    api.add_resource(AreaResource, '/area/<int:id_area>')

if __name__ == '__main__':
    app = create_app()
    app.run()