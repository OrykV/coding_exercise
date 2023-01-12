import flask
import json

from playhouse.shortcuts import model_to_dict

from . import database


blueprint = flask.Blueprint("tasks", __name__)


@blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    """List all tasks.py."""
    tasks = database.Task.select()
    return flask.jsonify({
        "data": [task.to_response(flask.request.base_url) for task in tasks]
    })


@blueprint.route('/tasks', methods=['POST'])
def create_task():
    """Create the new docker task"""
    if "data" not in flask.request.json:
        return flask.jsonify({"error": "data is required"}), 400

    if "attributes" not in flask.request.json["data"]:
        return flask.jsonify({"error": "data.attributes is required"}), 400

    if "title" not in flask.request.json["data"]["attributes"]:
        return flask.jsonify({"error": "data.attributes.title is required"}), 400

    task = database.Task.create(
        title=flask.request.json["data"]["attributes"]["title"],
        command=flask.request.json["data"]["attributes"]["command"],
        image=flask.request.json["data"]["attributes"]["image"],
        description=flask.request.json["data"]["attributes"]["description"],
    )

    return flask.jsonify({"data": task.to_response(flask.request.base_url)}), 201


@blueprint.route('/tasks/<id>', methods=['DELETE'])
def delete_task_object(id):
    database.Task.delete_by_id(id)
    return flask.jsonify({"result": f"Successfully deleted item {id}"}), 200


@blueprint.route('/tasks/<id>', methods=['GET'])
def get_task_by_id(id):
    task = database.Task.get_by_id(id)
    return flask.jsonify({
        "data": [task.to_response(flask.request.base_url)]
    })


@blueprint.route('/tasks/<id>', methods=['PATCH'])
def edit_task_by_id(id):
    task = database.Task.get_by_id(id)
    updated_task = task.update(
        title=flask.request.json["data"]["attributes"]["title"],
        command=flask.request.json["data"]["attributes"]["command"],
        image=flask.request.json["data"]["attributes"]["image"],
        description=flask.request.json["data"]["attributes"]["description"],
    )
    updated_task.execute()
    performed_task = database.Task.get_by_id(id)
    return flask.jsonify({
        "data": [performed_task.to_response(flask.request.base_url)]
    })



@blueprint.route('/tasks/<id>/logs', methods=['GET'])
def get_task_logs_by_id(id):
    task = database.Task.get_by_id(id)




