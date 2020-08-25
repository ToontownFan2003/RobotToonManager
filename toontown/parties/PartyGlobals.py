#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Aug 2008
#
# Purpose: Central repository for Toontown Party variables
#-------------------------------------------------------------------------------
from random import randint

from pandac.PandaModules import Vec3
from pandac.PandaModules import BitMask32
from pandac.PandaModules import Point3
from pandac.PandaModules import Point4

from direct.showbase import PythonUtil

from toontown.toonbase import TTLocalizer

### Limits for net messages
MaxSetInvites = 1000
MaxSetPartiesInvitedTo = 100
MaxSetHostedParties = 50

### Events Page
EventsPageGuestNameMaxWidth = 0.42
EventsPageHostNameMaxWidth = 0.37

### Party creation
PartyRefundPercentage = 0.95 # You get this times the total cost back as a refund
# in minutes, preferably equal to UberdogCheckPartyStartFrequency
# so if this was 5 and current server time was 8:02 am, choosing asap will give 8:05 am start time
PartyPlannerAsapMinuteRounding = 5
assert( 60 % PartyPlannerAsapMinuteRounding) == 0  # planner code assumes this is true
UberdogCheckPartyStartFrequency = 5.0 # In minutes, how often we check for parties that can start
UberdogPartiesSanityCheckFrequency = 60 # In minutes, how often we check for started but orphaned parties
JarLabelTextColor = (0.95, 0.95, 0.0, 1.0)
JarLabelMaxedTextColor = (1.0, 0.0, 0.0, 1.0)
TuftsOfGrass = 75
MaxToonsAtAParty = 20
DefaultPartyDuration = 0.5 # hours
#DefaultPartyDuration = 0.05 # hours # use this for testing
DelayBeforeAutoKick = 30.0 # seconds
MaxHostedPartiesPerToon = 1 # how many parties can he host in the future

PartyEditorGridBounds = ( (-0.11, 0.289), (0.55, -0.447) )
PartyEditorGridCenter = (
    PartyEditorGridBounds[0][0] + (PartyEditorGridBounds[1][0] - PartyEditorGridBounds[0][0])/2.0,
    PartyEditorGridBounds[1][1] + (PartyEditorGridBounds[0][1] - PartyEditorGridBounds[1][1])/2.0,
)
PartyEditorGridSize = (18, 15)
PartyEditorGridSquareSize = (
    (PartyEditorGridBounds[1][0] - PartyEditorGridBounds[0][0]) / float(PartyEditorGridSize[0]),
    (PartyEditorGridBounds[0][1] - PartyEditorGridBounds[1][1]) / float(PartyEditorGridSize[1]),
)
PartyEditorGridRotateThreshold = 0.08

TrashCanPosition = (-0.24, 0.0, -0.65)
TrashCanScale = 0.7
PartyEditorTrashBounds = ((-0.16, -0.38), (-0.05, -0.56))

InviteStatus = PythonUtil.Enum(
    (
        "NotRead",
        "ReadButNotReplied",
        "Accepted",
        "Rejected",
    ),
)

InviteTheme = PythonUtil.Enum(
    (
        "Birthday",
        "GenericMale",
        "GenericFemale",
    ),
)

PartyStatus = PythonUtil.Enum(
    (
        "Pending", # party's start time is still in the future
        "Cancelled", # user cancelled this party
        "Finished", # party started and then finished
        "CanStart", # party can start, time is good, go button hasn't been hit yet
        "Started", # Party has started
        "NeverStarted", # End time has passed, party was never started
    )
)

# TODO For all error codes add differentiation between
# the different ways validation and database errors can fail
AddPartyErrorCode = PythonUtil.Enum(
    (
        "AllOk",
        "ValidationError",
        "DatabaseError",
        "TooManyHostedParties",    
    ),
)

