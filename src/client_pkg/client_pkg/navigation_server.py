#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
from custom_interfaces.action import NavigateTo
from rclpy.task import Future
from rclpy.action.server import ServerGoalHandle
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from rclpy.action import ActionServer
class action_server(Node):
    def __init__(self):
        super().__init__('nod2')
        self.get_logger().info('Hello from nod2')# this is what prints in the terminal
        self.action_server=ActionServer(self,NavigateTo,"navigate_turtle",self.execute_callback)
        self.publisher=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.subscriber=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)



        self.current_pose:Pose=Pose() #? stores the latest location from the turtle
        self.mission_future:Future=Future()
        self.active_goal_handle:ServerGoalHandle|None=None
        self.target_x:float=0.0
        self.target_y:float=0.0


    async def execute_callback(self,goal_handle:ServerGoalHandle):
        
        self.get_logger().info("executing navigation action")
        
        self.active_goal_handle=goal_handle #! We have to update the goal handle or else the pose_callback() function wont continue
        self.target_x=goal_handle.request.x
        self.target_y=goal_handle.request.y

        self.mission_future=Future()

        result:NavigateTo.Result=await self.mission_future
        return result
    def pose_callback(self,msg:Pose):
        self.current_pose=msg
        if self.active_goal_handle is None:
            return
        dx=self.target_x-self.current_pose.x
        dy=self.target_y-self.current_pose.y
        distance=math.sqrt(dx**2+dy**2)
        if distance>0.1:
            target_angle=math.atan2(dy,dx)
            turtle_angle=self.current_pose.theta

            angle_error=target_angle-turtle_angle
            #? this is to achieve minimum rotaion possible
            while angle_error>math.pi:
                angle_error-=2*math.pi
            while angle_error<-1*math.pi:
                angle_error+=2*math.pi
            #* now angle_error contains the minimum rotatoin the turtle have to do
            #! creating cmd so we can publish it to turulesim
            cmd=Twist()
            cmd.linear.x=1.0*distance
            cmd.angular.z=4.0*angle_error
            self.publisher.publish(cmd)

            feedback_msg=NavigateTo.Feedback()
            feedback_msg.distance_remainig=distance
            self.active_goal_handle.publish_feedback(feedback_msg)

        else:
            stop_msg=Twist()
            self.publisher.publish(stop_msg)
            self.active_goal_handle.succeed()
            result=NavigateTo.Result()
            result.arrived=True
            self.mission_future.set_result(result)
            self.active_goal_handle=None

def main(args=None):
    rclpy.init(args=args)
    node = action_server()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()