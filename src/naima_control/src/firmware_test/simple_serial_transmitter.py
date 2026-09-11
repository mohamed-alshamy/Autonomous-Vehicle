#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32
import serial
import time

class SimpleSerialTransmitter(Node):
    def __init__(self):
        super().__init__('simple_serial_transmitter')

        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 9600)

        self.port__ = self.get_parameter('port').value
        self.baudrate__ = self.get_parameter('baudrate').value
        self.arduino__ = serial.Serial(self.port__, self.baudrate__, timeout=0.1)

        self.sub__ = self.create_subscription(String, 'serial_tx', self.msgcallback, 10)
        self.sub__
    
    def msgcallback(self, msg):
        self.arduino__.write(msg.data.encode("utf-8"))


def main(args=None):
    rclpy.init(args=args)
    node = SimpleSerialTransmitter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()