# used by both changePrivate and changePartyStatus
ChangePartyFieldErrorCode = PythonUtil.Enum(
    (
        "AllOk",
        "ValidationError",
        "DatabaseError"
    ),
)

ActivityTypes = PythonUtil.Enum(
    (
        "HostInitiated",
        "GuestInitiated",
        "Continuous",
    )
)

# Note : If this enum changes, TTLocalizer PartyActivityNameDict must change too
ActivityIds = PythonUtil.Enum(
    (
        "PartyJukebox",
        "PartyCannon",
        "PartyTrampoline",
        "PartyCatch",
        "PartyDance",
        "PartyTugOfWar",
        "PartyFireworks",
        "PartyClock",
    ),
)

# a list of activity ids which we are advertising but not letting people buy
UnreleasedActivityIds  = (
    ActivityIds.PartyCatch,
    ActivityIds.PartyTugOfWar,
    ActivityIds.PartyFireworks
    )

DecorationIds = PythonUtil.Enum(
    (
        "BalloonAnvil",
        "BalloonStage",
        "Bow",
        "Cake",
        "Castle",
        "GiftPile",
        "Horn",
        "MardiGras",
        "NoiseMakers",
        "Pinwheel",
    )
)

# a list of decor ids which we are advertising but not letting people buy
UnreleasedDecorationIds  = (
    DecorationIds.BalloonStage,
    DecorationIds.Bow,
    DecorationIds.MardiGras,
    DecorationIds.NoiseMakers,
    DecorationIds.Pinwheel
    )

GoToPartyStatus = PythonUtil.Enum(
    (
        "AllowedToGo",
        "PartyFull",
        "PrivateParty",
        "PartyOver",
        "PartyNotActive",
    ),
)

PlayGroundToPartyClockColors = {
    "the_burrrgh" : (53.0 / 255.0, 116.0 / 255.0, 148.0 / 255.0, 1.0),
    "daisys_garden" : (52.0 / 255.0, 153.0 / 255.0, 95.0 / 255.0, 1.0),
    "donalds_dock" : (60.0 / 255.0, 98.0 / 255.0, 142.0 / 255.0, 1.0),
    "donalds_dreamland" : (79.0 / 255.0, 92.0 / 255.0, 120.0 / 255.0, 1.0),
    "minnies_melody_land" : (128.0 / 255.0, 62.0 / 255.0, 142.0 / 255.0, 1.0),
    "toontown_central" : (77.0 / 255.0, 137.0 / 255.0, 52.0 / 255.0, 1.0),
}

# Multiply party grid units by this to get panda units
PartyGridUnitLength = [14.4, 14.6]
PartyGridHeadingConverter = 15.0 # mudulo divide by this before sending over the wire
                                 # multiply by this after receiving over the wire
                                 # to get it back into degrees
PartyGridToPandaOffset = (
    -PartyGridUnitLength[0]*PartyEditorGridSize[0]/2.0,
    -PartyGridUnitLength[1]*PartyEditorGridSize[1]/2.0,
)

MinimumPartyCost = 100

