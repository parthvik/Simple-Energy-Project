# central_server.py
import eventlet
eventlet.monkey_patch()
from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json
from message_queue import setup_message_queue
from collections import Counter

app = Flask(__name__)
CORS(app)

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

socketio = setup_message_queue(app)

@app.route('/update_state', methods=['POST'])
def update_state():
    data = request.get_json()
    signal_id = data.get('signal_id')
    state = data.get('state')

    if signal_id and state:
        # Update signal state in Redis
        r.hset('signals', signal_id, state)
        # Add to recent updates in Redis
        recent_update = json.dumps({'signal_id': signal_id, 'state': state})
        r.lpush('recent_updates', recent_update)
        r.ltrim('recent_updates', 0, 9)  # Keep only the last 10 updates
        # Publish update to Redis Pub/Sub
        r.publish('signal_updates', recent_update)
        print(f"Published update: {recent_update}")
        return 'OK', 200
    else:
        return 'Bad Request', 400

@app.route('/get_states', methods=['GET'])
def get_states():
    # Retrieve signal states from Redis
    signals_data = r.hgetall('signals')
    signals = {k.decode('utf-8'): v.decode('utf-8') for k, v in signals_data.items()}
    # Calculate counts
    counts = Counter(signals.values())
    # Retrieve recent updates from Redis
    recent_updates_data = r.lrange('recent_updates', 0, -1)
    recent_updates = [json.loads(update.decode('utf-8')) for update in recent_updates_data]
    return jsonify({
        'signals': signals,
        'counts': counts,
        'recent_updates': recent_updates
    })

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)