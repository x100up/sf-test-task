from flask import Blueprint, request, abort, jsonify, current_app
from functools import wraps
from lib import AuthError

auth_module = Blueprint('auth', __name__, url_prefix='/auth/')

def auth_service_needed(func):
    """

    :param func: The view function to decorate.
    :type func: function
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        auth_service = current_app.extensions['auth_extension']
        return func(auth_service, *args, **kwargs)

    return wrapped


@auth_module.route('signup/', methods=['POST'])
@auth_service_needed
def signup(auth_service):
    """
    :param auth_service:
    :type auth_service: lib.AuthExtension
    """
    user_type = request.form.get('type')
    if not user_type:
        abort(400, 'Type not specified')

    user = auth_service.build_user(user_type, {k: request.form[k] for k in request.form if k != 'type'})

    if not user.is_valid():
        abort(400, 'Invalid user data')

    try:
        auth_service.save_user(user)
    except AuthError as e:
        abort(400, e.message)
    except BaseException as e:
        abort(400, 'Unknown error')

    return jsonify(success=True)


@auth_module.route('signin/', methods=['POST'])
@auth_service_needed
def signin(auth_service):
    type_ = request.form.get('type')
    if not type_:
        abort(400, 'Type not specified')

    try:
        user = auth_service.build_user(type_, {k: request.form[k] for k in request.form if k != 'type'})
        token = auth_service.get_token(user)
    except AuthError as e:
        abort(400, e.message)
    except BaseException:
        abort(400, 'Unknown error')

    return jsonify(token=token)
