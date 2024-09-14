import requests
from retry import retry

CLAUDE_IP = 'http://claude-light.cheme.cmu.edu/api'

class GreenMachine1:
    """One input -> one output instrument.
    """
    @retry(tries=3, delay=2)
    def __call__(self, G=0):
        """Run the instrument.
        G : int, setting for the green LED channel.
        Returns the 515nm channel intensity.
        """
        resp = requests.get(CLAUDE_IP, params={'R': 0, 'G': G, 'B': 0})
        data = resp.json()
        return data['out']['515nm']


class GreenMachine3:
    """One input -> 3 outputs instrument.
    Returns list of outputs at 630nm, 515nm, and 445nm.
    """
    @retry(tries=3, delay=2)
    def __call__(self, G=0):
        resp = requests.get(CLAUDE_IP, params={'R': 0, 'G': G, 'B': 0})
        data = resp.json()
        return [data['out'][i] for i in ['630nm', '515nm', '445nm']]

    
class CLRGB:    
    """Three inputs -> three outputs instrument.
    Returns list of outputs at 630nm, 515nm, and 445nm.
    """
    @retry(tries=3, delay=2)
    def __call__(self, R=0, G=0, B=0):
        resp = requests.get(CLAUDE_IP, params={'R': R, 'G': G, 'B': B})
        data = resp.json()
        return [data['out'][i] for i in ['630nm', '515nm', '445nm']]

    
class CLLight:
    """Most general instrument. Three inputs -> all outputs.
    Returns all data in json.
    """
    @retry(tries=3, delay=2)
    def __call__(self, R=0, G=0, B=0):
        resp = requests.get(CLAUDE_IP, params={'R': R, 'G': G, 'B': B})
        data = resp.json()
        return data
