import numpy as np

class actions_super_simple(object):
    """
    {0,1,...,n-1}
    Example usage:
    self.action_space = actions_simple()
    """
    def __init__(self):
        pass
    
    def sample(self):
        return np.random.randint(low=0, high=2) ## Return a random number between 1 and 4 inclusive
    
    def contains(self, x):
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (x.dtype.kind in np.typecodes['AllInteger'] and x.shape == ()):
            as_int = int(x)
        else:
            return False
        return as_int >=0 and as_int <=1

    def __repr__(self):
        return "Actions simple"
    
    def __eq__(self, other):
        return True ## To do



class actions_simple(object):
    """
    {0,1,...,n-1}
    Example usage:
    self.action_space = actions_simple()
    """
    def __init__(self):
        pass
    def sample(self):
        return np.random.randint(low=0, high=4) ## Return a random number between 1 and 4 inclusive
    
    def contains(self, x):
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (x.dtype.kind in np.typecodes['AllInteger'] and x.shape == ()):
            as_int = int(x)
        else:
            return False
        return as_int >=0 and as_int <=3

    def __repr__(self):
        return "Actions simple"
    
    def __eq__(self, other):
        return True ## To do
