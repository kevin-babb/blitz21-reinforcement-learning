import numpy as np
import importlib
import actions as act
import observations as obs
import warnings
importlib.reload(act)
importlib.reload(obs)


class Blitz_21_super_simple(object):
    """
    Description:
        A Blackjack-esque card game

    Source:
        This courrespondes to the game developed by Tether and available on the Skillz platform, with some simplifications

    State Observations: 
        Type:
        Two piles, with number 0-6, one hot encoded
        One available card, with number 2 or 3
        
    Deck:
        List of numbers
    
    Actions:
        Type: Int
        Num	Action
        1 = Place Card on First Pile
        2 = Place Card on Second Pile
        
    Reward:
        Reward is 1 for every step taken, including the termination step

    Starting State:
        All piles have zero value, there are zero busts, there is one random card exposed a 51 cards remaining

    Episode Termination:
        Three busts
        There are zero cards remaining
    """
    
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
                
        self.action_space = act.actions_super_simple() 
        self.observation_space = obs.observations_super_simple() ## To do

        self.viewer = None
        self.state = None
        self.deck = None

        self.steps_beyond_done = None

    def step(self, action):
        #assert self.action_space, "error"
        assert self.action_space.contains(action), "%r (%s) invalid, state %r, action space %r"%(action, type(action), self.state, self.action_space)
        
        reward = 0
        state = self.state
        deck = self.deck
        busts, value_1, value_2, showing_card_value = state
        
        assert showing_card_value, "No card showing"

        #Increment the values based on the action
        if action == 0:
            value_1 += showing_card_value
        elif action == 1:
            value_2 += showing_card_value
        
        #Calculate busts
        for value in [value_1, value_2]:
            if value > 7:
                busts +=1
                reward -= 10
        
        #Reset after busts
        if value_1 > 7:
            value_1 = 0
        if value_2 > 7:
            value_2 = 0     
        
        #Reset and gain reward after 21
        if value_1 == 7:
            value_1 = 0
            reward += 5
        if value_2 == 7:
            value_2 = 0
            reward += 5

        #Get the next card from the deck, if any remain
        showing_card_value = None
        if len(deck) > 0:
            showing_card_value = deck[0]
            deck = np.delete(deck, [0])
        
        state = (busts, value_1, value_2, showing_card_value)
        self.state = state
        self.deck = deck
        
        #Done if the deck is empty or we have busted 3 times
        done = len(deck)==0 or busts >=3
        done = bool(done)

        if not done:
            reward += 1.0
        elif self.steps_beyond_done is None:
            # Game just ended
            self.steps_beyond_done = 0
            reward += 1.0
        else:
            if self.steps_beyond_done == 0:
                warnings.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(state), reward, done, deck

    def reset(self, new_game=False):
        # Create and shuffle the deck
        deck = np.array([2,2,2,2,
                         2,2,2,2,
                         2,2,2,2,
                         2,2,2,2,
                         2,2,2,2,
                         2,2,2,2,
                         2,2,2,2,
                         1,1,1,1,
                         1,1,1,1,
                         1,1,1,1,
                         1,1,1,1,
                         1,1,1,1,
                         1,1,1,1
                        ])
        np.random.shuffle(deck)
        
        
        if new_game: 
            busts = 0
            value_1 = 0
            value_2 = 0
        
            showing_card_value = deck[0]
            deck = np.delete(deck, [0])
            
        else: 
            busts = np.random.randint(low=0, high=3)
            value_1 = np.random.randint(low=0, high=7)
            value_2 = np.random.randint(low=0, high=7)
            cards_remaining = np.random.randint(low=1, high=53)
            deck = deck[:cards_remaining]
            showing_card_value = deck[0]
            deck = np.delete(deck, [0])
            
            
        self.state = (busts, value_1, value_2, showing_card_value)
        self.deck = deck
        self.steps_beyond_done = None
        return np.array(self.state), self.deck

    
    def render(self, mode='human'):
        busts, value_1, value_2, showing_card_value = self.state
        deck = self.deck
        print('Piles: | {:02} | {:02} |  Busts: {}  |  Next Card: {}  |'.format(
            value_1, value_2, busts, showing_card_value))

        
    def close(self): # This not really implemented
        if self.viewer:
            self.viewer.close()
            self.viewer = None



            
            
            
            

