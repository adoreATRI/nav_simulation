cmake_minimum_required(VERSION 3.8)
project(gazebo_simulation)

find_package(ament_cmake REQUIRED)

# Launch files, robot descriptions, configuration, worlds, and meshes must be installed so that
# get_package_share_directory() also works from an installed workspace.
install(DIRECTORY config launch meshes robots rviz worlds
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY models/mid360
  DESTINATION share/${PROJECT_NAME}/models
)

ament_package()
