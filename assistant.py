import pyttsx3
import speech_recognition as sr
from command_parser import Command_Parser
from decouple import config

VOICE_RECOGNITION_ERROR = "Failed to recognize your voice"

class BRI:
    '''B.R.I stands for Brain/Bernard's Responsive Interface'''

    def __init__(self, ai_name = config("AI_NAME")):
        self._name = ai_name.lower()
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self._parser = Command_Parser()

    def speak(self, response):
        '''A method to let the assistant make a particular statement'''

        self.engine.say(response)
        self.engine.runAndWait()

    def listen(self):
        '''A method to let the assistant listen to a command'''

        r = sr.Recognizer()
        with sr.Microphone() as from_microphone:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(from_microphone)
        try:
            print("Recognizing...")   
            user_command = r.recognize_google(audio, language ='en-in')
        except Exception as e:
            print(e)   
            return VOICE_RECOGNITION_ERROR

        return user_command
    
    def parse_command(self, command):
        '''A method that takes a command from the user and then parses 
        and provides the appropriate response.
        '''
        
        # respond_for_command = self._parser.get_reponse(command.lower()) #uncomment to use default parsing
        respond_for_command = self._parser.get_reponse(command.lower(), purpose='smart_home')
        self.speak(respond_for_command())
             

    def is_wake_up_command(self, command):
        '''Determines whether the AI is active or not to peform a command'''

        wake_up_commands = [f"hey {self._name}", self._name, f"hi {self._name}"]
        if len(command.split()) <= 3 and command.lower() in wake_up_commands:
            return True
        return False



if __name__ == '__main__':
    ai = BRI()
    user_stmt = ai.listen()
    ai.speak(f"You said: {user_stmt}")
    print(f"You said: {user_stmt}")

    # assert ai.is_wake_up_command("hey Bernie") == True
    # assert ai.is_wake_up_command("hi Bernie") == True
    # assert ai.is_wake_up_command("Bernie") == True
    # assert ai.is_wake_up_command("Hello Bernie") == False
    # assert ai.is_wake_up_command("Hey Google") == False
    # assert ai.is_wake_up_command("Hey Siri") == False

    # print("All test passed!")
