# ProfessorX
EEG operated raspbery pi (model 4b) vehicle, using the muse headband to detect jaw clenching and head orientation.
## Setup
1. Make sure to use the Mind Monitor app to transfer eeg data to your local computer from your phone, using the OSC protocol.   
2. Ensure the muse headband has connected correctly to your phone via bluetooth.
3. Connect the motor pins accordingly and update the pin number in movement.py.
4. Connect the ultra sonic sensor trig and echo pins to the pi, and update the pin numbers in distance.py.
5. In main.py, ensure local_ip is set to the local_ip of the computer running the main.py scripted along with setting the required port, line 232.
## How to operate
Once the muse headband is transfering eeg data to your local computer, the script will run for 90 seconds once run. 
1. To make the car go forward, tilt head forward and clentch teeth.
2. To make the car go backwards, tilt head backwards and clentch teeth.
3. To make the car turn left or right, blink to toggle between turning left and right, then cletch teeth to make the car turn. 
