# gazebo_simulation

基于gazebo的仿真环境

## 目录

- [文件结构](#文件结构)
- [启动参数](#启动参数)
  - [world_bringup.launch.py](#world_bringuplaunchpy)
  - [robot_bringup.launch.py](#robot_bringuplaunchpy)

## 文件结构

```text
gazebo_simulation
├── config                             # 配置文件     
├── launch
│   ├── robot_bringup.launch.py        # 启动机器人模型
│   ├── simulation_bringup.launch.py   # 启动仿真启动入口
│   └── world_bringup.launch.py        # 启动仿真世界
├── meshes                             # 机器人和世界网格文件
├── models                             # 传感器模型文件
├── robots                             # 机器人xacro文件  
├── rviz                               # rviz配置文件   
└── worlds                             # 世界sdf文件
```

## 启动文件说明

`robot_bringup.launch.py`：机器人基本启动文件，负责解析机器人xacro文件，生成URDF，加载到gazebo中，并启动机器人状态发布器，启动gz-ros桥接
`simulation_bringup.launch.py`：基本仿真启动入口，负责加载`robot_bringup.launch.py`和`world_bringup.launch.py`，并传递参数
`world_bringup.launch.py`：世界基本启动文件，负责加载gazebo世界sdf文件，并启动gazebo仿真环境

## 启动参数

### world_bringup.launch.py

| 参数 | 类型 | 默认值 | 说明 |
| ---- | ---- | ------ | ---- |
| `debug` | bool | `false` | 是否显示gazebo完整debug信息 |
| `world_name` | string | `empty` | Gazebo世界名称，使用其加载对应的SDF文件 |

### robot_bringup.launch.py

| 参数 | 类型 | 默认值 | 说明 |
| ---- | ---- | ------ | ---- |
| `robot_name` | string | `` | 机器人名称，使用其加载对应的URDF文件，比如 `sentry2026.urdf.xacro` |