ActivityInformationDict = {
    # id : { cost, model, ... }
    ActivityIds.PartyJukebox : {
        "cost" : 100,
        "gridsize" : (1,1),
        "numberPerPurchase" : 1,
        "limitPerParty" : 1,
        "paidOnly" : False,
        "editorSquare" : "PartyJukebox_activity_1x1",
    },
    ActivityIds.PartyCannon : {
        "cost" : 50,
        "gridsize" : (1,1),
        "numberPerPurchase" : 5,
        "limitPerParty" : 5,
        "paidOnly" : False,
        "editorSquare" : "PartyCannon_activity_1x1",
    },
    ActivityIds.PartyTrampoline : {
        "cost" : 50,
        "gridsize" : (2,2),
        "numberPerPurchase" : 1,
        "limitPerParty" : 4,
        "paidOnly" : False,
        "editorSquare" : "PartyTrampoline_activity_2x2",
    },
    ActivityIds.PartyCatch : {
        "cost" : 300,
        "gridsize" : (5,5),
        "numberPerPurchase" : 1,
        "limitPerParty" : 1,
        "paidOnly" : True,
        "editorSquare" : "PartyCatch_activity_5x5",
    },
    ActivityIds.PartyDance : {
        "cost" : 500,
        "gridsize" : (3,3),
        "numberPerPurchase" : 1,
        "limitPerParty" : 1,
        "paidOnly" : True,
        "editorSquare" : "PartyDance_activity_3x3",
    },
    ActivityIds.PartyTugOfWar : {
        "cost" : 200,
        "gridsize" : (4,4),
        "numberPerPurchase" : 1,
        "limitPerParty" : 1,
        "paidOnly" : False,
        "editorSquare" : "PartyTufOfWar_activity_4x4",
    },
    ActivityIds.PartyFireworks : {
        "cost" : 200,
        "gridsize" : (4,2),
        "numberPerPurchase" : 1,
        "limitPerParty" : 1,
        "paidOnly" : False,
        "editorSquare" : "PartyFireworks_activity_2x4",
    },
    ActivityIds.PartyClock : {
        "cost" : MinimumPartyCost,
        "gridsize" : (1,1),
        "numberPerPurchase" : 1,
        "limitPerParty" : 1,
        "paidOnly" : False,
        "editorSquare" : "PartyClock_activity_1x1",
    },
}

DecorationInformationDict = {}
for id in DecorationIds:
    DecorationInformationDict[id] = {
        "cost" : 50,
        "gridsize" : (1,1),
        "numberPerPurchase" : 1,
        "limitPerParty" : 5,
        "paidOnly" : False,
    }


### Activities ###
DefaultRulesTimeout = 10.0
# why a join or exit request is denied
DenialReasons = PythonUtil.Enum(
    (
        "Default",
        "Full",
    ),
    start = 0,
)

### Party Fireworks
# this enum starts at 200 to prevent clashing with Holiday name constants in
# ToontownGlobals, as both are used in effects/FireworkShows as keys into the
# shows dictionary
FireworkShows = PythonUtil.Enum(
    (
        "NewYears",
    ),
    start=200,
)

FireworksGlobalXOffset = 160.0
FireworksGlobalYOffset = -20.0
FireworksPostLaunchDelay = 3.0 # wait this long after launching the rocket to
                               # start the show

FireworksStartedEvent = "PartyFireworksStarted"
FireworksFinishedEvent = "PartyFireworksFinished"

# In addition to the show's duration, wait this much longer before telling
# clients to go to the disabled state to ensure that client-side shows are done
FireworksTransitionToDisabledDelay = 3.0

### Party Tug of War
TugOfWarStartDelay = 8.0 # in seconds. wait this long to allow more players to
                         # join after we have gotten the minimum number of 
                         # players
TugOfWarReadyDuration = 1.5 # time between "ready" and "go" when starting a game
TugOfWarGoDuration = 0.75 # time between "go" and when you can start pulling
TugOfWarDuration = 40.0 # in seconds
TugOfWarMinimumPlayersPerTeam = 1
TugOfWarMaximumPlayersPerTeam = 4
TugOfWarStartGameTimeout = 8 # wait this many seconds after we get the minimum
                             # number of players before starting the game
TugOfWarTeams = PythonUtil.Enum(
    (
        "LeftTeam",
        "RightTeam",
    ),
    start=0,
)
TugOfWarNeitherTeam = 3 # special value indicating neither team
TugOfWarJoinCollisionEndPoints = [
    Point3( 6.0, 0.0, 0.0),
    Point3(-6.0, 0.0, 0.0),
]
TugOfWarJoinCollisionRadius = 1.75
TugOfWarJoinCollisionPositions = [
    Point3(-10.5,  0.25, 4.5), # left team
    Point3( 10.5, -0.25, 4.5), # right team
]
TugOfWarInitialToonPositionsXOffset = 8.0 # defines X position of toon nearest
                                          # the edge relative to the center of
                                          # the play area
