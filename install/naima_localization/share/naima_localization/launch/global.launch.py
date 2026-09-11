from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_global',
            output='screen',
            parameters=['/home/men3m/Naima/src/naima_localization/config/global_ekf.yaml'],
            remappings=[('odometry/filtered', 'odometry/global'),
                        ('/set_pose', '/initialpose'),]
           )
        
    ])
