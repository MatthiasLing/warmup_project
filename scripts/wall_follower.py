#!/usr/bin/env python3

from re import M
from sys import is_finalizing
import rospy
from geometry_msgs.msg import Point, PointStamped, Twist
from std_msgs.msg import Header

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Vector3

import math
'''
error = where we want - where we are
kp = 0.1

z = kp * error

'''


# x and z are linear and rotational velocity values
# it makes it faster to type
x = 0.1
z = 0.2
# A constant value for calculating what to modify velocity to 
kp = 0.05

# normalizes an angle around 270 - 270->90 becomes 0->180
# 270->90 becomes 0->-180
def normalize_270(angle):
    if angle in range(90,270): 
        angle = angle - 270
    elif angle in range(270,360):
        angle = angle - 270
    else:
        angle = angle + 90
    return angle

#class for the first task - driving in a square based on a timer 
class wall_follower(object):
    # initializes values for following the wall:
        # publisher and subscriber
        # a standard twist value to be modified
        # a minimum distance from the wall that the robot needs to be 
    def __init__(self):
        rospy.init_node("wall_follower")
        self.publisher = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.subscriber = rospy.Subscriber("/scan", LaserScan, self.scan)
        
        lin = Vector3()
        ang = Vector3()
        self.twist = Twist(linear=lin,angular=ang)

        self.min_dist = 0.75
        # self.at_corner = False

    # The infinite function that is called
    def drive(self):
        rospy.spin()
    
    def scan(self, data):

        # md is the measured distance to the nearest wall
        # angle is the robot's angle to that nearest wall
        md = float("inf")

        for i in data.ranges:
            if i > 0:
                md = min(md,i)

        angle = data.ranges.index(md)
        
        # linear and angular are the speed components that I'll modify
        linear = self.twist.linear.x
        angular = self.twist.angular.z

        # If the robot is too close to the wall or at the threshold, move conditionally away from it 
        if md <= self.min_dist:
            linear = x
            angular = 0

            norm = normalize_270(angle)
           
            angular = kp*(norm)/2.5

        # If the robot is too far from the wall, move conditionally towards it 
        else:        
            
            #normalize around 0 -> turns angles to the left of the origin to negative values.
            if angle > 180: 
                angle -= 360
            # if the robot doesn't have its back to the person, move forward.
            if angle in range(-90,90):
                linear = x

            angular = kp*(angle)/2.5
            
        self.twist.linear.x = linear
        self.twist.angular.z = angular
        self.publisher.publish(self.twist)



if __name__ == '__main__':
    node = wall_follower()
    node.drive()