TugOfWarToonPositionXSeparation = 2.0 # how far between toons of the same team
TugOfWarToonPositionZ = 2.55
TugOfWarTextWordScale = 0.135
TugOfWarTextCountdownScale = 4.0
TugOfWarCameraPos = Point3( 0.0, -33.0, 10.0 )
TugOfWarCameraInitialHpr = Point3( 0.0, -6.91123, 0.0 ) # HACK: this value is derived from the CameraLookAtHeightOffest. If you change that, update this
TugOfWarCameraLookAtHeightOffset = 6.0
TugOfWarPowerMeterSize = 17
TugOfWarPowerMeterRulesTarget = 8 # show power meter at this level while
                                  # explaining rules
TugOfWarDisabledArrowColor = Point4(1.0, 0.0, 0.0, 0.3)
TugOfWarEnabledArrowColor = Point4(1.0, 0.0, 0.0, 1.0)
TugOfWarHilightedArrowColor = Point4(1.0, 0.7, 0.0, 1.0)
# tells clients how fast to push keys, and how long to sustain that rate
# durations should add up to equal the game length (TugOfWarDuration above)
TugOfWarTargetRateList = [
    (8.0, 6), # duration, ideal speed (as number of alternating key presses in
    (5.0, 7), # the last second)
    (6.0, 8),
    (6.0, 10),
    (7.0, 11),
    (8.0, 12),
] 
TugOfWarKeyPressTimeToLive = 1.0 # key presses are considered valid towards the
                                 # rate for this long
TugOfWarKeyPressUpdateRate = 0.1 # delay between updates of the player's rate
                                 # of pressing the arrow keys
TugOfWarKeyPressReportRate = 0.2 # period of updates from clients to AI
TugOfWarMovementFactor = 0.03 # maps force difference to movement
TugOfWarSplashZOffset = 1.0
TugOfWarHeadings = [
    240.0, # heading for team 1
    120.0, # heading for team 2
]
TugOfWarConclusionDuration = 4.0
TugOfWarFallInWinReward = 15
TugOfWarFallInLossReward = 4
TugOfWarWinReward = 12
TugOfWarLossReward = 8
TugOfWarTieReward = 5
TugOfWarTieThreshold = 0.75 # if the teams moved this much or less from their
                            # start position, consider it a tie
        
### Party Trampoline
TrampolineDuration = 60.0 # kick you off the trampoline after this long 
TrampolineSignOffset = Point3(-6.0, -6.0, 0.0)
TrampolineLeverOffset = Point3(-5.0, -9.0, 0.0)
TrampolineNumJellyBeans = 12
TrampolineJellyBeanBonus = 10

### Party Catch

# this is the duration of the tag game music...
CatchActivityDuration = 55.0 # TODO-Shawn : Changing this does not end dropping
CatchActivityBitmask = BitMask32(0x10)
CatchLeverOffset = Point3(-3.0, -2.0, 0.0) # offset from sign's position
CatchDropShadowHeight = 0.5
CatchConclusionDuration = 3.0
# this class is purely for syntactic convenience;
# with it, we can reference properties of drop object types by name
# 'name' == name of the drop object
# 'good' == is this a good thing to catch
# onscreenDurMult is how many times longer the object should take to fall,
#   once on-screen, than baseline objects (durationMult==1.)
#   For instance, an object type with an onscreenDurMult of .5 will be
#   on-screen half as long as a baseline object.
class DropObject:
    def __init__(self, name, good, onscreenDurMult, modelPath):
        self.name = name
        self.good = good
        self.onscreenDurMult = onscreenDurMult
        self.modelPath = modelPath

    def isBaseline(self):
        return (self.onscreenDurMult == 1.)

