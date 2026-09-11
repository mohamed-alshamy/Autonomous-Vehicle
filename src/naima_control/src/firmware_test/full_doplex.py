#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy


class SerialNode(Node):
    def __init__(self):
        super().__init__('serial_node')

        qos = QoSProfile(
            durability=QoSDurabilityPolicy.VOLATILE,
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )

        # Declare and get parameters
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 9600)

        self.port__ = self.get_parameter('port').value
        self.baudrate__ = self.get_parameter('baudrate').value


        # Setup serial connection
        try:
            self.arduino__ = serial.Serial(self.port__, self.baudrate__, timeout=0.1)
            self.get_logger().info(f'Serial connected on {self.port__} at {self.baudrate__} baudrate')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to serial: {e}')
            return

        # Publisher to serial_rx topic
        self.publisher_ = self.create_publisher(String, 'serial_rx',  qos)

        # Subscriber to serial_tx topic
        self.subscriber_ = self.create_subscription(String, 'serial_tx', self.msg_callback, qos)

        # Timer to check for incoming serial data
        self.timer_ = self.create_timer(0.1, self.read_serial_callback)

    def read_serial_callback(self):
        if self.arduino__.in_waiting > 0:
            data = self.arduino__.readline()
            try:
                decoded = data.decode('utf-8').strip()
                msg = String()
                msg.data = decoded
                self.publisher_.publish(msg)
                self.get_logger().info(f'Published: {decoded}')
            except UnicodeDecodeError:
                self.get_logger().warn('Received undecodable data')

    def msg_callback(self, msg):
        try:
            self.arduino__.write((msg.data + "\n") .encode('utf-8'))
            self.get_logger().info(f'Sent: {msg.data}')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to write to serial: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = SerialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
