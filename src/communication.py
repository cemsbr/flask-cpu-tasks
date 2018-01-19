"""Initialize task queue and SocketIO server.

Import CELERY and/or get_socketio from this module as soon as possible so that
eventlet can patch the standard library.
"""
import eventlet
eventlet.monkey_patch()  # NOQA

# As imports should be wrote first, we ignore this kind of error with both
# pylint pragma and isort's NOQA.
# pylint: disable=wrong-import-position
from celery import Celery
from flask_socketio import SocketIO

# settings.py must have the current redis IP
from settings import BROKER

CELERY = Celery('worker', broker=BROKER)


def get_socketio(flask_app=None):
    """Return either a server (given flask_app) or a client."""
    return SocketIO(app=flask_app, async_mode='eventlet',
                    message_queue=BROKER, logger=True, engineio_logger=True)
