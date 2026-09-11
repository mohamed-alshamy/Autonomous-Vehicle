#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2
import math

class PointCloudInspector(Node):
    def __init__(self):
        super().__init__('point_cloud_inspector')
        self.subscription = self.create_subscription(
            PointCloud2,
            '/zed/zed_node/point_cloud/cloud_registered',
            self.callback,
            10
        )

    def callback(self, msg):
        gen = pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=False)
        valid_points = 0
        total_points = 0
        min_z = float('inf')
        max_z = float('-inf')
        min_range = float('inf')
        max_range = float('-inf')
        for point in gen:
            total_points += 1
            x, y, z = point
            if not any([math.isnan(p) or math.isinf(p) for p in [x, y, z]]):
                valid_points += 1
                min_z = min(min_z, z)
                max_z = max(max_z, z)
                range_xy = math.sqrt(x**2 + y**2)
                min_range = min(min_range, range_xy)
                max_range = max(max_range, range_xy)
        self.get_logger().info(
            f'Valid points: {valid_points}/{total_points}, '
            f'Z range: [{min_z:.2f}, {max_z:.2f}], '
            f'Range (xy): [{min_range:.2f}, {max_range:.2f}]'
        )

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudInspector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()