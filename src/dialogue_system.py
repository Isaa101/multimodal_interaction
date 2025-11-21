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
        self._questions = [
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
        self._screen_coord = (0, 728)
        self.load_robot_script()
        self._current_state = 'introduction'
        self._questions_asked = 0

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
    def robot_speech(self, speech):
        '''For reproducing sounds, we can use the pygame.mixer.Sound(path_to_the
            file) method to create a Sound object and use the play() method that Sound objects
            have for playing the audio cue. Calling the play() method returns a channel object
            representing the audio channel through which the audio is being played. We chan
            check if audio is being played by calling the channel.get_busy() method (it will
            return False if the sound is not being played, True if it is). We can use this to block
            the execution of our program until the entire audio clip has been played.'''
        pygame.mixer.init()
        sound = pygame.mixer.Sound('audio/' + speech + '.mp3')
        channel = sound.play()
        while channel.get_busy():
            time.sleep(0.1)


    # Method for displaying multimedia content on the robot's "screen"
    def display_multimedia_content(self, screen, screen_content,):
        '''We have a 1000x272 area at the bottom of the screen to display
        multimedia content and menus. In the gui.py file, you can see how to display a
        static image in pygame. You will use the pygame.image.load method to load the
        image to display, use the blit(image, position) method to place it on the screen, and
        the pygame.display.flip() method for updating the screen and displaying the new
        image. For menus, you can use a static image for the background, and then on top
        of that place texts showing the question and four possible answers. In pygame, you
        can use the pygame.font.Font object to define a new font to be used for writing
        texts (you can have multiple if you need different text sizes, for example), and then
        use the Font.render() method to write text onto the screen.'''
        elements = screen_content.split('&')
        for element in elements:
            type_content = element.split(';')
            content = type_content[1]
            if type_content[0] == 'image':
                img = pygame.image.load('screen/' + content)
                screen.blit(img, self._screen_coord)
            elif type_content[0] == 'text':
                text_position = 'center'
                if '*' in content:
                    content, text_position = content.split('*')
                font = pygame.font.Font(None, 36)
                text_surface = font.render(content, True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                if text_position == 'center':
                    text_rect.center = (self._screen_coord[0] + 500, self._screen_coord[1] + 136)
                screen.blit(text_surface, text_rect)
        
        if self._current_state == 'ask_question':
            question_data = self._questions[self._questions_asked - 1]
            question_text = question_data['question']
            answers = ['A', 'B', 'C', 'D']
            answer_texts = [f"{ans}: {question_data[ans]}" for ans in answers]
            
            # Render question
            font = pygame.font.Font(None, 36)
            question_surface = font.render(question_text, True, (255, 255, 255))
            question_rect = question_surface.get_rect(center=(self._screen_coord[0] + 500, self._screen_coord[1] + 50))
            screen.blit(question_surface, question_rect)
            
            # Render answers
            for i, answer_text in enumerate(answer_texts):
                answer_surface = font.render(answer_text, True, (255, 255, 255))
                answer_rect = answer_surface.get_rect(center=(self._screen_coord[0] + 125 + i*250, self._screen_coord[1] + 200))
                screen.blit(answer_surface, answer_rect)


        
        
        pygame.display.flip()

    # Method for playing an animation
    def play_animation(self, screen, animation):
        ''' animations will be achieved by displaying a
            sequence of frames at a certain rate. This can be done by following the same
            process you used for showing static images on the robot’s screen, and just update
            the image being displayed every X seconds to the next frame in the animation, until
            all the frames have been shown. X will define your animation’s fps (e.g. if we want
            to achieve 20 FPS, we need to update the image every 0.05 seconds). Animations
            can be find in the animations folder. We will have one sub-folder per animation,
            with all the frames inside.'''
        animation_path = os.getcwd() + '/animations/' + animation
        if os.path.isdir(animation_path):
            frame_files = sorted(os.listdir(animation_path))
            for frame_file in frame_files:
                img = pygame.image.load(os.path.join(animation_path, frame_file))
                screen.blit(img, (0,0))
                pygame.display.flip()
                time.sleep(0.05)  # Assuming 20 FPS
        


##################### METHODS FOR MANAGING THE ROBOT'S PERCEPTION #####################
    # Method for capturing user inputs. It should receive the type of input expected, and act accordingly
    def obtain_user_answer(self):
        ''' The application described in this manual requires the agent to be able to accept inputs
        coming through two different channels: text-based, and screen-based.
        ● A text-based input will be used when the virtual agent asks the user if they need to
        hear the instructions for the game. We need to have a way to capture the answer to
        that question through the keyboard. For this, we can use python’s built-in
        input(prompt) method. In this case, prompt is the message that the user will see
        on the terminal. The method returns a string containing the sequence of keys
        pressed by the user.
        6
        ● Screen-based inputs will be used for allowing the user to answer questions. When
        the user clicks on one of the answers on the screen, we need to capture the position
        where the user clicked, and then associate this with one of the possible answers.
        For the former, we can check if we receive a pygame event with type
        pygame.MOUSEBUTTONDOWN, and then store the position for the click using the
        get_pos() method provided by the pygame.mouse library. For the later, because we
        are always going to have four possible answers on screen, we can divide the screen
        in four regions (see Figure 8), check if the coordinates for the click fall in one of this
        four regions. and return the letter associated with each option (A, B, C, or D).
        '''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # Assuming screen width is 1000 and height is 272
                    if 0 <= x < 250:
                        return 'A'
                    elif 250 <= x < 500:
                        return 'B'
                    elif 500 <= x < 750:
                        return 'C'
                    elif 750 <= x <= 1000:
                        return 'D'
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                #input-based
            user_input = input("Your answer (A/B/C/D): ").strip().lower()
            if user_input in ['a', 'b', 'c', 'd']:
                return user_input.upper()
    

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
            # Logic to check if the answer is correct 
            if user_answer == self._questions[self._questions_asked - 1]['correct_answer']:
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
            self._current_state = 'end'
        
    def execute_state(self, screen):
        dialogue_step = self.obtain_dialogue_step(self._current_state)
        self.expressiveness_system(dialogue_step['speech'], 
                                    dialogue_step['screen'], 
                                    dialogue_step['animation'])  
        return



