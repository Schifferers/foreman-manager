__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
servers.py
- Servers API
"""


from flask import session, jsonify, request, current_app
from minecraft_manager.blueprints.api import blueprint
from minecraft_manager import constants
from minecraft_manager.db import db
from minecraft_manager.controllers.minecraft import execute_action
from minecraft_manager.utils.servers import query_server_status
from minecraft_manager.models import constants as model_constants
from minecraft_manager.blueprints.api import user_required, requires_auth
from minecraft_manager.blueprints.api.manager.validators import ServerActionInput
from minecraft_manager.blueprints.api.validators import validate_payload, validate_user, check_dependent_object, validate_server
from minecraft_manager.blueprints.api.exceptions import error_response
from minecraft_manager.utils.users import filtered_server_list, filtered_server
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from datetime import datetime
import logging


@blueprint.route('/servers', methods=['GET'])
@requires_auth
@user_required
def get_server_list(current_user):
    current_app.logger.debug(f"GET /servers: {request}, current_user: {current_user}")

    server_list = filtered_server_list(current_user)
    current_app.logger.debug("server_list: %s", server_list)

    return {
        'servers': server_list,
    }


@blueprint.route('/servers/<server_id>', methods=['GET'])
@user_required
def get_server(current_user, server_id):
    current_app.logger.debug(f"GET /servers/{server_id}: {request}, current_user: {current_user}")

    server = validate_server(server_id, current_user)

    return server


@blueprint.route('/servers/<server_id>/action', methods=['POST'])
@user_required
def post_server_action(current_user, server_id):
    current_app.logger.debug(f"POST /servers/{server_id}/action: {request}, current_user: {current_user}")

    validate_payload(ServerActionInput, request)
    data = request.get_json()
    if data.get('server_id') != server_id:
        raise error_response(BadRequest, 'bad_request',
                             "Server ID in URL does not match server ID in payload")
    server = validate_server(server_id, current_user)

    action_id = execute_action(data, server, current_user)

    return {
        'action_id': action_id,
    }, 202
