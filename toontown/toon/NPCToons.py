
from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
import random
from toontown.hood import ZoneUtil
import ToonDNA
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownBattleGlobals

# These are the various modes for DistributedNPC setMovie
QUEST_MOVIE_CLEAR = 0
QUEST_MOVIE_REJECT = 1
QUEST_MOVIE_COMPLETE = 2
QUEST_MOVIE_INCOMPLETE = 3
QUEST_MOVIE_ASSIGN = 4
QUEST_MOVIE_BUSY = 5
QUEST_MOVIE_QUEST_CHOICE = 6
QUEST_MOVIE_QUEST_CHOICE_CANCEL = 7
QUEST_MOVIE_TRACK_CHOICE = 8
QUEST_MOVIE_TRACK_CHOICE_CANCEL = 9
QUEST_MOVIE_TIMEOUT = 10
QUEST_MOVIE_TIER_NOT_DONE = 11

PURCHASE_MOVIE_CLEAR = 0
PURCHASE_MOVIE_START = 1
PURCHASE_MOVIE_START_BROWSE = 9
PURCHASE_MOVIE_COMPLETE = 2
PURCHASE_MOVIE_NO_MONEY = 3
PURCHASE_MOVIE_TIMEOUT = 8
PURCHASE_MOVIE_START_NOROOM = 10

SELL_MOVIE_CLEAR = 0
SELL_MOVIE_START = 1
SELL_MOVIE_COMPLETE = 2
SELL_MOVIE_NOFISH = 3
SELL_MOVIE_TROPHY = 4
SELL_MOVIE_TIMEOUT = 8
SELL_MOVIE_PETRETURNED = 9     #these have to live nicely with the fish clerk ones
SELL_MOVIE_PETADOPTED = 10
SELL_MOVIE_PETCANCELED = 11

# The following are used by DistributedPartyPerson/AI
PARTY_MOVIE_CLEAR = 0
PARTY_MOVIE_START = 1
PARTY_MOVIE_COMPLETE = 2
PARTY_MOVIE_ALREADYHOSTING = 3
PARTY_MOVIE_MAYBENEXTTIME = 4
PARTY_MOVIE_ONLYPAID = 5
PARTY_MOVIE_COMINGSOON = 6
PARTY_MOVIE_MINCOST = 7
PARTY_MOVIE_TIMEOUT = 8

BLOCKER_MOVIE_CLEAR = 0
BLOCKER_MOVIE_START = 1
BLOCKER_MOVIE_TIMEOUT = 8

NPC_REGULAR = 0
NPC_CLERK = 1
NPC_TAILOR = 2
NPC_HQ = 3
NPC_BLOCKER = 4
NPC_FISHERMAN = 5
NPC_PETCLERK = 6
NPC_KARTCLERK = 7
NPC_PARTYPERSON = 8

CLERK_COUNTDOWN_TIME = 120
TAILOR_COUNTDOWN_TIME = 300

def getRandomDNA(seed, gender):
    randomDNA = ToonDNA.ToonDNA()
    randomDNA.newToonRandom(seed, gender, 1)
    return randomDNA.asTuple()

def createNPC(air, npcId, desc, zoneId, posIndex=0, questCallback=None):
    import DistributedNPCToonAI
    import DistributedNPCClerkAI
    import DistributedNPCTailorAI
    import DistributedNPCBlockerAI
    import DistributedNPCFishermanAI
    import DistributedNPCPetclerkAI
    import DistributedNPCKartClerkAI
    import DistributedNPCPartyPersonAI
    canonicalZoneId, name, dnaType, gender, protected, type = desc
    if (type == NPC_REGULAR):
        npc = DistributedNPCToonAI.DistributedNPCToonAI(
                air, npcId,
                questCallback=questCallback)
    elif (type == NPC_HQ):
        npc = DistributedNPCToonAI.DistributedNPCToonAI(
                air, npcId,
                questCallback=questCallback, hq=1)
    elif (type == NPC_CLERK):
        npc = DistributedNPCClerkAI.DistributedNPCClerkAI(air, npcId)
    elif (type == NPC_TAILOR):
        npc = DistributedNPCTailorAI.DistributedNPCTailorAI(air, npcId)
    elif (type == NPC_BLOCKER):
        npc = DistributedNPCBlockerAI.DistributedNPCBlockerAI(air, npcId)
    elif (type == NPC_FISHERMAN):
        npc = DistributedNPCFishermanAI.DistributedNPCFishermanAI(air, npcId)
    elif (type == NPC_PETCLERK):
        npc = DistributedNPCPetclerkAI.DistributedNPCPetclerkAI(air, npcId)
    elif (type == NPC_KARTCLERK):
        npc = DistributedNPCKartClerkAI.DistributedNPCKartClerkAI(air, npcId) 
    elif (type == NPC_PARTYPERSON):
        npc = DistributedNPCPartyPersonAI.DistributedNPCPartyPersonAI(air, npcId) 
    else:
        print 'createNPC() error!!!'
    npc.setName(name)
    dna = ToonDNA.ToonDNA()
    if dnaType == "r":
        # ...random dna.
        dnaList = getRandomDNA(npcId, gender)
    else:
        dnaList = dnaType
    dna.newToonFromProperties(*dnaList)
    npc.setDNAString(dna.makeNetString())
    npc.setHp(15)
    npc.setMaxHp(15)
    # NOTE: The npc will be placed on the client when it is created
    npc.setPositionIndex(posIndex)
    npc.generateWithRequired(zoneId)

    npc.d_setAnimState("neutral", 1.)
    return npc

def createNpcsInZone(air, zoneId):
    npcs = []
    canonicalZoneId = ZoneUtil.getCanonicalZoneId(zoneId)
    npcIdList = zone2NpcDict.get(canonicalZoneId, [])
    for i in range(len(npcIdList)):
        npcId = npcIdList[i]
        npcDesc = NPCToonDict.get(npcId)
        assert npcDesc
        npcs.append(createNPC(air, npcId, npcDesc, zoneId, posIndex=i))
    return npcs

def createLocalNPC(npcId):
    import Toon
    if (not NPCToonDict.has_key(npcId)):
        return None
    desc = NPCToonDict[npcId]
    canonicalZoneId, name, dnaType, gender, protected, type = desc
    npc = Toon.Toon()
    npc.setName(name)
    # You cannot click on the nametags of npc sos toons
    npc.setPickable(0)
    npc.setPlayerType(NametagGroup.CCNonPlayer)
    dna = ToonDNA.ToonDNA()
    if dnaType == "r":
        # ...random dna.
        dnaList = getRandomDNA(npcId, gender)
    else:
        dnaList = dnaType
    dna.newToonFromProperties(*dnaList)
    npc.setDNAString(dna.makeNetString())

    npc.animFSM.request("neutral")
    return npc

def isZoneProtected(zoneId):
    """
    isZoneProtected(zoneId)

    Returns true if the building with the indicated interior zone ID
    is marked as a protected building: the NPC toon(s) standing within
    it won't be conquered by a wandering suit.

    The building may still be taken over with a magic word, but a suit
    will be too afraid to take over a protected building automatically.
    """

    # The building is protected if any NPC toon standing within it is
    # marked protected.  This is just the most natural place for us to
    # indicate 'protected' status from a designer's point of view,
    # although the code has to go through some hoops to get to it.

    npcs = []
    npcIdList = zone2NpcDict.get(zoneId, [])
    for npcId in npcIdList:
        npcDesc = NPCToonDict.get(npcId)
        assert npcDesc
        if npcDesc[4]:
            return 1

    return 0


# Since the names are localized, we cannot simply type them in here. Instead we will
# read them out of the localizer.
# Just to make the NPCToonDict a little smaller and easier to read, lets store a local
# variable on the NPCToonNames dict. lnames is short for localized names.
lnames = TTLocalizer.NPCToonNames

