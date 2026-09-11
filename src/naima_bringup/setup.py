from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'naima_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='men3m',
    maintainer_email='mamree6@gmail.com',
    description='Launch files to start Naima robot and ZED camera',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'bringup = naima_bringup.bringup:main',
            'model = naima_bringup.model:main',
        ],
    },
)

