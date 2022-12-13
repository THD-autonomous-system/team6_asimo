#! /usr/bin/env python
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Wall:


    def __init__(self):
        
        self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
        self.velocity = Twist()
        self.RATE = rospy.get_param('/rate', 50)
        
        self.sub = rospy.Subscriber('/scan', LaserScan, self.call_values)
        self.list=[]

       
    def call_values(self, msg):
        self.sub = rospy.Subscriber('/scan', LaserScan, self.call_values)
        # not rospy.is_shutdown():
        while not rospy.is_shutdown():
        
        
            print("CALLING VALUES STARTED")
            #global x
            #self.list= np.array(msg.ranges)
            self.list=msg.ranges
            #print(x)
            #print(n)
            print("End") 
            #print(self.list)
            #self.front= self.list[0:360]
            #print("type")
            #print(type(self.front))
            #print(self.front)
            print(self.list)
        rospy.spin()
        
        
        
           
    def move_forward(self):
        velocity= Twist()
        velocity.linear.x= 0.1
        self.pub.publish(velocity)
        #print("moving forward")
    
    def stop(self):
        velocity= Twist()
        velocity.linear.x= 0.0
        velocity.angular.z= 0.0

        self.pub.publish(velocity)


    def turn_left(self):
        velocity= Twist()
        velocity.linear.x= 0
        velocity.angular.z= -0.3
        self.pub.publish(velocity)

    def turn_right(self):
        velocity= Twist()
        velocity.linear.x= 0
        velocity.angular.z= 0.3
        self.pub.publish(velocity)


    def is_front_clear(self):
        state= True
        for i in range(-20, 20) :
            if self.list[i] < 0.1:
                state= False
            
        return state

    def is_left_clear(self):
        state= True
        for i in range(70 , 90) :
            if self.list[i] < 0.05:
                state= False
            
        return state

    def is_right_clear(self):
        state= True
        for i in range(270, 290) :
            if self.list[i] < 0.05:
                state= False
            
        return state

    def find_wall(self):
        print("FINDING WALL")
        
        Flag= True
        #print(self.front)
        #print(len(self.front))

        while Flag == True:
            
            for i in range (-20, 20):
                #print("checking")
            
                #print(self.front[i])
                if self.list[i] < 1:
                    print("WALL DETETED")
                    Flag= False
                    self.stop()
                
            if Flag == True:
                #print(self.list)
                
                self.move_forward()
                

            else:
                while self.is_front_clear == False:
                    print("TURNING RIGHT")
                    velocity= Twist()
                    velocity.linear.x= 0
                    velocity.angular.z= 0.3
                    self.pub.publish(velocity)
                    
                    Flag= False    
                    return Flag


    def final_control(self):

        
            flag=0
            print("Rospy is running Final Control")
            #print(self.list)
            self.call_values()

        
            level=self.find_wall()
            print (f"The state of wall is {level}")
        
            while flag == 0:


                if self.is_left_clear() == True:
                    self.velocity= self.turn_left()
            
                elif self.is_front_clear() == True:
                    self.velocity= self.move_forward()

                elif self.is_right_clear()== True:
                    self.velocity= self.turn_right()

                else:
                    print("Error")
                    flag=1
                
                self.pub.publish(self.velocity)
            print("LAST")
        
        

            
            


if __name__== '__main__':
    rospy.init_node('scan_values')
    task=Wall()
    task.final_control()

    


                

