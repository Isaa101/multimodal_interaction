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
    def expressiveness_system(self):
        pass

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
        
    def execute_state(self, screen):
        if self._current_state == 'introduction':
            dialogue_step = self.obtain_dialogue_step('introduction')
            self.expressiveness_system()
            return



