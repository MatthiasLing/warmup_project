#!/usr/bin/env python3

from re import M
import rospy
from geometry_msgs.msg import Point, PointStamped, Twist
from std_msgs.msg import Header
from geometry_msgs.msg import Vector3

from math import pi

# number of seconds that the robot spins for
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

    def drive(self):
        
        node.reset()
        for i in range(4):
            rospy.sleep(1)
            node.run()
            node.rotate()
 
    def run(self):
 
        self.msg.linear.x = 0.3
        self.msg.linear.z = 0
        self.msg.angular.x = 0
        self.msg.angular.y = 0
        self.msg.angular.z = 0
        
        self.publisher.publish(self.msg)
        rospy.sleep(rest)

    def reset(self):

        self.msg.linear.x = 0.0
        self.msg.linear.y = 0.0
        self.msg.linear.z = 0.0
        self.msg.angular.x = 0.0
        self.msg.angular.y = 0.0
        self.msg.angular.z = 0.0
        self.publisher.publish(self.msg)


    def rotate(self):

        self.msg.linear.x = 0.0
        self.msg.angular.z = (pi/2)/rest

        self.publisher.publish(self.msg)
        rospy.sleep(rest)

if __name__ == '__main__':
    node = drive_square()
    node.drive()
