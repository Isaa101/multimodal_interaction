#! /usr/env/python3

# Aina Crespi Hromcova
# Isabel Gregorio Diez

import pygame
from dialogue_system import FSMDialogueSystem


class Gui:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((1000, 1000))
        pygame.display.set_caption("Multimodal interaction lab")
        image = pygame.image.load("images/mini.jpg").convert()
        self._screen.blit(image, (296,0))
        pygame.display.flip()
        self._clock = pygame.time.Clock()
        self._dm = FSMDialogueSystem()

    def run(self):
        while self._dm._current_state != 'end':
            self._dm.execute_state(self._screen)
            self._dm.update_state() 


if __name__=='__main__':
    gui = Gui()
    gui.run()