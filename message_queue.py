# message_queue.py
import redis
import json
from flask_socketio import SocketIO

r = redis.Redis(host='localhost', port=6379, db=0)

def setup_message_queue(app):
    socketio = SocketIO(app, cors_allowed_origins="*")

    def message_handler(message):
        data = json.loads(message['data'])
        print(f"Received message: {data}")
        socketio.emit('signal_update', data)

    pubsub = r.pubsub()
    pubsub.subscribe(**{'signal_updates': message_handler})
    pubsub.run_in_thread(sleep_time=0.001)

    return socketio