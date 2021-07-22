# virtualboard
 Virtual Board using OpenCv and Numpy
 Virtual Board can be used to draw virtually without a board or any special pointer right on your screen
 This program requires working camera, it uses image masking  to write on the video of the user. 

# Dependencies:
Python 3.7 or above
OpenCv
Numpy

# Installation Guide-

For Windows-
Go to command prompt and paste the following commands one by one
 // To check current version of Python
    python --version

//To install Opencv 
    pip install opencv-contrib-python


For Ubuntu-

// To check current version of Python
    python3 --version

//Installing pip command
    sudo apt install python3-pip

//To install Opencv 
    pip install opencv-contrib-python


# Setting Up
    Clone the file into your system.

    Run the "first_run.py" after installing the dependencies.


    Firstly select the camera input( select once you see yourself .). Select current camera using 's' , change the camera using 'n' and 'p'.

    Secondly, adjust the hue sliders till you only see your pointer and rest every other object disappears. Better the accuracy of this step, sharper will be the stroke rendering on the screen.

    You are ready to draw now, draw whatever you want to using the virtual board and enjoy! 

    After you have selected the pointer, you can reuse that again by running "main.py", in case you want to change camera input or pointer, just run the "first_run.py" again.