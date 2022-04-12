#!/usr/bin/env python3

from re import M
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Header

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Vector3

from math import pi

# Class for a robot to follow a person
class person_follower(object):
    
    # Initializes variables
        # publisher and subscriber - for setting speeds and getting info about surrounding
        # twist - velocity values to be set
        # min_dist - minimum threshold distance from person, under which robot stops moving
    def __init__(self):
        rospy.init_node("person_follower")
        self.publisher = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.subscriber = rospy.Subscriber("/scan", LaserScan, self.scan)
        
        lin = Vector3()
        ang = Vector3()
        self.twist = Twist(linear=lin,angular=ang)

        self.min_dist = 0.75
    
    # Function called to start the scanning
    def drive(self):
        rospy.spin()
    
    def scan(self, data):

        # Find the minimum distance in data.ranges, ie distance to the person
        min_dist = float("inf")
        for i in data.ranges:
            if i > 0:
                min_dist = min(min_dist,i)

        # If the robot is within the desired threshold distance, stop moving
        if min_dist <= self.min_dist:
            self.twist.linear.x = 0
            self.twist.angular.z = 0
        
        else:
            # Setting a default linear velocity so the robot can drive towards the person
            self.twist.linear.x = 0.2

            # Determines whether or not the robot needs to turn left or right
            # Depends on which side of the robot the person is on
            if data.ranges.index(min_dist) in range(180):
                self.twist.angular.z = 0.3
            else:
                self.twist.angular.z = -0.3

            # If the person is directly behind the robot, don't move forward, just rotate
            if data.ranges.index(min_dist) in range(90,270):
                self.twist.linear.x = 0

        # Sends the data to the robot
        self.publisher.publish(self.twist)


if __name__ == '__main__':
    node = person_follower()
    node.drive()
