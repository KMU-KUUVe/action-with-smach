#!/usr/bin/env python

import roslib; roslib.load_manifest('smach_ros')
import rospy
import smach
import smach_ros
from keyboard.msg import Key

mission_code = '\0'

class KeyListener():
    def __init__(self):
        self.key_sub = rospy.Subscriber('keyboard/keydown', Key, self.keyboard_cb)

    def keyboard_cb(self, data):
        mission_code = char(data.code)
        print(mission_code)
        return mission_code

#define state Foo
class Foo(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1', 'outcome2'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        rospy.sleep(3)
        if self.counter < 3:
            self.counter += 1
            return 'outcome1'
        else:
            return 'outcome2'

#define state Bar
class Bar(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome2'])

    def execute(self, userdata):
        rospy.loginfo('Executing state BAR')
        rospy.sleep(3)
        return 'outcome2'

#main
def main():
    rospy.init_node('smach_example_state_machine')

    myKey = KeyListener()
    #Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['outcome4', 'outcome5'])

    #Open the container
    with sm:
        smach.StateMachine.add('BAR', smach_ros.MonitorState("/keyboard/keydown", Key, keyboard_cb), transitions={'2':'FOO'})
        smach.StateMachine.add('FOO', smach_ros.MonitorState("/keyboard/keydown", Key, keyboard_cb), transitions={'1':'BAR'})
        #Add states to the container
        #smach.StateMachine.add('FOO', Foo(), transitions={'outcome1':'BAR', 'outcome2':'outcome4'})
        #smach.StateMachine.add('BAR', Bar(), transitions={'outcome2':'FOO'})

    #Execute SMACH plan
    outcome = sm.execute()
    
    rospy.spin()

if __name__ == '__main__':
    main()

