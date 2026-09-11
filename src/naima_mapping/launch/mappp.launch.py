import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
import launch_ros.actions


def generate_launch_description():

    ld = LaunchDescription()

    # Map server
    map_server_config_path = os.path.join(
        get_package_share_directory('naima_mapping'),
        'config',
        'map_server_params.yaml'
    )



    map_server_cmd = Node(
        package='nav2_map_server',
        executable='map_server',
        output='screen',
        parameters=[map_server_config_path])


    lifecycle_nodes = ['map_server']
    use_sim_time = False
    autostart = True

    start_lifecycle_manager_cmd = launch_ros.actions.Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager',
            output='screen',
            emulate_tty=True,  # https://github.com/ros2/launch/issues/188
            parameters=[{'use_sim_time': use_sim_time},
                        {'autostart': autostart},
                        {'node_names': lifecycle_nodes}])


    # Static transform publisher from map to odom with zero offset
    static_tf = Node(   
    package='tf2_ros',
    executable='static_transform_publisher',
    name='static_map_to_odom_tf',
    arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
    output='screen'
    )
    static_camera_tf = Node(   
    package='tf2_ros',
    executable='static_transform_publisher',
    name='static_camera_tf',
    arguments=['0', '0', '0', '0', '0', '0', 'zed2_camera_link', 'zed_camera_link'],
    output='screen'
    )


    ld.add_action(map_server_cmd)
    ld.add_action(start_lifecycle_manager_cmd)
    ld.add_action(static_tf)
    ld.add_action(static_camera_tf)
    return ld

