#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class CmdVelToSerial(Node):
    def __init__(self):
        super().__init__('cmd_vel_to_serial')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.publisher = self.create_publisher(String, '/serial_tx', 10)
        self.get_logger().info("Node started: Listening to /cmd_vel and publishing to /serial_tx")

    def cmd_vel_callback(self, msg: Twist):
        linear = msg.linear.x
        angular = msg.angular.z

        # --- Convert angular.z to steering angle A in range [-15, 15]
        steering_angle = max(min(angular , 15.0), -15.0)
        steering_angle = round(steering_angle)

        # --- Convert linear.x to throttle B
        if linear == 0:
            throttle = 0
        elif 0 < linear < 0.5:
            throttle = 1
        else:  # linear >= 0.5
            throttle = 2

        # --- Horn is always off
        horn = 0

        # --- Format string: A:<steering>,B:<throttle>C:<horn>
        serial_str = f"A:{steering_angle},B:{throttle},C:{horn}"

        # Publish
        msg_out = String()
        msg_out.data = serial_str
        self.publisher.publish(msg_out)
        self.get_logger().info(f"Published: {serial_str}")

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelToSerial()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
