import mongoengine.errors
import logging
from datetime import datetime
from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import create_access_token, decode_token, get_jwt, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Users

logger = logging.getLogger(__name__)
auth = Blueprint('auth', __name__)
BLOCKLIST = set()


@auth.route('/login', methods=['POST'])
def login():
    """
    Method to log in the user provided the email and password sent as a JSON body
    :return:
    """
    data = request.json
    email = data['email']
    password = data['password']
    error = None

    user = Users.objects(email__exact=email).first()
    if user is None:
        error = 'This email does not exist, please sign up!'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password, please retry!'

    if error is None:
        access_token = create_access_token(identity=str(user.id))
        user.last_logged_in = datetime.utcnow()
        user.save()
        return jsonify({'access_token': access_token}), 200
    logger.error(f"Error while login - {error}")
    return error, 422


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Log out the user by clearing the session cookie from the UI
    :return:
    """
    jti = get_jwt()['jti']
    BLOCKLIST.add(jti)
    return jsonify({'message': 'Logged Out!'}), 200


@auth.route('/signup', methods=['POST'])
def signup():
    """
    Creating a new user in the DB provided a JSON body containing user's name, email and password
    :return:
    """
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']

    try:
        new_user = Users(name=name, email=email, password=generate_password_hash(password))
        new_user.save()
        return new_user.to_json(), 201
    except mongoengine.errors.NotUniqueError:
        message = {'message': 'A user with this username already exists, please login!'}
        logger.error(f"Error while sign up - {message}")
        return jsonify(message), 409
    except Exception as e:
        logger.error(f"Error while sign up - {e}")
        raise e


@auth.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    """
    Method to delete a user account from the DB
    :return:
    """
    user_id = decode_token(request.headers.get('Authorization').split()[1])['sub']
    try:
        user = Users.objects.get(id=user_id)
    except Exception as e:
        message = {'message': 'User does not exist!'}
        logger.error(f"Error while deleting account - message")
        return jsonify(message), 422
    if user:
        user.delete()
        session.clear()
        message = {'message': 'Delete successful!'}
        logger.info(f"User deleted successfully")
        return jsonify(message), 204
    message = {'message': 'Unable to delete user, user not logged in!'}
    logger.error(f"Error in deleting user account - {message}")
    return jsonify(message), 422
