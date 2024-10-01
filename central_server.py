from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import Counter, deque
import redis
import json
from message_queue import setup_message_queue

app = Flask(__name__)
CORS(app)

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# Store the state of each signal
signals = {}
# Store the last 10 updates
recent_updates = deque(maxlen=10)

@app.route('/update_state', methods=['POST'])
def update_state():
    data = request.get_json()
    signal_id = data.get('signal_id')
    state = data.get('state')

    if signal_id and state:
        # Update signal state
        signals[signal_id] = state
        # Add to recent updates
        recent_updates.appendleft({'signal_id': signal_id, 'state': state})
        # Publish update to Redis
        r.publish('signal_updates', json.dumps({'signal_id': signal_id, 'state': state}))
        return 'OK', 200
    else:
        return 'Bad Request', 400

@app.route('/get_states', methods=['GET'])
def get_states():
    # Calculate counts
    counts = Counter(signals.values())
    return jsonify({
        'signals': signals,
        'counts': counts,
        'recent_updates': list(recent_updates)
    })

# Add this line after creating the Flask app
socketio = setup_message_queue(app)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)