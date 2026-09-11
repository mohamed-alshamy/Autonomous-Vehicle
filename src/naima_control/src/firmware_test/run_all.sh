#!/bin/bash

# تشغيل سكريبت full_doplex.py
gnome-terminal -- bash -c "cd ~/Naima/src/naima_control/src/firmware_test && ./full_doplex.py; exec bash"

# تشغيل سكريبت model(2).py
gnome-terminal -- bash -c "cd ~/Naima/src/naima/test && ./model\(2\).py; exec bash"

# تشغيل سكريبت cmd_vel_to_serial.py
gnome-terminal -- bash -c "cd ~/Naima/src/naima_control/src/firmware_test && ./cmd_vel_to_serial.py; exec bash"

# تشغيل ROS2 teleop_twist_keyboard
gnome-terminal -- bash -c "source /opt/ros/humble/setup.bash && ros2 run teleop_twist_keyboard teleop_twist_keyboard; exec bash"
