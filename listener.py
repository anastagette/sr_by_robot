#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter", String, callback)
    rospy.spin()

def callback(command_msg):
    rospy.loginfo(command_msg.data)
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    
    vel_msg = Twist()
    speed = 3
    distance = 1
    angle = 90
    PI = 3.1415926535897
    angular_speed = speed*2*PI/360
    relative_angle = angle*2*PI/360

    if command_msg.data.find("forward") > -1 or command_msg.data.find("go") > -1:
        vel_msg.linear.x = abs(speed)
    elif command_msg.data.find("backwards") > -1:
        vel_msg.linear.x = -abs(speed)
    elif command_msg.data.find("right") > -1:
        vel_msg.angular.z = -abs(angular_speed)
        distance = relative_angle
        speed = angular_speed
    elif command_msg.data.find("left") > -1:
        vel_msg.angular.z = abs(angular_speed)
        distance = relative_angle
        speed = angular_speed
    elif command_msg.data.find("turn around") > -1:
        vel_msg.angular.z = abs(angular_speed)
        distance = relative_angle*2
        speed = angular_speed
    elif command_msg.data.find("stop") > -1:          
        vel_msg = Twist()
        
    t0 = rospy.Time.now().to_sec()
    current_distance = 0
        
    while(current_distance < distance):
        velocity_publisher.publish(vel_msg)
        t1=rospy.Time.now().to_sec()
        current_distance = speed*(t1-t0)

    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    
if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
