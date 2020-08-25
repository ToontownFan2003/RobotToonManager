
# Indicies into show desciptors
FW_T = 0
FW_STYLE = 1
FW_COLOR1 = 2
FW_COLOR2 = 3
FW_AMP = 4
FW_POS_X = 5
FW_POS_Y = 6
FW_POS_Z = 7


# Firework styles
CIRCLE = 0
ROCKET = 1
RING = 2
CIRCLELARGE = 3
CIRCLESMALL = 4
POP = 5
CIRCLESPRITE = 6

# For the editor to print out a show
styleNames = ['CIRCLE',
              'ROCKET',
              'RING',
              'CIRCLELARGE',
              'CIRCLESMALL',
              'POP',
              'CIRCLESPRITE']

styleNamesShort = ['CIR',
                   'RKT',
                   'RNG',
                   'CLG',
                   'CSM',
                   'POP',
                   'SPR']

# Firework descriptions, for the gui labels
Names = ["Pow",
         "Rocket",
         "Ring",
         "Large\nPow",
         "Small\nPow",
         "Pop",
         "Widow\nMaker",
         ]
         
# Firework colors
WHITE = 0
RED = 1
BLUE = 2
YELLOW = 3
GREEN = 4
PINK = 5
PURPLE = 6
CYAN = 7
PEACH = 8

ColorNames = ['White',
              'Red',
              'Blue',
              'Yellow',
              'Green',
              'Pink',
              'Purple',
              'Cyan',
              'Peach']

# Firework sprite models (textures)
SNOWFLAKE = 0
MUSICNOTE = 1
FLOWER = 2
ICECREAM = 3
STARFISH = 4
ZZZ = 5

skyTransitionDuration = 2.0 # duration (in seconds) of sky color
                            # transition from light to dark or
                            # vice versa
preShowPauseDuration = 2.0 # duration of pause between sky
                           # darkening and when the actual show
                           # starts (in seconds)
postShowPauseDuration = 4.0 # duration of pause between when show
                            # ends and when sky returns to normal
                            # daylight color
preNormalMusicPauseDuration = 0.5 # wait this long (in seconds) 
                                  # after sky has returned to
                                  # normal to play the default
                                  # music 
