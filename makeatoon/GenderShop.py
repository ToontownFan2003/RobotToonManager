"""GenderShop module: contains the GenderShop class"""

from pandac.PandaModules import *
from direct.fsm import StateData
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer

class GenderShop(StateData.StateData):
    """GenderShop class: contains methods for changing the Avatar's
    gendervia user input"""

    def __init__(self, doneEvent):
        """__init__(self, Event)
        Set-up the gender to shop to query user about toons gender
        """
        StateData.StateData.__init__(self, doneEvent)
        self.shopsVisited = []
        self.toon = None
        self.gender = "m"
        return

    def enter(self):
        """enter(self)
        """
        # turn off any user control
        base.disableMouse()
        return None

    def showButtons(self):
        return None
        
    def exit(self):
        """exit(self)
        Remove events and restore display
        """
        return None

    def load(self):
        """load(self)
        """

        return

    def unload(self):
        """unload(self)
        """

        return

    def setGender(self, choice):
        self.__setGender(choice)
        
    # event handlers

    def __setGender(self, choice):
        if (choice == -1):
            self.gender = "m"
        else:
            self.gender = "f"
        messenger.send(self.doneEvent)





