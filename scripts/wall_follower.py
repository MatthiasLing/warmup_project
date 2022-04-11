#!/usr/bin/env python3

from re import M
import rospy
from geometry_msgs.msg import Point, PointStamped, Twist
from std_msgs.msg import Header

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Vector3

from math import pi

rest = 8


#class for the first task - driving in a square based on a timer 
class wall_follower(object):
    
    def __init__(self):
        rospy.init_node("wall_follower")
        self.publisher = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.subscriber = rospy.Subscriber("/scan", LaserScan, self.scan)
        
        lin = Vector3()
        ang = Vector3()
        self.twist = Twist(linear=lin,angular=ang)

        self.min_dist = 1.5
    
    def drive(self):
        rospy.spin()
    
    def scan(self, data):

        min_dist = min(data.ranges)
        linear = self.twist.linear.x
        angular = self.twist.angular.z

        # nothing nearby
        if min_dist == 0:
            print("case 0: moving forward ")
            self.twist.linear.x = 0.1
            self.twist.angular.z = 0
        
        # too far from wall
        elif min_dist > self.min_dist:
            print("case 1: too far from wall, moving forward")
            self.twist.linear.x = 0.1
     

        # too close to wall
        elif min_dist < self.min_dist:
            print("case 2: too close")
            angle = data.ranges.index(min_dist)
            print(angle)
            if angle == 0:
                print("2.0")
                linear = 0
                angular = 0.1
            elif angle > 180:
                print("2.1")
                linear = 0.05
                angular = 0.1
            elif angle < 90:
                print("2.2")
                angular = -0.1
                linear = 0
            else:
                print("2.3")
                angular = 0.1
                linear = 0

        else: #just right distance from wall

            angle = data.ranges.index(min_dist)
            print("case 3: right ")
            if angle == 270:
                print("3.0")
                linear = 0.1
                angular = 0
            elif angle < 270:
                print("3.1")
                self.twist.angular.z = -0.1
                # self.twist.linear.x = 0.05
            else:
                print("3.2")
                self.twist.angular.z = 0.1
                # self.twist.linear.x = 0

        self.twist.linear.x = linear
        self.twist.angular.z = angular
        self.publisher.publish(self.twist)
        
    
    def reset(self):
        m = Twist()


        m.linear.x = 0.0
        m.linear.y = 0.0
        m.linear.z = 0.0
        m.angular.x = 0.0
        m.angular.y = 0.0
        m.angular.z = 0.0
        self.publisher.publish(m)
        # rospy.sleep(2)
        print("speed reset")



if __name__ == '__main__':
    node = wall_follower()
    node.drive()
