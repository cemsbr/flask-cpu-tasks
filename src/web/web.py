"""Web server.

There's only a simple page to diplay the log messages sent by workers and other
web servers.
"""
# Disable the warning because eventlet must patch the standard library as soon
# as possible.
from communication import (CELERY,
                           get_socketio)  # pylint: disable=wrong-import-order

import socket
from datetime import datetime

from flask import Flask, jsonify, render_template, request

HOSTNAME = socket.gethostname()
FLASK = Flask(__name__)
SOCKETIO = get_socketio(FLASK)


@FLASK.route('/')
def show_log():
    """Display the page that will show log messages using JavaScript."""
    return render_template('index.html', hostname=HOSTNAME)


@FLASK.route('/tasks', methods=['POST'])
def new_task():
    """Receive new tasks from users via POST method."""
    # Create the log message
    time = datetime.now().strftime('%H:%M:%S')
    name = request.json['name']
    log = '{} Web server {} received Task {}'

    # Send the message as a "log" event
    SOCKETIO.emit('log', {'data': log.format(time, HOSTNAME, name)})
    # Send the task to workers (asynchronous result, non-blocking)
    task = CELERY.send_task('worker.add_task', args=(name,))
    # Return the task ID (keeping progress of the task is currently not
    # implemented).
    return jsonify(data={'task': {'id': task.id}})
