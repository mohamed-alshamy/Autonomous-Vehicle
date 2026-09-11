#!/usr/bin/env python3
import math
import numpy as np
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
import tf_transformations as tf
from tf2_ros import TransformBroadcaster

from geometry_msgs.msg import TransformStamped
import PyKDL as kdl



class KinematicBicycleModel(Node):
    def __init__(self):
        super().__init__('kinematic_bicycle_model')
        self.tf_br = TransformBroadcaster(self)
        # Initial pose
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.x_dot = 0.0
        self.y_dot = 0.0
        self.theta_dot = 0.0
        self.wheel_base = 2.1
        
        # Publisher
        self.odom_pub = self.create_publisher(Odometry, 'wheel/odometry', 10)
        
        # Timer for publishing odometry at 10 Hz
        self.timer = self.create_timer(0.1, self.publish_odometry)
        
        # Motion parameters
        self.v = 0.0  # Speed (m/s)
        self.delta = 0.0  # Steering angle (degrees)
        self.mode = 1
    def update(self, dt):
        """Update vehicle state using kinematic bicycle model"""
        delta = math.radians(self.delta)
        if self.mode == 0:
            self.x += self.v * math.cos(self.theta) * dt
            self.y += self.v * math.sin(self.theta) * dt
            self.theta += (self.v / self.wheel_base) * math.tan(delta) * dt
        elif self.mode == 1:
            self.x += self.v * math.cos(self.theta + delta) * dt
            self.y += self.v * math.sin(self.theta + delta) * dt
            self.theta += (self.v / self.wheel_base) * math.sin(delta) * dt
        elif self.mode == 2:
            l_r = 0.214 * self.wheel_base
            l_f = self.wheel_base - l_r
            beta = math.atan(l_r * math.tan(delta) / self.wheel_base)
            self.x += self.v * math.cos(self.theta + beta) * dt
            self.y += self.v * math.sin(self.theta + beta) * dt
            self.theta += (self.v * math.tan(delta) * math.cos(beta) / self.wheel_base) * dt

        # Compute velocities
        self.x_dot = self.v * math.cos(self.theta)
        self.y_dot = self.v * math.sin(self.theta)
        self.theta_dot = (self.v / self.wheel_base) * math.tan(delta)

    def publish_odometry(self):
        """Publish the odometry message"""
        dt = 0.1  # Time step (10 Hz)
        self.update(dt)

        odom_msg = Odometry()
        odom_msg.header.stamp = self.get_clock().now().to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_footprint'

        # Position
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0

        # Orientation
        quat = tf.quaternion_from_euler(0, 0, self.theta)
        odom_msg.pose.pose.orientation = Quaternion(
            x=quat[0], y=quat[1], z=quat[2], w=quat[3]
        )

        # Velocity
        odom_msg.twist.twist.linear.x = self.x_dot
        odom_msg.twist.twist.linear.y = self.y_dot
        odom_msg.twist.twist.angular.z = self.theta_dot
        
        


        # Publish odometry
        self.odom_pub.publish(odom_msg)
        self.get_logger().info(f'Published odometry: x={self.x:.2f}, y={self.y:.2f}, θ={self.theta:.2f}')
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "odom"
        t.child_frame_id = "base_footprint"
        t.transform.translation.x = odom_msg.pose.pose.position.x
        t.transform.translation.y = odom_msg.pose.pose.position.y
        t.transform.translation.z = odom_msg.pose.pose.position.z
        t.transform.rotation.x = odom_msg.pose.pose.orientation.x
        t.transform.rotation.y = odom_msg.pose.pose.orientation.y
        t.transform.rotation.z = odom_msg.pose.pose.orientation.z
        t.transform.rotation.w = odom_msg.pose.pose.orientation.w

        self.tf_br.sendTransform(t)





def main(args=None):
    rclpy.init(args=args)
    node = KinematicBicycleModel()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