class Blitz_21_simple(object):
    """
    Description:
        A Blackjack-esque card game

    Source:
        This courrespondes to the game developed by Tether and available on the Skillz platform, with some simplifications

    State Observations: 
        Type: array
        Num	Observation
        0 = Number of Busts (int)
        1 = Card Value in First Pile (int)
        2 = Card Value in Second Pile (int)
        3 = Card Value in Third Pile (int)
        4 = Card Value in Fourth Pile (int)
        5 = Card Showing (int)
        
    Deck:
        list of numbers
    
    Actions:
        Type: Int
        Num	Action
        1 = Place Card on First Pile
        2 = Place Card on Second Pile
        3 = Place Card on Third Pile
        4 = Place Card on Fourth Pile
        
    Reward:
        Reward is 1 for every step taken, including the termination step

    Starting State:
        All piles have zero value, there are zero busts, there is one random card exposed a 51 cards remaining

    Episode Termination:
        Three busts
        There are zero cards remaining
    """
    
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
                
        self.action_space = act.actions_simple() 
        self.observation_space = obs.observations_simple() ## To do

        self.viewer = None
        self.state = None
        self.deck = None

        self.steps_beyond_done = None

    def step(self, action):
        #assert self.action_space, "error"
        assert self.action_space.contains(action), "%r (%s) invalid, state %r, action space %r"%(action, type(action), self.state, self.action_space)
        
        reward = 0
        state = self.state
        deck = self.deck
        busts, value_1, value_2, value_3, value_4, showing_card_value = state
        
        assert showing_card_value, "No card showing"

        #Increment the values based on the action
        if action == 0:
            value_1 += showing_card_value
        elif action == 1:
            value_2 += showing_card_value
        elif action == 2:
            value_3 += showing_card_value
        else:
            value_4 += showing_card_value
        
        #Calculate busts
        for value in [value_1, value_2, value_3, value_4]:
            if value > 21:
                busts +=1
                reward -= 10
        
        #Reset after busts
        if value_1 > 21:
            value_1 = 0
        if value_2 > 21:
            value_2 = 0
        if value_3 > 21:
            value_3 = 0
        if value_4 > 21:
            value_4 = 0       
        
        #Reset and gain reward after 21
        if value_1 == 21:
            value_1 = 0
            reward += 5
        if value_2 == 21:
            value_2 = 0
            reward += 5
        if value_3 == 21:
            value_3 = 0
            reward += 5
        if value_4 == 21:
            value_4 = 0
            reward += 5

        #Get the next card from the deck, if any remain
        showing_card_value = None
        if len(deck) > 0:
            showing_card_value = deck[0]
            deck = np.delete(deck, [0])
        
        state = (busts, value_1, value_2, value_3, value_4, showing_card_value)
        self.state = state
        self.deck = deck
        
        #Done if the deck is empty or we have busted 3 times
        done = len(deck)==0 or busts >=3
        done = bool(done)

        if not done:
            reward += 1.0
        elif self.steps_beyond_done is None:
            # Game just ended
            self.steps_beyond_done = 0
            reward += 1.0
        else:
            if self.steps_beyond_done == 0:
                warnings.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(state), reward, done, deck

    def reset(self, new_game=False):
        # Create and shuffle the deck
        deck = np.array([2,2,2,2,
                         3,3,3,3,
                         4,4,4,4,
                         5,5,5,5,
                         6,6,6,6,
                         7,7,7,7,
                         8,8,8,8,
                         9,9,9,9,
                         10,10,10,10,
                         10,10,10,10,
                         10,10,10,10,
                         10,10,10,10,
                         11,11,11,11
                        ])
        np.random.shuffle(deck)
        
        
        if new_game: 
            busts = 0
            value_1 = 0
            value_2 = 0
            value_3 = 0
            value_4 = 0
        
            showing_card_value = deck[0]
            deck = np.delete(deck, [0])
            
        else: 
            busts = np.random.randint(low=0, high=3)
            value_1 = np.random.randint(low=0, high=21)
            value_2 = np.random.randint(low=0, high=21)
            value_3 = np.random.randint(low=0, high=21)
            value_4 = np.random.randint(low=0, high=21)
            cards_remaining = np.random.randint(low=1, high=53)
            deck = deck[:cards_remaining]
            showing_card_value = deck[0]
            deck = np.delete(deck, [0])
            
            
        self.state = (busts, value_1, value_2, value_3, value_4, showing_card_value)
        self.deck = deck
        self.steps_beyond_done = None
        return np.array(self.state), self.deck

    
    def render(self, mode='human'):
        busts, value_1, value_2, value_3, value_4, showing_card_value = self.state
        deck = self.deck
        print('Piles: | {:02} | {:02} | {:02} | {:02} |  Busts: {}  |  Next Card: {}  |'.format(
            value_1, value_2, value_3, value_4, busts, showing_card_value))

        
    def close(self): # This not really implemented
        if self.viewer:
            self.viewer.close()
            self.viewer = None
            
            

            
