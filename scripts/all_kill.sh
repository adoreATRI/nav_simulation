#!/usr/bin/env bash
# Stop all ROS 2 and Gazebo Sim processes started by this user.

set -u

readonly process_patterns=(
  '(^|[[:space:]])ros2([[:space:]]|$)'
  '/opt/ros/[^[:space:]]*/lib/'
  '(^|/)(gzserver|gzclient|gazebo)([[:space:]]|$)'
  '(^|[[:space:]])gz[[:space:]]+sim([[:space:]]|$)'
  '/opt/ros/[^[:space:]]*/opt/gz_'
)

signal_processes() {
  local signal="$1"
  local pattern

  for pattern in "${process_patterns[@]}"; do
    pkill "-${signal}" -f "${pattern}" 2>/dev/null || true
  done
}

echo '正在退出 ROS 2 和 Gazebo 进程...'
signal_processes INT
sleep 1
signal_processes TERM
sleep 1
signal_processes KILL
echo 'done!'
