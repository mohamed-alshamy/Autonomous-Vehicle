#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import signal
import sys

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class TeleopNode(Node):
    def __init__(self):
        super().__init__('web_teleop_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

    def publish_cmd(self, linear_x, angular_z):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published: linear_x={linear_x}, angular_z={angular_z}")

ros_node = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('move_command')
def handle_move_command(json):
    linear_x = float(json.get('linear_x', 0))
    angular_z = float(json.get('angular_z', 0))
    print(f"Received: linear_x={linear_x}, angular_z={angular_z}")
    ros_node.publish_cmd(linear_x, angular_z)
    emit('response', {'status': 'ok'})

def ros_spin():
    rclpy.spin(ros_node)

def signal_handler(sig, frame):
    rclpy.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    rclpy.init()
    ros_node = TeleopNode()
    ros_thread = threading.Thread(target=ros_spin, daemon=True)
    ros_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