class Blitz_21(object):
    """
    Description:
        A Blackjack-esque card game

    Source:
        This courrespondes to the game developed by Tether and available on the Skillz platform, with some simplifications

    State Observations: 
        Type: array
        Num	Observation
        0 = Number of Busts (int)
        1 = Card Value in First Pile (int)
        2 = Card Value in Second Pile (int)
        3 = Card Value in Third Pile (int)
        4 = Card Value in Fourth Pile (int)
        5 = Card Showing (int) (-1 for wild card)
        6 = # cards in First Pile (int)
        7 = # cards in Second Pile (int)
        8 = # cards in Third Pile (int)
        9 = # cards in Fourth Pile (int)
        10 = is first pile soft
        11 = is second pile soft
        12 = is third pile soft
        13 = is fourth pile soft
        14 = # of cards remaining in deck
        15 = Next card (after card showing) (-1 for wild card)
        16 = probability next unknown card is 2
        17 = probability next unknown card is 3
        18 = probability next unknown card is 4
        19 = probability next unknown card is 5
        20 = probability next unknown card is 6
        21 = probability next unknown card is 7
        22 = probability next unknown card is 8
        23 = probability next unknown card is 9
        24 = probability next unknown card is 10
        25 = probability next unknown card is 11
        26 = probability next unknown card is -1 (wild card)
        27 = current streak
        
    Deck:
        list of numbers (not observable by agent)
    
    Actions:
        Type: Int
        Num	Action
        0 = Place Card on First Pile
        1 = Place Card on Second Pile
        2 = Place Card on Third Pile
        3 = Place Card on Fourth Pile
        4 = Undo (if not possible, this does nothing)
        
        
    Reward:
        Reward is -1 for every step taken. There are rewards for clearing, for 5 cards, and for combos. There is a penalty for the first bust.

    Starting State:
        All piles have zero value, there are zero busts, there is one random card exposed a 51 cards remaining

    Episode Termination:
        Three busts
        There are zero cards remaining
    """
    
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
                
        self.action_space = act.actions_simple() 
        self.observation_space = obs.observations_simple() ## To do

        self.viewer = None
        self.state = None
        self.deck = None
        
        self.first_bust_reward = -100
        self.clear_reward = 400
        self.five_card_reward = 600
        self.wild_card_reward = 200
        self.streak_2_reward = 250 # Great streak
        self.streak_3_reward = 500  # Super streak
        self.streak_4_reward = 750 # Mega streak
        self.streak_5_reward = 1000 # Monster streak
        self.streak_6_reward = 1250 # Never achieved this!
        self.steps_beyond_done = None

    def step(self, action):
        #assert self.action_space, "error"
        assert self.action_space.contains(action), "%r (%s) invalid, state %r, action space %r"%(action, type(action), self.state, self.action_space)
        
        reward = 0
        state = self.state
        deck = self.deck
        busts, value_1, value_2, value_3, value_4, showing_card_value = state
        
        assert showing_card_value, "No card showing"

        #Increment the values based on the action
        if action == 0:
            value_1 += showing_card_value
        elif action == 1:
            value_2 += showing_card_value
        elif action == 2:
            value_3 += showing_card_value
        else:
            value_4 += showing_card_value
        
        #Calculate busts
        for value in [value_1, value_2, value_3, value_4]:
            if value > 21:
                busts +=1
                reward -= 10
        
        #Reset after busts
        if value_1 > 21:
            value_1 = 0
        if value_2 > 21:
            value_2 = 0
        if value_3 > 21:
            value_3 = 0
        if value_4 > 21:
            value_4 = 0       
        
        #Reset and gain reward after 21
        if value_1 == 21:
            value_1 = 0
            reward += 5
        if value_2 == 21:
            value_2 = 0
            reward += 5
        if value_3 == 21:
            value_3 = 0
            reward += 5
        if value_4 == 21:
            value_4 = 0
            reward += 5

        #Get the next card from the deck, if any remain
        showing_card_value = None
        if len(deck) > 0:
            showing_card_value = deck[0]
            deck = np.delete(deck, [0])
        
        state = (busts, value_1, value_2, value_3, value_4, showing_card_value)
        self.state = state
        self.deck = deck
        
        #Done if the deck is empty or we have busted 3 times
        done = len(deck)==0 or busts >=3
        done = bool(done)

        if not done:
            reward += 1.0
        elif self.steps_beyond_done is None:
            # Game just ended
            self.steps_beyond_done = 0
            reward += 1.0
        else:
            if self.steps_beyond_done == 0:
                warnings.warn("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(state), reward, done, deck

    def reset(self, new_game=False):
        # Create and shuffle the deck
        deck = np.array([2,2,2,2,
                         3,3,3,3,
                         4,4,4,4,
                         5,5,5,5,
                         6,6,6,6,
                         7,7,7,7,
                         8,8,8,8,
                         9,9,9,9,
                         10,10,10,10,
                         10,10,10,10,
                         10,10,10,10,
                         10,10,10,10,
                         11,11,11,11
                        ])
        np.random.shuffle(deck)
        
        
        if new_game: 
            busts = 0
            value_1 = 0
            value_2 = 0
            value_3 = 0
            value_4 = 0
            cards_1 = 0
            cards_2 = 0
            cards_3 = 0
            cards_4 = 0
            car
        
            showing_card_value = deck[0]
            deck = np.delete(deck, [0])
            
        else: 
            busts = np.random.randint(low=0, high=3)
            value_1 = np.random.randint(low=0, high=21)
            value_2 = np.random.randint(low=0, high=21)
            value_3 = np.random.randint(low=0, high=21)
            value_4 = np.random.randint(low=0, high=21)
            cards_remaining = np.random.randint(low=1, high=53)
            deck = deck[:cards_remaining]
            showing_card_value = deck[0]
            deck = np.delete(deck, [0])
            
            
        self.state = (busts, value_1, value_2, value_3, value_4, showing_card_value)
        self.deck = deck
        self.steps_beyond_done = None
        return np.array(self.state), self.deck

    
    def render(self, mode='human'):
        busts, value_1, value_2, value_3, value_4, showing_card_value = self.state
        deck = self.deck
        print('Piles: | {:02} | {:02} | {:02} | {:02} |  Busts: {}  |  Next Card: {}  |'.format(
            value_1, value_2, value_3, value_4, busts, showing_card_value))

        
    def close(self): # This not really implemented
        if self.viewer:
            self.viewer.close()
            self.viewer = None