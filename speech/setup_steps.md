# Setup Steps

////you need to install this to do remote desk
sudo apt-get install xrdp


////The following you need for setting up the Text To Speech (speech.py and speech2.py)
pip install pyttsx3
sudo apt-get update && sudo apt-get install espeak
sudo apt-get install python3-espeak



//// The rest of these steps are to get speech recognition working

pip install SpeechRecognition
sudo apt-get install flac
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install portaudio19-dev
sudo pip install pyaudio