NPCToonDict = {
    # (INTERIOR zoneId, "name", "r"|<dna>, "m"|"f", protected, type),
    # if protected is 1, the building will not be taken over automatically.
    # DNA is  (head, torso, legs, armColor, gloveColor, legColor, headColor,
    #          topTexture, bottomTexture)
    # These are for the tutorial. We do not actually use the zoneId here
    # But the quest posters need to know his name
    20000 : (-1, lnames[20000], "r", "m", 1, NPC_REGULAR),
    999 : (-1, lnames[999], "r", "m", 1, NPC_TAILOR),
    1000 : (-1, lnames[1000], "r", "m", 1, NPC_HQ),
    # Flippy DNA matches marketing materials
    20001 : (-1, lnames[20001], ('dss', 'ms', 'm', 'm', 17,0,17,17,3,3,3,3,7,2), "m", 1, NPC_BLOCKER),
    
    # Toontown Central
    # This Flippy DNA matches the tutorial Flippy
    # He is in Toon Hall
    # Flippy DNA matches marketing materials
    2001 : (2513, lnames[2001], ('dss', 'ms', 'm', 'm', 17,0,17,17,3,3,3,3,7,2), "m", 1, NPC_REGULAR),
    2002 : (2514, lnames[2002], "r", "m", 1, NPC_REGULAR),
    2003 : (2516, lnames[2003], "r", "m", 1, NPC_REGULAR),
    2004 : (2521, lnames[2004], ('rll', 'md', 'm', "f", 15,0,5,7,3,5,3,5,0,3), "f", 1, NPC_TAILOR),
    2005 : (2518, lnames[2005], "r", "m", 1, NPC_REGULAR),
    2006 : (2519, lnames[2006], "r", "m", 1, NPC_CLERK),
    2011 : (2519, lnames[2011], "r", "f", 1, NPC_CLERK),
    2007 : (2520, lnames[2007], "r", "m", 1, NPC_HQ),
    2008 : (2520, lnames[2008], "r", "m", 1, NPC_HQ),
    2009 : (2520, lnames[2009], "r", "f", 1, NPC_HQ),
    2010 : (2520, lnames[2010], "r", "f", 1, NPC_HQ),
    2012 : (2000, lnames[2012], "r", "m", 1, NPC_FISHERMAN),
    2013 : (2522, lnames[2013], "r", "m", 1, NPC_PETCLERK),
    2014 : (2522, lnames[2014], "r", "f", 1, NPC_PETCLERK),
    2015 : (2522, lnames[2015], "r", "m", 1, NPC_PETCLERK),
    2016 : (2000, lnames[2016], ("sls", "ls", "m", "m", 10, 0, 9, 9, 0, 3, 0, 3, 0, 18), "m", 1, NPC_PARTYPERSON),
    2017 : (2000, lnames[2017], ("sss", "ld", "m", "f", 10, 0, 9, 9, 0, 23, 0, 23, 0, 5), "f", 1, NPC_PARTYPERSON),

    2101 : (2601, lnames[2101], "r", "m", 0, NPC_REGULAR),
    2102 : (2619, lnames[2102], "r", "f", 0, NPC_REGULAR),
    2103 : (2616, lnames[2103], ("csl", "ss", "s", 'm', 9,0,8,5,0,11,0,11,2,10), "m", 0, NPC_REGULAR), # Tribute
    2104 : (2671, lnames[2104], "r", "m", 1, NPC_HQ),
    2105 : (2671, lnames[2105], "r", "m", 1, NPC_HQ),
    2106 : (2671, lnames[2106], "r", "f", 1, NPC_HQ),
    2107 : (2671, lnames[2107], "r", "f", 1, NPC_HQ),
    2108 : (2603, lnames[2108], "r", "f", 0, NPC_REGULAR),
    2109 : (2604, lnames[2109], "r", "m", 0, NPC_REGULAR),
    2110 : (2605, lnames[2110], "r", "m", 0, NPC_REGULAR),
    2111 : (2607, lnames[2111], "r", "m", 0, NPC_REGULAR),
    2112 : (2610, lnames[2112], "r", "m", 1, NPC_REGULAR),
    2113 : (2617, lnames[2113], "r", "m", 0, NPC_REGULAR),
    2114 : (2618, lnames[2114], "r", "f", 0, NPC_REGULAR),
    2115 : (2621, lnames[2115], "r", "f", 0, NPC_REGULAR),
    2116 : (2624, lnames[2116], "r", "m", 0, NPC_REGULAR),
    2117 : (2625, lnames[2117], "r", "f", 0, NPC_REGULAR),
    2118 : (2626, lnames[2118], "r", "m", 0, NPC_REGULAR),
    2119 : (2629, lnames[2119], "r", "f", 1, NPC_REGULAR),
    2120 : (2632, lnames[2120], "r", "m", 0, NPC_REGULAR),
    2121 : (2633, lnames[2121], "r", "f", 0, NPC_REGULAR),
    2122 : (2639, lnames[2122], "r", "m", 0, NPC_REGULAR),
    2123 : (2643, lnames[2123], "r", "f", 0, NPC_REGULAR),
    2124 : (2644, lnames[2124], "r", "f", 0, NPC_REGULAR),
    2125 : (2649, lnames[2125], "r", "m", 0, NPC_REGULAR),
    2126 : (2654, lnames[2126], "r", "f", 1, NPC_REGULAR),
    2127 : (2655, lnames[2127], "r", "m", 1, NPC_REGULAR),
    2128 : (2656, lnames[2128], "r", "m", 1, NPC_REGULAR),
    2129 : (2657, lnames[2129], "r", "m", 0, NPC_REGULAR),
    2130 : (2659, lnames[2130], "r", "f", 0, NPC_REGULAR),
    2131 : (2660, lnames[2131], "r", "f", 1, NPC_REGULAR),
    2132 : (2661, lnames[2132], "r", "m", 0, NPC_REGULAR),
    2133 : (2662, lnames[2133], "r", "m", 0, NPC_REGULAR),
    2134 : (2664, lnames[2134], "r", "f", 0, NPC_REGULAR),
    2135 : (2665, lnames[2135], "r", "f", 1, NPC_REGULAR),
    2136 : (2666, lnames[2136], "r", "m", 0, NPC_REGULAR),
    2137 : (2667, lnames[2137], "r", "f", 0, NPC_REGULAR),
    2138 : (2669, lnames[2138], "r", "m", 0, NPC_REGULAR),
    2139 : (2670, lnames[2139], "r", "m", 0, NPC_REGULAR),
    2140 : (2156, lnames[2140], "r", "m", 0, NPC_FISHERMAN),

    2201 : (2711, lnames[2201], "r", "m", 1, NPC_REGULAR),
    2202 : (2718, lnames[2202], "r", "f", 1, NPC_REGULAR),
    2203 : (2742, lnames[2203], "r", "m", 1, NPC_HQ),
    2204 : (2742, lnames[2204], "r", "m", 1, NPC_HQ),
    2205 : (2742, lnames[2205], "r", "f", 1, NPC_HQ),
    2206 : (2742, lnames[2206], "r", "f", 1, NPC_HQ),
    2207 : (2705, lnames[2207], "r", "m", 1, NPC_REGULAR),
    2208 : (2708, lnames[2208], "r", "m", 1, NPC_REGULAR),
    2209 : (2712, lnames[2209], "r", "m", 1, NPC_REGULAR),
    2210 : (2713, lnames[2210], "r", "f", 1, NPC_REGULAR),
    2211 : (2716, lnames[2211], "r", "f", 1, NPC_REGULAR),
    2212 : (2717, lnames[2212], "r", "m", 0, NPC_REGULAR),
    2213 : (2720, lnames[2213], "r", "f", 1, NPC_REGULAR),
    2214 : (2723, lnames[2214], "r", "m", 0, NPC_REGULAR),
    2215 : (2727, lnames[2215], "r", "m", 0, NPC_REGULAR),
    2216 : (2728, lnames[2216], "r", "f", 0, NPC_REGULAR),
    2217 : (2729, lnames[2217], "r", "m", 1, NPC_REGULAR),
    2218 : (2730, lnames[2218], "r", "f", 0, NPC_REGULAR),
    2219 : (2732, lnames[2219], "r", "m", 0, NPC_REGULAR),
    2220 : (2733, lnames[2220], "r", "m", 0, NPC_REGULAR),
    2221 : (2734, lnames[2221], "r", "f", 0, NPC_REGULAR),
    2222 : (2735, lnames[2222], "r", "m", 0, NPC_REGULAR),
    2223 : (2739, lnames[2223], "r", "f", 0, NPC_REGULAR),
    2224 : (2740, lnames[2224], "r", "m", 0, NPC_REGULAR),
    2225 : (2236, lnames[2225], "r", "m", 0, NPC_FISHERMAN),

    2301 : (2804, lnames[2301], "r", "m", 1, NPC_REGULAR),
    2302 : (2831, lnames[2302], "r", "m", 1, NPC_REGULAR),
    2303 : (2834, lnames[2303], "r", "f", 0, NPC_REGULAR),
    2304 : (2832, lnames[2304], "r", "m", 1, NPC_HQ),
    2305 : (2832, lnames[2305], "r", "m", 1, NPC_HQ),
    2306 : (2832, lnames[2306], "r", "f", 1, NPC_HQ),
    2307 : (2832, lnames[2307], "r", "f", 1, NPC_HQ),
    2308 : (2801, lnames[2308], "r", "f", 0, NPC_REGULAR),
    2309 : (2802, lnames[2309], "r", "m", 0, NPC_REGULAR),
    2311 : (2809, lnames[2311], "r", "m", 1, NPC_REGULAR),
    2312 : (2837, lnames[2312], "r", "f", 0, NPC_REGULAR),
    2313 : (2817, lnames[2313], "r", "f", 0, NPC_REGULAR),
    2314 : (2818, lnames[2314], "r", "m", 0, NPC_REGULAR),
    2315 : (2822, lnames[2315], "r", "m", 0, NPC_REGULAR),
    2316 : (2823, lnames[2316], "r", "f", 0, NPC_REGULAR),
    2318 : (2829, lnames[2318], "r", "m", 0, NPC_REGULAR),
    2319 : (2830, lnames[2319], "r", "m", 0, NPC_REGULAR),
    2320 : (2839, lnames[2320], "r", "m", 0, NPC_REGULAR),
    2321 : (2341, lnames[2321], "r", "m", 0, NPC_FISHERMAN),

    # Donald's Dock
    1001 : (1506, lnames[1001], "r", "m", 0, NPC_CLERK),
    1002 : (1506, lnames[1002], "r", "m", 0, NPC_CLERK),
    1003 : (1507, lnames[1003], "r", "m", 0, NPC_HQ),
    1004 : (1507, lnames[1004], "r", "f", 0, NPC_HQ),
    1005 : (1507, lnames[1005], "r", "m", 0, NPC_HQ),
    1006 : (1507, lnames[1006], "r", "f", 0, NPC_HQ),
    1007 : (1508, lnames[1007], "r", "m", 0, NPC_TAILOR),
    1008 : (1000, lnames[1008], "r", "m", 0, NPC_FISHERMAN),
    1009 : (1510, lnames[1009], "r", "m", 0, NPC_PETCLERK),
    1010 : (1510, lnames[1010], "r", "f", 0, NPC_PETCLERK),
    1011 : (1510, lnames[1011], "r", "f", 0, NPC_PETCLERK),
    1012 : (1000, lnames[1012], ("fls", "ms", "l", "m", 14, 0, 3, 3, 0, 1, 0, 1, 0, 13), "m", 1, NPC_PARTYPERSON),
    1013 : (1000, lnames[1013], ("fss", "ms", "m", "f", 2, 0, 3, 3, 1, 6, 1, 6, 5, 6), "f", 1, NPC_PARTYPERSON),

    1101 : (1627, lnames[1101], "r", "m", 0, NPC_REGULAR),
    1102 : (1612, lnames[1102], "r", "m", 0, NPC_REGULAR),
    1103 : (1626, lnames[1103], "r", "m", 0, NPC_REGULAR),
    1104 : (1617, lnames[1104], "r", "m", 0, NPC_REGULAR),
    1105 : (1606, lnames[1105], "r", "m", 0, NPC_REGULAR),
    1106 : (1604, lnames[1106], "r", "f", 0, NPC_REGULAR),
    1107 : (1621, lnames[1107], "r", "m", 0, NPC_REGULAR),
    1108 : (1629, lnames[1108], "r", "m", 0, NPC_HQ),
    1109 : (1629, lnames[1109], "r", "f", 0, NPC_HQ),
    1110 : (1629, lnames[1110], "r", "m", 0, NPC_HQ),
    1111 : (1629, lnames[1111], "r", "f", 0, NPC_HQ),
    1112 : (1602, lnames[1112], "r", "m", 0, NPC_REGULAR),
    1113 : (1608, lnames[1113], "r", "f", 0, NPC_REGULAR),
    1114 : (1609, lnames[1114], "r", "m", 0, NPC_REGULAR),
    1115 : (1613, lnames[1115], "r", "f", 0, NPC_REGULAR),
    1116 : (1614, lnames[1116], "r", "f", 0, NPC_REGULAR),
    1117 : (1615, lnames[1117], "r", "m", 0, NPC_REGULAR),
    1118 : (1616, lnames[1118], "r", "m", 0, NPC_REGULAR),
    1121 : (1619, lnames[1121], "r", "f", 0, NPC_REGULAR),
    1122 : (1620, lnames[1122], "r", "m", 0, NPC_REGULAR),
    1123 : (1622, lnames[1123], "r", "f", 0, NPC_REGULAR),
    1124 : (1624, lnames[1124], "r", "m", 0, NPC_REGULAR),
    1125 : (1628, lnames[1125], "r", "f", 0, NPC_REGULAR),
    1126 : (1129, lnames[1126], "r", "m", 0, NPC_FISHERMAN),
    
    1201 : (1710, lnames[1201], "r", "f", 0, NPC_REGULAR),
    1202 : (1713, lnames[1202], "r", "m", 0, NPC_REGULAR),
    1203 : (1725, lnames[1203], "r", "m", 0, NPC_REGULAR),
    1204 : (1712, lnames[1204], "r", "m", 0, NPC_REGULAR),
    1205 : (1729, lnames[1205], "r", "m", 0, NPC_HQ),
    1206 : (1729, lnames[1206], "r", "f", 0, NPC_HQ),
    1207 : (1729, lnames[1207], "r", "m", 0, NPC_HQ),
    1208 : (1729, lnames[1208], "r", "f", 0, NPC_HQ),
    1209 : (1701, lnames[1209], "r", "f", 0, NPC_REGULAR),
    1210 : (1703, lnames[1210], "r", "m", 0, NPC_REGULAR),
    1211 : (1705, lnames[1211], "r", "m", 0, NPC_REGULAR),
    1212 : (1706, lnames[1212], "r", "m", 0, NPC_REGULAR),
    1213 : (1707, lnames[1213], "r", "m", 0, NPC_REGULAR),
    1214 : (1709, lnames[1214], "r", "f", 0, NPC_REGULAR),
    1215 : (1711, lnames[1215], "r", "f", 0, NPC_REGULAR),
    1216 : (1714, lnames[1216], "r", "m", 0, NPC_REGULAR),
    1217 : (1716, lnames[1217], "r", "f", 0, NPC_REGULAR),
    1218 : (1717, lnames[1218], "r", "m", 0, NPC_REGULAR),
    1219 : (1718, lnames[1219], "r", "m", 0, NPC_REGULAR),
    1220 : (1719, lnames[1220], "r", "f", 0, NPC_REGULAR),
    1221 : (1720, lnames[1221], "r", "m", 0, NPC_REGULAR),
    1222 : (1721, lnames[1222], "r", "m", 0, NPC_REGULAR),
    1223 : (1723, lnames[1223], "r", "m", 0, NPC_REGULAR),
    1224 : (1724, lnames[1224], "r", "f", 0, NPC_REGULAR),
    1225 : (1726, lnames[1225], "r", "m", 0, NPC_REGULAR),
    1226 : (1727, lnames[1226], "r", "m", 0, NPC_REGULAR),
    1227 : (1728, lnames[1227], "r", "f", 0, NPC_REGULAR),
    1228 : (1236, lnames[1228], "r", "m", 0, NPC_FISHERMAN),

    1301 : (1828, lnames[1301], "r", "f", 0, NPC_REGULAR),
    1302 : (1832, lnames[1302], "r", "m", 0, NPC_REGULAR),
    1303 : (1826, lnames[1303], "r", "m", 0, NPC_REGULAR),
    1304 : (1804, lnames[1304], "r", "f", 0, NPC_REGULAR),
    1305 : (1835, lnames[1305], "r", "m", 0, NPC_HQ),
    1306 : (1835, lnames[1306], "r", "f", 0, NPC_HQ),
    1307 : (1835, lnames[1307], "r", "m", 0, NPC_HQ),
    1308 : (1835, lnames[1308], "r", "f", 0, NPC_HQ),
    1309 : (1802, lnames[1309], "r", "f", 0, NPC_REGULAR),
    1310 : (1805, lnames[1310], "r", "m", 0, NPC_REGULAR),
    1311 : (1806, lnames[1311], "r", "f", 0, NPC_REGULAR),
    1312 : (1807, lnames[1312], "r", "m", 0, NPC_REGULAR),
    1313 : (1808, lnames[1313], "r", "m", 0, NPC_REGULAR),
    1314 : (1809, lnames[1314], "r", "m", 0, NPC_REGULAR),
    1315 : (1810, lnames[1315], "r", "f", 0, NPC_REGULAR),
    1316 : (1811, lnames[1316], "r", "f", 0, NPC_REGULAR),
    1317 : (1813, lnames[1317], "r", "f", 0, NPC_REGULAR),
    1318 : (1814, lnames[1318], "r", "m", 0, NPC_REGULAR),
    1319 : (1815, lnames[1319], "r", "m", 0, NPC_REGULAR),
    1320 : (1818, lnames[1320], "r", "m", 0, NPC_REGULAR),
    1321 : (1819, lnames[1321], "r", "f", 0, NPC_REGULAR),
    1322 : (1820, lnames[1322], "r", "f", 0, NPC_REGULAR),
    1323 : (1821, lnames[1323], "r", "m", 0, NPC_REGULAR),
    1324 : (1823, lnames[1324], "r", "f", 0, NPC_REGULAR),
    1325 : (1824, lnames[1325], "r", "m", 0, NPC_REGULAR),
    1326 : (1825, lnames[1326], "r", "f", 0, NPC_REGULAR),
    1327 : (1829, lnames[1327], "r", "f", 0, NPC_REGULAR),
    1328 : (1830, lnames[1328], "r", "m", 0, NPC_REGULAR),
    1329 : (1831, lnames[1329], "r", "f", 0, NPC_REGULAR),
    1330 : (1833, lnames[1330], "r", "m", 0, NPC_REGULAR),
    1331 : (1834, lnames[1331], "r", "m", 0, NPC_REGULAR),
    1332 : (1330, lnames[1332], "r", "m", 0, NPC_FISHERMAN),

    # The Brrgh
    3001 : (3506, lnames[3001], "r", "f", 0, NPC_REGULAR),
    3002 : (3508, lnames[3002], "r", "m", 0, NPC_HQ),
    3003 : (3508, lnames[3003], "r", "f", 0, NPC_HQ),
    3004 : (3508, lnames[3004], "r", "m", 0, NPC_HQ),
    3005 : (3508, lnames[3005], "r", "m", 0, NPC_HQ),
    3006 : (3507, lnames[3006], "r", "m", 0, NPC_CLERK),
    3007 : (3507, lnames[3007], "r", "f", 0, NPC_CLERK),
    3008 : (3509, lnames[3008], "r", "m", 0, NPC_TAILOR),
    3009 : (3000, lnames[3009], "r", "f", 0, NPC_FISHERMAN),
    3010 : (3511, lnames[3010], "r", "m", 0, NPC_PETCLERK),
    3011 : (3511, lnames[3011], "r", "f", 0, NPC_PETCLERK),
    3012 : (3511, lnames[3012], "r", "m", 0, NPC_PETCLERK),
    3013 : (3000, lnames[3013], ("cls", "ss", "m", "m", 18, 0, 17, 17, 1, 7, 1, 7, 1, 9), "m", 1, NPC_PARTYPERSON),
    3014 : (3000, lnames[3014], ("css", "sd", "m", "f", 17, 0, 16, 16, 0, 24, 0, 24, 0, 9), "f", 1, NPC_PARTYPERSON),

    # Walrus Way
    3101 : (3611, lnames[3101], "r", "m", 0, NPC_REGULAR),
    3102 : (3625, lnames[3102], "r", "f", 0, NPC_REGULAR),
    3103 : (3641, lnames[3103], "r", "m", 0, NPC_REGULAR),
    3104 : (3602, lnames[3104], "r", "f", 0, NPC_REGULAR),
    3105 : (3651, lnames[3105], "r", "m", 0, NPC_REGULAR),
    3106 : (3636, lnames[3106], ('fll', 'ls', 'l', 'm', 8,2,8,8,10,27,0,27,7,11), "m", 0, NPC_REGULAR),
    3107 : (3630, lnames[3107], "r", "f", 0, NPC_REGULAR),
    3108 : (3638, lnames[3108], "r", "m", 0, NPC_REGULAR),
    3109 : (3637, lnames[3109], "r", "f", 0, NPC_REGULAR),
    3110 : (3629, lnames[3110], ('fss', 'ms', 'l', 'm', 10,10,10,10,16,4,0,4,5,4), "m", 0, NPC_REGULAR),
    3111 : (3627, lnames[3111], ('dsl', 'ls', 's', 'm', 6,0,6,6,14,27,10,27,1,14), "m", 1, NPC_REGULAR),
    3112 : (3607, lnames[3112], "r", "m", 0, NPC_REGULAR),
    3113 : (3618, lnames[3113], "r", "m", 0, NPC_REGULAR),
    3114 : (3620, lnames[3114], "r", "m", 0, NPC_REGULAR),
    3115 : (3654, lnames[3115], "r", "m", 0, NPC_HQ),
    3116 : (3654, lnames[3116], "r", "f", 0, NPC_HQ),
    3117 : (3654, lnames[3117], "r", "m", 0, NPC_HQ),
    3118 : (3654, lnames[3118], "r", "m", 0, NPC_HQ),
    3119 : (3653, lnames[3119], "r", "m", 0, NPC_REGULAR),
    3120 : (3610, lnames[3120], "r", "m", 0, NPC_REGULAR),
    3121 : (3601, lnames[3121], "r", "m", 0, NPC_REGULAR),
    3122 : (3608, lnames[3122], "r", "f", 0, NPC_REGULAR),
    3123 : (3612, lnames[3123], "r", "m", 0, NPC_REGULAR),
    3124 : (3613, lnames[3124], "r", "m", 0, NPC_REGULAR),
    3125 : (3614, lnames[3125], "r", "m", 0, NPC_REGULAR),
    3126 : (3615, lnames[3126], "r", "f", 0, NPC_REGULAR),
    3127 : (3617, lnames[3127], "r", "f", 0, NPC_REGULAR),
    3128 : (3621, lnames[3128], "r", "m", 0, NPC_REGULAR),
    3129 : (3623, lnames[3129], "r", "f", 0, NPC_REGULAR),
    3130 : (3624, lnames[3130], "r", "f", 0, NPC_REGULAR),
    3131 : (3634, lnames[3131], "r", "m", 0, NPC_REGULAR),
    3132 : (3635, lnames[3132], "r", "f", 0, NPC_REGULAR),
    3133 : (3642, lnames[3133], "r", "m", 0, NPC_REGULAR),
    3134 : (3643, lnames[3134], "r", "m", 0, NPC_REGULAR),
    3135 : (3644, lnames[3135], "r", "f", 0, NPC_REGULAR),
    3136 : (3647, lnames[3136], "r", "f", 0, NPC_REGULAR),
    3137 : (3648, lnames[3137], "r", "m", 0, NPC_REGULAR),
    3138 : (3649, lnames[3138], "r", "f", 0, NPC_REGULAR),
    3139 : (3650, lnames[3139], "r", "f", 0, NPC_REGULAR),
    3140 : (3136, lnames[3140], "r", "f", 0, NPC_FISHERMAN),

    # Sleet Street
    3201 : (3715, lnames[3201], "r", "f", 0, NPC_REGULAR),
    3202 : (3723, lnames[3202], "r", "m", 0, NPC_REGULAR),
    3203 : (3712, lnames[3203], "r", "m", 0, NPC_REGULAR),
    3204 : (3734, lnames[3204], "r", "f", 0, NPC_REGULAR),
    3205 : (3721, lnames[3205], "r", "m", 0, NPC_REGULAR),
    3206 : (3722, lnames[3206], "r", "f", 0, NPC_REGULAR),
    3207 : (3713, lnames[3207], "r", "m", 0, NPC_REGULAR),
    3208 : (3732, lnames[3208], "r", "m", 0, NPC_REGULAR),
    3209 : (3737, lnames[3209], "r", "m", 0, NPC_REGULAR),
    # Simian Sam is now a monkey!
    #3210 : (3728, lnames[3210], "r", "m", 0, NPC_REGULAR),
    3210 : (3728, lnames[3210], ('pls', 'ls', 's', 'm', 13,0,13,13,2,1,2,1,5,2), "m", 0, NPC_REGULAR),
    3211 : (3710, lnames[3211], "r", "f", 0, NPC_REGULAR),
    3212 : (3707, lnames[3212], "r", "m", 0, NPC_REGULAR),
    3213 : (3739, lnames[3213], "r", "m", 0, NPC_HQ),
    3214 : (3739, lnames[3214], "r", "f", 0, NPC_HQ),
    3215 : (3739, lnames[3215], "r", "m", 0, NPC_HQ),
    3216 : (3739, lnames[3216], "r", "m", 0, NPC_HQ),
    # At some point Sweaty Pete accidentally became female
    # We'll just change him/her back to male
    3217 : (3738, lnames[3217], "r", "m", 0, NPC_REGULAR),
    3218 : (3702, lnames[3218], "r", "m", 0, NPC_REGULAR),
    3219 : (3705, lnames[3219], "r", "m", 0, NPC_REGULAR),
    3220 : (3706, lnames[3220], "r", "m", 0, NPC_REGULAR),
    3221 : (3708, lnames[3221], "r", "f", 0, NPC_REGULAR),
    3222 : (3716, lnames[3222], "r", "f", 0, NPC_REGULAR),
    3223 : (3718, lnames[3223], "r", "m", 0, NPC_REGULAR),
    3224 : (3719, lnames[3224], "r", "f", 0, NPC_REGULAR),
    3225 : (3724, lnames[3225], "r", "m", 0, NPC_REGULAR),
    3226 : (3725, lnames[3226], "r", "m", 0, NPC_REGULAR),
    3227 : (3726, lnames[3227], "r", "m", 0, NPC_REGULAR),
    3228 : (3730, lnames[3228], "r", "f", 0, NPC_REGULAR),
    3229 : (3731, lnames[3229], "r", "f", 0, NPC_REGULAR),
    3230 : (3735, lnames[3230], "r", "m", 0, NPC_REGULAR),
    3231 : (3736, lnames[3231], "r", "m", 0, NPC_REGULAR),
    3232 : (3236, lnames[3232], "r", "m", 0, NPC_FISHERMAN),

    # Polar Place
    3301 : (3810, lnames[3301], "r", "f", 0, NPC_REGULAR),
    3302 : (3806, lnames[3302], "r", "m", 0, NPC_REGULAR),
    3303 : (3830, lnames[3303], "r", "m", 0, NPC_REGULAR),
    # Yeti Eddie
    3304 : (3828, lnames[3304], ('pll', 'ls', 'l', 'm', 0,0,0,0,1,5,1,5,1,6), "f", 0, NPC_REGULAR),
    3305 : (3812, lnames[3305], "r", "m", 0, NPC_REGULAR),
    # Paula Behr
    3306 : (3821, lnames[3306], ('bss', 'sd', 'm', 'f', 0,0,0,0,31,27,22,27,8,11), "f", 0, NPC_REGULAR),
    3307 : (3329, lnames[3307], "r", "f", 0, NPC_FISHERMAN),
    3308 : (3815, lnames[3308], "r", "m", 0, NPC_REGULAR),
    3309 : (3826, lnames[3309], "r", "m", 0, NPC_REGULAR),
    # Professor Flake
    3310 : (3823, lnames[3310], ('pll', 'ms', 'm', 'm', 10,0,10,10,60,27,49,27,0,13), "m", 0, NPC_REGULAR),
    3311 : (3829, lnames[3311], "r", "f", 0, NPC_REGULAR),
    # March Harry
    3312 : (3813, lnames[3312], ('rss', 'ms', 'l', 'm', 4,0,4,4,5,2,5,2,1,10), "m", 0, NPC_REGULAR),
    # Toon HQ
    3313 : (3801, lnames[3313], "r", "m", 0, NPC_HQ),
    3314 : (3801, lnames[3314], "r", "f", 0, NPC_HQ),
    3315 : (3801, lnames[3315], "r", "m", 0, NPC_HQ),
    3316 : (3801, lnames[3316], "r", "f", 0, NPC_HQ),
    3317 : (3816, lnames[3317], "r", "f", 0, NPC_REGULAR),
    # Johnny Cashmere
    3318 : (3808, lnames[3318], ('dss', 'ms', 'm', 'm', 18,0,18,18,57,1,46,1,12,1), "m", 0, NPC_REGULAR),
    3319 : (3825, lnames[3319], "r", "m", 0, NPC_REGULAR),
    3320 : (3814, lnames[3320], "r", "f", 0, NPC_REGULAR),
    3321 : (3818, lnames[3321], "r", "m", 0, NPC_REGULAR),
    3322 : (3819, lnames[3322], "r", "m", 0, NPC_REGULAR),
    3323 : (3811, lnames[3323], "r", "m", 0, NPC_REGULAR),
    3324 : (3809, lnames[3324], "r", "m", 0, NPC_REGULAR),
    3325 : (3827, lnames[3325], "r", "m", 0, NPC_REGULAR),
    3326 : (3820, lnames[3326], "r", "f", 0, NPC_REGULAR),
    3327 : (3824, lnames[3327], "r", "m", 0, NPC_REGULAR),
    3328 : (3807, lnames[3328], "r", "f", 0, NPC_REGULAR),
    3329 : (3817, lnames[3329], "r", "m", 0, NPC_REGULAR),
    
    # Minnie's Melody Land
    4001 : (4502, lnames[4001], "r", "f", 0, NPC_REGULAR),
    4002 : (4504, lnames[4002], "r", "m", 0, NPC_HQ),
    4003 : (4504, lnames[4003], "r", "f", 0, NPC_HQ),
    4004 : (4504, lnames[4004], "r", "f", 0, NPC_HQ),
    4005 : (4504, lnames[4005], "r", "f", 0, NPC_HQ),
    4006 : (4503, lnames[4006], "r", "f", 0, NPC_CLERK),
    4007 : (4503, lnames[4007], "r", "m", 0, NPC_CLERK),
    4008 : (4506, lnames[4008], "r", "f", 0, NPC_TAILOR),
    4009 : (4000, lnames[4009], "r", "f", 0, NPC_FISHERMAN),
    4010 : (4508, lnames[4010], "r", "m", 0, NPC_PETCLERK),
    4011 : (4508, lnames[4011], "r", "m", 0, NPC_PETCLERK),
    4012 : (4508, lnames[4012], "r", "f", 0, NPC_PETCLERK),
    4013 : (4000, lnames[4013], ("bll", "ls", "s", "m", 3, 0, 19, 19, 0, 8, 0, 8, 1, 12), "m", 1, NPC_PARTYPERSON),
    4014 : (4000, lnames[4014], ("bss", "md", "m", "f", 24, 0, 19, 19, 0, 24, 0, 24, 0, 12), "f", 1, NPC_PARTYPERSON),

    4101 : (4603, lnames[4101], "r", "m", 0, NPC_REGULAR),
    4102 : (4605, lnames[4102], "r", "f", 0, NPC_REGULAR),
    4103 : (4612, lnames[4103], "r", "m", 0, NPC_REGULAR),
    4104 : (4659, lnames[4104], "r", "m", 0, NPC_HQ),
    4105 : (4659, lnames[4105], "r", "f", 0, NPC_HQ),
    4106 : (4659, lnames[4106], "r", "f", 0, NPC_HQ),
    4107 : (4659, lnames[4107], "r", "f", 0, NPC_HQ),
    4108 : (4626, lnames[4108], "r", "m", 0, NPC_REGULAR),
    4109 : (4606, lnames[4109], "r", "m", 0, NPC_REGULAR),
    4110 : (4604, lnames[4110], "r", "f", 0, NPC_REGULAR),
    4111 : (4607, lnames[4111], "r", "m", 0, NPC_REGULAR),
    4112 : (4609, lnames[4112], "r", "f", 0, NPC_REGULAR),
    4113 : (4610, lnames[4113], "r", "f", 0, NPC_REGULAR),
    4114 : (4611, lnames[4114], "r", "m", 0, NPC_REGULAR),
    4115 : (4614, lnames[4115], "r", "f", 0, NPC_REGULAR),
    4116 : (4615, lnames[4116], "r", "m", 0, NPC_REGULAR),
    4117 : (4617, lnames[4117], "r", "f", 0, NPC_REGULAR),
    4118 : (4618, lnames[4118], "r", "m", 0, NPC_REGULAR),
    4119 : (4619, lnames[4119], "r", "m", 0, NPC_REGULAR),
    4120 : (4622, lnames[4120], "r", "f", 0, NPC_REGULAR),
    4121 : (4623, lnames[4121], "r", "m", 0, NPC_REGULAR),
    4122 : (4625, lnames[4122], "r", "f", 0, NPC_REGULAR),
    4123 : (4628, lnames[4123], "r", "m", 0, NPC_REGULAR),
    4124 : (4629, lnames[4124], "r", "m", 0, NPC_REGULAR),
    4125 : (4630, lnames[4125], "r", "f", 0, NPC_REGULAR),
    4126 : (4631, lnames[4126], "r", "m", 0, NPC_REGULAR),
    4127 : (4632, lnames[4127], "r", "f", 0, NPC_REGULAR),
    4128 : (4635, lnames[4128], "r", "m", 0, NPC_REGULAR),
    4129 : (4637, lnames[4129], "r", "f", 0, NPC_REGULAR),
    4130 : (4638, lnames[4130], "r", "m", 0, NPC_REGULAR),
    4131 : (4639, lnames[4131], "r", "m", 0, NPC_REGULAR),
    4132 : (4641, lnames[4132], "r", "f", 0, NPC_REGULAR),
    4133 : (4642, lnames[4133], "r", "m", 0, NPC_REGULAR),
    4134 : (4645, lnames[4134], "r", "m", 0, NPC_REGULAR),
    4135 : (4648, lnames[4135], "r", "m", 0, NPC_REGULAR),
    4136 : (4652, lnames[4136], "r", "f", 0, NPC_REGULAR),
    4137 : (4654, lnames[4137], "r", "m", 0, NPC_REGULAR),
    4138 : (4655, lnames[4138], "r", "m", 0, NPC_REGULAR),
    4139 : (4657, lnames[4139], "r", "f", 0, NPC_REGULAR),
    4140 : (4658, lnames[4140], "r", "m", 0, NPC_REGULAR),
    4141 : (4148, lnames[4141], "r", "m", 0, NPC_FISHERMAN),

    4201 : (4704, lnames[4201], "r", "f", 0, NPC_REGULAR),
    4202 : (4725, lnames[4202], "r", "m", 0, NPC_REGULAR),
    4203 : (4702, lnames[4203], "r", "m", 0, NPC_REGULAR),
    4204 : (4739, lnames[4204], "r", "m", 0, NPC_HQ),
    4205 : (4739, lnames[4205], "r", "f", 0, NPC_HQ),
    4206 : (4739, lnames[4206], "r", "f", 0, NPC_HQ),
    4207 : (4739, lnames[4207], "r", "f", 0, NPC_HQ),
    4208 : (4730, lnames[4208], "r", "f", 0, NPC_REGULAR),
    4209 : (4701, lnames[4209], "r", "f", 0, NPC_REGULAR),
    4211 : (4703, lnames[4211], "r", "m", 0, NPC_REGULAR),
    4212 : (4705, lnames[4212], "r", "m", 0, NPC_REGULAR),
    4213 : (4707, lnames[4213], "r", "f", 0, NPC_REGULAR),
    4214 : (4709, lnames[4214], "r", "f", 0, NPC_REGULAR),
    4215 : (4710, lnames[4215], "r", "m", 0, NPC_REGULAR),
    4216 : (4712, lnames[4216], "r", "m", 0, NPC_REGULAR),
    4217 : (4713, lnames[4217], "r", "m", 0, NPC_REGULAR),
    4218 : (4716, lnames[4218], "r", "f", 0, NPC_REGULAR),
    4219 : (4717, lnames[4219], "r", "m", 0, NPC_REGULAR),
    4220 : (4718, lnames[4220], "r", "m", 0, NPC_REGULAR),
    4221 : (4719, lnames[4221], "r", "m", 0, NPC_REGULAR),
    4222 : (4720, lnames[4222], "r", "m", 0, NPC_REGULAR),
    4223 : (4722, lnames[4223], "r", "f", 0, NPC_REGULAR),
    4224 : (4723, lnames[4224], "r", "m", 0, NPC_REGULAR),
    4225 : (4724, lnames[4225], "r", "f", 0, NPC_REGULAR),
    4226 : (4727, lnames[4226], "r", "f", 0, NPC_REGULAR),
    4227 : (4728, lnames[4227], "r", "f", 0, NPC_REGULAR),
    4228 : (4729, lnames[4228], "r", "f", 0, NPC_REGULAR),
    4229 : (4731, lnames[4229], "r", "f", 0, NPC_REGULAR),
    4230 : (4732, lnames[4230], "r", "m", 0, NPC_REGULAR),
    4231 : (4735, lnames[4231], "r", "f", 0, NPC_REGULAR),
    4232 : (4736, lnames[4232], "r", "m", 0, NPC_REGULAR),
    4233 : (4737, lnames[4233], "r", "m", 0, NPC_REGULAR),
    4234 : (4738, lnames[4234], "r", "m", 0, NPC_REGULAR),
    4235 : (4240, lnames[4235], "r", "m", 0, NPC_FISHERMAN),

    4301 : (4819, lnames[4301], "r", "f", 0, NPC_REGULAR),
    4302 : (4821, lnames[4302], "r", "f", 0, NPC_REGULAR),
    4303 : (4853, lnames[4303], "r", "m", 0, NPC_REGULAR),
    4304 : (4873, lnames[4304], "r", "m", 0, NPC_HQ),
    4305 : (4873, lnames[4305], "r", "f", 0, NPC_HQ),
    4306 : (4873, lnames[4306], "r", "f", 0, NPC_HQ),
    4307 : (4873, lnames[4307], "r", "f", 0, NPC_HQ),
    4308 : (4835, lnames[4308], ('css', 'md', 'm', 'f', 6,0,6,6,3,5,3,5,0,14), "f", 0, NPC_REGULAR),
    4309 : (4801, lnames[4309], "r", "m", 0, NPC_REGULAR),
    4310 : (4803, lnames[4310], "r", "f", 0, NPC_REGULAR),
    4311 : (4804, lnames[4311], "r", "f", 0, NPC_REGULAR),
    4312 : (4807, lnames[4312], "r", "m", 0, NPC_REGULAR),
    4313 : (4809, lnames[4313], "r", "m", 0, NPC_REGULAR),
    4314 : (4817, lnames[4314], "r", "f", 0, NPC_REGULAR),
    4315 : (4827, lnames[4315], "r", "f", 0, NPC_REGULAR),
    4316 : (4828, lnames[4316], "r", "m", 0, NPC_REGULAR),
    4317 : (4829, lnames[4317], "r", "m", 0, NPC_REGULAR),
    4318 : (4836, lnames[4318], "r", "m", 0, NPC_REGULAR),
    4319 : (4838, lnames[4319], "r", "f", 0, NPC_REGULAR),
    4320 : (4840, lnames[4320], "r", "f", 0, NPC_REGULAR),
    4321 : (4841, lnames[4321], "r", "m", 0, NPC_REGULAR),
    4322 : (4842, lnames[4322], "r", "m", 0, NPC_REGULAR),
    4323 : (4844, lnames[4323], "r", "f", 0, NPC_REGULAR),
    4324 : (4845, lnames[4324], "r", "f", 0, NPC_REGULAR),
    4325 : (4848, lnames[4325], "r", "m", 0, NPC_REGULAR),
    4326 : (4850, lnames[4326], "r", "f", 0, NPC_REGULAR),
    4327 : (4852, lnames[4327], "r", "f", 0, NPC_REGULAR),
    4328 : (4854, lnames[4328], "r", "m", 0, NPC_REGULAR),
    4329 : (4855, lnames[4329], "r", "f", 0, NPC_REGULAR),
    4330 : (4862, lnames[4330], "r", "m", 0, NPC_REGULAR),
    4331 : (4867, lnames[4331], "r", "m", 0, NPC_REGULAR),
    4332 : (4870, lnames[4332], "r", "m", 0, NPC_REGULAR),
    4333 : (4871, lnames[4333], "r", "m", 0, NPC_REGULAR),
    4334 : (4872, lnames[4334], "r", "m", 0, NPC_REGULAR),
    4335 : (4345, lnames[4335], "r", "m", 0, NPC_FISHERMAN),

    # Daisy Gardens
    5001 : (5502, lnames[5001], "r", "m", 0, NPC_HQ),
    5002 : (5502, lnames[5002], "r", "m", 0, NPC_HQ),
    5003 : (5502, lnames[5003], "r", "f", 0, NPC_HQ),
    5004 : (5502, lnames[5004], "r", "f", 0, NPC_HQ),
    5005 : (5501, lnames[5005], "r", "f", 0, NPC_CLERK),
    5006 : (5501, lnames[5006], "r", "m", 0, NPC_CLERK),
    5007 : (5503, lnames[5007], "r", "f", 0, NPC_TAILOR),
    5008 : (5000, lnames[5008], "r", "f", 0, NPC_FISHERMAN),
    5009 : (5505, lnames[5009], "r", "f", 0, NPC_PETCLERK),
    5010 : (5505, lnames[5010], "r", "m", 0, NPC_PETCLERK),
    5011 : (5505, lnames[5011], "r", "m", 0, NPC_PETCLERK),
    5012 : (5000, lnames[5012], ("dls", "ms", "m", "m", 13, 0, 12, 12, 0, 1, 0, 1, 0, 6), "m", 1, NPC_PARTYPERSON),
    5013 : (5000, lnames[5013], ("dss", "md", "m", "f", 1, 0, 3, 3, 1, 5, 1, 5, 0, 5), "f", 1, NPC_PARTYPERSON),

    # Elm Street
    5101 : (5602, lnames[5101], "r", "m", 0, NPC_REGULAR),
    5102 : (5610, lnames[5102], "r", "f", 0, NPC_REGULAR),
    5103 : (5615, lnames[5103], "r", "m", 0, NPC_REGULAR),
    5104 : (5617, lnames[5104], "r", "m", 0, NPC_REGULAR),
    5105 : (5619, lnames[5105], "r", "m", 0, NPC_REGULAR),
    5106 : (5613, lnames[5106], "r", "m", 0, NPC_REGULAR),
    5107 : (5607, lnames[5107], "r", "m", 0, NPC_REGULAR),
    5108 : (5616, lnames[5108], "r", "f", 0, NPC_REGULAR),
    5109 : (5627, lnames[5109], "r", "m", 1, NPC_HQ),
    5110 : (5627, lnames[5110], "r", "m", 1, NPC_HQ),
    5111 : (5627, lnames[5111], "r", "f", 1, NPC_HQ),
    5112 : (5627, lnames[5112], "r", "f", 1, NPC_HQ),
    5113 : (5601, lnames[5113], "r", "f", 0, NPC_REGULAR),
    5114 : (5603, lnames[5114], "r", "m", 0, NPC_REGULAR),
    5115 : (5604, lnames[5115], "r", "f", 0, NPC_REGULAR),
    5116 : (5605, lnames[5116], "r", "m", 0, NPC_REGULAR),
    5117 : (5606, lnames[5117], "r", "f", 0, NPC_REGULAR),
    5118 : (5608, lnames[5118], "r", "m", 0, NPC_REGULAR),
    5119 : (5609, lnames[5119], "r", "m", 0, NPC_REGULAR),
    5120 : (5611, lnames[5120], "r", "m", 0, NPC_REGULAR),
    5121 : (5618, lnames[5121], "r", "f", 0, NPC_REGULAR),
    5122 : (5620, lnames[5122], "r", "m", 0, NPC_REGULAR),
    5123 : (5621, lnames[5123], "r", "f", 0, NPC_REGULAR),
    5124 : (5622, lnames[5124], "r", "m", 0, NPC_REGULAR),
    5125 : (5623, lnames[5125], "r", "m", 0, NPC_REGULAR),
    5126 : (5624, lnames[5126], "r", "f", 0, NPC_REGULAR),
    5127 : (5625, lnames[5127], "r", "f", 0, NPC_REGULAR),
    5128 : (5626, lnames[5128], "r", "f", 0, NPC_REGULAR),
    5129 : (5139, lnames[5129], "r", "f", 0, NPC_FISHERMAN),

    # Maple Street
    5201 : (5702, lnames[5201], "r", "m", 0, NPC_REGULAR),
    5202 : (5703, lnames[5202], "r", "f", 0, NPC_REGULAR),
    5203 : (5704, lnames[5203], "r", "f", 0, NPC_REGULAR),
    5204 : (5726, lnames[5204], "r", "m", 0, NPC_REGULAR),
    5205 : (5718, lnames[5205], "r", "m", 0, NPC_REGULAR),
    5206 : (5720, lnames[5206], "r", "m", 0, NPC_REGULAR),
    5207 : (5717, lnames[5207], "r", "f", 0, NPC_REGULAR),
    5208 : (5719, lnames[5208], "r", "f", 0, NPC_REGULAR),
    5209 : (5728, lnames[5209], "r", "m", 1, NPC_HQ),
    5210 : (5728, lnames[5210], "r", "m", 1, NPC_HQ),
    5211 : (5728, lnames[5211], "r", "f", 1, NPC_HQ),
    5212 : (5728, lnames[5212], "r", "f", 1, NPC_HQ),
    5213 : (5701, lnames[5213], "r", "m", 0, NPC_REGULAR),
    5214 : (5705, lnames[5214], "r", "f", 0, NPC_REGULAR),
    5215 : (5706, lnames[5215], "r", "f", 0, NPC_REGULAR),
    5216 : (5707, lnames[5216], "r", "m", 0, NPC_REGULAR),
    5217 : (5708, lnames[5217], "r", "m", 0, NPC_REGULAR),
    5218 : (5709, lnames[5218], "r", "m", 0, NPC_REGULAR),
    5219 : (5710, lnames[5219], "r", "m", 0, NPC_REGULAR),
    5220 : (5711, lnames[5220], "r", "f", 0, NPC_REGULAR),
    5221 : (5712, lnames[5221], "r", "f", 0, NPC_REGULAR),
    5222 : (5713, lnames[5222], "r", "f", 0, NPC_REGULAR),
    5223 : (5714, lnames[5223], "r", "m", 0, NPC_REGULAR),
    5224 : (5715, lnames[5224], "r", "m", 0, NPC_REGULAR),
    5225 : (5716, lnames[5225], "r", "f", 0, NPC_REGULAR),
    5226 : (5721, lnames[5226], "r", "m", 0, NPC_REGULAR),
    5227 : (5725, lnames[5227], "r", "f", 0, NPC_REGULAR),
    5228 : (5727, lnames[5228], "r", "m", 0, NPC_REGULAR),
    5229 : (5245, lnames[5229], "r", "f", 0, NPC_FISHERMAN),

    # Oak Street
    5301 : (5802, lnames[5301], "r", "f", 1, NPC_HQ),
    5302 : (5802, lnames[5302], "r", "f", 1, NPC_HQ),
    5303 : (5802, lnames[5303], "r", "m", 1, NPC_HQ),
    5304 : (5802, lnames[5304], "r", "f", 1, NPC_HQ),
    5305 : (5804, lnames[5305], "r", "f", 0, NPC_REGULAR), # ("Just Vase It", ""),
    5306 : (5805, lnames[5306], "r", "m", 0, NPC_REGULAR), # ("Snail Mail", ""),
    5307 : (5809, lnames[5307], "r", "m", 0, NPC_REGULAR), # ("Fungi Clown School", ""),
    5308 : (5810, lnames[5308], "r", "f", 0, NPC_REGULAR), # ("Honeydew This", ""),
    5309 : (5811, lnames[5309], "r", "f", 0, NPC_REGULAR), # ("Lettuce Inn", ""),
    5310 : (5815, lnames[5310], "r", "m", 0, NPC_REGULAR), # ("Grass Roots", ""),
    5311 : (5817, lnames[5311], "r", "f", 0, NPC_REGULAR), # ("Apples and Oranges", ""),
    5312 : (5819, lnames[5312], "r", "m", 0, NPC_REGULAR), # ("Green Bean Jeans", ""),
    5313 : (5821, lnames[5313], "r", "m", 0, NPC_REGULAR), # ("Squash and Stretch Gym", ""),
    5314 : (5826, lnames[5314], "r", "f", 0, NPC_REGULAR), # ("Ant Farming Supplies", ""),
    5315 : (5827, lnames[5315], "r", "m", 0, NPC_REGULAR), # ("Dirt. Cheap.", ""),
    5316 : (5828, lnames[5316], "r", "m", 0, NPC_REGULAR), # ("Couch Potato Furniture", ""),
    5317 : (5830, lnames[5317], "r", "m", 0, NPC_REGULAR), # ("Spill the Beans", ""),
    5318 : (5833, lnames[5318], "r", "m", 0, NPC_REGULAR), # ("The Salad Bar", ""),
    5319 : (5835, lnames[5319], "r", "f", 0, NPC_REGULAR), # ("Flower Bed and Breakfast", ""),
    5320 : (5836, lnames[5320], "r", "f", 0, NPC_REGULAR), # ("April's Showers and Tubs", ""),
    5321 : (5837, lnames[5321], "r", "f", 0, NPC_REGULAR), # ("School of Vine Arts", ""),
    5322 : (5318, lnames[5322], "r", "f", 0, NPC_FISHERMAN),
    #(head, torso, legs, sex, armColor, gloveColor, legColor, headColor,
    #          topTexture, bottomTexture)
    #['White', 'Peach', 'Bright Red', 'Red', 'Maroon',
    #          'Sienna', 'Brown', 'Tan', 'Coral', 'Orange',
    #          'Yellow', 'Cream', 'Citrine', 'Lime', 'Sea Green',
    #          'Green', 'Light Blue', 'Aqua', 'Blue',
    #          'Periwinkle', 'Royal Blue', 'Slate Blue', 'Purple',
    #          'Lavender', 'Pink', 'Plum', 'Black']
    
    # Goofy's Speedway
    8001 : (8501, lnames[8001], ("psl", "ms", "m", 'm', 13, 0, 13,  13,  0, 11, 0, 11, 2, 10), "m", 0, NPC_KARTCLERK),
    8002 : (8501, lnames[8002], ("psl", "ld", "s", 'f', 23, 0, 23,  23,  0, 11, 0, 11, 2, 10), "f", 0, NPC_KARTCLERK),
    8003 : (8501, lnames[8003], ("pll", "ss", "l", 'f', 1, 0, 1,  1,  0, 11, 0, 11, 2, 10), "f", 0, NPC_KARTCLERK),
    8004 : (8501, lnames[8004], ("pls", "ms", "l", 'm', 16, 0, 16,  16,  0, 11, 0, 11, 2, 10), "m", 0, NPC_KARTCLERK),

    # Dreamland
    9001 : (9503, lnames[9001], "r", "f", 0, NPC_REGULAR),
    9002 : (9502, lnames[9002], "r", "m", 0, NPC_REGULAR),
    9003 : (9501, lnames[9003], "r", "m", 0, NPC_REGULAR),
    9004 : (9505, lnames[9004], "r", "f", 1, NPC_HQ),
    9005 : (9505, lnames[9005], "r", "f", 1, NPC_HQ),
    9006 : (9505, lnames[9006], "r", "m", 1, NPC_HQ),
    9007 : (9505, lnames[9007], "r", "m", 1, NPC_HQ),
    9008 : (9504, lnames[9008], "r", "f", 0, NPC_CLERK),
    9009 : (9504, lnames[9009], "r", "m", 0, NPC_CLERK),
    9010 : (9506, lnames[9010], "r", "m", 0, NPC_TAILOR),
    9011 : (9000, lnames[9011], "r", "m", 0, NPC_FISHERMAN),
    9012 : (9508, lnames[9012], "r", "f", 0, NPC_PETCLERK),
    9013 : (9508, lnames[9013], "r", "f", 0, NPC_PETCLERK),
    9014 : (9508, lnames[9014], "r", "m", 0, NPC_PETCLERK),
    9015 : (9000, lnames[9015], ("rss", "ls", "l", "m", 21, 0, 20, 20, 0, 12, 0, 12, 0, 11), "m", 1, NPC_PARTYPERSON),
    9016 : (9000, lnames[9016], ("rls", "md", "l", "f", 6, 0, 21, 21, 1, 11, 1, 11, 0, 11), "f", 1, NPC_PARTYPERSON),

    9101 : (9604, lnames[9101], "r", "m", 0, NPC_REGULAR),
    9102 : (9607, lnames[9102], "r", "f", 0, NPC_REGULAR),
    9103 : (9620, lnames[9103], "r", "m", 0, NPC_REGULAR),
    9104 : (9642, lnames[9104], "r", "f", 0, NPC_REGULAR),
    9105 : (9609, lnames[9105], "r", "m", 0, NPC_REGULAR),
    9106 : (9619, lnames[9106], "r", "m", 0, NPC_REGULAR),
    9107 : (9601, lnames[9107], "r", "f", 0, NPC_REGULAR),
    9108 : (9602, lnames[9108], "r", "m", 0, NPC_REGULAR),
    9109 : (9605, lnames[9109], "r", "f", 0, NPC_REGULAR),
    9110 : (9608, lnames[9110], "r", "f", 0, NPC_REGULAR),
    9111 : (9616, lnames[9111], "r", "f", 0, NPC_REGULAR),
    9112 : (9617, lnames[9112], "r", "m", 0, NPC_REGULAR),
    9113 : (9622, lnames[9113], "r", "m", 0, NPC_REGULAR),
    9114 : (9625, lnames[9114], "r", "f", 0, NPC_REGULAR),
    9115 : (9626, lnames[9115], "r", "m", 0, NPC_REGULAR),
    9116 : (9627, lnames[9116], "r", "m", 0, NPC_REGULAR),
    9117 : (9628, lnames[9117], "r", "f", 0, NPC_REGULAR),
    9118 : (9629, lnames[9118], "r", "f", 0, NPC_REGULAR),
    9119 : (9630, lnames[9119], "r", "m", 0, NPC_REGULAR),
    9120 : (9631, lnames[9120], "r", "f", 0, NPC_REGULAR),
    9121 : (9634, lnames[9121], "r", "f", 0, NPC_REGULAR),
    9122 : (9636, lnames[9122], "r", "m", 0, NPC_REGULAR),
    9123 : (9639, lnames[9123], "r", "m", 0, NPC_REGULAR),
    9124 : (9640, lnames[9124], "r", "f", 0, NPC_REGULAR),
    9125 : (9643, lnames[9125], "r", "m", 0, NPC_REGULAR),
    9126 : (9644, lnames[9126], "r", "f", 0, NPC_REGULAR),
    9127 : (9645, lnames[9127], "r", "f", 0, NPC_REGULAR),
    9128 : (9647, lnames[9128], "r", "m", 0, NPC_REGULAR),
    9129 : (9649, lnames[9129], "r", "f", 0, NPC_REGULAR),
    9130 : (9650, lnames[9130], "r", "m", 0, NPC_REGULAR),
    9131 : (9651, lnames[9131], "r", "f", 0, NPC_REGULAR),

    9132 : (9652, lnames[9132], "r", "f", 0, NPC_HQ),
    9133 : (9652, lnames[9133], "r", "m", 0, NPC_HQ),
    9134 : (9652, lnames[9134], "r", "m", 0, NPC_HQ),
    9135 : (9652, lnames[9135], "r", "m", 0, NPC_HQ),
    9136 : (9153, lnames[9136], "r", "m", 0, NPC_FISHERMAN),
    
    9201 : (9752, lnames[9201], ('psl', 'ss', 'm', 'm', 9,0,9,9,17,11,0,11,7,20), 'm', 0, NPC_REGULAR),
    9202 : (9703, lnames[9202], ('dss', 'ss', 's', 'm', 21,0,21,21,8,3,8,3,1,17), 'm', 0, NPC_REGULAR),
    9203 : (9741, lnames[9203], ('pls', 'ls', 's', 'm', 5,0,5,5,37,27,26,27,7,4), 'm', 0, NPC_REGULAR),
    9204 : (9704, lnames[9204], ('fsl', 'sd', 's', 'f', 19,0,19,19,21,10,0,10,8,23), 'f', 0, NPC_REGULAR),
    9205 : (9736, lnames[9205], ('dsl', 'ms', 'm', 'm', 15,0,15,15,45,27,34,27,2,17), 'm', 0, NPC_REGULAR),
    9206 : (9727, lnames[9206], ('rls', 'ld', 'l', 'f', 8,0,8,8,25,27,16,27,10,27), 'f', 0, NPC_REGULAR),
    9207 : (9709, lnames[9207], ('hss', 'ss', 's', 'f', 24,0,24,24,36,27,25,27,9,27), 'f', 0, NPC_REGULAR),
    9208 : (9705, lnames[9208], ('dsl', 'ms', 's', 'm', 20,0,20,20,46,27,35,27,6,27), 'm', 0, NPC_REGULAR),
    9209 : (9706, lnames[9209], ('pll', 'ss', 'm', 'm', 13,0,13,13,8,12,8,12,1,12), 'm', 0, NPC_REGULAR),
    9210 : (9740, lnames[9210], ('hsl', 'ls', 'l', 'm', 6,0,6,6,1,0,1,0,0,0), 'm', 0, NPC_REGULAR),
    9211 : (9707, lnames[9211], ('rll', 'ss', 's', 'f', 3,0,3,3,22,22,0,22,6,22), 'f', 0, NPC_REGULAR),
    9212 : (9753, lnames[9212], ('pss', 'md', 'm', 'f', 16,0,16,16,45,27,34,27,0,3), 'f', 0, NPC_REGULAR),
    9213 : (9711, lnames[9213], ('fsl', 'ss', 'm', 'm', 2,0,2,2,37,27,26,27,7,18), 'm', 0, NPC_REGULAR),
    9214 : (9710, lnames[9214], ('rll', 'ls', 'l', 'm', 18,0,18,18,10,27,0,27,0,13), 'm', 0, NPC_REGULAR),
    9215 : (9744, lnames[9215], ('csl', 'ls', 'l', 'm', 18,0,18,18,11,4,0,4,0,4), 'm', 0, NPC_REGULAR),
    9216 : (9725, lnames[9216], ('csl', 'sd', 'm', 'f', 14,0,14,14,1,7,1,7,3,7), 'f', 0, NPC_REGULAR),
    9217 : (9713, lnames[9217], ('mss', 'ms', 'm', 'f', 17,0,17,17,20,26,0,26,5,12), 'f', 0, NPC_REGULAR),
    9218 : (9737, lnames[9218], ('dss', 'md', 'l', 'f', 23,0,23,23,24,27,15,27,11,27), 'f', 0, NPC_REGULAR),
    9219 : (9712, lnames[9219], ('hll', 'sd', 'l', 'f', 10,0,10,10,9,22,9,22,12,27), 'f', 0, NPC_REGULAR),
    9220 : (9716, lnames[9220], ('mls', 'ms', 'l', 'm', 7,0,7,7,0,27,0,27,1,10), 'm', 0, NPC_REGULAR),
    9221 : (9738, lnames[9221], ('fss', 'md', 'l', 'f', 22,0,22,22,45,27,34,27,0,6), 'f', 0, NPC_REGULAR),
    9222 : (9754, lnames[9222], ('hsl', 'ls', 'l', 'm', 10,0,10,10,52,27,41,27,12,27), 'm', 0, NPC_REGULAR),
    9223 : (9714, lnames[9223], ('fsl', 'ms', 'm', 'm', 20,0,20,20,43,27,32,27,0,0), 'm', 0, NPC_REGULAR),
    9224 : (9718, lnames[9224], ('css', 'ms', 'm', 'f', 1,0,1,1,6,8,6,8,6,8), 'f', 0, NPC_REGULAR),
    9225 : (9717, lnames[9225], ('rss', 'md', 'm', 'f', 11,0,11,11,40,27,29,27,0,27), 'f', 0, NPC_REGULAR),
    9226 : (9715, lnames[9226], ('mls', 'ms', 's', 'm', 12,0,12,12,3,10,3,10,6,10), 'm', 0, NPC_REGULAR),
    9227 : (9721, lnames[9227], ('cls', 'ss', 's', 'm', 13,0,13,13,8,5,8,5,3,18), 'm', 0, NPC_REGULAR),
    9228 : (9720, lnames[9228], ('fss', 'sd', 's', 'f', 4,0,4,4,15,5,11,5,8,5), 'f', 0, NPC_REGULAR),
    9229 : (9708, lnames[9229], ('css', 'ld', 'm', 'f', 4,0,4,4,22,21,0,21,4,21), 'f', 0, NPC_REGULAR),
    9230 : (9719, lnames[9230], ('mss', 'ss', 's', 'm', 8,0,8,8,53,27,42,27,13,27), 'm', 0, NPC_REGULAR),
    9231 : (9722, lnames[9231], ('dll', 'ss', 's', 'm', 6,0,6,6,27,27,18,27,3,8), 'm', 0, NPC_REGULAR),
    9232 : (9759, lnames[9232], ('pss', 'ld', 'm', 'f', 21,0,21,21,0,27,0,27,13,27), 'f', 0, NPC_REGULAR),

    9233 : (9756, lnames[9233], "r", "f", 0, NPC_HQ),
    9234 : (9756, lnames[9234], "r", "m", 0, NPC_HQ),
    9235 : (9756, lnames[9235], "r", "m", 0, NPC_HQ),
    9236 : (9756, lnames[9236], "r", "m", 0, NPC_HQ),
    9237 : (9255, lnames[9237], "r", "m", 0, NPC_FISHERMAN),   


    # Tutorial IDs start at 20000, and are not part of this table.
    # Don't add any Toon id's at 20000 or above, for this reason!
    # Look in TutorialBuildingAI.py for more details.

    }

