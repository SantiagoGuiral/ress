# Ress: Register Chess Movement

Chess register is a program coded in Python using tkinter that allows the user to register and tracks the movements of the chess pieces in a chess game. The program uses image processing techniques as the fundamental tool to know the positioning of the pieces and tracks their movement through mathematical operations.

The program was developed as the final project for the digital image processing course from the university of Antioquia.

Authors:

Santiago Ríos Guiral(@SantiagoGuiral)

Emmanuel Gomez Ospina(@Ego2509)

University of Antioquia.

Electronic and Telecommunications department.

Medellin, Colombia.


## Install Python dependencies

The application requires the following dependencies.

```sh
pip install numpy
pip install matplotlib
pip install opencv-python
pip install Pillow
```

## Exexute Ress

To execute the application use the following command

```sh
python ress.py
```
## Features

- Record a live chess match
- Capture a chess match from a video
- Export a PGN format to analyze the chess match

## Ress usage
The flow of the program is shown below:

1. Establish the video capture method. Choose a video file or a live recording with the help of the IP webcam application. Inside the program, in the ress.py file, copy the video file route in the URL variable or copy the IP address obtained from your phone server. Lastly, save the file changes.

2. Place the camera at a vertical angle from the chessboard.

3. Initiate the program using Python, this will open a Tkinter graphical interface.

4. While the board is empty, capture an image frame from the recording using the 'Recognize Board' button. This action will take a screenshot and check if there is an available chessboard in the recording frame. Also allows to get the dimensions of the board and gets the perspective for checking the pieces' movement. This will show if the board was capture correctly.

5. Place the chess pieces inside the board in their initial positions.

6. After everything is ready to start the chess game, press the 'Start Recording' button to start tracking the pieces.

7. The program uses a motion detection algorithm to detect when a player moves a piece. If there is no motion the program compares two frames and according to their difference establishes the previous and actual position of the piece. These values give us the initial and final position of the piece moves on the board.

8. After finalizing the game press the  'Stop Recording' button to finalize the recording. This action generates a text file with the movement of the pieces.

9. The users can use the text file to study and analyze the chess game to improve their abilities.
