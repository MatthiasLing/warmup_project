#!/usr/bin/env python3

from re import M
import rospy
from geometry_msgs.msg import Point, PointStamped, Twist
from std_msgs.msg import Header

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Vector3

from math import pi


#class for the first task - driving in a square based on a timer 
class person_follower(object):
    
    def __init__(self):
        rospy.init_node("person_follower")
        self.publisher = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.subscriber = rospy.Subscriber("/scan", LaserScan, self.scan)
        
        lin = Vector3()
        ang = Vector3()
        self.twist = Twist(linear=lin,angular=ang)

        self.min_dist = 1
    
    def scan(self, data):

        min_dist = min(data.ranges)
        if min_dist <= self.min_dist:
            self.twist.linear.x = 0
            self.twist.angular.z = 0
        else:
            self.twist.linear.x = 0.1

            if min_dist == data.ranges[0]:
                self.twist.angular.z = 0

            elif data.ranges.index(min_dist) in range(180):
                self.twist.angular.z = 0.3
            else:
                self.twist.angular.z = -0.3

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

    def drive(self):
        rospy.spin()

if __name__ == '__main__':
    node = person_follower()
    node.drive()