# definitions of drop types, in arbitrary order
DropObjectTypes = [
    # order is not important
    DropObject('apple',      1, 1., 'phase_4/models/minigames/apple'),
    DropObject('orange',     1, 1., 'phase_4/models/minigames/orange'),
    DropObject('pear',       1, 1., 'phase_4/models/minigames/pear'),
    DropObject('coconut',    1, 1., 'phase_4/models/minigames/coconut'),
    DropObject('watermelon', 1, 1., 'phase_4/models/minigames/watermelon'),
    DropObject('pineapple',  1, 1., 'phase_4/models/minigames/pineapple'),
    DropObject('anvil',      0, .4, 'phase_4/models/props/anvil-mod'),
]

# index into Name2DropObjectType by object name, then access named properties
# (see class DropObject above for property names)
Name2DropObjectType = {}
for type in DropObjectTypes:
    Name2DropObjectType[type.name] = type

# for transmitting drop-object types over the network, it's more efficient
# to be sending a number (DOTypeId) than a string.
#
# Name2DOTypeId and DOTypeId2Name map between name strings
# and typeIds:
#   Name2DOTypeId['apple'] == some number
#   DOTypeId2Name[some number] == 'apple'
Name2DOTypeId = {}
names = Name2DropObjectType.keys()
names.sort()
for i in range(len(names)):
    Name2DOTypeId[names[i]] = i
# our sorted list of names just happens to be the typeId->name table
DOTypeId2Name = names

"""
import CatchActivityGlobals
for np in range(4):
    for sz in (2000,1000,5000,4000,3000,9000):
        numFruits = CatchActivityGlobals.NumFruits[np][sz]
        jb = int(int(numFruits / 2) + round(numFruits / 4.))
        print '%s: %s: %s' % (np, sz, jb)
"""
# this is for the AI, so it doesn't have to do calculations, and so the
# client code can calculate these values in a straightforward manner.
# index by numToons-1, then safezone ID
# THIS TABLE WAS GENERATED BY DistributedCatchActivity.py; DO NOT EDIT
NumFruits = [
    # 1 player
    {2000:18,1000:19,5000:22,4000:24,3000:27,9000:28,},
    # 2 players
    {2000:30,1000:33,5000:38,4000:42,3000:46,9000:50,},
    # 3 players
    {2000:42,1000:48,5000:54,4000:60,3000:66,9000:71,},
    # 4 players
    {2000:56,1000:63,5000:70,4000:78,3000:85,9000:92,},
    ]


#===============================================================================
# Dance Activity
#===============================================================================

# TODO make DistributedDanceFloorBase to support 8, 16 and 24 move Dance floors 

# rule first 3 letters must be unique
# Dance Patterns to Animations
DancePatternToAnims = {
#    "ddd" : "down",
    "dduu" : "slip-backward",
#    "drul" : "sad-walk",
#    "ldr" : "push",    
    "ldddud" : "happy-dance",
#    "ldu" : "sprinkle-dust",    
    "lll" : "left",
#    "llrr" : "firehose",    
#    "lrlr" : "wave",    
#    "ludr" : "conked",
#    "lurd" : "walk",    
#    "rdl" : "shrug",
    "rdu" : "struggle",    
#    "rlrl" : "confused",    
    "rrr" : "right",
    "rulu" : "running-jump",    
#    "uddd" : "reel-neutral",
    "udlr" : "good-putt",    
#    "udud" : "angry",
    "udllrr" : "victory",
    "ulu" : "jump",
    "uudd" : "slip-forward",    
#    "uuu" : "up",
    }

