#!/usr/bin/env python3

from re import M
import rospy
from geometry_msgs.msg import Point, PointStamped, Twist
from std_msgs.msg import Header
from geometry_msgs.msg import Vector3

from math import pi

# rest seconds - arbitrary value
rest = 5


#class for the first task - driving in a square based on a timer 
class drive_square(object):
    
    # initializes the publisher, sets
    def __init__(self):
        rospy.init_node("drive_square")
        self.publisher = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        
        lin = Vector3()
        ang = Vector3()
        self.msg = Twist(linear=lin,angular=ang)

    # Function that is called to initiate movement
    def drive(self):
        
        node.reset()
        for i in range(4):
            rospy.sleep(1)
            node.run()
            node.rotate()
        node.reset()
 
    # Causes robot to move in a straight line for rest/1.5 seconds
    def run(self):
 
        self.msg.linear.x = 0.3
        self.msg.linear.z = 0
        self.msg.angular.x = 0
        self.msg.angular.y = 0
        self.msg.angular.z = 0
        
        self.publisher.publish(self.msg)
        rospy.sleep(rest/1.5)

    # Stops all movement
    def reset(self):

        self.msg.linear.x = 0.0
        self.msg.linear.y = 0.0
        self.msg.linear.z = 0.0
        self.msg.angular.x = 0.0
        self.msg.angular.y = 0.0
        self.msg.angular.z = 0.0
        self.publisher.publish(self.msg)

    # Function for the 90 degree turns
    def rotate(self):

        # Stops linear motion, sets angular velocity
        self.msg.linear.x = 0.0
        self.msg.angular.z = (pi/2)/rest

        self.publisher.publish(self.msg)

        # Subtract a little from the rest to prevent over-turning 
        rospy.sleep(rest-0.5)

if __name__ == '__main__':
    node = drive_square()
    node.drive()
