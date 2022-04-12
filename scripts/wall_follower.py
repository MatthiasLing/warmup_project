#!/usr/bin/env python3

from re import M
from sys import is_finalizing
import rospy
from geometry_msgs.msg import Point, PointStamped, Twist
from std_msgs.msg import Header

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Vector3

from math import pi

# x and z are linear and rotational velocity values
# it makes it faster to type
x = 0.2
z = 0.2
# A constant value for calculating what to modify velocity to 
const = 0.1

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

        self.min_dist = 0.5
    
    # The infinite function that is called
    def drive(self):
        rospy.spin()
    
    def scan(self, data):

        # md is the measured distance to the nearest wall
        # angle is the robot's angle to that nearest wall
        md = min(data.ranges)
        angle = data.ranges.index(md)
        
        # linear and angular are the speed components that I'll modify
        linear = self.twist.linear.x
        angular = self.twist.angular.z

        # If the robot is too far for detection, just move forward
        if md == float("inf"):
            linear = x

        # If the robot is too close to the wall or at the threshold, move conditionally away from it 
        if md <= self.min_dist:
            if angle in range(270, 360):
                angular = z
                linear = const * x * (360 - angle)/360

            if angle in range(180,270):
                linear = x
                angular = -z

            if angle in range(90,180):
                linear = 0
                angular = -z
            if angle in range(0,90):
                linear = 0
                angular = z

        # If the robot is too far from the wall, move conditionally towards it 
        if md > self.min_dist:
            if angle in range(0,90):
                linear = x
                angular = z
            if angle in range(90,180):
                linear = const * x *(180-angle)/180
                angular = z
            if angle in range(180,270):
                angular = -z
                linear = const * x * (angle-180)/180
            if angle in range(270,360):
                linear = x
                angular = z
        self.twist.linear.x = linear
        self.twist.angular.z = angular
        self.publisher.publish(self.twist)



if __name__ == '__main__':
    node = wall_follower()
    node.drive()