# Dance animation to the names displayed
DanceAnimToName = {
    "right" : TTLocalizer.DanceAnimRight,
    "reel-neutral" : TTLocalizer.DanceAnimReelNeutral,
    "conked" : TTLocalizer.DanceAnimConked,
    "happy-dance" : TTLocalizer.DanceAnimHappyDance,
    "confused" : TTLocalizer.DanceAnimConfused,
    "walk" : TTLocalizer.DanceAnimWalk,
    "jump" : TTLocalizer.DanceAnimJump,
    "firehose" : TTLocalizer.DanceAnimFirehose,
    "shrug" : TTLocalizer.DanceAnimShrug,
    "slip-forward" : TTLocalizer.DanceAnimSlipForward,
    "sad-walk" : TTLocalizer.DanceAnimSadWalk,
    "wave" : TTLocalizer.DanceAnimWave,
    "struggle" : TTLocalizer.DanceAnimStruggle,
    "running-jump" : TTLocalizer.DanceAnimRunningJump,
    "slip-backward" : TTLocalizer.DanceAnimSlipBackward,
    "down" : TTLocalizer.DanceAnimDown,
    "up" : TTLocalizer.DanceAnimUp,
    "good-putt" : TTLocalizer.DanceAnimGoodPutt,
    "victory" : TTLocalizer.DanceAnimVictory,
    "push" : TTLocalizer.DanceAnimPush,
    "angry" : TTLocalizer.DanceAnimAngry,
    "left" : TTLocalizer.DanceAnimLeft,
}

# Which animations need to reverse loop (loop is play forwards then on reverse)
DanceReverseLoopAnims = ["left", "right", "up", "down", "good-putt"]

# Used to transfer state data between clietns
ToonDancingStates = PythonUtil.Enum(
    (
        "Init",
        "DanceMove",
        "Run",
        "Cleanup",
    ),
)

#===============================================================================
# ("And be a") Jukebox ("hero, stars in his eyes")
#===============================================================================

JUKEBOX_TIMEOUT = 30.0 # seconds

# Used to get the path of the music file when playing a song
MUSIC_PATH = "phase_%s/audio/bgm/"

# Used to determine how many times a song should loop:
# times = round(music_min_lenght_seconds / length)
MUSIC_MIN_LENGTH_SECONDS = 50.0
# Seconds to wait between tunes
MUSIC_GAP = 2.5

# TODO handle 20, 50, 80, etc song jukeboxes

