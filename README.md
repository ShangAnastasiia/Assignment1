# Here are the assignment 1 of RT course
____
## Assignment 1: Python Robotics Simulation
____
Sensors can detect boxes around all directions (from -180.0 degrees to 180.0 degrees). Write a python script for achieving this robot’s behaviour:

* constrantly drive the robot around the circuit in the counter-clockwise direction
* avoid touching the golden boxes
* when the robot is close to a silver box, it should grab it, and move it behind itself

## The first task is in /assignment_1
____
# Installing and running
The simulator requires a Python 2.7 installation, the pygame library, PyPyBox2D, and PyYAML.

Pygame, unfortunately, can be tricky (though not impossible) to install in virtual environments. If you are using pip, you might try pip install hg+https://bitbucket.org/pygame/pygame, or you could use your operating system's package manager. Windows users could use Portable Python. PyPyBox2D and PyYAML are more forgiving, and should install just fine using pip or easy_install.
____
# Troubleshooting
When running python run.py <file>, you may be presented with an error: ImportError: No module named 'robot'. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
  * Find the location of srtools: pip show sr.tools
  * Get the location. In my case this was /usr/local/lib/python2.7/dist-packages
  * Create symlink: ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/
  ____
  # Open a terminal, git clone the task and run the following commands:

$ python run.py Ex1.py
  ____
  # Solution:
  
