from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # عقدة تحويل السحابة النقطية إلى مسح ليزري
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            output='screen',
            parameters=[{
                'target_frame': 'zed_left_camera_frame',
                'transform_tolerance': 0.2,  
                'min_height': -10.0,  
                'max_height': 10.0,   
                'angle_min': -1.57,   
                'angle_max': 1.57,   
                'angle_increment': 0.0087, 
                'scan_time': 0.0333,  
                'range_min': 0.2,    
                'range_max': 10.0,    
                'use_inf': True,
                'inf_epsilon': 1.0  
            }],
            remappings=[
                ('cloud_in', '/zed/zed_node/point_cloud/cloud_registered'),
        #         ('scan', '/scan')     # نشر على /scan لتلبية احتياجات Nav2
        #     ],
        #     arguments=['--ros-args', '--log-level', 'debug']  # تصحيح الأخطاء
        # ),

        # # عقدة تحويل TF ثابت (اضبط الإحداثيات حسب موضع الكاميرا)
        # Node(
        #     package='tf2_ros',
        #     executable='static_transform_publisher',
        #     name='static_transform_publisher',
        #     arguments=[
        #         '--x', '0', '--y', '0', '--z', '0.2',  # افتراض: الكاميرا مرتفعة 20 سم
        #         '--qx', '0', '--qy', '0', '--qz', '0', '--qw', '1',
        #         '--frame-id', 'base_link', '--child-frame-id', 'zed_left_camera_frame'
            ]
        )
    ])