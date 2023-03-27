# Ambient Intelligence - Intelligent Elevator

Implementation of an intelligent elevator to install in our homes. 

Makes life easier and accessible to everyone! 

## Installation

In the Raspeberry Pi, use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages:
 * SpeechRecognition
 * pyttsx3
 * face-recognition
 * opencv-python
 * pyaudio

and the using the 'apt-get' also install the following packages: 
 * libespeak1
 * libatlas-base-dev
 * flac

 So you should be executing the following commands:
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

## Usage

Steps:
For the 3 arduinos, only power is needed. The code has already been uploaded

For the Rapberry Pi, turn it on, and on the terminal console, after installing everything(see Installation), go to the download location, open it, run the 'master.py' as follows 
    
```bash 
python master.py
```


## License

@Tecnico

- Bernardo Santos - ist1105709
- João Travassos - ist1105710
- Olga Silva - ist1105714