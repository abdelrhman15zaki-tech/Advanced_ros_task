from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld=LaunchDescription()
    
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim_node'
    )

    
    validation_server_node = Node(
        package='client_pkg',
        executable='validation_server',
        name='validation_server'
    )

    
    navigation_server_node = Node(
        package='client_pkg',
        executable='navigation_server',
        name='action_server'
    )

    #4. The Navigation Client
    #Commented out because you usually want to pass dynamic coordinates via the terminal.
    #If you want it to run automatically with hardcoded coordinates, uncomment this block.
    client_node = Node(
        package='client_pkg',
        executable='navigation_client',
        name='navigation_client',
        arguments=['5.5', '8.0'] # This simulates sys.argv[1] and sys.argv[2]
    )
    
    ld.add_action(turtlesim_node)
    ld.add_action(validation_server_node)
    ld.add_action(navigation_server_node)
    #comment it if u gonna input the parameters urself
    ld.add_action(client_node)
    return ld
   