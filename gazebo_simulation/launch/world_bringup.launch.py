import os

from ament_index_python.packages import get_package_prefix, get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():
    # ============= 获取包路径 =============
    pkg_gazebo_simulation = get_package_share_directory("gazebo_simulation")
    prefix_gazebo_simulation = get_package_prefix("gazebo_simulation")

    # =========== 声明启动参数 ===========
    debug = LaunchConfiguration("debug")
    world_name = LaunchConfiguration("world_name")

    declare_debug_cmd = DeclareLaunchArgument(
        "debug",
        default_value="false",
        description="Whether to launch Gazebo in debug mode",
    )
    declare_world_name_cmd = DeclareLaunchArgument(
        "world_name",
        default_value="empty.sdf",
        description="World filename in gazebo_simulation/worlds.",
    )

    # =========== 参数设置 ===========
    world_sdf_path = PathJoinSubstitution([
        pkg_gazebo_simulation,
        "worlds",
        world_name,
        "world.sdf",
    ])
    gui_config_path = PathJoinSubstitution([
        pkg_gazebo_simulation,
        "worlds",
        world_name,
        "gui.config",
    ])

    # =========== gazebo资源环境路径设置 ===========
    set_resource_path = SetEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH",
        [
            os.path.join(prefix_gazebo_simulation, "share"),
            ":",
            os.path.join(pkg_gazebo_simulation),
            ":",
            EnvironmentVariable("GZ_SIM_RESOURCE_PATH", default_value=""),
        ],
    )

    # =========== 启动gazebo ===========
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
        ),
        condition=UnlessCondition(debug),
        launch_arguments={
            "gz_version": "8",  # Gazebo Harmonic (ROS 2 Jazzy)
            "gz_args": [
                "-r -v 3 --gui-config ", gui_config_path, " ", world_sdf_path
            ],  # 启动后立即运行仿真
            "on_exit_shutdown": "true",
        }.items(),
    )

    gazebo_launch_debug = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
        ),
        condition=IfCondition(debug),
        launch_arguments={
            "gz_version": "8",  # Gazebo Harmonic (ROS 2 Jazzy)
            "gz_args": [
                "-r -v 4 --gui-config ", gui_config_path, " ", world_sdf_path
            ],  # 设置日志级别为4
            "on_exit_shutdown": "true",
        }.items(),
    )

    # =========== 桥接世界clock话题 ===========
    clock_bridge_launch = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
        ],
        output="screen",
    )

    ld = LaunchDescription()

    ld.add_action(declare_debug_cmd)
    ld.add_action(declare_world_name_cmd)
    ld.add_action(set_resource_path)
    
    ld.add_action(gazebo_launch)
    ld.add_action(gazebo_launch_debug)
    ld.add_action(clock_bridge_launch)
    
    return ld
