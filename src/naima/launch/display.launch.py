import launch
from launch.substitutions import LaunchConfiguration
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription


def generate_launch_description():

    urdf_file_name = 'naima.urdf.xacro'
    urdf = os.path.join(
        get_package_share_directory('naima'),
        'urdf',
        urdf_file_name)
    
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}],
        arguments=[urdf]
    )
    
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )
    
    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    )
    
    rviz_config_file = os.path.join(get_package_share_directory('naima'), 'rviz', 'config.rviz')

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]  # Load the RViz configuration file
    )

    map_server_launch = IncludeLaunchDescription(
      PythonLaunchDescriptionSource(
          os.path.join(
              get_package_share_directory('naima_localization'),
              'launch',
              'mappp.launch.py'
        )
    )
)

    gps_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ublox_gps'),
                'launch',
                'ublox_gps_node_1-launch.py'  
            )
        )
    )

    

    camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('zed_wrapper'),
                'launch',
                'zed_camera.launch.py'  
            )
        ),
        launch_arguments={
            'camera_model': LaunchConfiguration('zed2')
        }.items()
    )




    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
                                             description='Flag to enable joint_state_publisher_gui'),
                DeclareLaunchArgument(name='zed2', default_value='zed2',
                              description='Camera model for ZED'),
        
        # Node(
        #     package='naima',  # Replace with your actual package name
        #     executable='model(1).py',  # Name of the Python script you want to run
        #     name='odom_model',
        #     output='screen',
        #     # parameters=[]  # If you have any parameters, you can specify them here
        # ),
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node,
        map_server_launch,
        camera_launch,
        gps_launch
    ])

