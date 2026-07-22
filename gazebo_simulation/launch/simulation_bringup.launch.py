import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():
    # ============= 获取包路径 =============
    pkg_gazebo_simulation = get_package_share_directory("gazebo_simulation")

    # =========== 启动参数设置 ===========
    debug = LaunchConfiguration("debug")
    world_name = LaunchConfiguration("world_name")
    robot_name = LaunchConfiguration("robot_name")

    declare_debug_cmd = DeclareLaunchArgument(
        "debug",
        default_value="false",
        description="Whether to launch Gazebo in debug mode",
    )
    declare_world_name_cmd = DeclareLaunchArgument(
        "world_name",
        default_value="rmuc2026",
        description="Name of the Gazebo world to load",
    )
    declare_robot_name_cmd = DeclareLaunchArgument(
        "robot_name",
        default_value="sentry2026",
        description="Name of the robot model to load",
    )

    # =========== 启动gazebo世界 ===========
    world_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_simulation, "launch", "world_bringup.launch.py")
        ),
        launch_arguments={
            "debug": debug,
            "world_name": world_name,
        }.items(),
    )

    # =========== 加载机器人模型 ===========
    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_simulation, "launch", "robot_bringup.launch.py")
        ),
        launch_arguments={
            "robot_name": robot_name
        }.items(),
    )

    ld = LaunchDescription()

    ld.add_action(declare_debug_cmd)
    ld.add_action(declare_world_name_cmd)
    ld.add_action(declare_robot_name_cmd)

    ld.add_action(world_launch)
    ld.add_action(robot_launch)

    return ld
