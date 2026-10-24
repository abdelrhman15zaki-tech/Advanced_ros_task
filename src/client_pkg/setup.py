from setuptools import find_packages, setup

package_name = 'client_pkg'

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
    maintainer='abdelrhman',
    maintainer_email='abdelrhman@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'navigation_server = client_pkg.navigation_server:main',
            'validation_server = client_pkg.validation_server:main',
            'navigation_client = client_pkg.navigation_client:main',
        ],
    },
)
