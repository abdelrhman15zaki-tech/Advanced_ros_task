#!/usr/bin/env python3
import rclpy
import sys
import time
from rclpy.node import Node
from rclpy.task import Future
from rclpy.action.client import ClientGoalHandle
from rclpy.action import ActionClient
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from custom_interfaces.srv import SetDestination
from custom_interfaces.action import NavigateTo
class Client(Node):
    def __init__(self):
        super().__init__('nod1')
        self.get_logger().info('Hello from nod1!')# this is what prints in the terminal
        self.client=self.create_client(SetDestination,"point_validation")
        self.nav_client = ActionClient(self, NavigateTo, 'navigate_turtle')
        self.target_x=0.0
        self.target_y=0.0
        self.arrived=False

    def send_request(self,target_x:float,target_y:float):
        while not self.client.wait_for_service(timeout_sec=0.5):
            self.get_logger().info("waiting for the sever`s validation")
        self.target_x=target_x
        self.target_y=target_y
        request=SetDestination.Request()
        request.x=target_x
        request.y=target_y
        flag=self.client.call_async(request)
        flag.add_done_callback(self.send_coords)

    def send_coords(self,future:Future):
        response=future.result()
        if response.is_valid:
            self.get_logger().info(f'Valid Destination Point sent to ({self.target_x},{self.target_y})')
            self.nav_client.wait_for_server()
            goal_msg=NavigateTo.Goal()
            goal_msg.x=self.target_x
            goal_msg.y = self.target_y
            
            self.future=self.nav_client.send_goal_async(goal_msg,feedback_callback=self.feedback_callback)

            self.future.add_done_callback(self.goal_response_callback)
        else:
            self.get_logger().error(f'Invalid Destination Point')

    def feedback_callback(self, feedback_msg):
        distance=feedback_msg.feedback.distance_remainig
        self.get_logger().info(f'Distance remaining: {distance}')



    def goal_response_callback(self, future:Future):
        goal_handle:ClientGoalHandle=future.result()
        if not goal_handle.accepted:
            self.get_logger().error("failed")
            return
        self.get_logger().info('the turtle is moving')



        self.future_result:Future=goal_handle.get_result_async()
        self.future_result.add_done_callback(self.get_result_callback)

    def get_result_callback(self,future:Future):
        result:NavigateTo.Result=future.result().result
        did_the_turtle_reach=result.arrived
        if did_the_turtle_reach:
            self.get_logger().info('target reached')
            time.sleep(2.0)
            if not self.arrived:
                self.get_logger().info('return to the origin')
                self.send_request(5.544445,5.544445)
            self.arrived=True
def main(args=None):
    rclpy.init(args=args)
    node = Client()
    x_input=float(sys.argv[1])
    y_input=float(sys.argv[2])
    node.send_request(x_input,y_input)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()