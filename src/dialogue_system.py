#! /usr/env/python3
# Aina Crespi Hromcova
# Isabel Gregorio Diez

import os
import sys
import yaml
import time
import pygame




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
        self._correct_answers = 0
        self._prize_levels = [100, 200, 500, 1000, 5000]  #prize for 1...5 correct answers


#---------------------------------------
# HELPERS FOR POSITION OF DISPLAYED CONTENT


    def _answer_positions(self):
        """Centros donde dibujas A, B, C y D sobre tablet.png"""
        return {
            'A': (self._screen_coord[0] + 275, self._screen_coord[1] + 145),
            'B': (self._screen_coord[0] + 725, self._screen_coord[1] + 145),
            'C': (self._screen_coord[0] + 275, self._screen_coord[1] + 215),
            'D': (self._screen_coord[0] + 725, self._screen_coord[1] + 215),
        }

    def _answer_rects(self):
        """Rectángulos clicables que corresponden a las píldoras verdes."""
        return {
            'A': pygame.Rect(self._screen_coord[0] + 55,  self._screen_coord[1] + 115, 420, 60),
            'B': pygame.Rect(self._screen_coord[0] + 525, self._screen_coord[1] + 115, 420, 60),
            'C': pygame.Rect(self._screen_coord[0] + 55,  self._screen_coord[1] + 185, 420, 60),
            'D': pygame.Rect(self._screen_coord[0] + 525, self._screen_coord[1] + 185, 420, 60),
        }

#---------------------------------------

#---------------------------------------
# HELPER FOR FINAL SCORE AND PRIZE COMPUTATION

    def _compute_final_prize_and_message(self):
        """
        Returns (prize_euros, message_str).
        prize_euros: 0 if no correct answers, else one of [10,20,50,100,500]
        message_str: congratulatory if all correct, encouragement otherwise
        """
        n = self._correct_answers
        if n <= 0:
            prize = 0
        else:
            # Cap at the length of the prize ladder
            prize = self._prize_levels[min(n, len(self._prize_levels)) - 1]

        if n == len(self._questions):
            message = "Congratulations! You answered all questions correctly!"
        else:
            message = f"Good try! You answered {n} out of {len(self._questions)} correctly."

        return prize, message
#---------------------------------------

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
        # Lists to track running processes
        running_processes = []
        
        # PLAY ANIMATION (if provided)
        if animation:
            # We'll run animation in a separate thread to not block speech
            import threading
            anim_thread = threading.Thread(target=self.play_animation, args=(screen, animation))
            anim_thread.daemon = True
            anim_thread.start()
            running_processes.append(('animation', anim_thread))
            
    
        # DISPLAY SCREEN CONTENT (if provided)
        if screen_content:
            self.display_multimedia_content(screen, screen_content)
        
        # PLAY SPEECH and WAIT for it to finish (this is our main blocking call)
        if speech:
            self.robot_speech(speech)
            # robot_speech should block until audio finishes playing
            if animation:
                anim_thread.join()
        
        # If no speech but animation is running, wait for animation to complete
        #if not speech and animation:
        #    anim_thread.join()

    # Method for playing the robot's voice
    def robot_speech(self, speech):
        pygame.mixer.init()
        sound = pygame.mixer.Sound('audios/' + speech + '.mp3')
        channel = sound.play()
        while channel.get_busy():
            time.sleep(0.1)


    # Method for displaying multimedia content on the robot's "screen"
    def display_multimedia_content(self, screen, screen_content,):
        pygame.font.init()

        # Define the font once
        font_question = pygame.font.Font(None, 36)  # for question or prompt
        font_answer   = pygame.font.Font(None, 36)  # for answers/YES/NO

        # Clear the lower area (1000x272) before drawing new content
        clear_rect = pygame.Rect(self._screen_coord[0], self._screen_coord[1], 1000, 272)
        screen.fill((0, 0, 0), clear_rect)  # Black background

        elements = screen_content.split('&')
        for element in elements:
            type_content = element.split(';')
            content = type_content[1]

            if type_content[0] == 'image':
                img = pygame.image.load('images/' + content)
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
        
        
        if self._current_state == 'explanation_needed':
            # Text of the question in the upper box
            prompt_text = "Do you need to hear the instructions?"
            prompt_surface = font_question.render(prompt_text, True, (255, 255, 255))
            prompt_rect = prompt_surface.get_rect(center=(self._screen_coord[0] + 500, self._screen_coord[1] + 65))
            screen.blit(prompt_surface, prompt_rect)

            # YES and NO in positions A and B
            positions = self._answer_positions()
            yes_surface = font_answer.render("YES", True, (255, 255, 255))
            yes_rect = yes_surface.get_rect(center=positions['A'])
            screen.blit(yes_surface, yes_rect)

            no_surface = font_answer.render("NO", True, (255, 255, 255))
            no_rect = no_surface.get_rect(center=positions['B'])
            screen.blit(no_surface, no_rect)

        elif self._current_state == 'ask_question':
            question_data = self._questions[self._questions_asked - 1]
            question_text = question_data['question']
            answers = ['A', 'B', 'C', 'D']
            answer_texts = [f"{ans}: {question_data[ans]}" for ans in answers]
            
            # Render question
            question_surface = font_question.render(question_text, True, (255, 255, 255))
            question_rect = question_surface.get_rect(center=(self._screen_coord[0] + 500, self._screen_coord[1] + 65))
            screen.blit(question_surface, question_rect)
            
            # Render answers
            positions = self._answer_positions()

            for i, answer_text in enumerate(answer_texts):
                ans_key = answers[i]
                answer_surface = font_answer.render(answer_text, True, (255, 255, 255))
                answer_rect = answer_surface.get_rect(center=positions[ans_key])
                screen.blit(answer_surface, answer_rect)

        
        elif self._current_state == 'score':
            prize, msg = self._compute_final_prize_and_message()

            # Fonts
            pygame.font.init()
            font_title  = pygame.font.Font(None, 30)
            font_prize  = pygame.font.Font(None, 100)
            font_footer = pygame.font.Font(None, 32)

            area_x, area_y = self._screen_coord

            # Title/message in the top pill
            title_surface = font_title.render(msg, True, (0, 0, 0))
            title_rect    = title_surface.get_rect(center=(area_x + 500, area_y + 75))
            screen.blit(title_surface, title_rect)

            # Prize in the first answer row center (use B center for emphasis)
            prize_text = f"{prize}€" if prize > 0 else "No prize"
            prize_surface = font_prize.render(prize_text, True, (255, 140, 0))
            prize_rect    = prize_surface.get_rect(center=(area_x + 500, area_y + 145))  # centered between A/B
            screen.blit(prize_surface, prize_rect)



        '''
        # Debug to show areas to click
        
        if self._current_state in ("explanation_needed", "ask_question"):
            rects = self._answer_rects()
            color = (255, 0, 0)
            width = 2
            if self._current_state == "explanation_needed":
                pygame.draw.rect(screen, color, rects['A'], width)  # YES
                pygame.draw.rect(screen, color, rects['B'], width)  # NO
            else:
                for r in rects.values():
                    pygame.draw.rect(screen, color, r, width)
        '''        
        
        pygame.display.flip()

    # Method for playing an animation
    def play_animation(self, screen, animation):
        animation_path = os.getcwd() + '/animations/' + animation
        if os.path.isdir(animation_path):
            frame_files = sorted(os.listdir(animation_path))
            for frame_file in frame_files:
                img = pygame.image.load(os.path.join(animation_path, frame_file))
                screen.blit(img, (296,0))
                pygame.display.flip()
                time.sleep(0.05)  # Assuming 20 FPS
        


