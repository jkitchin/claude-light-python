"""The API for Claude-Light.

Instruments
-----------

# GreenMachine1

This instrument has one input, the green channel, and one output at 515nm.

# GreenMachine3

This instrument has one input, the green LED channel, and it has three outputs,
for the 630nm, 515nm, and 445nm.

# CLRGB

This instrument has three inputs, the red, green and blue LED settings, and it
has three outputs: the intensities at 630nm, 515nm, and 445nm.

# CLLight

This instrument has three inputs: the red, green and blue LED settings. It
returns all data in json. These are the wavelengths included:

415nm	445nm	480nm	515nm	555nm	590nm	630nm	680nm	clear	nir

"""
import requests
from retry import retry

CLAUDE_URL = 'https://claude-light.cheme.cmu.edu/api'


class GreenMachine1:
    """One input -> one output instrument.

    You set the green LED intensity and measure the 515nm output intensity.
    """

    @retry(tries=3, delay=2)
    def __call__(self, G=0):
        """Run the instrument.

        G : int, setting for the green LED channel.
        Returns the 515nm channel intensity.
        """
        resp = requests.get(CLAUDE_URL, params={'R': 0, 'G': G, 'B': 0})
        data = resp.json()
        return data['out']['515nm']


class GreenMachine3:
    """One input -> 3 outputs instrument.

    Returns list of outputs at 630nm, 515nm, and 445nm.
    """

    @retry(tries=3, delay=2)
    def __call__(self, G=0):
        """Run the instrument.

        Parameters
        ----------
        G : int, optional
            Setting for the green LED channel. Default is 0.

        Returns
        -------
        list
            List of outputs at 630nm, 515nm, and 445nm.
        """
        resp = requests.get(CLAUDE_URL, params={'R': 0, 'G': G, 'B': 0})
        data = resp.json()
        return [data['out'][i] for i in ['630nm', '515nm', '445nm']]


class CLRGB:
    """Three inputs -> three outputs instrument.

    Returns list of outputs at 630nm, 515nm, and 445nm.
    """

    @retry(tries=3, delay=2)
    def __call__(self, R=0, G=0, B=0):
        """Run the instrument.

        Parameters
        ----------
        R : int, optional
            Setting for the red LED channel. Default is 0.
        G : int, optional
            Setting for the green LED channel. Default is 0.
        B : int, optional
            Setting for the blue LED channel. Default is 0.


        Returns
        -------
        list
            List of outputs at 630nm, 515nm, and 445nm.
        """
        resp = requests.get(CLAUDE_URL, params={'R': R, 'G': G, 'B': B})
        data = resp.json()
        return [data['out'][i] for i in ['630nm', '515nm', '445nm']]


class CLLight:
    """Most general instrument. Three inputs -> all outputs.

    Returns all data in json. These are the wavelengths included.
    415nm	445nm	480nm	515nm	555nm	590nm	630nm	680nm	clear	nir
    """

    @retry(tries=3, delay=2)
    def __call__(self, R=0, G=0, B=0):
        """Run the instrument.

        Parameters
        ----------
        R : int, optional
            Setting for the red LED channel. Default is 0.
        G : int, optional
            Setting for the green LED channel. Default is 0.
        B : int, optional
            Setting for the blue LED channel. Default is 0.

        Returns
        -------
        dict
            All data in json format.
        """
        resp = requests.get(CLAUDE_URL, params={'R': R, 'G': G, 'B': B})
        data = resp.json()
        return data
