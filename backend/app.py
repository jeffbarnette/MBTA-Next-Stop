from flask import Flask
from flask_cors import CORS
from api.routes.main import main_api

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    CORS(app)

    # Default Path
    @app.route('/', methods=['GET'])
    def home():
        return "<p>This service is working.</p>"

    # API path
    app.register_blueprint(main_api, url_prefix='/api')

    return app

# This is being run from command line as the main application
if __name__ == '__main__':
    from argparse import ArgumentParser
    # Allow -p flag to overide the default port number
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='127.0.0.1', port=port)
