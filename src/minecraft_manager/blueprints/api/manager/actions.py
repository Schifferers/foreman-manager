__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
actions.py
- Actions API
"""


from flask import session, jsonify, request, current_app
from minecraft_manager.blueprints.api import blueprint
from minecraft_manager import constants
from minecraft_manager.db import db
from minecraft_manager.controllers.minecraft import execute_action
from minecraft_manager.models import constants as model_constants
from minecraft_manager.blueprints.api import user_required, requires_auth
from minecraft_manager.blueprints.api.manager.validators import ServerActionInput
from minecraft_manager.blueprints.api.validators import validate_payload, validate_user, check_dependent_object, validate_server
from minecraft_manager.blueprints.api.exceptions import error_response
from minecraft_manager.utils.users import filtered_server_list, filtered_server
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from datetime import datetime
import logging


@blueprint.route('/actions/<action_id>', methods=['GET'])
@requires_auth
@user_required
def get_server_list(current_user, action_id):
    current_app.logger.debug(f"GET /actions/{action_id}: {request}, current_user: {current_user}")

    # TODO

    return {
        # TODO
    }
