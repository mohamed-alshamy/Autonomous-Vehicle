#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time


class SimpleSerialReceiver(Node):
    def __init__(self):
        super().__init__('simple_serial_receiver')
        self.pub__ = self.create_publisher(String, 'serial_rx', 10)
        self.frequency__ = 0.01
        self.get_logger().info('Publishing to serial_rx topic at %d Hz' % self.frequency__)

        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 9600)

        self.port__ = self.get_parameter('port').value
        self.baudrate__ = self.get_parameter('baudrate').value
        self.arduino__ = serial.Serial(self.port__, self.baudrate__)

        self.timer__ = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        if rclpy.ok() and self.arduino__.is_open:
            data = self.arduino__.readline()
            try:
                data = data.decode("utf-8")
            except UnicodeDecodeError:
                self.get_logger().error('Failed to decode data')
                return
            
            msg = String()
            msg.data = str(data)
            self.pub__.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SimpleSerialReceiver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


    