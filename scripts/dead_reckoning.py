#! /usr/bin/env python3

"""
A quick script to implement dead reckoning
"""

import rospy
from geometry_msgs.msg import Point, Pose, Vector3
from sensor_msgs.msg import Imu


initial_pos = Point(0, 0, 0)
initial_vel = Vector3(0, 0, 0)
initial_acc = Vector3(0, 0, 0)

old_pos = new_pos = initial_pos
old_vel = new_vel = initial_vel
old_acc = new_acc = initial_acc

def imu_callback(new_msg):
    """
    Gets Imu data
    """

    global old_pos
    global new_pos
    global old_vel
    global new_vel
    global old_acc
    global new_acc

    try:

        orienta = new_msg.orientation
        new_acc = new_msg.linear_acceleration

        new_vel.x = old_vel.x + ((new_acc.x) / 10)
        new_vel.y = old_vel.y + ((new_acc.y) / 10)
        new_vel.z = old_vel.z + ((new_acc.z) / 10)

        new_pos.x = old_pos.x + new_vel.x / 10 + new_acc.x / (2 * (10 * 10))
        new_pos.y = old_pos.y + new_vel.y / 10 + new_acc.y / (2 * (10 * 10))
        new_pos.z = old_pos.z + new_vel.z / 10 + new_acc.z / (2 * (10 * 10))

        old_pos = new_pos
        old_vel = new_vel
        old_acc = new_acc

        print(new_pos)

        #  p = Pose(new_pos, orienta)
        #  pub.publish(p)


    except:
        print("imu callback error, resetting to initial state")
        old_pos = initial_pos


def initialize_node():
    """
    Initialize node
    """
    pub = rospy.Publisher('dead', Pose, queue_size=10)
    rospy.Subscriber('imu', Imu, imu_callback)
    rospy.init_node('dead_node')
    rate = rospy.Rate(10)

    print("node Initialized")

    return pub, rate



if __name__ == "__main__":
    
    pub, rate = initialize_node()

    while not rospy.is_shutdown():
        pass
