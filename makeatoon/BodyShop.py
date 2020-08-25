"""BodyShop module: contains the BodyShop class"""

from pandac.PandaModules import *
from toontown.toon import ToonDNA
from direct.fsm import StateData
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from MakeAToonGlobals import *
import random
import random
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from toontown.toontowngui import TeaserPanel

class BodyShop(StateData.StateData):
    """
    BodyShop class: contains methods for changing the Avatar's
    head, torso, and legs via user input
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("BodyShop")

    def __init__(self, doneEvent):
        """
        Set-up the body shop interface to change body parts on the
        given toon
        """
        StateData.StateData.__init__(self, doneEvent)
        self.toon = None
        self.torsoChoice = 0
        self.legChoice = 0
        self.headChoice = 0

    def enter(self, toon, shopsVisited=[]):
        # turn off any user control
        base.disableMouse()

        # load up the given toon
        self.toon = toon
        self.dna = self.toon.getStyle()
        gender = self.toon.style.getGender()
        
        # if its the first time in ghost the "left" arrows
        if BODYSHOP not in shopsVisited:
            self.headLButton['state'] = DGG.DISABLED
            self.torsoLButton['state'] = DGG.DISABLED
            self.legLButton['state'] = DGG.DISABLED
            self.headStart = ToonDNA.toonHeadTypes.index(self.dna.head)
            self.torsoStart = ToonDNA.toonTorsoTypes.index(self.dna.torso)
            self.legStart = ToonDNA.toonLegTypes.index(self.dna.legs)
            self.headChoice = self.headStart
            self.torsoChoice = self.torsoStart % 3
            self.legChoice = self.legStart
        else:
            # We've already been to the clothes shop
            self.headChoice = ToonDNA.toonHeadTypes.index(self.dna.head)
            self.torsoChoice = ToonDNA.toonTorsoTypes.index(self.dna.torso) % 3
            self.legChoice = ToonDNA.toonLegTypes.index(self.dna.legs)

        if CLOTHESSHOP in shopsVisited:
            self.clothesPicked = 1
        else:
            self.clothesPicked = 0
            
        # if we have visited the ClothesShop and the returned to the
        # GenderShop it's possible that our gender has changed and our DNA
        # has not. Update these bits...
        if (len(self.dna.torso) != 1):
            if (gender == 'm' or 
                ToonDNA.GirlBottoms[self.dna.botTex][1] == ToonDNA.SHORTS):
                torsoStyle = 's'
            else:
                torsoStyle = 'd'
            
            # update the clothes and eye lashes, just in case
            self.__swapTorso(0)
            self.__swapHead(0)

        # set up the "last" button
        self.acceptOnce("last", self.__handleBackward)
        # set up the "next" button
        self.accept("next", self.__handleForward)

        # possibly override the last hook
        self.restrictHeadType(self.dna.head)
        
    def showButtons(self):
        self.headLButton.show()
        self.headRButton.show()
        self.torsoLButton.show()
        self.torsoRButton.show()
        self.legLButton.show()
        self.legRButton.show()        

    def hideButtons(self):
        self.headLButton.hide()
        self.headRButton.hide()
        self.torsoLButton.hide()
        self.torsoRButton.hide()
        self.legLButton.hide()
        self.legRButton.hide()
        
    def exit(self):
        """
        Remove events and restore display
        """
        try:
            del self.toon
        except:
            self.notify.warning("BodyShop: toon not found")
            
        self.hideButtons()
        
        self.ignore("last")
        self.ignore("next")
        self.ignore("enter")

    def load(self):
        self.gui = loader.loadModel("phase_3/models/gui/create_a_toon_gui")

        guiRArrowDown = self.gui.find("**/CrtATn_R_Arrow_DN")
        guiRArrowRollover = self.gui.find("**/CrtATn_R_Arrow_RLVR")
        guiRArrowUp = self.gui.find("**/CrtATn_R_Arrow_UP")

        self.headLButton = DirectButton(
            relief = None,
            image = (guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp),
            image_scale = (-1,1,1),
            image3_color = Vec4(0.5,0.5,0.5,0.75),
            pos = (-0.9,0,0.3),
            text = TTLocalizer.BodyShopHead,
            text_scale = 0.0625,
            text_pos = (0.025, 0),
            text_fg = (0.8,0.1,0,1),
            command = self.__swapHead,
            extraArgs = [-1],
            )
        self.headRButton = DirectButton(
            relief = None,
            image = (guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp),
            image3_color = Vec4(0.5,0.5,0.5,0.75),
            text = TTLocalizer.BodyShopHead,
            text_scale = 0.0625,
            text_pos = (-0.025, 0),            
            text_fg = (0.8,0.1,0,1),
            pos = (0,0,0.3),
            command = self.__swapHead,
            extraArgs = [1],
            )

        self.torsoLButton = DirectButton(
            relief = None,
            image = (guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp),
            image_scale = (-1,1,1),
            image3_color = Vec4(0.5,0.5,0.5,0.75),
            text = TTLocalizer.BodyShopBody,
            text_scale = 0.0625,
            text_pos = (0.025, 0),            
            text_fg = (0.8,0.1,0,1),
            pos = (-0.9,0,-0.1),
            command = self.__swapTorso,
            extraArgs = [-1],
            )
        self.torsoRButton = DirectButton(
            relief = None,
            image = (guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp),
            image3_color = Vec4(0.5,0.5,0.5,0.75),
            text = TTLocalizer.BodyShopBody,
            text_scale = 0.0625,
            text_pos = (-0.025, 0),            
            text_fg = (0.8,0.1,0,1),
            pos = (0,0,-0.1),
            command = self.__swapTorso,
            extraArgs = [1],
            )

        self.legLButton = DirectButton(
            relief = None,
            image = (guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp),
            image_scale = (-1,1,1),
            image3_color = Vec4(0.5,0.5,0.5,0.75),
            text = TTLocalizer.BodyShopLegs,
            text_scale = 0.0625,
            text_pos = (0.025, 0),            
            text_fg = (0.8,0.1,0,1),
            pos = (-0.9,0,-0.5),
            command = self.__swapLegs,
            extraArgs = [-1],
            )
        self.legRButton = DirectButton(
            relief = None,
            image = (guiRArrowUp, guiRArrowDown, guiRArrowRollover, guiRArrowUp),
            image3_color = Vec4(0.5,0.5,0.5,0.75),
            text = TTLocalizer.BodyShopLegs,
            text_scale = 0.0625,
            text_pos = (-0.025, 0),            
            text_fg = (0.8,0.1,0,1),
            pos = (0,0,-0.5),
            command = self.__swapLegs,
            extraArgs = [1],
            )

        self.headLButton.hide()
        self.headRButton.hide()
        self.torsoLButton.hide()
        self.torsoRButton.hide()
        self.legLButton.hide()
        self.legRButton.hide()

    def unload(self):
        self.gui.removeNode()
        del self.gui

        self.headLButton.destroy()
        self.headRButton.destroy()
        self.torsoLButton.destroy()
        self.torsoRButton.destroy()
        self.legLButton.destroy()
        self.legRButton.destroy()

        del self.headLButton
        del self.headRButton
        del self.torsoLButton
        del self.torsoRButton
        del self.legLButton
        del self.legRButton

    # event handlers

    def __swapTorso(self, offset):
        # if this is the first time through only choose from naked torsos
        # (they are at 6-8)
        gender = self.toon.style.getGender()
        if not (self.clothesPicked):
            length = len(ToonDNA.toonTorsoTypes[6:])
            torsoOffset =  6
        # otherwise use either the male or female clothed torsos
        else:
            # Note: we need to correct colors that are not cross-gender
            # male (0-2)
            if (gender == 'm'):
                length = len(ToonDNA.toonTorsoTypes[:3])
                torsoOffset = 0
                if self.dna.armColor not in ToonDNA.defaultBoyColorList:
                    self.dna.armColor = ToonDNA.defaultBoyColorList[0]
                if self.dna.legColor not in ToonDNA.defaultBoyColorList:
                    self.dna.legColor = ToonDNA.defaultBoyColorList[0]
                if self.dna.headColor not in ToonDNA.defaultBoyColorList:
                    self.dna.headColor = ToonDNA.defaultBoyColorList[0]
                # Make sure the topTex, sleeveTex, and botTex are all within
                # valid index range for boys in case we're switching gender
                if (self.toon.style.topTex not in ToonDNA.MakeAToonBoyShirts):
                    randomShirt = ToonDNA.getRandomTop(gender, ToonDNA.MAKE_A_TOON)
                    shirtTex, shirtColor, sleeveTex, sleeveColor = randomShirt                    
                    self.toon.style.topTex = shirtTex
                    self.toon.style.topTexColor = shirtColor
                    self.toon.style.sleeveTex = sleeveTex
                    self.toon.style.sleeveTexColor = sleeveColor
                # Only use the boy shorts used in MakeAToon
                if (self.toon.style.botTex not in ToonDNA.MakeAToonBoyBottoms):
                    # Pick one randomly
                    botTex, botTexColor = ToonDNA.getRandomBottom(gender, ToonDNA.MAKE_A_TOON)
                    self.toon.style.botTex = botTex
                    self.toon.style.botTexColor = botTexColor
                    
            # female (0-5)
            else:
                length = len(ToonDNA.toonTorsoTypes[3:6])
                if (self.toon.style.torso[1] == 'd'):
                    torsoOffset = 3
                else:
                    torsoOffset = 0
                if self.dna.armColor not in ToonDNA.defaultGirlColorList:
                    self.dna.armColor = ToonDNA.defaultGirlColorList[0]
                if self.dna.legColor not in ToonDNA.defaultGirlColorList:
                    self.dna.legColor = ToonDNA.defaultGirlColorList[0]
                if self.dna.headColor not in ToonDNA.defaultGirlColorList:
                    self.dna.headColor = ToonDNA.defaultGirlColorList[0]
                # Make sure the topTex, sleeveTex, and botTex are all within
                # valid index range for girls in case we're switching gender
                if (self.toon.style.topTex not in ToonDNA.MakeAToonGirlShirts):
                    randomShirt = ToonDNA.getRandomTop(gender, ToonDNA.MAKE_A_TOON)
                    shirtTex, shirtColor, sleeveTex, sleeveColor = randomShirt                    
                    self.toon.style.topTex = shirtTex
                    self.toon.style.topTexColor = shirtColor
                    self.toon.style.sleeveTex = sleeveTex
                    self.toon.style.sleeveTexColor = sleeveColor
                # Only use the girl bottoms used in MakeAToon
                if (self.toon.style.botTex not in ToonDNA.MakeAToonGirlBottoms):
                    if (self.toon.style.torso[1] == 'd'):
                        botTex, botTexColor = ToonDNA.getRandomBottom(gender, ToonDNA.MAKE_A_TOON,
                                                                      girlBottomType = ToonDNA.SKIRT)
                        self.toon.style.botTex = botTex
                        self.toon.style.botTexColor = botTexColor
                        torsoOffset = 3
                    else:
                        botTex, botTexColor = ToonDNA.getRandomBottom(gender, ToonDNA.MAKE_A_TOON,
                                                                      girlBottomType = ToonDNA.SHORTS)
                        self.toon.style.botTex = botTex
                        self.toon.style.botTexColor = botTexColor
                        torsoOffset = 0
                
        assert(self.notify.debug('torsoChoice before: %d' % self.torsoChoice))
        self.torsoChoice = (self.torsoChoice + offset) % length
        assert(self.notify.debug('new torsoChoice: %d offset: %d length: %d torsoOffset: %d torsoStart: %d' % (self.torsoChoice, offset, length, torsoOffset, self.torsoStart)))
        # ghost the pickers if at the end of the 'wheel'
        self.__updateScrollButtons(self.torsoChoice, length, self.torsoStart,
                                   self.torsoLButton, self.torsoRButton)
        torso = ToonDNA.toonTorsoTypes[torsoOffset + self.torsoChoice]
        assert(self.notify.debug('torso start: %d new torso: %s old torso: %s botTex: %d' % (self.torsoStart, torso, self.dna.torso, self.toon.style.botTex)))
        self.dna.torso = torso
        self.toon.swapToonTorso(torso)
        self.toon.loop("neutral", 0)
        self.toon.swapToonColor(self.dna)
        
    def __swapLegs(self, offset):
        length = len(ToonDNA.toonLegTypes)
        self.legChoice = (self.legChoice + offset) % length
        # ghost the pickers if at the end of the 'wheel'
        self.notify.debug("self.legChoice=%d, length=%d, self.legStart=%d" % (self.legChoice, length, self.legStart))
        self.__updateScrollButtons(self.legChoice, length, self.legStart,
                                   self.legLButton, self.legRButton)
        newLeg = ToonDNA.toonLegTypes[self.legChoice]
        self.dna.legs = newLeg
        self.toon.swapToonLegs(newLeg)
        self.toon.loop("neutral", 0)
        self.toon.swapToonColor(self.dna)

    def __swapHead(self, offset):
        length = len(ToonDNA.toonHeadTypes)
        
        self.headChoice = (self.headChoice + offset) % length
        # ghost the pickers if at the end of the 'wheel'
        self.__updateScrollButtons(self.headChoice, length, self.headStart,
                                   self.headLButton, self.headRButton)
        newHead = ToonDNA.toonHeadTypes[self.headChoice]
        self.dna.head = newHead
        self.toon.swapToonHead(newHead)
        self.toon.loop("neutral", 0)
        self.toon.swapToonColor(self.dna)
        self.restrictHeadType(newHead)

    def __updateScrollButtons(self, choice, length, start, lButton, rButton):
        # ghost the pickers if at the end of the 'wheel'
        if choice == (start - 1) % length:
            rButton['state'] = DGG.DISABLED
        elif choice == (start - 2) % length:
            rButton['state'] = DGG.NORMAL
        if choice == start % length:
            lButton['state'] = DGG.DISABLED
        elif choice == (start + 1) % length:
            lButton['state'] = DGG.NORMAL

        #RAU guard code against both buttons getting disabled, unable to reproduce, but
        #screen shot shows it can happen,  bug 15281
        if (lButton['state']==DGG.DISABLED) and (rButton['state']==DGG.DISABLED):
            self.notify.info("Both buttons got disabled! Doing fallback code. choice%d, length=%d, start=%d, lButton=%s, rButton=%s" % (choice, length, start, lButton, rButton))
            if (choice == start % length):
                lButton['state']=DGG.DISABLED
                rButton['state']=DGG.NORMAL
            elif choice == (start-1) % length:
                lButton['state']=DGG.NORMAL
                rButton['state']=DGG.DISABLED
            else:
                lButton['state']=DGG.NORMAL
                rButton['state']=DGG.NORMAL
            
    def __handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def __handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)

    def restrictHeadType(self, head):
        # restrict free players from choose Monkey, Bear or Horse
        if not base.cr.isPaid():
            if head[0] in ('h', 'p', 'b'):
                # intercept the "next" button event
                self.accept("next", self.__restrictForward)
            else:
                # reset the "next" button event
                self.accept("next", self.__handleForward)
           
    def __restrictForward(self):
        TeaserPanel.TeaserPanel(pageName='species')
