# Ambient Intelligence - Intelligent Elevator

## Installation

In the Raspberry Pi 4 execute the following commands:
  ```bash 
  pip install SpeechRecognition
  pip install pyttsx3
  pip install face-recognition
  pip install opencv-python
  pip install pyaudio

  sudo apt-get install libespeak1
  sudo apt-get install libatlas-base-dev
  sudo apt-get install flac
  ```

The above commands install the required libraries and plugins needed to run the project.

## Usage

Connect the 3 Arduinos to a power source, preferably a computer (not charging). The code is already uploaded so you don't need to do anything more.

Connect the Raspberry PI to the main Arduino (the one with all the elevator floor buttons and the LED). To run the code you should be able to connect it to a screen, a camera, a mouse, a keyboard and a speaker (included in the screen or an external one). 

After that please run the following command on the terminal console (at the download location).

```bash 
$ python master.py
```