# { phase : { "filename": ["name", seconds], ...}, ... }
PhaseToMusicData = {
    3.5 : {
        #"encntr_general_bg.mid" : [TTLocalizer.MusicEncntrGeneralBg, 30],
        #"TC_SZ_activity.mid" : [TTLocalizer.MusicTcSzActivity, 53],
        "TC_SZ.mid" : [TTLocalizer.MusicTcSz, 57],
    },
    3 : {
        "create_a_toon.mid" : [TTLocalizer.MusicCreateAToon, 175],
        "tt_theme.mid" : [TTLocalizer.MusicTtTheme, 51],
    },
    4 : {
        # "minigame_race.mid" : [TTLocalizer.MusicMinigameRace, 77],
        # "MG_Pairing.mid" : [TTLocalizer.MusicMgPairing, 60],
        "TC_nbrhood.mid" : [TTLocalizer.MusicTcNbrhood, 59],
        # "MG_Diving.mid" : [TTLocalizer.MusicMgDiving, 30],
        # "MG_cannon_game.mid" : [TTLocalizer.MusicMgCannonGame, 29],
        "MG_TwoDGame.mid" : [TTLocalizer.MusicMgTwodgame, 60],
        # "MG_CogThief.mid" : [TTLocalizer.MusicMgCogthief, 61],
        # "MG_Travel.mid" : [TTLocalizer.MusicMgTravel, 31],
        # "MG_tug_o_war.mid" : [TTLocalizer.MusicMgTugOWar, 29],
        "MG_Vine.mid" : [TTLocalizer.MusicMgVine, 32],
        # "MG_IceGame.mid" : [TTLocalizer.MusicMgIcegame, 56],
        # "MG_toontag.mid" : [TTLocalizer.MusicMgToontag, 57],
        # "m_match_bg2.mid" : [TTLocalizer.MusicMMatchBg2, 9],
        # "MG_Target.mid" : [TTLocalizer.MusicMgTarget, 30],
        "FF_safezone.mid" : [TTLocalizer.MusicFfSafezone, 47],
    },
    6 : {
        "DD_SZ.mid" : [TTLocalizer.MusicDdSz, 33],
        #"MM_nbrhood.mid" : [TTLocalizer.MusicMmNbrhood, 55],
        #"GZ_PlayGolf.mid" : [TTLocalizer.MusicGzPlaygolf, 61],
        "GS_SZ.mid" : [TTLocalizer.MusicGsSz, 60],
        "OZ_SZ.mid" : [TTLocalizer.MusicOzSz, 31],
        #"GS_Race_CC.mid" : [TTLocalizer.MusicGsRaceCc, 58],
        #"GS_Race_SS.mid" : [TTLocalizer.MusicGsRaceSs, 61],
        #"GS_Race_RR.mid" : [TTLocalizer.MusicGsRaceRr, 60],
        "GZ_SZ.mid" : [TTLocalizer.MusicGzSz, 59],
        "MM_SZ.mid" : [TTLocalizer.MusicMmSz, 76],
        #"MM_SZ_activity.mid" : [TTLocalizer.MusicMmSzActivity, 40],
        #"DD_nbrhood.mid" : [TTLocalizer.MusicDdNbrhood, 67],
        #"GS_KartShop.mid" : [TTLocalizer.MusicGsKartshop, 32],
        #"DD_SZ_activity.mid" : [TTLocalizer.MusicDdSzActivity, 62],
    },
    7 : {
        #"encntr_general_bg_indoor.mid" : [TTLocalizer.MusicEncntrGeneralBgIndoor, 31],
        #"tt_elevator.mid" : [TTLocalizer.MusicTtElevator, 12],
        #"encntr_toon_winning_indoor.mid" : [TTLocalizer.MusicEncntrToonWinningIndoor, 32],
        #"encntr_general_suit_winning_indoor.mid" : [TTLocalizer.MusicEncntrGeneralSuitWinningIndoor, 36],
    },
    8 : {
        #"TB_nbrhood.mid" : [TTLocalizer.MusicTbNbrhood, 51],
        #"DL_nbrhood.mid" : [TTLocalizer.MusicDlNbrhood, 30],
        #"DL_SZ_activity.mid" : [TTLocalizer.MusicDlSzActivity, 32],
        "DG_SZ.mid" : [TTLocalizer.MusicDgSz, 48],
        "DL_SZ.mid" : [TTLocalizer.MusicDlSz, 33],
        #"TB_SZ_activity.mid" : [TTLocalizer.MusicTbSzActivity, 48],
        "TB_SZ.mid" : [TTLocalizer.MusicTbSz, 54],
        #"DG_nbrhood.mid" : [TTLocalizer.MusicDgNbrhood, 55],
    },
    9 : {
        "encntr_hall_of_fame.mid" : [TTLocalizer.MusicEncntrHallOfFame, 51],
        #"encntr_suit_HQ_nbrhood.mid" : [TTLocalizer.MusicEncntrSuitHqNbrhood, 42],
        #"CHQ_FACT_bg.mid" : [TTLocalizer.MusicChqFactBg, 50],
        "CogHQ_finale.mid" : [TTLocalizer.MusicCoghqFinale, 64],
        #"encntr_toon_winning.mid" : [TTLocalizer.MusicEncntrToonWinning, 30],
        #"encntr_suit_winning.mid" : [TTLocalizer.MusicEncntrSuitWinning, 31],
        #"encntr_head_suit_theme.mid" : [TTLocalizer.MusicEncntrHeadSuitTheme, 29],
    },
    11 : {
        "LB_juryBG.mid" : [TTLocalizer.MusicLbJurybg, 30],
        #"LB_courtyard.mid" : [TTLocalizer.MusicLbCourtyard, 32],
    },
    12 : {
        #"Bossbot_CEO_v2.mid" : [TTLocalizer.MusicBossbotCeoV2, 31],
        #"Bossbot_Factory_v1.mid" : [TTLocalizer.MusicBossbotFactoryV1, 30],
        #"Bossbot_CEO_v1.mid" : [TTLocalizer.MusicBossbotCeoV1, 31],
    },
    13 : {
        "party_original_theme.mid" : [TTLocalizer.MusicPartyOriginalTheme, 56],
        #"party_polka_dance.mid" : [TTLocalizer.MusicPartyPolkaDance, 63],
        #"party_swing_dance.mid" : [TTLocalizer.MusicPartySwingDance, 62],
        #"party_waltz_dance.mid" : [TTLocalizer.MusicPartyWaltzDance, 63],
        "party_generic_theme_jazzy.mid" : [TTLocalizer.MusicPartyGenericThemeJazzy, 64],
        #"party_generic_theme.mid" : [TTLocalizer.MusicPartyGenericTheme, 65],
    },
}


