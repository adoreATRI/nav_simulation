cmake_minimum_required(VERSION 3.8)
project(gazebo_simulation)

find_package(ament_cmake REQUIRED)

# Launch files, robot descriptions, configuration, worlds, and meshes must be installed so that
# get_package_share_directory() also works from an installed workspace.
install(DIRECTORY config launch meshes robots worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
