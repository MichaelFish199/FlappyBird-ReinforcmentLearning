# For screen capture
from mss import mss
# For sending commands
import pydirectinput
# For frame preprocessing
import cv2
# For array transformations
import numpy as np
# For slowing down game
import time
# Bese Environment components
from gym import Env
from gym.spaces import Box, Discrete

class Flappy_Bird(Env):
    
    def __init__(self):
        super().__init__()
        # Specify observation space and action space
        self.observation_space = Box(low=0, high=255, shape=(1,80,80), dtype=np.uint8)
        self.action_space = Discrete(2)
        # Capture game frames
        self.cap = mss()
        # You might need to change these numbers below
#         self.game_location = {'top': 118, 'left': 468, 'width': 265, 'height': 388}
#         self.done_location = {'top': 260, 'left': 464, 'width': 1, 'height': 1}
#         self.x_click = 486
#         self.y_click = 486
        
        self.game_location = {'top': 200, 'left': 640, 'width': 420, 'height': 600}
        self.done_location = {'top': 360, 'left': 760, 'width': 1, 'height': 1}
        self.x_click = 750
        self.y_click = 670

    def step(self, action):
        # Action
        if action == 0:
            # Jump
            pydirectinput.click(x=self.x_click, y=self.y_click)
        else:
            # Do nothink
            time.sleep(0.18)

        # Checking if game is done
        done, done_cap = self.get_done() 
        # Getting observation
        observation = self.get_observation()
        reward = 1 
        info = {}
        return observation, reward, done, info
    
    def reset(self):
        # Reseting game
        time.sleep(2)
        for _ in range(3):
            time.sleep(0.08)
            pydirectinput.click(x=self.x_click, y=self.y_click)
        return self.get_observation()
        
    def render(self):
        # Rendering
        cv2.imshow('Game', self.current_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.close()
    
    def get_observation(self):
        # Frame preprocessing
        raw = np.array(self.cap.grab(self.game_location))[:,:,:3].astype(np.uint8)
        gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (80,80))
        channel = np.reshape(resized, (1,80,80))
        return channel
    
    def get_done(self):
        # Has game ended
        done_cap = np.array(self.cap.grab(self.done_location))
        done=False
        if 700 < np.sum(done_cap) < 720 :
            done = True
            
        return done, done_cap
    
    def close(self):
        # Closing env
        cv2.destroyAllWindows()
