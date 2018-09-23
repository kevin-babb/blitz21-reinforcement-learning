import numpy as np

class observations_super_simple(object):
    """
    {0,1,...,n-1}
    Example usage:
    self.observations_simple = observations_simple()
    """
    def __init__(self):
        pass
    def sample(self):
        value_1, value_2, value_3, value_4 = np.random.randint(low=0, high=21, size=4)
        busts = np.random.randint(low=0, high=3)
        cards_remaining = np.random.randint(low=1, high=53)
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
        deck = deck[:cards_remaining]
        showing_card_value = deck[0]
        deck = np.delete(deck, [0])
        
        state = (busts, value_1, value_2, value_3, value_4, deck, showing_card_value)
        return state, deck
    
    def contains(self, obs_state, obs_deck):
        # check that deck contains 52 cards
        busts, value_1, value_2, value_3, value_4, showing_card_value = obs_state
        deck = obs_deck
        
        if busts > 3:
            return False
        elif value_1 > 7 or value_2 > 7 or value_3 > 7 or value_4 > 7:
            return False
        elif showing_card_value <=0 or showing_card_value >=3:
            return False
        elif len(deck) >= 52:
            return False
        else:
            return True

    def __repr__(self):
        return "Discrete(%d)" % self.n
    def __eq__(self, other):
        return True ## to do




class observations_simple(object):
    """
    {0,1,...,n-1}
    Example usage:
    self.observations_simple = observations_simple()
    """
    def __init__(self):
        pass
    
    def sample(self):
        value_1, value_2, value_3, value_4 = np.random.randint(low=0, high=21, size=4)
        busts = np.random.randint(low=0, high=3)
        cards_remaining = np.random.randint(low=1, high=53)
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
        deck = deck[:cards_remaining]
        showing_card_value = deck[0]
        deck = np.delete(deck, [0])
        
        state = (busts, value_1, value_2, value_3, value_4, deck, showing_card_value)
        return state, deck
    
    def contains(self, obs_state, obs_deck):
        # check that deck contains 52 cards
        busts, value_1, value_2, value_3, value_4, showing_card_value = obs_state
        deck = obs_deck
        
        if busts > 3:
            return False
        elif value_1 > 21 or value_2 > 21 or value_3 > 21 or value_4 > 21:
            return False
        elif showing_card_value <=0 or showing_card_value >=12:
            return False
        elif len(deck) >= 52:
            return False
        else:
            return True

    def __repr__(self):
        return "Discrete(%d)" % self.n
    def __eq__(self, other):
        return True ## to do
    
    