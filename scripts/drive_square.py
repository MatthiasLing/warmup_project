#!/usr/bin/env python3

from re import M
import rospy
from geometry_msgs.msg import Point, PointStamped, Twist
from std_msgs.msg import Header

from math import pi

rest = 8


#class for the first task - driving in a square based on a timer 
class drive_square(object):
    
    def __init__(self):
        rospy.init_node("drive_square")
        self.publisher = rospy.Publisher("cmd_vel", Twist, queue_size=1)
        self.time = None
        self.time = rospy.Time.now()
        self.angle = 0
     
    def drive(self):
        
        node.reset()
        for i in range(4):
            node.run()
            node.reset()
            node.rotate()
            node.reset()
        node.run()
        node.reset()
 
    def run(self):
        
        self.time = rospy.Time.now()

        msg = Twist()
        
        msg.linear.x = 0.3
        msg.linear.z = 0
        msg.angular.x = 0
        msg.angular.y = 0
        msg.angular.z = 0
        
        self.publisher.publish(msg)
        rospy.sleep(rest/2)

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


    def rotate(self):
        print("rotating")
        move = Twist()

        move.linear.x = 0.0
        move.linear.y = 0.0
        move.angular.z = (pi/2)/rest

        self.publisher.publish(move)
        rospy.sleep(rest)

        move.angular.z = 0
        self.publisher.publish(move)

if __name__ == '__main__':
    node = drive_square()
    node.drive()
