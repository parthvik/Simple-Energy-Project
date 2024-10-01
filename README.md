# Traffic Signal Monitoring System

This project is a Traffic Signal Monitoring System that simulates traffic signals, updates their states, and provides a web interface to monitor these signals in real-time.

## Components

1. **signal_box_client.py**: Simulates traffic signals and sends state updates to the central server.
2. **index.html**: Web interface to display the current state of all signals and recent updates.
3. **message_queue.py**: Sets up a Redis message queue to handle real-time updates.
4. **central_server.py**: Central server that receives state updates, stores them in Redis, and serves the web interface.
5. **requirements.txt**: Lists the dependencies required for the project.

## Setup

### Prerequisites

- Python 3.x
- Redis server
- Node.js (for serving the web interface)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/traffic-signal-monitoring.git
    cd traffic-signal-monitoring
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Start the Redis server:
    ```sh
    redis-server
    ```

### Running the Project

1. **Start the Central Server**:
    ```sh
    python central_server.py
    ```

2. **Start the Signal Box Clients**:
    ```sh
    NUM_SIGNALS=100 python signal_box_client.py
    ```
    Adjust the `NUM_SIGNALS` environment variable to the desired number of simulated signals.

3. **Serve the Web Interface**:
    Open `index.html` in a web browser or use a simple HTTP server to serve the file:
    ```sh
    npx http-server .
    ```

### Usage

- Open the web interface in your browser to monitor the traffic signals.
- The interface displays the count of signals in each state (red, amber, green) and recent updates.
- The signals are updated in real-time using WebSockets.

## File Descriptions

- **signal_box_client.py**: Simulates traffic signals and sends state updates to the central server. Handles retries for failed updates.
- **index.html**: Web interface for monitoring the traffic signals. Uses Socket.IO for real-time updates.
- **message_queue.py**: Sets up a Redis message queue to handle real-time updates and emits them via Socket.IO.
- **central_server.py**: Flask server that handles state updates, stores them in Redis, and serves the web interface.
- **requirements.txt**: Lists the dependencies required for the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Redis](https://redis.io/)
- [Socket.IO](https://socket.io/)
- [Eventlet](http://eventlet.net/)
