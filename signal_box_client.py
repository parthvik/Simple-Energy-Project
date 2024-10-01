# signal_box_client.py
import requests
import time
import random
import threading
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

SERVER_URL = 'http://localhost:5001/update_state'

# Initialize unsent_messages and its lock
unsent_messages = []
unsent_messages_lock = threading.Lock()

def send_state_update(session, signal_id, state):
    data = {
        'signal_id': signal_id,
        'state': state
    }
    try:
        response = session.post(SERVER_URL, json=data)
        if response.status_code == 200:
            print(f"State update sent for {signal_id}: {state}")
            # Remove from buffer if it was a retry
            with unsent_messages_lock:
                if data in unsent_messages:
                    unsent_messages.remove(data)
        else:
            print(f"Failed to send state update for {signal_id}: {response.status_code}")
            buffer_message(data)
    except requests.exceptions.RequestException as e:
        print(f"Error sending state update for {signal_id}: {e}")
        buffer_message(data)

def buffer_message(data):
    with unsent_messages_lock:
        if data not in unsent_messages:
            unsent_messages.append(data)

def resend_buffered_messages(session):
    with unsent_messages_lock:
        for data in unsent_messages[:]:
            try:
                response = session.post(SERVER_URL, json=data)
                if response.status_code == 200:
                    print(f"Buffered message sent for {data['signal_id']}: {data['state']}")
                    unsent_messages.remove(data)
            except requests.exceptions.RequestException:
                # Connection is still down; stop trying
                break

def run_signal(signal_id):
    states = ['red', 'amber', 'green']

    # Configure session with retry strategy
    session = requests.Session()
    retry_strategy = Retry(
        total=0,  # We handle retries manually
        backoff_factor=0,
        status_forcelist=[],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    while True:
        state = random.choice(states)
        resend_buffered_messages(session)
        send_state_update(session, signal_id, state)
        time.sleep(random.uniform(5, 15))  # Random interval between updates

def main(num_signals):
    threads = []
    for i in range(num_signals):
        signal_id = f'signal_{i+1:03d}'  # Creates IDs like signal_001, signal_002, etc.
        thread = threading.Thread(target=run_signal, args=(signal_id,))
        thread.start()
        threads.append(thread)

    # Threads run indefinitely; no need to join

if __name__ == '__main__':
    num_signals = int(os.environ.get('NUM_SIGNALS', 100))  # Default to 25 if not specified
    main(num_signals)