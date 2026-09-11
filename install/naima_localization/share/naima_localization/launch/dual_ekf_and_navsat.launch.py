from launch import LaunchDescription
import launch_ros.actions
import os
import yaml
from launch.substitutions import EnvironmentVariable
import pathlib
import launch.actions
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    naima_localization_dir = get_package_share_directory('naima_localization')
    parameters_file_dir = os.path.join(naima_localization_dir, 'config')
    parameters_file_path = os.path.join(parameters_file_dir, 'dual_ekf_and_navsat.yaml')
    os.environ['FILE_PATH'] = str(parameters_file_dir)
    return LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'output_final_position',
            default_value='false'),
        launch.actions.DeclareLaunchArgument(
            'output_location',
	    default_value='~/dual_ekf_navsat_example_debug.txt'),
	
    # launch_ros.actions.Node(
    #         package='robot_localization',
    #         executable='ekf_node',
    #         name='ekf_filter_node_odom',
    #         output='screen',
    #         parameters=[parameters_file_path],
    # ),
    launch_ros.actions.Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_map',
            output='screen',
            parameters=[parameters_file_path],
            remappings=[('odometry/filtered', 'odometry/global'),
                        ('/set_pose', '/initialpose')]
    ),           
    launch_ros.actions.Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform',
            output='screen',
            parameters=[parameters_file_path],
            remappings=[('imu', 'zed/zed_node/imu/data'),
                        ('gps/fix', '/fix'),
                        ('odometry/filtered', 'odometry/global')])
])




  # Start the navsat transform node which converts GPS data into the world coordinate frame
#   start_navsat_transform_cmd = Node(
#     package='robot_localization',
#     executable='navsat_transform_node',
#     name='navsat_transform',
#     output='screen',
#     parameters=[robot_localization_file_path, 
#     {'use_sim_time': use_sim_time}],
#     remappings=[('imu', 'imu/data'),
#                 ('gps/fix', 'gps/fix'), 
#                 ('gps/filtered', 'gps/filtered'),
#                 ('odometry/gps', 'odometry/gps'),
#                 ('odometry/filtered', 'odometry/global')])

  # Start robot localization using an Extended Kalman filter...map->odom transform
#   start_robot_localization_global_cmd = Node(
#     package='robot_localization',
#     executable='ekf_node',
#     name='ekf_filter_node_map',
#     output='screen',
#     parameters=[robot_localization_file_path, 
#     {'use_sim_time': use_sim_time}],
#     remappings=[('odometry/filtered', 'odometry/global'),
#                 ('/set_pose', '/initialpose')])

  # Start robot localization using an Extended Kalman filter...odom->base_footprint transform
#   start_robot_localization_local_cmd = Node(
#     package='robot_localization',
#     executable='ekf_node',
#     name='ekf_filter_node_odom',
#     output='screen',
#     parameters=[robot_localization_file_path, 
#     {'use_sim_time': use_sim_time}],
#     remappings=[('odometry/filtered', 'odometry/local'),
#                 ('/set_pose', '/initialpose')])
