
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

        self.min_distance = 0.5
    
    def scan(self, data):

        min_dist = min(data.ranges)

        # nothing nearby
        if min_dist == 0:
            self.twist.linear.x = 0.1
            self.twist.angular.z = 0
        
        # too far from wall
        elif min_dist > self.min_dist:
            
            # if right in front, move towards it 
            if min_dist == data.ranges[0]:
                self.twist.linear.x = 0.1
                self.twist.angular.z = 0
                self.publisher.publish(self.twist)
                # rospy.sleep((min_dist - self.min_dist)/0.1)
            # turn towards it 
            else:
                angle = data.ranges.index(min_dist)
                self.twist.linear.x = 0

                if angle > 180:
                    self.twist.angular.z = -0.1
                else:
                    self.twist.angular.z = 0.1

                self.publisher.publish(self.twist)
                # rospy.sleep((min_dist - self.min_dist)/0.1)

        # too close to wall
        elif min_dist < self.min_dist:
            angle = data.ranges.index(min_dist)

            if angle >= 270:
                self.twist.angular.z = 0.1
            else:
                self.twist.linear.x = 0.1
                

        else: #just right distance from wall
            self.twist.angular.z = 0
            self.twist.linear.x = 0.1
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
    node = wall_follower()
    node.drive()
