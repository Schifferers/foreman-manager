__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""


from flask import current_app
from minecraft_manager import constants
from minecraft_manager.utils.servers import query_server_status
from minecraft_manager.common.exceptions import ForbiddenException, NotFoundException, ActionNotSupportedException
import logging


def _check_perms(obj:dict, user:str) -> bool:
    current_app.logger.debug("obj: %s, user: %s", obj, user)

    users = obj.get('users')
    current_app.logger.debug("users: %s", users)
    if users is None:
        current_app.logger.debug("Users dictionary is not present (no restrictions); returning true.")
        return True

    allowed_users = users.get('allowed')
    current_app.logger.debug("allowed_users: %s", allowed_users)
    denied_users = users.get('denied')
    current_app.logger.debug("denied_users: %s", denied_users)

    if (denied_users is not None) and (user in denied_users):
        current_app.logger.debug("User found in denied users list; returning false.")
        return False

    if allowed_users is None:
        current_app.logger.debug("Allowed users list is not present (no restrictions); returning true.")
        return True

    if len(allowed_users) == 0:
        current_app.logger.debug("Allowed users list is empty (implicit deny); returning false.")
        return False

    if user in allowed_users:
        current_app.logger.debug("User found in allowed users list (explicit allow); returning true.")
        return True

    current_app.logger.debug("Fell through; return false.")
    return False


def _check_action(action:dict, user:str) -> bool:
    current_app.logger.debug("action: %s, user: %s", action, user)

    return _check_perms(action, user)


def _check_server(server:dict, user:str) -> bool:
    current_app.logger.debug("server: %s, user: %s", server, user)

    return _check_perms(server, user)


def filtered_server(server_id:str, user:str) -> dict:
    """
    Returns the specified server, if the user is permitted to access it.
    If no server was found, returns None. If a server was found, but the user
    was not permitted, returns an empty dict.
    """
    current_app.logger.debug("server_id: %s, user: %s", server_id, user)

    servers = current_app.config[constants.SERVERS]
    current_app.logger.debug("servers: %s", servers)

    for server in servers:
        current_app.logger.debug("server: %s", server)
        if server['id'] == server_id:
            if _check_server(server, user):
                server = query_server_status(server)
                current_app.logger.debug("Check server call passed; return server.")
                return server
            else:
                current_app.logger.debug("Check server call failed; return empty object.")
                return {}

    current_app.logger.debug("Server loop exited; return None.")
    return None


def validate_action(server:dict, action:str, user:str):
    """
    Validate that the action can be performed by the user on the server.
    """
    current_app.logger.debug("server: %s, action: %s, user: %s", server, action, user)

    if not _check_server(server, user):
        raise ForbiddenException

    action_data = server.get('actions', {}).get(action)
    if action_data is None:
        raise NotFoundException

    if not _check_action(action_data, user):
        raise ForbiddenException

    return action_data


def filtered_server_list(user:str) -> list:
    """
    Returns a list of servers that the user is permitted to access.
    """
    current_app.logger.debug("user: %s", user)

    servers = current_app.config[constants.SERVERS]
    current_app.logger.debug("servers: %s", servers)

    filtered_servers = []
    for server in servers:
        current_app.logger.debug("server: %s", server)
        if _check_server(server, user):
            server = query_server_status(server)
            filtered_servers.append(server)
    current_app.logger.debug("filtered_servers: %s", filtered_servers)

    return filtered_servers
