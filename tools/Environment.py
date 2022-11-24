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
        self.observation_space = Box(low=0, high=255, shape=(1,40,40), dtype=np.uint8)
        self.action_space = Discrete(2)
        # Capture game frames
        self.cap = mss()
        self.game_location = {'top': 170, 'left': 500, 'width': 550, 'height': 488}
        self.done_location = {'top': 270, 'left': 540, 'width': 1, 'height': 1}
        self.x_click = 550
        self.y_click = 600
        
    def step(self, action):
        # Action
        if action == 0:
            # Jump
            pydirectinput.press("space")
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
        time.sleep(1.5)
        pydirectinput.click(x=550, y=600)
        time.sleep(0.4)
        pydirectinput.press("space")
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
        resized = cv2.resize(gray, (40,40))
        channel = np.reshape(resized, (1,40,40))
        return channel
    
    def get_done(self):
        # Has game ended
        done_cap = np.array(self.cap.grab(self.done_location))
        done=False
        if 680 < np.sum(done_cap) < 715 :
            done = True
            
        return done, done_cap
    
    def close(self):
        # Closing env
        cv2.destroyAllWindows()