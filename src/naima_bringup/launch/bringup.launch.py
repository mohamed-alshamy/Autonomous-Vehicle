import launch
import launch_ros
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    camera_model_arg = DeclareLaunchArgument(
        'camera_model',
        default_value='zed2',
        description='The model of the ZED camera'
    )

    return LaunchDescription([
        camera_model_arg,

        # URDF + Robot State Publisher
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                FindPackageShare('naima_description').find('naima_description') + '/launch/display.launch.py'
            ])
        ),
        
                # Pointcloud to LaserScan
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                FindPackageShare('naima_bringup').find('naima_bringup') + '/launch/pointcloud_to_laserscan.launch.py'
            ])
        ),


        # GNSS node
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                FindPackageShare('ublox_gps').find('ublox_gps') + '/launch/ublox_gps_node_1-launch.py'
            ])
        ),

        # ZED Camera Node with TF publication disabled
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                FindPackageShare('zed_wrapper').find('zed_wrapper') + '/launch/zed_camera.launch.py'
            ]),
            launch_arguments={
                'camera_model': LaunchConfiguration('camera_model'),
                'publish_tf': 'false'  
            }.items()
        ),

        # Static TF from base_link to zed_camera_link
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_zed_broadcaster',
            arguments=['0', '0', '0', '0', '0', '0', 'zed2_camera_link', 'zed_camera_link'],
            output='screen'
        ),

        # Localization: dual_ekf_and_navsat
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                FindPackageShare('naima_localization').find('naima_localization') + '/launch/dual_ekf_and_navsat.launch.py'
            ])
        ),

        # Localization: local.launch.py
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                FindPackageShare('naima_localization').find('naima_localization') + '/launch/local.launch.py'
            ])
        ),

        # Localization: mappp.launch.py
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                FindPackageShare('naima_localization').find('naima_localization') + '/launch/mappp.launch.py'
            ])
        ),
        
          #  Add the model.py node
        Node(
            package='naima_bringup',
            executable='model',
            name='kinematic_bicycle_model',
            output='screen'
        ),
    ])
