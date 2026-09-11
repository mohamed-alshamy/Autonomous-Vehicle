#  Naima 

Welcome to the **Naima Project**!  This is a powerful, modular framework for ROS 2, designed to integrate the ZED 2 stereo camera , UBLOX GPS , and advanced navigation tools . It’s perfect for developers and researchers working on autonomous robotic systems, offering seamless sensor fusion, localization, and navigation with modern ROS 2 tools for high-performance, real-time applications.

---

## 📋 Table of Contents

- [✨ Features](#features)
- [🛠️ Prerequisites](#prerequisites)
- [📦 Installation](#installation)
  - [ZED SDK and CUDA](#zed-sdk-and-cuda)
  - [UBLOX GPS Driver](#ublox-gps-driver)
  - [ZED ROS 2 Wrapper](#zed-ros2-wrapper)
  - [ZED ROS 2 Examples](#zed-ros2-examples)
  - [Cyclone DDS](#cyclone-dds)
  - [Navigation and SLAM Packages](#navigation-and-slam-packages)
- [⚙️ Configuration](#configuration)
  - [GNSS and Camera Fusion](#gnss-and-camera-fusion)
  - [TF Configuration](#tf-configuration)
  - [Cyclone DDS Setup](#cyclone-dds-setup)
- [📍 Localization](#localization)
  - [Dual EKF and NavSat Transform](#dual-ekf-and-navsat-transform)
  - [Local EKF Setup](#local-ekf-setup)
  - [Role of GPS in Localization](#role-of-gps-in-localization)
- [🚀 Usage](#usage)
  - [Launching the System](#launching-the-system)
  - [Launching Individual Components](#launching-individual-components)
  - [Published Topics](#published-topics)
  - [Running Nodes](#running-nodes)
- [🛡️ Troubleshooting](#troubleshooting)
- [🤝 Contributing](#contributing)


---

## ✨ Features

- **📷 ZED 2 Camera Integration**: Stereo vision, depth sensing, and point cloud generation.
- **🛰️ GNSS Fusion**: Combines UBLOX GPS data with ZED camera pose for precise localization.
- **🗺️ ROS 2 Navigation Stack**: Includes Nav2 and SLAM Toolbox for robust mapping and navigation.
- **⚡ Cyclone DDS Support**: Optimized for low-latency, high-performance communication.
- **🚗 Kinematic Bicycle Model**: Ensures precise robot motion control.
- **🧩 Modular Launch Files**: Easily customizable for various camera models and setups.

---

## 🛠️ Prerequisites

- **💻 Operating System**: Ubuntu 22.04 (Jammy) with ROS 2 Humble installed.
- **🖥️ Hardware**:
  - NVIDIA GPU with CUDA support for ZED SDK.
  - ZED 2 or ZED 2i stereo camera.
  - UBLOX GPS module.
- **📥 Software**:
  - [ZED SDK](https://www.stereolabs.com/docs/installation/linux) (v4.0 or later recommended).
  - [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit-archive) (compatible with your GPU).
  - ROS 2 Humble: Follow the [official installation guide](https://docs.ros.org/en/humble/Installation.html).

---

## 📦 Installation

### ZED SDK and CUDA

1. Install the ZED SDK following the [official guide](https://www.stereolabs.com/docs/installation/linux). 📥
2. Ensure CUDA is installed. The ZED SDK installer will automatically download and install CUDA if not detected.
   - Verify CUDA installation:  
     ```bash
     nvcc --version
     ```
3. Restart your system to update paths: 🔄
   ```bash
   sudo reboot
   ```

### UBLOX GPS Driver

1. Create a workspace and clone the UBLOX GPS driver: 
   ```bash
   mkdir -p ~/ublox_ws/src
   cd ~/ublox_ws/src
   git clone https://github.com/men3m-4/naima_ublox_gps.git
   cd ..
   colcon build
   source install/setup.bash
   ```
2. Launch the driver: 🚀
   ```bash
   ros2 launch ublox_gps ublox_gps_node_1-launch.py
   ```

### ZED ROS 2 Wrapper

1. Clone and build the ZED ROS 2 wrapper in your ROS 2 workspace: 
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
   git clone https://github.com/stereolabs/zed-ros2-wrapper.git
   cd ..
   sudo apt update
   rosdep update
   rosdep install --from-paths src --ignore-src -r -y
   colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release --parallel-workers $(nproc)
   echo "source $(pwd)/install/local_setup.bash" >> ~/.bashrc
   source ~/.bashrc
   ```

### ZED ROS 2 Examples

1. Clone and build the ZED ROS 2 examples: 
   ```bash
   cd ~/ros2_ws/src
   git clone https://github.com/stereolabs/zed-ros2-examples.git
   cd ..
   sudo apt update
   rosdep update
   rosdep install --from-paths src --ignore-src -r -y
   colcon build --symlink-install --cmake-args=-CMAKE_BUILD_TYPE=Release
   source ~/.bashrc
   ```

### Cyclone DDS

1. Install Cyclone DDS for optimized communication: ⚡
   ```bash
   sudo apt install ros-humble-rmw-cyclonedds-cpp
   ```
2. Configure Cyclone DDS as the ROS 2 middleware: 🔧
   ```bash
   echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
   source ~/.bashrc
   ```

### Navigation and SLAM Packages

1. Install Nav2 and SLAM Toolbox: 
   ```bash
   sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-slam-toolbox
   ```

---

## ⚙️ Configuration

### GNSS and Camera Fusion

To enable GNSS fusion with the ZED camera: 🛰️📷

1. Edit the `common.yaml` file located at:
   ```
   ~/ros2_ws/src/zed-ros2-wrapper/zed_wrapper/config/common.yaml
   ```
2. Update the GNSS fusion section:
   ```yaml
   gnss_fusion:
     gnss_fusion_enabled: true
     gnss_fix_topic: '/fix'
   ```

### TF Configuration

The Transform (TF) tree defines the spatial relationships between your robot's frames. Follow these steps to configure and verify the TF setup: 🌐

1. **Disable ZED Default TF Publication**:
   - Open the ZED camera launch file:
     ```
     ~/ros2_ws/src/zed-ros2-wrapper/zed_wrapper/launch/zed_camera.launch.py
     ```
   - Locate the `publish_tf` parameter (typically around lines 345–350, depending on the file version).
   - Set `publish_tf` to `false` to disable the ZED node's default TF publication:
     ```python
     'publish_tf': 'false'
     ```
   - Save the file and rebuild the workspace:
     ```bash
     cd ~/ros2_ws
     colcon build
     ```

2. **Static Transform Publisher**:
   - The main launch file includes a static transform publisher to define the transform between `zed2_camera_link` and `zed_camera_link`:
     ```python
     Node(
         package='tf2_ros',
         executable='static_transform_publisher',
         name='base_to_zed_broadcaster',
         arguments=['0', '0', '0', '0', '0', '0', 'zed2_camera_link', 'zed_camera_link'],
         output='screen'
     )
     ```
   - This publishes a static transform with zero offset, aligning the frames as shown in the TF tree.

3. **TF Tree Overview**:
   - The TF hierarchy starts with `map` and `odom` at the top level, with `base_footprint` and `base_link` forming the robot's base structure.
   - The ZED camera frames (`zed2_camera_link`, `zed_camera_link`, `zed_camera_center`, etc.) are attached to `base_link`.
   - Additional sensor frames (e.g., `gps_link`, `imu_link`, `3D_lidar`) and wheel/steering frames (e.g., `front_left_wheel_link`, `steering_link`) are also linked to `base_link`.
   - Use the following command to visualize the TF tree: 
     ```bash
     ros2 run tf2_tools view_frames
     ```
   - This generates a `frames.pdf` file detailing the tree structure, including parent-child relationships, broadcasters, and transform rates.

4. **Key Frames and Relationships**:
   - `map` → `odom` (rate: 30.201 Hz)
   - `odom` → `base_footprint` (rate: 10.204 Hz)
   - `base_footprint` → `base_link` (static)
   - `base_link` → `zed2_camera_link` (static), `3D_lidar`, `gps_link`, `imu_link`, etc.
   - `zed2_camera_link` → `zed_camera_link` → `zed_camera_center` → `zed_left_camera_frame`, `zed_right_camera_frame`, etc.

### Cyclone DDS Setup

Ensure Cyclone DDS is set as the default middleware: ⚡

```bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```

Add this to `~/.bashrc` for persistence:

```bash
echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
source ~/.bashrc
```

---

## 📍 Localization

Localization in this project uses the `robot_localization` package to fuse sensor data and estimate the robot's pose. Two configurations are provided: a dual EKF setup for global and local localization, and a single EKF setup for local-only localization.

### Dual EKF and NavSat Transform

The `dual_ekf_and_navsat.launch.py` file sets up a dual Extended Kalman Filter (EKF) configuration, which is ideal for outdoor navigation requiring both global accuracy and local continuity. 🌍

- **Global EKF (`ekf_filter_node_map`)**:
  - Produces `/odometry/global` in the `map` frame.
  - Fuses data from:
    - Wheel odometry (e.g., `/wheel/odometry`)
    - IMU (`/zed/zed_node/imu/data`)
    - Transformed GPS data (`/odometry/gps` from `navsat_transform`)
  - Publishes the `map` to `odom` transform (rate: ~30 Hz, as per TF tree).

- **NavSat Transform (`navsat_transform`)**:
  - Converts GPS data (`/fix`) into the local frame, producing `/odometry/gps`.
  - Uses IMU data (`/zed/zed_node/imu/data`) for orientation and `/odometry/global` for alignment.
  - Essential for integrating GPS into the global EKF.

- **Local EKF (Optional, Commented Out)**:
  - An `ekf_filter_node_odom` node can be enabled to produce `/odometry/local` in the `odom` frame, focusing on local continuity using odometry and IMU data without GPS.

To launch:

```bash
ros2 launch naima_localization dual_ekf_and_navsat.launch.py
```

### Local EKF Setup

The `local.launch.py` file provides a simpler setup for local localization, focusing on the `odom` to `base_footprint` transform. 📍

- **EKF Node (`ekf_filter_node`)**:
  - Produces a pose estimate in the `odom` frame.
  - Fuses data from local sensors (e.g., wheel odometry, IMU).
  - Does not integrate GPS, making it suitable for indoor or GPS-denied environments.

To launch:

```bash
ros2 launch naima_localization local.launch.py
```

### Role of GPS in Localization

GPS, provided by the UBLOX GPS node (`/fix`), plays a critical role in global localization: 🛰️

- **Global Reference**: Provides absolute position (latitude, longitude, altitude) to correct odometry drift.
- **Integration**:
  - The `navsat_transform_node` converts GPS data into the local frame (`/odometry/gps`).
  - The global EKF fuses this with odometry and IMU data to produce a globally consistent pose (`/odometry/global`).
- **Challenges**:
  - Low update rate (~5 Hz) compared to odometry/IMU (~100 Hz).
  - Susceptible to noise or outages (e.g., in urban canyons); the EKF compensates by relying on other sensors.
- **Verification**:
  - Check GPS data: `ros2 topic echo /fix`
  - Verify transformed GPS: `ros2 topic echo /odometry/gps`

---

## 🚀 Usage

### Launching the System

To launch the entire system, including the ZED camera, UBLOX GPS, localization, and navigation: 🌟

1. **Build the Workspace**:
   ```bash
   colcon build
   ```

2. **Source the Setup File**:
   ```bash
   source install/setup.bash
   ```

3. **Launch the Main System**:
   ```bash
   ros2 launch naima_bringup bringup.launch.py
   ```
   This launch file initializes:
   - 📷 ZED 2 camera with depth and point cloud data.
   - 🛰️ UBLOX GPS for GNSS data.
   - 🤖 Robot State Publisher for URDF.
   - 📍 Localization with dual EKF and NavSat transform.
   - 🌐 Pointcloud to LaserScan conversion.
   - 🚗 Kinematic bicycle model for motion control.

4. **Launch Nav2 Navigation**:
   ```bash
   ros2 launch nav2_bringup navigation_launch.py use_sim_time:=false map:=/home/men3m/Naima/src/naima_mapping/maps/map1/map.yaml autostart:=true
   ```
   > **Note**: Update the `map` path to match your system’s directory structure if needed. This command starts the Nav2 stack with the specified map, enabling autonomous navigation.

### Launching Individual Components

- **UBLOX GPS Driver**: To run the UBLOX GPS driver independently: 🛰️
  ```bash
  ros2 launch ublox_gps ublox_gps_node_1-launch.py
  ```

- **ZED Camera**: To launch the ZED camera and visualize it in RViz2: 📷
  ```bash
  ros2 launch zed_wrapper zed_camera.launch.py camera_model:=zed2
  ros2 launch zed_display_rviz2 display_zed_cam.launch.py camera_model:=zed2
  ```

### Published Topics

The system publishes a wide range of topics, including: 📡

- **Camera Topics**: `/zed/zed_node/rgb/image_rect_color`, `/zed/zed_node/depth/depth_registered`, `/zed/zed_node/point_cloud/cloud_registered`.
- **GNSS Topics**: `/fix`, `/gps/filtered`, `/odometry/gps`.
- **Navigation Topics**: `/cmd_vel`, `/global_costmap/costmap`, `/local_costmap/costmap`, `/plan`.
- **TF Topics**: `/tf`, `/tf_static`.

For a full list, run:

```bash
ros2 topic list
```

### Running Nodes

Key nodes include: 🖥️

- `/zed/zed_node`: ZED camera node.
- `/ublox_gps_node`: GPS driver.
- `/kinematic_bicycle_model`: Motion model.
- `/ekf_filter_node`: Localization filter.

To list all active nodes:

```bash
ros2 node list
```

---

## 🛡️ Troubleshooting

- **📷 ZED Camera Not Detected**: Ensure the ZED SDK is installed and the camera is connected. Run `zed-sdk-test` to verify.
- **🛰️ GPS Data Not Published**: Check the `/fix` topic and ensure the UBLOX GPS driver is running.
- **⚡ High Latency**: Verify Cyclone DDS is set as the middleware (`RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`).
- **🌐 TF Errors**: Confirm `publish_tf` is set to `false` in the ZED launch file and the `base_to_zed_broadcaster` node is publishing to `/tf_static`. Use `view_frames` to debug transform issues.
- **📍 Localization Drift**: Verify GPS data (`/fix`) and IMU (`/zed/zed_node/imu/data`) are being published. Check the `dual_ekf_and_navsat.yaml` configuration for proper sensor fusion settings.
- **⚠️ Build Errors**: Run `rosdep install --from-paths src --ignore-src -r -y` to resolve missing dependencies.

---

## 🤝 Contributing

Contributions are welcome! To contribute: 🌟

1. Fork the repository: [https://github.com/men3m-4/Naima](https://github.com/men3m-4/Naima).
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

---

