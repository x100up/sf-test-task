from flask import Flask, jsonify
from lib import AuthExtension
from auth import auth_module

def create_app(config=None, environment=None):
    app = Flask(__name__)
    app.config.from_object(config or {})
    app.register_blueprint(auth_module)
    AuthExtension(app)

    @app.errorhandler(400)
    def bad_request(error):
        """
        Jsonify errors
        :param error:
        :type error: werkzeug.exceptions.BadRequest
        :return:
        :rtype: tuple
        """
        return jsonify(error_code=400, message=error.description), 400

    return app




