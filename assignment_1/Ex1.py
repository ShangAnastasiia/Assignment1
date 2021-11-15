from __future__ import print_function

import time
from sr.robot import *

a_th = 1.5
""" float: Threshold for the control of the linear distance"""
d_th = 0.4
""" float: Threshold for the control of the orientation"""

w=0
e=0
R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_token(): 
    """
    Function to find the closest silver token
    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected at a distance more than 3) 
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected at a distance more than 3)
    """
    dist=10
    for token in R.see():
    
        if token.dist < dist and token.rot_y>-20 and token.rot_y< 20 and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist=token.dist
	    rot_y=token.rot_y

    if dist>3:
	return -1, -1
    else:
   	return dist, rot_y   
    

def find_golden_token():
    """     
    Orientation function by side golden token
    Returns:
       Gdist(float): distance to the side nearest gold token (-1 if the gold token is found in the range 89<Grot_y<91 or -89>Grot_y>-91
       Grot_y (float): the angle between the robot and the gold token (-1 if the gold token is detected in the range 89<Grot_y<91 or -89>Grot_y>-91)
    """
    Gdist=1.5
    for token in R.see():
    
	if token.dist < Gdist and  token.rot_y<135 and token.rot_y>45 and token.info.marker_type is MARKER_TOKEN_GOLD:
            Gdist=token.dist
	    Grot_y=token.rot_y

	if token.dist < Gdist and token.rot_y>-135 and token.rot_y<-45 and token.info.marker_type is MARKER_TOKEN_GOLD:
            Gdist=token.dist
	    Grot_y=token.rot_y

    if Grot_y>89 and Grot_y<91 or Grot_y<-89 and Grot_y>-91:
	return -1, -1
    else:
   	return Gdist, Grot_y

	    
def forward_token():
    """
       Function to find the nearest front gold token
    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected at a distance more than 3)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected at a distance more than 3)
    """  

    forward=8
    for token in R.see():
        if token.dist < forward and token.rot_y>-5 and token.rot_y<5 and token.info.marker_type is MARKER_TOKEN_GOLD:
            forward=token.dist
	    rot=token.rot_y
	    
    if forward<3:
	return forward, rot
    else:
   	return -1, -1
   	
#-----------------------------------------------------------------------------  
 
while 1:
   
   Gdist, Grot_y = find_golden_token()
   dist, rot_y = find_token()
   
   t=0.3
   """ 
    Access to the first token at the beginning
   """   
   if w==0:
       drive(700, 6)
       w=1

   """ 
    Movement until the silver token is visible
   """   
   if dist==-1:

       Gdist, Grot_y = find_golden_token()
       dist, rot_y = find_token()
       
       """  Alignment for moving straight """
       
       while Grot_y!=-1 and  dist==-1:
           Gdist, Grot_y = find_golden_token()
	   dist, rot_y = find_token()
	   print("  @@ Grot_y=", Grot_y )
	   
	   if Grot_y < -45 and Grot_y > -90:    
               turn(3, t)
               e=-1
               
	   elif Grot_y > 45 and Grot_y < 90 :
               turn(-3, t)
               e=1
               
           elif Grot_y > -135 and Grot_y < -90:    
               turn(-3, t)
               e=-2
               
	   elif Grot_y > 90 and Grot_y < 135 :
               turn(3, t)
               e=2               
       
       """ Front Wall Detection """
       if Grot_y==-1 and  dist==-1:        
           forward, rot = forward_token()
           dist, rot_y = find_token()
           
           """ Moving backwards when approaching the wall """
           if forward<0.5 and forward>0:
               print("           STOP        ")
               drive(-15, 1)
               forward, rot = forward_token()
               print( "      forward =   ", forward )
                       
           if forward<0.75 and forward>0.5:
               print("            BACK ")
               drive(-5, 1)
               forward, rot = forward_token()
               print( "      forward =   ", forward )
           
           
           """ Mid-distance turn """
           if forward>0.75 and forward<1.25:
               print("      !! E",e, " find_token ")
               dist, rot_y = find_token()
               
               if e == 1:  
                   turn(-30,1)
               if e == 2:  
                   turn(-30,1) 
               if e == -1:  
                   turn(30,1)
               if e == -2:  
                   turn(30,1)
               
               drive(60, 1)
               Gdist, Grot_y = find_golden_token()
               dist, rot_y = find_token()
               forward, rot = forward_token()
               print("  f = ", forward, " dist=", dist," Grot_y=", Grot_y )              
           
           """ Moving forward a long distance to the wall """
           if forward<2 and forward>1.25:
               print("            FORWARD       ")
               drive(5, 1)
               forward, rot = forward_token()
               dist, rot_y = find_token()
               print( "      forward =   ", forward,  )

           if  forward>2 :
               drive(10, 1)
               forward, rot = forward_token()
               Gdist, Grot_y = find_golden_token()
               dist, rot_y = find_token()       
               print("      Go to wall!", forward )
           
           elif forward==-1:
               drive(150, 0.2)
               forward, rot = forward_token()
               Gdist, Grot_y = find_golden_token()  
               print("      Go to wall!", forward  )

#-----------------------------------------------------------------------------    

   elif dist <d_th:  # if we are close to the token, we try grab it.
        print("            Found it!")
        if R.grab(): # if we grab the token, we move the robot on the right, we release the token, and we move the robot back and on the left
            print("            Gotcha!")
	    turn(35, 2)
	    R.release()
	    drive(-15,2)
	    turn(-35,2)
	else:
            print("  Aww, I'm not close enough.")
   elif -a_th<= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
	print("Ah, that'll do.")
        drive(10, 0.5)
   elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        forward, rot = forward_token()
        print(" dist=", dist )
        print("Left a bit...")
        turn(-2, 0.5)
   elif rot_y > a_th:
        forward, rot = forward_token()
        print("  dist=", dist )
        print("Right a bit...")
        turn(+2, 0.5)

