import mongoengine
import logging
from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Users, Watchlist
from app.shoonya.shoonya import update_closing_prices, update_symbols

logger = logging.getLogger(__name__)
views = Blueprint('views', __name__)


@views.route('/watchlist', methods=['POST'])
@jwt_required()
def watchlist():
    data = request.json
    name = data['name']
    investments = data['investments']
    try:
        user = Users.objects(id=ObjectId(get_jwt_identity())).first()
        new_watchlist = Watchlist(name=name, investments=investments, author=user)
        new_watchlist.save()
        return new_watchlist.to_json(), 201
    except mongoengine.errors.NotUniqueError:
        message = {'message': 'A watchlist with this name already exists!'}
        logger.info(f"Error saving watchlist - {message}")
        return jsonify(message), 409
    except Exception as e:
        logger.error(f"Error saving watchlist - {e}")
        raise e


@views.route('/', methods=['GET'])
@jwt_required()
def get_watchlists():
    try:
        user = Users.objects(id=ObjectId(get_jwt_identity())).first()
        return Watchlist.objects(author=user).to_json(), 200
    except Exception as e:
        logger.error(f"Error fetching watchlist - {e}")
        raise e


@views.route('/update_db_symbols', methods=['POST'])
@jwt_required()
def update_db_symbols():
    update_symbols()
    message = {'message': 'Symbols have been updated!'}
    logger.info(f"{message}")
    return jsonify(message), 200


@views.route('/update_db_prices', methods=['PUT'])
@jwt_required()
def update_db_prices():
    update_closing_prices()
    message = {'message': 'Prices have been updated!'}
    logger.info(f"{message}")
    return jsonify(message), 204
