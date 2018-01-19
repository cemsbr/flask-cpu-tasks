# Flask, SocketIO and Celery

This is a scalable solution to distribute CPU-intensive tasks among workers. A REST API receives a task, send it to workers and after processing, the worker will send the results directly to the users. The solution is asynchronous and scales well by just adding workers.


## Requirements

If you can't or don't want to install dependencies in your system, follow the docker instructions.


### Local Install

- Redis: `apt install redis` on Debian/Ubuntu;
- Python >= 3.5.4
- `pip3 install requirements.txt`

Launch:

```bash
# Make sure Redis is running
systemctl status redis
# Launch the web server
FLASK_APP=src/web/web.py flask run
# In a second terminal, run a worker
cd src/worker
celery worker -A worker -P eventlet -c 1 --prefetch-multiplier=1
```

The web server should be in http://localhost:5000. You can run more workers in other terminals. To stop them, use `stop` instead of `status` for redis and hit CTRL+c in Flask and Celery terminals.


### Docker

Instead of installing packages, you can use docker:

```bash
# Run "make docker" only once to create the web and worker images.
# Run it again if you change the settings.py file or any other source code.
make docker
docker run --name=redis -d redis
# If needed, change Redis IP address in settings.py
docker run --name=web01 -d web
docker run --name=worker01 -d worker
```

If you had no other container previously, the web server is probably at http://172.17.0.2. Launch other web or worker containers at any time. You hardly will need more than one web instance.

To stop the containers:

```bash
docker stop worker01 web01 redis
```

Later, you can start them again. To have the same IP addresses, use the same order as below or edit *settings.py* with a different Redis IP.

```bash
docker start redis
docker start web01
docker start worker01
```

To delete the containers, use the `stop` and then `rm` commands.


## Creating Tasks

With curl (`http://localhost:5000/tasks` for local install):

`curl -X POST -H "Content-Type: application/json" -d '{"name": "Hello"}' http://172.17.0.2/tasks`

With httpie (`172.17.0.2/tasks` for docker install):

`http :5000/tasks name=Hello`


## Troubleshooting

### WebSocket disconnected

After adding or removing instances, including the first worker, the WebSocket will disconnect only once during a task execution (I'm still investigating this issue). You may lose the task completion message, but don't worry: the task will be completed, the reconnection is automatic and you'll see all the messages for the subsequent tasks.
