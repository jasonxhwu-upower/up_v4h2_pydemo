from setuptools import find_packages, setup

package_name = 'mmap_opencv'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lawrencexu',
    maintainer_email='lawrence.xu@upower.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'mmap_opencv_ros2_node = mmap_opencv.mmap_opencv_ros2:main',
        ],
    },
)