##################### METHODS FOR MANAGING THE ROBOT'S PERCEPTION #####################
    # Method for capturing user inputs. It should receive the type of input expected, and act accordingly
    def obtain_user_answer(self):
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # mouse click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if self._current_state == "explanation_needed":
                        rects = self._answer_rects()
                        if rects['A'].collidepoint(x, y):
                            print("User answer: YES\n")
                            return 'YES'
                        elif rects['B'].collidepoint(x, y):
                            print("User answer: NO\n")
                            return 'NO'
                        # (Ignores clicks on C/D in this state)

                    elif self._current_state == "ask_question":
                        rects = self._answer_rects()
                        for opt in ['A', 'B', 'C', 'D']:
                            if rects[opt].collidepoint(x, y):
                                print(f"User answer: {opt}\n")
                                return opt
                            
            # keyboard events
            keys = pygame.key.get_pressed()
            
            if self._current_state == "explanation_needed":
                if keys[pygame.K_y]:
                    print("User answer: YES\n"); return 'YES'
                elif keys[pygame.K_n]:
                    print("User answer: NO\n");  return 'NO'
            elif self._current_state == "ask_question":
                if keys[pygame.K_a]: print("User answer: A\n"); return 'A'
                if keys[pygame.K_b]: print("User answer: B\n"); return 'B'
                if keys[pygame.K_c]: print("User answer: C\n"); return 'C'
                if keys[pygame.K_d]: print("User answer: D\n"); return 'D'


            pygame.time.wait(100)   # small delay to avoid busy waiting

    

##################### METHODS FOR CONTROLLING THE INTERACTION FLOW #####################

    def update_state(self):
        if self._current_state == 'introduction':
            self._current_state = 'explanation_needed'
        elif self._current_state == 'explanation_needed':
            user_answer = self.obtain_user_answer()
            if user_answer == 'YES':
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
                self._correct_answers += 1
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
            self._current_state = 'goodbye'
        elif self._current_state == 'goodbye':
            self._current_state = 'end'
        
    def execute_state(self, screen):
        dialogue_step = self.obtain_dialogue_step(self._current_state)
        print(dialogue_step['text'][0])  # Print the text to console
        print()
        #Print question and possible answers in console
        if self._current_state == "ask_question":
            question = self._questions[self._questions_asked - 1]
            print("Question:", question['question'])
            for option in ['A', 'B', 'C', 'D']:
                print(f"{option}: {question[option]}")
            print ("\nPress Y (Yes), N (No), A, B, C, or D ->      ")

        if self._current_state == 'explanation_needed':
            print ("\nPress Y (Yes), N (No), A, B, C, or D ->      ")

        self.expressiveness_system(screen, dialogue_step['audio'][0], 
                                    dialogue_step['screen'][0], 
                                    dialogue_step['animation'][0] if 'animation' in dialogue_step else None)  
        return



