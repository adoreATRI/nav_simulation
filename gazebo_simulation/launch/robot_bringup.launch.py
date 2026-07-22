import os

from ament_index_python.packages import get_package_prefix, get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import (
    Command,
    EnvironmentVariable,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
    PythonExpression,
)
from launch_ros.actions import Node


def generate_launch_description(): 
    # =========== 重映射话题 ============
    remappings = [("/tf", "tf"), ("/tf_static", "tf_static")]

    # =========== 获取包路径 ============
    pkg_gazebo_simulation = get_package_share_directory("gazebo_simulation")
    prefix_gazebo_simulation = get_package_prefix("gazebo_simulation")

    # =========== 声明启动参数 ============
    robot_name = LaunchConfiguration("robot_name")    

    declare_robot_name_cmd = DeclareLaunchArgument(
        "robot_name",
        default_value="sentry2026",
        description="Robot name",
    )

    # =========== 参数定义 ============
    robot_xacro_file = PathJoinSubstitution([
        pkg_gazebo_simulation,
        "robots",
        PythonExpression(["'", robot_name, "' + '.urdf.xacro'"]),
    ])
    robot_spawn_params = PathJoinSubstitution([
        pkg_gazebo_simulation, "config", robot_name, "gz_spawn_params.yaml"
    ])
    robot_ros_gz_bridge = PathJoinSubstitution([
        pkg_gazebo_simulation, "config", robot_name, "ros_gz_bridge.yaml"
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

    # =========== 生成机器人描述 ============
    robot_description = Command(
        [
            FindExecutable(name="xacro"),
            " ",   
            robot_xacro_file,
            " use_sim:=true",
        ]
    )

    # =========== 启动机器人状态发布器 ============
    # 给ros2发送机器人tf信息
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{
            "robot_description": robot_description,
            "use_sim_time": True,
        }],
        remappings=remappings,
    )

    # =========== 在gazebo中生成机器人 ============
    spawn_robot_node = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        parameters=[robot_spawn_params],
    )

    # =========== 启动gazebo-ros2 桥接节点 ============
    bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        output="screen",
        remappings=remappings,
        parameters=[{
            "config_file": robot_ros_gz_bridge,
            "use_sim_time": True,
        }],
    )

    ld = LaunchDescription()

    ld.add_action(declare_robot_name_cmd)
    ld.add_action(set_resource_path)

    ld.add_action(spawn_robot_node)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(bridge_node)

    return ld