# We are done with this now
del lnames

BlockerPositions = {
    TTLocalizer.Flippy : (Point3(207.4, 18.81, -0.475), 90.0),
    }

# Maps toon interior zones to NPC ids
# The toon interior zone is the branch zone + 500 + block number
# You have to look in the dna to know what block numbers there are
# they are not necessary
zone2NpcDict = {}

# Fill out the zone2NpcDict so we can efficiently lookup toons by zoneId
for id, npcDesc in NPCToonDict.items():
    zoneId = npcDesc[0]
    if zone2NpcDict.has_key(zoneId):
        zone2NpcDict[zoneId].append(id)
    else:
        zone2NpcDict[zoneId] = [id]

def getNPCName(npcId):
    npc = NPCToonDict.get(npcId)
    if npc:
        return npc[1]
    else:
        return None

def getNPCZone(npcId):
    npc = NPCToonDict.get(npcId)
    if npc:
        return npc[0]
    else:
        return None

# NOTE: building article and name now stored as a tuple.
# If no article is defined an empty string is returned.

def getBuildingArticle(zoneId):
    return TTLocalizer.zone2TitleDict.get(zoneId, "Toon Building")[1]

def getBuildingTitle(zoneId):
    return TTLocalizer.zone2TitleDict.get(zoneId, "Toon Building")[0]