# helper functions for globals:

def getRandomMusicInfo(phase=13):
    if phase == -1:
        # Get random phase
        keys = PhaseToMusicData.keys()
        phase = keys[randint(0, len(keys) - 1)]
    
    # From that phase, get random filename
    values = PhaseToMusicData[phase].keys()
    filename = values[randint(0, len(values) - 1)]
    
    return (phase, filename)

def getMusicRepeatTimes(length, minLength=MUSIC_MIN_LENGTH_SECONDS):
    times = round(float(minLength) / length) 
    if minLength <= 0 or times < 1.0:
        times = 1.0
    return times

def sanitizePhase(phase):
    if phase == int(phase):
        phase = int(phase)
    return phase

def getMusicData(phase, filename):
    data = []
    phase = sanitizePhase(phase)
    phase = PhaseToMusicData.get(phase)
    if phase:
        data = phase.get(filename, [])
    return data

#===============================================================================
# Cannons
#===============================================================================

CANNON_TIMEOUT = 30
CANNON_MOVIE_LOAD = 1
CANNON_MOVIE_CLEAR = 2
CANNON_MOVIE_FORCE_EXIT = 3
CANNON_MOVIE_LANDED = 4

CannonJellyBeanReward = 2
CannonMaxTotalReward = 100 # from 1 shot, whats the maximum beans they'll ever get, no matter how many clouds hit

PartyCannonCollisions = {
    "clouds" : ["cloudSphere-0"],
    
    "bounce" : [
        "wall_collision",
        "discoBall_collision",
        "platform_left_collision",
        "platform_right_collision",
        ],
        
    "trampoline_bounce" : "TrampolineCollision",
    
    "ground" : [
        "floor_collision",
        "danceFloor_collision",
        "danceFloorRamp_collision",
        "hill_collision",
        "fence_floor",
        ],
        
    "fence" : [
        "dockTube1_collision",
        "dockTube2_collision",
        "dockTube2_collision",
        "dockTube2_collision",
        "palm_collision_01",
        "palm_collision_02",
        "palm_collision_03",
        "wall_1_collision",
        "wall_2_collision",
        "wall_3_collision",
        "wall_4_collision",
        "wall_5_collision",
        "wall_6_collision",
        "tree_collision",
        "partyDecoration_collision",
        "launchPad_railing_collision",
        "launchPad_floor_collision",
        "launchPad_collision",
        "launchPad_railing2_collision",
        "launchPad__rocket_collision",
        "launchPad_lever_collision",
        "launchPad_bridge_collision",
        "launchPad_sphere2_collision",
        "launchPad_sphere1_collision",
        "partyClock_collision",
        "sign_collision"
        ],
}
