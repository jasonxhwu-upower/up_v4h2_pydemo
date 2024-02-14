sudo apt install software-properties-common -y
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt install ros-galactic-ros-base ros-galactic-demo-nodes-py ros-dev-tools ros-galactic-rmw-fastrtps-cpp -y
. /opt/ros/galactic/setup.bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
echo 'export RMW_IMPLEMENTATION=rmw_fastrtps_cpp' >> ~/.bashrc
echo 'source /opt/ros/galactic/setup.bash' >> ~/.bashrc

echo "Barebones ROS2 Galactic installed. Try running the demo listener/talker examples with the following commands:"
echo ""
echo "'ros2 run demo_nodes_py listener'"
echo "'ros2 run demo_nodes_py talker'"
echo "" 