npcFriends = {
    # A dictionary of tuples, indexed by rescued toon npcId
    # Each tuple consists of (type, level, hp, rarity) except for the
    # restock sos which consists of (type, track, 0, rarity)
    
    # Healers
    # Flippy
    2001 : (ToontownBattleGlobals.HEAL_TRACK, 5, ToontownGlobals.MaxHpLimit,5),
    # Daffy Don 
    2132 : (ToontownBattleGlobals.HEAL_TRACK, 5, 70, 4), 
    # Madam Chuckle 
    2121 : (ToontownBattleGlobals.HEAL_TRACK, 5, 45, 3), 
        
    # Trappers
    # Clerk Clara
    2011 : (ToontownBattleGlobals.TRAP_TRACK, 4, 180, 5), 
    # Clerk Penny 
    3007 : (ToontownBattleGlobals.TRAP_TRACK, 4, 70, 4), 
    # Clerk Will
    1001 : (ToontownBattleGlobals.TRAP_TRACK, 4, 50, 3), 

    # Lurers
    # Lil Oldman
    3112 : (ToontownBattleGlobals.LURE_TRACK, 5, 0, 5), 
    # Stinky Ned 
    1323 : (ToontownBattleGlobals.LURE_TRACK, 5, 0, 3), 
    # Nancy Gas 
    2308 : (ToontownBattleGlobals.LURE_TRACK, 5, 0, 3), 

    # Musicians
    # Moe Zart 
    4119 : (ToontownBattleGlobals.SOUND_TRACK, 5, 80, 5), 
    # Sid Sonata 
    4219 : (ToontownBattleGlobals.SOUND_TRACK, 5, 50, 4), 
    # Barbara Seville 
    4115 : (ToontownBattleGlobals.SOUND_TRACK, 5, 40, 3), 

    # Droppers
    # Barnacle Bessie
    1116 : (ToontownBattleGlobals.DROP_TRACK, 5, 170, 5), 
    # Franz Neckvein
    2311 : (ToontownBattleGlobals.DROP_TRACK, 5, 100, 4), 
    # Clumsy Ned 
    4140 : (ToontownBattleGlobals.DROP_TRACK, 5, 60, 3), 

    # Cogs miss
    # Mr. Freeze
    3137 : (ToontownBattleGlobals.NPC_COGS_MISS, 0, 0, 4), 
    # Flim Flam
    4327 : (ToontownBattleGlobals.NPC_COGS_MISS, 0, 0, 4), 
    # Julius Wheezer 
    4230 : (ToontownBattleGlobals.NPC_COGS_MISS, 0, 0, 4), 

    # Toons hit
    # Soggy Nell
    3135 : (ToontownBattleGlobals.NPC_TOONS_HIT, 0, 0, 4), 
    # Sticky Lou 
    2208 : (ToontownBattleGlobals.NPC_TOONS_HIT, 0, 0, 4), 
    # Soggy Bottom 
    5124 : (ToontownBattleGlobals.NPC_TOONS_HIT, 0, 0, 4), 

    # Restockers
    # Professor Pete 
    2003 : (ToontownBattleGlobals.NPC_RESTOCK_GAGS, -1, 0, 5), 
    # Professor Guffaw
    2126 : (ToontownBattleGlobals.NPC_RESTOCK_GAGS, 
            ToontownBattleGlobals.HEAL_TRACK, 0, 3),
    # Clerk Ray
    4007 : (ToontownBattleGlobals.NPC_RESTOCK_GAGS, 
            ToontownBattleGlobals.TRAP_TRACK, 0, 3),
    # Doctor Drift 
    1315 : (ToontownBattleGlobals.NPC_RESTOCK_GAGS, 
            ToontownBattleGlobals.LURE_TRACK, 0, 3),
    # Sophie Squirt
    5207 : (ToontownBattleGlobals.NPC_RESTOCK_GAGS, 
            ToontownBattleGlobals.SQUIRT_TRACK, 0, 3),
    # Baker Bridget 
    3129 : (ToontownBattleGlobals.NPC_RESTOCK_GAGS, 
            ToontownBattleGlobals.THROW_TRACK, 0, 3),
    # Melody Wavers
    4125 : (ToontownBattleGlobals.NPC_RESTOCK_GAGS,
            ToontownBattleGlobals.SOUND_TRACK, 0, 3),
    # Shelly Seaweed
    1329 : (ToontownBattleGlobals.NPC_RESTOCK_GAGS,
            ToontownBattleGlobals.DROP_TRACK, 0, 3), 
    }

def getNPCTrack(npcId):
    if (npcFriends.has_key(npcId)):
        return npcFriends[npcId][0]
    return None

def getNPCTrackHp(npcId):
    if (npcFriends.has_key(npcId)):
        track, level, hp, rarity = npcFriends[npcId]
        return track,  hp
    return None, None

def getNPCTrackLevelHp(npcId):
    if (npcFriends.has_key(npcId)):
        track, level, hp, rarity = npcFriends[npcId]
        return track, level, hp
    return None, None, None


def getNPCTrackLevelHpRarity(npcId):
    if (npcFriends.has_key(npcId)):
        return npcFriends[npcId]
    return None, None, None, None
