"""Worker application.

It calls an external slow task and send its output, line by line, as "log"
events through SocketIO. The web page will then print the lines.
"""
# Disable the warning because eventlet must patch the standard library as soon
# as possible.
from communication import (CELERY,
                           get_socketio)  # pylint: disable=wrong-import-order

import socket
from datetime import datetime
from subprocess import PIPE, Popen

SOCKETIO = get_socketio()


def announce():
    """Tell this worker is up and running."""
    hostname = socket.gethostname()
    time = datetime.now().strftime('%H:%M:%S')
    msg = '{} Worker {} is up.'.format(time, hostname)
    SOCKETIO.emit('log', {'data': msg})


announce()


@CELERY.task
def add_task(name):
    """Run the slow task as a subprocess and send results to the web site."""
    args = './slow_task.sh', str(name)
    with Popen(args, stdout=PIPE, universal_newlines=True) as proc:
        for line in proc.stdout:
            SOCKETIO.emit('log', {'data': line.rstrip()})
