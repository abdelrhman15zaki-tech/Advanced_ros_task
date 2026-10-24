#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from custom_interfaces.srv import SetDestination
class Server(Node):
    def __init__(self):
        super().__init__('nod2')
        self.get_logger().info('Hello from nod2')# this is what prints in the terminal
        self.server=self.create_service(SetDestination,"point_validation",self.validate)

    def validate(self,request:SetDestination.Request,response:SetDestination.Response)->SetDestination.Response:
        target_x=request.x
        target_y=request.y
        if 0<=target_x<11 and 0<=target_y<11:
            response.is_valid=True
            self.get_logger().info('Valid Point')
        else:
            response.is_valid=False
            self.get_logger().info('Invalid Point')

        return response
def main(args=None):
    rclpy.init(args=args)
    node = Server()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()