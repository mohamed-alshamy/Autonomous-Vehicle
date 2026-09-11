import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare  # Correct import for FindPackageShare

def generate_launch_description():
    # Declare launch arguments
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    package_name = 'naima'
    pkg_share = FindPackageShare(package=package_name).find(package_name)

    # Get URDF file path
    urdf_file_name = 'naima.urdf.xacro'
    urdf = os.path.join(pkg_share, 'urdf', urdf_file_name)

    # Open the URDF file in binary mode and decode
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    # Remove the XML declaration from the URDF string
    robot_desc_lines = robot_desc.splitlines(keepends=True)
    if robot_desc_lines[0].strip().startswith('<?xml'):
        robot_desc = ''.join(robot_desc_lines[1:])  # Remove the first line

    robot_description = {"robot_description": robot_desc.strip()}  # Trim any leading/trailing whitespace

    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'robot_description': robot_description["robot_description"]
        }],
    )

    # Joint State Publisher Node
    start_joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        name='joint_state_publisher',
    )

    # Spawn the robot in Gazebo
    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=["-topic", "/robot_description", 
                    "-entity", 'naima',
                    "-x", '0.0',
                    "-y", '0.0',
                    "-z", '0.05',
                    "-Y", '0.0'],
    )

    # Launch Gazebo
    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', 
             '-s', 'libgazebo_ros_init.so'], output='screen',
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        robot_state_publisher_node,
        start_joint_state_publisher_cmd,
        spawn,
        gazebo
    ])
