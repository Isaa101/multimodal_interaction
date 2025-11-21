#! /usr/env/python3

import os
import sys
import yaml
import time
import pygame

#pygame.mixer.Sound('file.mp3')
"""
sentence_id: "introduction"
text: 
    -Hello! Welcome to the multimodal interaction lab.
audio:
    -congratulate
screen:
    -image;green.png&text;congratulations*center
animation:
    -happy
"""
#type;content&type;content*position


questions = [
    {
        'question': 'What is 2 + 2?',
        'A': '4',
        'B': '22',
        'C': '5',
        'D': '3',
        'correct_answer': 'A'},
    {
        'question': 'What is the capital of France?',
        'A': 'Berlin',
        'B': 'Madrid',
        'C': 'Paris',
        'D': 'Rome',
        'correct_answer': 'C'},
    {
        'question': 'What is the largest planet in our solar system?',
        'A': 'Earth',
        'B': 'Jupiter',
        'C': 'Mars',
        'D': 'Saturn',
        'correct_answer': 'B'},
    {
        'question': 'Who wrote "Romeo and Juliet"?',
        'A': 'Charles Dickens',
        'B': 'Mark Twain',
        'C': 'William Shakespeare',
        'D': 'Jane Austen',
        'correct_answer': 'C'},
    {
        'question': 'What is the chemical symbol for water?',
        'A': 'O2',
        'B': 'H2O',
        'C': 'CO2',
        'D': 'NaCl',
        'correct_answer': 'B'}
]

class FSMDialogueSystem:
    def __init__(self):
        self._robot_script = None
        self._questions = []
        self._screen_coord = (0, 728)
        self.load_robot_script()

##################### METHODS FOR MANAGING THE APPLICATION'S SCRIPT #####################
# These methods load the script.yaml file in the script folder (the os.getcwd() gets the current directory where the script is running)

    def load_robot_script(self):
        path = os.getcwd() + '/script'
        if os.path.isdir(path):
            self._robot_script = yaml.safe_load(open(path + '/script.yaml'))
            for item in self._robot_script:
                if item['sentence_id'] == 'question':
                    self._questions.append(item)

    def obtain_dialogue_step(self, sentence_id):
        for item in self._robot_script:
            if item['sentence_id'] == sentence_id:
                return item

##################### METHODS FOR MANAGING THE ROBOT'S EXPRESSIVENESS #####################
    # Method for controling the agents expressiveness. It should receive the parameters required for executing the different actions
    # and decide when to call each method
    def expressiveness_system(self, screen, speech=None, screen_content=None, animation=None):
        """ BORRAR QUIZAS LUEGO
        Coordinates and synchronizes all expressive channels of the robot.
        
        Args:
            screen: The pygame screen object to draw on
            speech: Audio file name to play (without .wav extension)
            screen_content: String containing screen instructions in format "type;content&type;content*position"
            animation: Animation folder name to play
        """
        
        # Lists to track running processes
        running_processes = []
        
        # 1. PLAY ANIMATION (if provided)
        if animation:
            # We'll run animation in a separate thread so it doesn't block speech
            import threading
            anim_thread = threading.Thread(target=self.play_animation, args=(screen, animation))
            anim_thread.daemon = True
            anim_thread.start()
            running_processes.append(('animation', anim_thread))
    
        # 2. DISPLAY SCREEN CONTENT (if provided)
        if screen_content:
            self.display_multimedia_content(screen, screen_content)
        
        # 3. PLAY SPEECH and WAIT for it to finish (this is our main blocking call)
        if speech:
            self.robot_speech(speech)
            # robot_speech should block until audio finishes playing
        
        # 4. If no speech but animation is running, wait for animation to complete
        if not speech and animation:
            anim_thread.join()

    # Method for playing the robot's voice
    def robot_speech(self):
        pass

    # Method for displaying multimedia content on the robot's "screen"
    def display_multimedia_content(self):
        pass

    # Method for playing an animation
    def play_animation(self, screen, animation):
        pass

##################### METHODS FOR MANAGING THE ROBOT'S PERCEPTION #####################
    # Method for capturing user inputs. It should receive the type of input expected, and act accordingly
    def obtain_user_answer(self):
        pass

##################### METHODS FOR CONTROLLING THE INTERACTION FLOW #####################

    def update_state(self):
        if self._current_state == 'introduction':
            self._current_state = 'explanation_needed'
        elif self._current_state == 'explanation_needed':
            user_answer = self.obtain_user_answer()
            if user_answer == 'yes':
                self._current_state = 'explanation'
            else:
                self._current_state = 'start_questions'
        elif self._current_state == 'explanation':
            self._current_state = 'start_questions'
        elif self._current_state == 'start_questions':
            self._current_state = 'ask_question'
            self._questions_asked = 1
        elif self._current_state == 'ask_question':
            user_answer = self.obtain_user_answer()
            # Logic to check if the answer is correct can be added here
            if user_answer == questions[self._questions_asked - 1]['correct_answer']:
                self._current_state = 'congratulate'
            else:
                self._current_state = 'wrong'
        elif self._current_state == 'congratulate':
            if self._questions_asked < len(self._questions):
                self._current_state = 'next_question'
                self._questions_asked += 1
            else:
                self._current_state = 'score'
        elif self._current_state == 'wrong':
            self._current_state = 'score'
        elif self._current_state == 'next_question':
            self._current_state = 'ask_question'
        elif self._current_state == 'score':
            self._current_state = 'good_bye'
        elif self._current_state == 'good_bye':
            return
        
    def execute_state(self, screen):
        if self._current_state == 'introduction':
            dialogue_step = self.obtain_dialogue_step('introduction')
            self.expressiveness_system()
            return



