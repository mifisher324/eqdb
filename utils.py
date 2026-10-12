"""Utilities for EQDB"""
import os

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

here = os.path.dirname(__file__)


class ReducedItem:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


def convert_time(seconds):
    # Translate this into human readible
    hours = 0
    minutes = 0
    days = 0
    if seconds > 86400:
        days = int(seconds / 86400)
        seconds = seconds - (days * 86400)
    if seconds > 3600:
        hours = int(seconds / 3600)
        seconds = seconds - (hours * 3600)

    if seconds > 60:
        minutes = int(seconds / 60)
        seconds = seconds - (minutes * 60)

    if days > 0 and hours > 0 and minutes > 0 and seconds > 0:
        return f'{days} days, {hours} hours, {minutes} minutes, {seconds} seconds'
    elif days > 0 and hours > 0 and minutes > 0:
        return f'{days} days, {hours} hours, {minutes} minutes'
    elif days > 0 and hours > 0 and seconds > 0:
        return f'{days} days, {hours} hours, {seconds} seconds'
    elif days > 0 and minutes > 0 and seconds > 0:
        return f'{days} days, {minutes} minutes, {seconds} seconds'
    elif days > 0 and hours > 0:
        return f'{days} days, {hours} hours'
    elif days > 0 and minutes > 0:
        return f'{days} days, {minutes} minutes'
    elif days > 0 and seconds > 0:
        return f'{days} days, {seconds} seconds'
    elif days > 0:
        return f'{days} days'
    elif hours > 0 and minutes > 0 and seconds > 0:
        return f'{hours} hours, {minutes} minutes, {seconds} seconds'
    elif hours > 0 and minutes > 0:
        return f'{hours} hours, {minutes} minutes'
    elif hours > 0 and seconds > 0:
        return f'{hours} hours, {seconds} seconds'
    elif hours > 0:
        return f'{hours} hours'
    elif minutes > 0 and seconds > 0:
        return f'{minutes} minutes, {seconds} seconds'
    elif minutes > 0:
        return f'{minutes} minutes'
    else:
        return f'{seconds} seconds'


def get_spell_class(class_num):
    if class_num == 1:
        return 'Warrior'
    elif class_num == 2:
        return 'Cleric'
    elif class_num == 3:
        return 'Paladin'
    elif class_num == 4:
        return 'Ranger'
    elif class_num == 5:
        return 'Shadow Knight'
    elif class_num == 6:
        return 'Druid'
    elif class_num == 7:
        return 'Monk'
    elif class_num == 8:
        return 'Bard'
    elif class_num == 9:
        return 'Rogue'
    elif class_num == 10:
        return 'Shaman'
    elif class_num == 11:
        return 'Necromancer'
    elif class_num == 12:
        return 'Wizard'
    elif class_num == 13:
        return 'Magician'
    elif class_num == 14:
        return 'Enchanter'
    elif class_num == 15:
        return 'Beastlord'
    elif class_num == 16:
        return 'Berserker'


def get_zone_waypoint(short_name):
    if short_name == 'blackburrow':
        return {'y': 38, 'x': -7, 'z': 3}
    elif short_name == 'commons':
        return {'y': -127, 'x': 503, 'z': -51}
    elif short_name == 'ecommons':
        return {'y': -1603, 'x': -356, 'z': 3}
    elif short_name == 'feerrott':
        return {'y': -430, 'x': -1830, 'z': -51}
    elif short_name == 'freportw':
        return {'y': -283, 'x': -396, 'z': -23}
    elif short_name == 'grobb':
        return {'y': 223, 'x': -200, 'z': 3.75}
    elif short_name == 'everfrost':
        return {'y': 2133, 'x': -6972, 'z': -58}
    elif short_name == 'halas':
        return {'y': 26, 'x': 0, 'z': 3.75}
    elif short_name == 'highkeep':
        return {'y': -17, 'x': -1, 'z': -4}
    elif short_name == 'lavastorm':
        return {'y': 918, 'x': 1318, 'z': 119}
    elif short_name == 'neriakb':
        return {'y': 3, 'x': -493, 'z': -10}
    elif short_name == 'northkarana':
        return {'y': -688, 'x': -175, 'z': -7.5}
    elif short_name == 'eastkarana':
        return {'y': 1333, 'x': 423, 'z': 1}
    elif short_name == 'oasis':
        return {'y': 532, 'x': 110, 'z': 6}
    elif short_name == 'oggok':
        return {'y': 465, 'x': 513, 'z': 3.75}
    elif short_name == 'oot':
        return {'y': 394, 'x': -9172, 'z': 6}
    elif short_name == 'qey2hh1':
        return {'y': -3570, 'x': -14816, 'z': 36}
    elif short_name == 'qeynos2':
        return {'y': 165, 'x': 392, 'z': 4}
    elif short_name == 'qrg':
        return {'y': 45, 'x': -66, 'z': 4}
    elif short_name == 'rivervale':
        return {'y': -10, 'x': -140, 'z': 4}
    elif short_name == 'gukbottom':
        return {'y': 1157, 'x': -233, 'z': -80}
    elif short_name == 'lakerathe':
        return {'y': 2404, 'x': 2673, 'z': 95}
    elif short_name == 'southkarana':
        return {'y': -6689, 'x': 1027, 'z': 0}
    elif short_name == 'akanon':
        return {'y': 1279, 'x': -761, 'z': -24.25}
    elif short_name == 'cauldron':
        return {'y': -1790, 'x': -700, 'z': 100}
    elif short_name == 'felwithea':
        return {'y': 240, 'x': -626, 'z': -10.25}
    elif short_name == 'gfaydark':
        return {'y': 458, 'x': -385, 'z': 0}
    elif short_name == 'kaladima':
        return {'y': 90, 'x': 197, 'z': 3.75}
    elif short_name == 'mistmoore':
        return {'y': -294, 'x': 122, 'z': -179}
    elif short_name == 'erudnext':
        return {'y': -1216, 'x': -240, 'z': 52}
    elif short_name == 'hole':
        return {'y': 287, 'x': -543, 'z': -140}
    elif short_name == 'paineel':
        return {'y': 839, 'x': 210, 'z': 4}
    elif short_name == 'tox':
        return {'y': -1510, 'x': -916, 'z': -33}
    elif short_name == 'stonebrunt':
        return {'y': -4531, 'x': 673, 'z': 0}
    elif short_name == 'dulak':
        return {'y': -190, 'x': -1190, 'z': 4}
    elif short_name == 'gunthak':
        return {'y': 1402, 'x': -410, 'z': 3}
    elif short_name == 'burningwood':
        return {'y': 7407, 'x': -3876, 'z': -233}
    elif short_name == 'cabeast':
        return {'y': 969, 'x': -136, 'z': 4.68}
    elif short_name == 'citymist':
        return {'y': 249, 'x': -572, 'z': 4}
    elif short_name == 'dreadlands':
        return {'y': 3005, 'x': 9633, 'z': 1049}
    elif short_name == 'fieldofbone':
        return {'y': -1684, 'x': 1617, 'z': -55}
    elif short_name == 'firiona':
        return {'y': -2397, 'x': 1825, 'z': -98}
    elif short_name == 'frontiermtns':
        return {'y': 53, 'x': 392, 'z': -102}
    elif short_name == 'karnor':
        return {'y': 251, 'x': 160, 'z': 3.75}
    elif short_name == 'lakeofillomen':
        return {'y': 985, 'x': -1070, 'z': 78}
    elif short_name == 'overthere':
        return {'y': -2757, 'x': 1480, 'z': 11}
    elif short_name == 'skyfire':
        return {'y': -3100, 'x': 780, 'z': -158}
    elif short_name == 'timorous':
        return {'y': -12256.8, 'x': 4366.5, 'z': -278}
    elif short_name == 'trakanon':
        return {'y': -1620, 'x': -4720, 'z': -473}
    elif short_name == 'chardokb':
        return {'y': 315, 'x': -210, 'z': 1.5}
    elif short_name == 'cobaltscar':
        return {'y': -1064, 'x': -1633, 'z': 296}
    elif short_name == 'eastwastes':
        return {'y': -4037, 'x': 464, 'z': 144}
    elif short_name == 'greatdivide':
        return {'y': -6646, 'x': 3287, 'z': -35}
    elif short_name == 'iceclad':
        return {'y': 1300, 'x': 3127, 'z': 111}
    elif short_name == 'wakening':
        return {'y': 1455, 'x': 4552, 'z': -60}
    elif short_name == 'westwastes':
        return {'y': 1323, 'x': 808, 'z': -196}
    elif short_name == 'cobaltscar':
        return {'y': -1065, 'x': -1634, 'z': 299}
    elif short_name == 'sirens':
        return {'y': -590, 'x': 20, 'z': -93}
    elif short_name == 'dawnshroud':
        return {'y': -280, 'x': -1260, 'z': 97}
    elif short_name == 'fungusgrove':
        return {'y': 2398, 'x': 1359, 'z': -261}
    elif short_name == 'sharvahl':
        return {'y': 55, 'x': 250, 'z': -188}
    elif short_name == 'ssratemple':
        return {'y': 0, 'x': -6.5, 'z': 4}
    elif short_name == 'tenebrous':
        return {'y': -1514, 'x': -967, 'z': -56}
    elif short_name == 'umbral':
        return {'y': -640, 'x': 1840, 'z': 24}
    elif short_name == 'twilight':
        return {'y': 1338, 'x': -1028, 'z': 39}
    elif short_name == 'scarlet':
        return {'y': -956, 'x': -1777, 'z': -99}
    elif short_name == 'paludal':
        return {'y': -1175, 'x': 220, 'z': -236}
    elif short_name == 'bazaar':
        return {'y': -175, 'x': 105, 'z': -15}
    elif short_name == 'airplane':
        return {'y': 1560, 'x': 700, 'z': -680}
    elif short_name == 'fearplane':
        return {'y': -1305, 'x': 1065, 'z': 3}
    elif short_name == 'hateplaneb':
        return {'y': 680, 'x': -400, 'z': 4}
    elif short_name == 'poknowledge':
        return {'y': 50, 'x': -215, 'z': -160}
    elif short_name == 'potranquility':
        return {'y': -192, 'x': -8, 'z': -628}
    elif short_name == 'potimea':
        return {'y': 110, 'x': 0, 'z': 8}
    elif short_name == 'barindu':
        return {'y': -515, 'x': 210, 'z': -117}
    elif short_name == 'kodtaz':
        return {'y': -2422, 'x': 1536, 'z': -348}
    elif short_name == 'natimbi':
        return {'y': 125, 'x': -310, 'z': 520}
    elif short_name == 'qvic':
        return {'y': -1403, 'x': -1018, 'z': -490}
    elif short_name == 'txevu':
        return {'y': -20, 'x': -316, 'z': -420}
    elif short_name == 'wallofslaughter':
        return {'y': 13, 'x': -943, 'z': 130}
    else:
        return {}


def get_bane_dmg_body(num):
    """Returns the "Body Type" of a bane."""
    if num == 1:
        return 'Humanoid'
    elif num == 2:
        return 'Lycanthrope'
    elif num == 3:
        return 'Undead'
    elif num == 4:
        return 'Giant'
    elif num == 5:
        return 'Construct'
    elif num == 6:
        return 'Extraplanar'
    elif num == 7:
        return 'Monster'
    elif num == 8:
        return 'Undead Pet'
    elif num == 9:
        return 'Raid Giant'
    elif num == 10:
        return 'Raid Coldain'
    elif num == 11:
        return 'Untargetable'
    elif num == 12:
        return 'Vampyre'
    elif num == 13:
        return 'Atenha Ra'
    elif num == 14:
        return 'Greater Akheva'
    elif num == 15:
        return 'Khati Sha'
    elif num == 16:
        return 'Seru'
    elif num == 17:
        return 'Grieg Veneficus'
    elif num == 18:
        return 'Draz Nurakk'
    elif num == 19:
        return 'God'
    elif num == 20:
        return 'Luggald'
    elif num == 21:
        return 'Animal'
    elif num == 22:
        return 'Insect'
    elif num == 23:
        return 'Fire Creature'
    elif num == 24:
        return 'Elemental'
    elif num == 25:
        return 'Plant'
    elif num == 26:
        return 'Dragon'
    elif num == 27:
        return 'Summoned Creature'
    elif num == 28:
        return 'Summoned Creature 2'
    elif num == 29:
        return 'Dragon 2'
    elif num == 30:
        return 'Velious Dragon'
    elif num == 31:
        return 'Familiar'
    elif num == 32:
        return 'Dragon 3'
    elif num == 33:
        return 'Boxes'
    elif num == 34:
        return 'Muramite'
    elif num == 60:
        return 'Untargetable 2'
    elif num == 63:
        return 'Swarm Pet'
    elif num == 64:
        return 'Monster Summoning'
    elif num == 66:
        return 'Invisible Man'
    elif num == 67:
        return 'Special'
    elif num == 257:
        return 'Terris Thule'
    else:
        return f'Unknown body num {num}'


def get_bane_dmg_race(num):
    """Returns the "Race Type" of a bane."""
    if num == 1:
        return "Human"
    elif num == 2:
        return "Barbarian"
    elif num == 3:
        return "Erudite"
    elif num == 4:
        return "Wood Elf"
    elif num == 5:
        return "High Elf"
    elif num == 6:
        return "Dark Elf"
    elif num == 7:
        return "Half Elf"
    elif num == 8:
        return "Dwarf"
    elif num == 9:
        return "Troll"
    elif num == 10:
        return "Ogre"
    elif num == 11:
        return "Halfling"
    elif num == 12:
        return "Gnome"
    elif num == 13:
        return "Aviak"
    elif num == 14:
        return "Werewolf"
    elif num == 15:
        return "Brownie"
    elif num == 16:
        return "Centaur"
    elif num == 17:
        return "Golem"
    elif num == 18:
        return "Giant"
    elif num == 19:
        return "Trakanon"
    elif num == 20:
        return "Venril Sathir"
    elif num == 21:
        return "Evil Eye"
    elif num == 22:
        return "Beetle"
    elif num == 23:
        return "Kerran"
    elif num == 24:
        return "Fish"
    elif num == 25:
        return "Fairy"
    elif num == 26:
        return "Froglok"
    elif num == 27:
        return "Froglok"
    elif num == 28:
        return "Fungusman"
    elif num == 29:
        return "Gargoyle"
    elif num == 30:
        return "Gasbag"
    elif num == 31:
        return "Gelatinous Cube"
    elif num == 32:
        return "Ghost"
    elif num == 33:
        return "Ghoul"
    elif num == 34:
        return "Bat"
    elif num == 35:
        return "Eel"
    elif num == 36:
        return "Rat"
    elif num == 37:
        return "Snake"
    elif num == 38:
        return "Spider"
    elif num == 39:
        return "Gnoll"
    elif num == 40:
        return "Goblin"
    elif num == 41:
        return "Gorilla"
    elif num == 42:
        return "Wolf"
    elif num == 43:
        return "Bear"
    elif num == 44:
        return "Guard"
    elif num == 45:
        return "Demi Lich"
    elif num == 46:
        return "Imp"
    elif num == 47:
        return "Griffin"
    elif num == 48:
        return "Kobold"
    elif num == 49:
        return "Dragon"
    elif num == 50:
        return "Lion"
    elif num == 51:
        return "Lizard Man"
    elif num == 52:
        return "Mimic"
    elif num == 53:
        return "Minotaur"
    elif num == 54:
        return "Orc"
    elif num == 55:
        return "Beggar"
    elif num == 56:
        return "Pixie"
    elif num == 57:
        return "Drachnid"
    elif num == 58:
        return "Solusek Ro"
    elif num == 59:
        return "Goblin"
    elif num == 60:
        return "Skeleton"
    elif num == 61:
        return "Shark"
    elif num == 62:
        return "Tunare"
    elif num == 63:
        return "Tiger"
    elif num == 64:
        return "Treant"
    elif num == 65:
        return "Vampire"
    elif num == 66:
        return "Rallos Zek"
    elif num == 67:
        return "Human"
    elif num == 68:
        return "Tentacle Terror"
    elif num == 69:
        return "Will-O-Wisp"
    elif num == 70:
        return "Zombie"
    elif num == 71:
        return "Human"
    elif num == 72:
        return "Ship"
    elif num == 73:
        return "Launch"
    elif num == 74:
        return "Piranha"
    elif num == 75:
        return "Elemental"
    elif num == 76:
        return "Puma"
    elif num == 77:
        return "Dark Elf"
    elif num == 78:
        return "Erudite"
    elif num == 79:
        return "Bixie"
    elif num == 80:
        return "Reanimated Hand"
    elif num == 81:
        return "Halfling"
    elif num == 82:
        return "Scarecrow"
    elif num == 83:
        return "Skunk"
    elif num == 84:
        return "Snake Elemental"
    elif num == 85:
        return "Spectre"
    elif num == 86:
        return "Sphinx"
    elif num == 87:
        return "Armadillo"
    elif num == 88:
        return "Clockwork Gnome"
    elif num == 89:
        return "Drake"
    elif num == 90:
        return "Barbarian"
    elif num == 91:
        return "Alligator"
    elif num == 92:
        return "Troll"
    elif num == 93:
        return "Ogre"
    elif num == 94:
        return "Dwarf"
    elif num == 95:
        return "Cazic Thule"
    elif num == 96:
        return "Cockatrice"
    elif num == 97:
        return "Daisy Man"
    elif num == 98:
        return "Vampire"
    elif num == 99:
        return "Amygdalan"
    elif num == 100:
        return "Dervish"
    elif num == 101:
        return "Efreeti"
    elif num == 102:
        return "Tadpole"
    elif num == 103:
        return "Kedge"
    elif num == 104:
        return "Leech"
    elif num == 105:
        return "Swordfish"
    elif num == 106:
        return "Guard"
    elif num == 107:
        return "Mammoth"
    elif num == 108:
        return "Eye"
    elif num == 109:
        return "Wasp"
    elif num == 110:
        return "Mermaid"
    elif num == 111:
        return "Harpy"
    elif num == 112:
        return "Guard"
    elif num == 113:
        return "Drixie"
    elif num == 114:
        return "Ghost Ship"
    elif num == 115:
        return "Clam"
    elif num == 116:
        return "Seahorse"
    elif num == 117:
        return "Ghost"
    elif num == 118:
        return "Ghost"
    elif num == 119:
        return "Sabertooth"
    elif num == 120:
        return "Wolf"
    elif num == 121:
        return "Gorgon"
    elif num == 122:
        return "Dragon"
    elif num == 123:
        return "Innoruuk"
    elif num == 124:
        return "Unicorn"
    elif num == 125:
        return "Pegasus"
    elif num == 126:
        return "Djinn"
    elif num == 127:
        return "Invisible Man"
    elif num == 128:
        return "Iksar"
    elif num == 129:
        return "Scorpion"
    elif num == 130:
        return "Vah Shir"
    elif num == 131:
        return "Sarnak"
    elif num == 132:
        return "Draglock"
    elif num == 133:
        return "Drolvarg"
    elif num == 134:
        return "Mosquito"
    elif num == 135:
        return "Rhinoceros"
    elif num == 136:
        return "Xalgoz"
    elif num == 137:
        return "Goblin"
    elif num == 138:
        return "Yeti"
    elif num == 139:
        return "Iksar"
    elif num == 140:
        return "Giant"
    elif num == 141:
        return "Boat"
    elif num == 144:
        return "Burynai"
    elif num == 145:
        return "Goo"
    elif num == 146:
        return "Sarnak Spirit"
    elif num == 147:
        return "Iksar Spirit"
    elif num == 148:
        return "Fish"
    elif num == 149:
        return "Scorpion"
    elif num == 150:
        return "Erollisi"
    elif num == 151:
        return "Tribunal"
    elif num == 152:
        return "Bertoxxulous"
    elif num == 153:
        return "Bristlebane"
    elif num == 154:
        return "Fay Drake"
    elif num == 155:
        return "Undead Sarnak"
    elif num == 156:
        return "Ratman"
    elif num == 157:
        return "Wyvern"
    elif num == 158:
        return "Wurm"
    elif num == 159:
        return "Devourer"
    elif num == 160:
        return "Iksar Golem"
    elif num == 161:
        return "Undead Iksar"
    elif num == 162:
        return "Man-Eating Plant"
    elif num == 163:
        return "Raptor"
    elif num == 164:
        return "Sarnak Golem"
    elif num == 165:
        return "Dragon"
    elif num == 166:
        return "Animated Hand"
    elif num == 167:
        return "Succulent"
    elif num == 168:
        return "Holgresh"
    elif num == 169:
        return "Brontotherium"
    elif num == 170:
        return "Snow Dervish"
    elif num == 171:
        return "Dire Wolf"
    elif num == 172:
        return "Manticore"
    elif num == 173:
        return "Totem"
    elif num == 174:
        return "Ice Spectre"
    elif num == 175:
        return "Enchanted Armor"
    elif num == 176:
        return "Snow Rabbit"
    elif num == 177:
        return "Walrus"
    elif num == 178:
        return "Geonid"
    elif num == 181:
        return "Yakkar"
    elif num == 182:
        return "Faun"
    elif num == 183:
        return "Coldain"
    elif num == 184:
        return "Dragon"
    elif num == 185:
        return "Hag"
    elif num == 186:
        return "Hippogriff"
    elif num == 187:
        return "Siren"
    elif num == 188:
        return "Giant"
    elif num == 189:
        return "Giant"
    elif num == 190:
        return "Othmir"
    elif num == 191:
        return "Ulthork"
    elif num == 192:
        return "Dragon"
    elif num == 193:
        return "Abhorrent"
    elif num == 194:
        return "Sea Turtle"
    elif num == 195:
        return "Dragon"
    elif num == 196:
        return "Dragon"
    elif num == 197:
        return "Ronnie Test"
    elif num == 198:
        return "Dragon"
    elif num == 199:
        return "Shik'Nar"
    elif num == 200:
        return "Rockhopper"
    elif num == 201:
        return "Underbulk"
    elif num == 202:
        return "Grimling"
    elif num == 203:
        return "Worm"
    elif num == 204:
        return "Evan Test"
    elif num == 205:
        return "Shadel"
    elif num == 206:
        return "Owlbear"
    elif num == 207:
        return "Rhino Beetle"
    elif num == 208:
        return "Vampire"
    elif num == 209:
        return "Earth Elemental"
    elif num == 210:
        return "Air Elemental"
    elif num == 211:
        return "Water Elemental"
    elif num == 212:
        return "Fire Elemental"
    elif num == 213:
        return "Wetfang Minnow"
    elif num == 214:
        return "Thought Horror"
    elif num == 215:
        return "Tegi"
    elif num == 216:
        return "Horse"
    elif num == 217:
        return "Shissar"
    elif num == 218:
        return "Fungal Fiend"
    elif num == 219:
        return "Vampire"
    elif num == 220:
        return "Stonegrabber"
    elif num == 221:
        return "Scarlet Cheetah"
    elif num == 222:
        return "Zelniak"
    elif num == 223:
        return "Lightcrawler"
    elif num == 224:
        return "Shade"
    elif num == 225:
        return "Sunfbelow"
    elif num == 226:
        return "Sun Revenant"
    elif num == 227:
        return "Shrieker"
    elif num == 228:
        return "Galorian"
    elif num == 229:
        return "Netherbian"
    elif num == 230:
        return "Akheva"
    elif num == 231:
        return "Grieg Veneficus"
    elif num == 232:
        return "Sonic Wolf"
    elif num == 233:
        return "Ground Shaker"
    elif num == 234:
        return "Vah Shir Skeleton"
    elif num == 235:
        return "Wretch"
    elif num == 236:
        return "Seru"
    elif num == 237:
        return "Recuso"
    elif num == 238:
        return "Vah Shir"
    elif num == 239:
        return "Guard"
    elif num == 240:
        return "Teleport Man"
    elif num == 241:
        return "Werewolf"
    elif num == 242:
        return "Nymph"
    elif num == 243:
        return "Dryad"
    elif num == 244:
        return "Treant"
    elif num == 245:
        return "Fly"
    elif num == 246:
        return "Tarew Marr"
    elif num == 247:
        return "Solusek Ro"
    elif num == 248:
        return "Clockwork Golem"
    elif num == 249:
        return "Clockwork Brain"
    elif num == 250:
        return "Banshee"
    elif num == 251:
        return "Guard of Justice"
    elif num == 252:
        return "Mini POM"
    elif num == 253:
        return "Diseased Fiend"
    elif num == 254:
        return "Solusek Ro Guard"
    elif num == 255:
        return "Bertoxxulous"
    elif num == 256:
        return "The Tribunal"
    elif num == 257:
        return "Terris Thule"
    elif num == 258:
        return "Vegerog"
    elif num == 259:
        return "Crocodile"
    elif num == 260:
        return "Bat"
    elif num == 261:
        return "Hraquis"
    elif num == 262:
        return "Tranquilion"
    elif num == 263:
        return "Tin Soldier"
    elif num == 264:
        return "Nightmare Wraith"
    elif num == 265:
        return "Malarian"
    elif num == 266:
        return "Knight of Pestilence"
    elif num == 267:
        return "Lepertoloth"
    elif num == 268:
        return "Bubonian"
    elif num == 269:
        return "Bubonian Underling"
    elif num == 270:
        return "Pusling"
    elif num == 271:
        return "Water Mephit"
    elif num == 272:
        return "Stormrider"
    elif num == 273:
        return "Junk Beast"
    elif num == 274:
        return "Broken Clockwork"
    elif num == 275:
        return "Giant Clockwork"
    elif num == 276:
        return "Clockwork Beetle"
    elif num == 277:
        return "Nightmare Goblin"
    elif num == 278:
        return "Karana"
    elif num == 279:
        return "Blood Raven"
    elif num == 280:
        return "Nightmare Gargoyle"
    elif num == 281:
        return "Mouth of Insanity"
    elif num == 282:
        return "Skeletal Horse"
    elif num == 283:
        return "Saryrn"
    elif num == 284:
        return "Fennin Ro"
    elif num == 285:
        return "Tormentor"
    elif num == 286:
        return "Soul Devourer"
    elif num == 287:
        return "Nightmare"
    elif num == 288:
        return "Rallos Zek"
    elif num == 289:
        return "Vallon Zek"
    elif num == 290:
        return "Tallon Zek"
    elif num == 291:
        return "Air Mephit"
    elif num == 292:
        return "Earth Mephit"
    elif num == 293:
        return "Fire Mephit"
    elif num == 294:
        return "Nightmare Mephit"
    elif num == 295:
        return "Zebuxoruk"
    elif num == 296:
        return "Mithaniel Marr"
    elif num == 297:
        return "Undead Knight"
    elif num == 298:
        return "The Rathe"
    elif num == 299:
        return "Xegony"
    elif num == 300:
        return "Fiend"
    elif num == 301:
        return "Test Object"
    elif num == 302:
        return "Crab"
    elif num == 303:
        return "Phoenix"
    elif num == 304:
        return "Dragon"
    elif num == 305:
        return "Bear"
    elif num == 306:
        return "Giant"
    elif num == 307:
        return "Giant"
    elif num == 308:
        return "Giant"
    elif num == 309:
        return "Giant"
    elif num == 310:
        return "Giant"
    elif num == 311:
        return "Giant"
    elif num == 312:
        return "Giant"
    elif num == 313:
        return "War Wraith"
    elif num == 314:
        return "Wrulon"
    elif num == 315:
        return "Kraken"
    elif num == 316:
        return "Poison Frog"
    elif num == 317:
        return "Nilborien"
    elif num == 318:
        return "Valorian"
    elif num == 319:
        return "War Boar"
    elif num == 320:
        return "Efreeti"
    elif num == 321:
        return "War Boar"
    elif num == 322:
        return "Valorian"
    elif num == 323:
        return "Animated Armor"
    elif num == 324:
        return "Undead Footman"
    elif num == 325:
        return "Rallos Zek Minion"
    elif num == 326:
        return "Arachnid"
    elif num == 327:
        return "Crystal Spider"
    elif num == 328:
        return "Zebuxoruk's Cage"
    elif num == 329:
        return "BoT Portal"
    elif num == 330:
        return "Froglok"
    elif num == 331:
        return "Troll"
    elif num == 332:
        return "Troll"
    elif num == 333:
        return "Troll"
    elif num == 334:
        return "Ghost"
    elif num == 335:
        return "Pirate"
    elif num == 336:
        return "Pirate"
    elif num == 337:
        return "Pirate"
    elif num == 338:
        return "Pirate"
    elif num == 339:
        return "Pirate"
    elif num == 340:
        return "Pirate"
    elif num == 341:
        return "Pirate"
    elif num == 342:
        return "Pirate"
    elif num == 343:
        return "Frog"
    elif num == 344:
        return "Troll Zombie"
    elif num == 345:
        return "Luggald"
    elif num == 346:
        return "Luggald"
    elif num == 347:
        return "Luggalds"
    elif num == 348:
        return "Drogmore"
    elif num == 349:
        return "Froglok Skeleton"
    elif num == 350:
        return "Undead Froglok"
    elif num == 351:
        return "Knight of Hate"
    elif num == 352:
        return "Arcanist of Hate"
    elif num == 353:
        return "Veksar"
    elif num == 354:
        return "Veksar"
    elif num == 355:
        return "Veksar"
    elif num == 356:
        return "Chokidai"
    elif num == 357:
        return "Undead Chokidai"
    elif num == 358:
        return "Undead Veksar"
    elif num == 359:
        return "Vampire"
    elif num == 360:
        return "Vampire"
    elif num == 361:
        return "Rujarkian Orc"
    elif num == 362:
        return "Bone Golem"
    elif num == 363:
        return "Synarcana"
    elif num == 364:
        return "Sand Elf"
    elif num == 365:
        return "Vampire"
    elif num == 366:
        return "Rujarkian Orc"
    elif num == 367:
        return "Skeleton"
    elif num == 368:
        return "Mummy"
    elif num == 369:
        return "Goblin"
    elif num == 370:
        return "Insect"
    elif num == 371:
        return "Froglok Ghost"
    elif num == 372:
        return "Dervish"
    elif num == 373:
        return "Shade"
    elif num == 374:
        return "Golem"
    elif num == 375:
        return "Evil Eye"
    elif num == 376:
        return "Box"
    elif num == 377:
        return "Barrel"
    elif num == 378:
        return "Chest"
    elif num == 379:
        return "Vase"
    elif num == 380:
        return "Table"
    elif num == 381:
        return "Weapon Rack"
    elif num == 382:
        return "Coffin"
    elif num == 383:
        return "Bones"
    elif num == 384:
        return "Jokester"
    elif num == 385:
        return "Nihil"
    elif num == 386:
        return "Trusik"
    elif num == 387:
        return "Stone Worker"
    elif num == 388:
        return "Hynid"
    elif num == 389:
        return "Turepta"
    elif num == 390:
        return "Cragbeast"
    elif num == 391:
        return "Stonemite"
    elif num == 392:
        return "Ukun"
    elif num == 393:
        return "Ixt"
    elif num == 394:
        return "Ikaav"
    elif num == 395:
        return "Aneuk"
    elif num == 396:
        return "Kyv"
    elif num == 397:
        return "Noc"
    elif num == 398:
        return "Ratuk"
    elif num == 399:
        return "Taneth"
    elif num == 400:
        return "Huvul"
    elif num == 401:
        return "Mutna"
    elif num == 402:
        return "Mastruq"
    elif num == 403:
        return "Taelosian"
    elif num == 404:
        return "Discord Ship"
    elif num == 405:
        return "Stone Worker"
    elif num == 406:
        return "Mata Muram"
    elif num == 407:
        return "Lightning Warrior"
    elif num == 408:
        return "Succubus"
    elif num == 409:
        return "Bazu"
    elif num == 410:
        return "Feran"
    elif num == 411:
        return "Pyrilen"
    elif num == 412:
        return "Chimera"
    elif num == 413:
        return "Dragorn"
    elif num == 414:
        return "Murkglider"
    elif num == 415:
        return "Rat"
    elif num == 416:
        return "Bat"
    elif num == 417:
        return "Gelidran"
    elif num == 418:
        return "Discordling"
    elif num == 419:
        return "Girplan"
    elif num == 420:
        return "Minotaur"
    elif num == 421:
        return "Dragorn Box"
    elif num == 422:
        return "Runed Orb"
    elif num == 423:
        return "Dragon Bones"
    elif num == 424:
        return "Muramite Armor Pile"
    elif num == 425:
        return "Crystal Shard"
    elif num == 426:
        return "Portal"
    elif num == 427:
        return "Coin Purse"
    elif num == 428:
        return "Rock Pile"
    elif num == 429:
        return "Murkglider Egg Sack"
    elif num == 430:
        return "Drake"
    elif num == 431:
        return "Dervish"
    elif num == 432:
        return "Drake"
    elif num == 433:
        return "Goblin"
    elif num == 434:
        return "Kirin"
    elif num == 435:
        return "Dragon"
    elif num == 436:
        return "Basilisk"
    elif num == 437:
        return "Dragon"
    elif num == 438:
        return "Dragon"
    elif num == 439:
        return "Puma"
    elif num == 440:
        return "Spider"
    elif num == 441:
        return "Spider Queen"
    elif num == 442:
        return "Animated Statue"
    elif num == 445:
        return "Dragon Egg"
    elif num == 446:
        return "Dragon Statue"
    elif num == 447:
        return "Lava Rock"
    elif num == 448:
        return "Animated Statue"
    elif num == 449:
        return "Spider Egg Sack"
    elif num == 450:
        return "Lava Spider"
    elif num == 451:
        return "Lava Spider Queen"
    elif num == 452:
        return "Dragon"
    elif num == 453:
        return "Giant"
    elif num == 454:
        return "Werewolf"
    elif num == 455:
        return "Kobold"
    elif num == 456:
        return "Sporali"
    elif num == 457:
        return "Gnomework"
    elif num == 458:
        return "Orc"
    elif num == 459:
        return "Corathus"
    elif num == 460:
        return "Coral"
    elif num == 461:
        return "Drachnid"
    elif num == 462:
        return "Drachnid Cocoon"
    elif num == 463:
        return "Fungus Patch"
    elif num == 464:
        return "Gargoyle"
    elif num == 465:
        return "Witheran"
    elif num == 466:
        return "Dark Lord"
    elif num == 467:
        return "Shiliskin"
    elif num == 468:
        return "Snake"
    elif num == 469:
        return "Evil Eye"
    elif num == 470:
        return "Minotaur"
    elif num == 471:
        return "Zombie"
    elif num == 472:
        return "Clockwork Boar"
    elif num == 473:
        return "Fairy"
    elif num == 474:
        return "Witheran"
    elif num == 475:
        return "Air Elemental"
    elif num == 476:
        return "Earth Elemental"
    elif num == 477:
        return "Fire Elemental"
    elif num == 478:
        return "Water Elemental"
    elif num == 479:
        return "Alligator"
    elif num == 480:
        return "Bear"
    elif num == 481:
        return "Scaled Wolf"
    elif num == 482:
        return "Wolf"
    elif num == 483:
        return "Spirit Wolf"
    elif num == 484:
        return "Skeleton"
    elif num == 485:
        return "Spectre"
    elif num == 486:
        return "Bolvirk"
    elif num == 487:
        return "Banshee"
    elif num == 488:
        return "Banshee"
    elif num == 489:
        return "Elddar"
    elif num == 490:
        return "Forest Giant"
    elif num == 491:
        return "Bone Golem"
    elif num == 492:
        return "Horse"
    elif num == 493:
        return "Pegasus"
    elif num == 494:
        return "Shambling Mound"
    elif num == 495:
        return "Scrykin"
    elif num == 496:
        return "Treant"
    elif num == 497:
        return "Vampire"
    elif num == 498:
        return "Ayonae Ro"
    elif num == 499:
        return "Sullon Zek"
    elif num == 500:
        return "Banner"
    elif num == 501:
        return "Flag"
    elif num == 502:
        return "Rowboat"
    elif num == 503:
        return "Bear Trap"
    elif num == 504:
        return "Clockwork Bomb"
    elif num == 505:
        return "Dynamite Keg"
    elif num == 506:
        return "Pressure Plate"
    elif num == 507:
        return "Puffer Spore"
    elif num == 508:
        return "Stone Ring"
    elif num == 509:
        return "Root Tentacle"
    elif num == 510:
        return "Runic Symbol"
    elif num == 511:
        return "Saltpetter Bomb"
    elif num == 512:
        return "Floating Skull"
    elif num == 513:
        return "Spike Trap"
    elif num == 514:
        return "Totem"
    elif num == 515:
        return "Web"
    elif num == 516:
        return "Wicker Basket"
    elif num == 517:
        return "Nightmare/Unicorn"
    elif num == 518:
        return "Horse"
    elif num == 519:
        return "Nightmare/Unicorn"
    elif num == 520:
        return "Bixie"
    elif num == 521:
        return "Centaur"
    elif num == 522:
        return "Drakkin"
    elif num == 523:
        return "Giant"
    elif num == 524:
        return "Gnoll"
    elif num == 525:
        return "Griffin"
    elif num == 526:
        return "Giant Shade"
    elif num == 527:
        return "Harpy"
    elif num == 528:
        return "Mammoth"
    elif num == 529:
        return "Satyr"
    elif num == 530:
        return "Dragon"
    elif num == 531:
        return "Dragon"
    elif num == 532:
        return "Dyn'Leth"
    elif num == 533:
        return "Boat"
    elif num == 534:
        return "Weapon Rack"
    elif num == 535:
        return "Armor Rack"
    elif num == 536:
        return "Honey Pot"
    elif num == 537:
        return "Jum Jum Bucket"
    elif num == 538:
        return "Toolbox"
    elif num == 539:
        return "Stone Jug"
    elif num == 540:
        return "Small Plant"
    elif num == 541:
        return "Medium Plant"
    elif num == 542:
        return "Tall Plant"
    elif num == 543:
        return "Wine Cask"
    elif num == 544:
        return "Elven Boat"
    elif num == 545:
        return "Gnomish Boat"
    elif num == 546:
        return "Barrel Barge Ship"
    elif num == 547:
        return "Goo"
    elif num == 548:
        return "Goo"
    elif num == 549:
        return "Goo"
    elif num == 550:
        return "Merchant Ship"
    elif num == 551:
        return "Pirate Ship"
    elif num == 552:
        return "Ghost Ship"
    elif num == 553:
        return "Banner"
    elif num == 554:
        return "Banner"
    elif num == 555:
        return "Banner"
    elif num == 556:
        return "Banner"
    elif num == 557:
        return "Banner"
    elif num == 558:
        return "Aviak"
    elif num == 559:
        return "Beetle"
    elif num == 560:
        return "Gorilla"
    elif num == 561:
        return "Kedge"
    elif num == 562:
        return "Kerran"
    elif num == 563:
        return "Shissar"
    elif num == 564:
        return "Siren"
    elif num == 565:
        return "Sphinx"
    elif num == 566:
        return "Human"
    elif num == 567:
        return "Campfire"
    elif num == 568:
        return "Brownie"
    elif num == 569:
        return "Dragon"
    elif num == 570:
        return "Exoskeleton"
    elif num == 571:
        return "Ghoul"
    elif num == 572:
        return "Clockwork Guardian"
    elif num == 573:
        return "Mantrap"
    elif num == 574:
        return "Minotaur"
    elif num == 575:
        return "Scarecrow"
    elif num == 576:
        return "Shade"
    elif num == 577:
        return "Rotocopter"
    elif num == 578:
        return "Tentacle Terror"
    elif num == 579:
        return "Wereorc"
    elif num == 580:
        return "Worg"
    elif num == 581:
        return "Wyvern"
    elif num == 582:
        return "Chimera"
    elif num == 583:
        return "Kirin"
    elif num == 584:
        return "Puma"
    elif num == 585:
        return "Boulder"
    elif num == 586:
        return "Banner"
    elif num == 587:
        return "Elven Ghost"
    elif num == 588:
        return "Human Ghost"
    elif num == 589:
        return "Chest"
    elif num == 590:
        return "Chest"
    elif num == 591:
        return "Crystal"
    elif num == 592:
        return "Coffin"
    elif num == 593:
        return "Guardian CPU"
    elif num == 594:
        return "Worg"
    elif num == 595:
        return "Mansion"
    elif num == 596:
        return "Floating Island"
    elif num == 597:
        return "Cragslither"
    elif num == 598:
        return "Wrulon"
    elif num == 600:
        return "Invisible Man of Zomm"
    elif num == 601:
        return "Robocopter of Zomm"
    elif num == 602:
        return "Burynai"
    elif num == 603:
        return "Frog"
    elif num == 604:
        return "Dracolich"
    elif num == 605:
        return "Iksar Ghost"
    elif num == 606:
        return "Iksar Skeleton"
    elif num == 607:
        return "Mephit"
    elif num == 608:
        return "Muddite"
    elif num == 609:
        return "Raptor"
    elif num == 610:
        return "Sarnak"
    elif num == 611:
        return "Scorpion"
    elif num == 612:
        return "Tsetsian"
    elif num == 613:
        return "Wurm"
    elif num == 614:
        return "Nekhon"
    elif num == 615:
        return "Hydra Crystal"
    elif num == 616:
        return "Crystal Sphere"
    elif num == 617:
        return "Gnoll"
    elif num == 618:
        return "Sokokar"
    elif num == 619:
        return "Stone Pylon"
    elif num == 620:
        return "Demon Vulture"
    elif num == 621:
        return "Wagon"
    elif num == 622:
        return "God of Discord"
    elif num == 623:
        return "Feran Mount"
    elif num == 624:
        return "Ogre NPC"
    elif num == 625:
        return "Sokokar Mount"
    elif num == 626:
        return "Giant"
    elif num == 627:
        return "Sokokar"
    elif num == 628:
        return "10th Anniversary Banner"
    elif num == 629:
        return "10th Anniversary Cake"
    elif num == 630:
        return "Wine Cask"
    elif num == 631:
        return "Hydra Mount"
    elif num == 632:
        return "Hydra NPC"
    elif num == 633:
        return "Wedding Fbelows"
    elif num == 634:
        return "Wedding Arbor"
    elif num == 635:
        return "Wedding Altar"
    elif num == 636:
        return "Powder Keg"
    elif num == 637:
        return "Apexus"
    elif num == 638:
        return "Bellikos"
    elif num == 639:
        return "Brell's First Creation"
    elif num == 640:
        return "Brell"
    elif num == 641:
        return "Crystalskin Ambuloid"
    elif num == 642:
        return "Cliknar Queen"
    elif num == 643:
        return "Cliknar Soldier"
    elif num == 644:
        return "Cliknar Worker"
    elif num == 645:
        return "Coldain"
    elif num == 646:
        return "Coldain"
    elif num == 647:
        return "Crystalskin Sessiloid"
    elif num == 648:
        return "Genari"
    elif num == 649:
        return "Gigyn"
    elif num == 650:
        return "Greken"
    elif num == 651:
        return "Greken"
    elif num == 652:
        return "Cliknar Mount"
    elif num == 653:
        return "Telmira"
    elif num == 654:
        return "Spider Mount"
    elif num == 655:
        return "Bear Mount"
    elif num == 656:
        return "Rat Mount"
    elif num == 657:
        return "Sessiloid Mount"
    elif num == 658:
        return "Morell Thule"
    elif num == 659:
        return "Marionette"
    elif num == 660:
        return "Book Dervish"
    elif num == 661:
        return "Topiary Lion"
    elif num == 662:
        return "Rotdog"
    elif num == 663:
        return "Amygdalan"
    elif num == 664:
        return "Sandman"
    elif num == 665:
        return "Grandfather Clock"
    elif num == 666:
        return "Gingerbread Man"
    elif num == 667:
        return "Royal Guard"
    elif num == 668:
        return "Rabbit"
    elif num == 669:
        return "Blind Dreamer"
    elif num == 670:
        return "Cazic Thule"
    elif num == 671:
        return "Topiary Lion Mount"
    elif num == 672:
        return "Rot Dog Mount"
    elif num == 673:
        return "Goral Mount"
    elif num == 674:
        return "Selyrah Mount"
    elif num == 675:
        return "Sclera Mount"
    elif num == 676:
        return "Braxi Mount"
    elif num == 677:
        return "Kangon Mount"
    elif num == 678:
        return "Erudite"
    elif num == 679:
        return "Wurm Mount"
    elif num == 680:
        return "Raptor Mount"
    elif num == 681:
        return "Invisible Man"
    elif num == 682:
        return "Whirligig"
    elif num == 683:
        return "Gnomish Balloon"
    elif num == 684:
        return "Gnomish Rocket Pack"
    elif num == 685:
        return "Gnomish Hovering Transport"
    elif num == 686:
        return "Selyrah"
    elif num == 687:
        return "Goral"
    elif num == 688:
        return "Braxi"
    elif num == 689:
        return "Kangon"
    elif num == 690:
        return "Invisible Man"
    elif num == 691:
        return "Floating Tower"
    elif num == 692:
        return "Explosive Cart"
    elif num == 693:
        return "Blimp Ship"
    elif num == 694:
        return "Tumbleweed"
    elif num == 695:
        return "Alaran"
    elif num == 696:
        return "Swinetor"
    elif num == 697:
        return "Triumvirate"
    elif num == 698:
        return "Hadal"
    elif num == 699:
        return "Hovering Platform"
    elif num == 700:
        return "Parasitic Scavenger"
    elif num == 701:
        return "Grendlaen"
    elif num == 702:
        return "Ship in a Bottle"
    elif num == 703:
        return "Alaran Sentry Stone"
    elif num == 704:
        return "Dervish"
    elif num == 705:
        return "Regeneration Pool"
    elif num == 706:
        return "Teleportation Stand"
    elif num == 707:
        return "Relic Case"
    elif num == 708:
        return "Alaran Ghost"
    elif num == 709:
        return "Skystrider"
    elif num == 710:
        return "Water Spout"
    elif num == 711:
        return "Aviak Pull Along"
    elif num == 712:
        return "Gelatinous Cube"
    elif num == 713:
        return "Cat"
    elif num == 714:
        return "Elk Head"
    elif num == 715:
        return "Holgresh"
    elif num == 716:
        return "Beetle"
    elif num == 717:
        return "Vine Maw"
    elif num == 718:
        return "Ratman"
    elif num == 719:
        return "Fallen Knight"
    elif num == 720:
        return "Flying Carpet"
    elif num == 721:
        return "Carrier Hand"
    elif num == 722:
        return "Akheva"
    elif num == 723:
        return "Servant of Shadow"
    elif num == 724:
        return "Luclin"
    elif num == 725:
        return "Xaric"
    elif num == 726:
        return "Dervish"
    elif num == 727:
        return "Dervish"
    elif num == 728:
        return "Luclin"
    elif num == 729:
        return "Luclin"
    elif num == 730:
        return "Orb"
    elif num == 731:
        return "Luclin"
    elif num == 732:
        return "Pegasus"
    elif num == 2250:
        return "Interactive Object"
    elif num == 2254:
        return "Node"
    else:
        return f'Unknown Race {num}'


def get_elem_dmg_type(num):
    """Returns the elemental damage type."""
    if num == 1:
        return 'Magic'
    elif num == 2:
        return 'Fire'
    elif num == 3:
        return 'Cold'
    elif num == 4:
        return 'Poison'
    elif num == 5:
        return 'Disease'
    elif num == 6:
        return 'Chromatic'
    elif num == 7:
        return 'Prismatic'
    elif num == 8:
        return 'Phys'
    elif num == 9:
        return 'Corruption'
    else:
        raise Exception(f'Unknown elemental type: {num}')


def translate_specials(spc):
    specials = []
    if 'E' in spc:
        specials.append('Enrages')
    if 'F' in spc:
        specials.append('Flurries')
    if 'R' in spc:
        specials.append('Rampages')
    if 'r' in spc:
        specials.append('Wild Rampages')
    if 'S' in spc:
        specials.append('Summons')
    if 'T' in spc:
        specials.append('Triple Attacks')
    if 'Q' in spc:
        specials.append('Quad Attacks')
    if 'b' in spc:
        specials.append('Bane Attacks')
    if 'm' in spc:
        specials.append('Magical Attacks')
    if 'U' in spc:
        specials.append('Immune to Slow')
    if 'C' in spc:
        specials.append('Immune to Charm')
    if 'N' in spc:
        specials.append('Immune to Stuns')
    if 'I' in spc:
        specials.append('Immune to Snare')
    if 'D' in spc:
        specials.append('Immune to Slow')
    if 'K' in spc:
        specials.append('Immune to Dispel Magic')
    if 'A' in spc:
        specials.append('Immune to Melee')
    if 'B' in spc:
        specials.append('Immune to Magic')
    if 'f' in spc:
        specials.append('Will not flee')
    if 'O' in spc:
        specials.append('Immune to non-bane Melee')
    if 'W' in spc:
        specials.append('Immune to non-magical Melee')
    if 'G' in spc:
        specials.append('Cannot be agroed')
    if 'g' in spc:
        specials.append('Belly Caster')
    if 'd' in spc:
        specials.append('Ignores Feign Death')
    if 'Y' in spc:
        specials.append('Has a Ranged Attack')
    if 'L' in spc:
        specials.append('Dual Wields')
    if 't' in spc:
        specials.append('Focused Hate')
    if 'n' in spc:
        specials.append('Does not buff/heal friends')
    if 'p' in spc:
        specials.append('Immune to Pacify')
    if 'J' in spc:
        specials.append('Leashed to combat area')
    if 'j' in spc:
        specials.append('Thetered to combat area')
    if 'o' in spc:
        specials.append('Destructible Object')
    if 'Z' in spc:
        specials.append('Immune to player damage')
    if 'i' in spc:
        specials.append('Immune to Taunt')
    if 'e' in spc:
        specials.append('Will always flee')
    if 'h' in spc:
        specials.append('Flee at low percent health')

    return specials


def get_all_skills():
    return [{0: '1H Blunt'},
            {1: '1H Slashing'},
            {2: '2H Blunt'},
            {3: '2H Slashing'},
            {4: 'Abjuration'},
            {5: 'Alteration'},
            {6: 'Apply Poison'},
            {7: 'Archery'},
            {8: 'Backstab'},
            {9: 'Bind Wound'},
            {10: 'Bash'},
            {11: 'Block'},
            {12: 'Brass Instruments'},
            {13: 'Channeling'},
            {14: 'Conjuration'},
            {15: 'Defense'},
            {16: 'Disarm'},
            {17: 'Disarm Traps'},
            {18: 'Divination'},
            {19: 'Dodge'},
            {20: 'Double Attack'},
            {21: 'Dragon Punch'},
            {22: 'Dual Wield'},
            {23: 'Eagle Strike'},
            {24: 'Evocation'},
            {25: 'Feign Death'},
            {26: 'Flying Kick'},
            {27: 'Forage'},
            {28: 'Hand to Hand'},
            {29: 'Hide'},
            {30: 'Kick'},
            {31: 'Meditate'},
            {32: 'Mend'},
            {33: 'Offense'},
            {34: 'Parry'},
            {35: 'Pick Lock'},
            {36: '1H Piercing'},
            {37: 'Riposte'},
            {38: 'Round Kick'},
            {39: 'Safe Fall'},
            {40: 'Sense Heading'},
            {41: 'Singing'},
            {42: 'Sneak'},
            {43: 'Specialize Abjure'},
            {44: 'Specialize Alteration'},
            {45: 'Specialize Conjuration'},
            {46: 'Specialize Divination'},
            {47: 'Specialize Evocation'},
            {48: 'Pick Pockets'},
            {49: 'Stringed Instruments'},
            {50: 'Swimming'},
            {51: 'Throwing'},
            {52: 'Tiger Claw'},
            {53: 'Tracking'},
            {54: 'Wind Instruments'},
            {55: 'Fishing'},
            {56: 'Make Poison'},
            {57: 'Tinkering'},
            {58: 'Research'},
            {59: 'Alchemy'},
            {60: 'Baking'},
            {61: 'Tailoring'},
            {62: 'Sense Traps'},
            {63: 'Blacksmithing'},
            {64: 'Fletching'},
            {65: 'Brewing'},
            {66: 'Alcohol Tolerance'},
            {67: 'Begging'},
            {68: 'Jewelry Making'},
            {69: 'Pottery'},
            {70: 'Percussion Instruments'},
            {71: 'Intimidation'},
            {72: 'Berserking'},
            {73: 'Taunt'},
            {74: 'Frenzy'},
            {75: 'Remove Trap'},
            {76: 'Triple Attack'},
            {77: '2H Piercing'}]


def get_aug_restrict(num):
    if num == 0:
        return 'No Restrictions'
    elif num == 1:
        return 'Armor Only'
    elif num == 2:
        return 'Weapons Only'
    elif num == 3:
        return 'One-Handed Weapons Only'
    elif num == 4:
        return 'Two-Handed Weapons ONly'
    elif num == 5:
        return 'One-Handed Slashing Weapons Only'
    elif num == 6:
        return 'One-Handed Blunt Weapons Only'
    elif num == 7:
        return 'One-Handed Piercing Weapons Only'
    elif num == 8:
        return 'Hand-to-Hand Weapons Only'
    elif num == 9:
        return 'Two-Handed Slashing Weapons Only'
    elif num == 10:
        return 'Two-Handed Blunt Weapons Only'
    elif num == 11:
        return 'Two-Handed Piercing Weapons Only'
    elif num == 12:
        return 'Ranged Weapons Only'
    elif num == 13:
        return 'Shields Only'
    elif num == 14:
        return 'One-Handed Slashing Weapons, One-Handed Blunt Weaspons, or Hand-to-Hand Weapons Only'
    elif num == 15:
        return 'One-Handed Blunt Weapons or Hand-to-Hand Weapons Only'
    else:
        return 'Unknown Restrictions'


def get_aug_types(num):
    out_str = ""
    while num > 0:
        if num >= 4096:
            return 'AUGMENT HIGHER THAN 13, FIX ME'
        if num >= 2048:
            num -= 2048
            out_str += '12 (FIX ME) '
        if num >= 1024:
            num -= 1024
            out_str += '11 (FIX ME) '
        if num >= 512:
            num -= 512
            out_str += '10 (FIX ME) '
        if num >= 256:
            num -= 256
            out_str += '9 (FIX ME) '
        if num >= 128:
            num -= 128
            out_str += '8 (FIX ME) '
        if num >= 64:
            num -= 64
            out_str += '7 (FIX ME) '
        if num >= 32:
            num -= 32
            out_str += '6 (FIX ME) '
        if num >= 16:
            num -= 16
            out_str += '5 (FIX ME) '
        if num >= 8:
            num -= 8
            out_str += '4 (Weapon) '
        if num >= 4:
            num -= 4
            out_str += '3 (Spells) '
        if num >= 2:
            num -= 2
            out_str += '2 (Elite) '
        if num >= 1:
            num -= 1
            out_str += '1 (Stats) '
    return out_str.strip()


def get_aug_slot_type(num):
    if num == 1:
        return '1 (Stats)'
    elif num == 2:
        return '2 (Elite)'
    elif num == 3:
        return '3 (Spells)'
    elif num == 4:
        return '4 (Weapon)'
    else:
        return 'HEY IDIOT, FIX ME'


def get_class_string(num):
    """Returns the classes that can use this item."""
    out_str = ''
    if num == 65535:
        return 'ALL'
    elif num == 0:
        return 'NONE'

    while num > 0:
        if num >= 32768:
            num -= 32768
            out_str += 'BER '
        if num >= 16384:
            num -= 16384
            out_str += 'BST '
        if num >= 8192:
            num -= 8192
            out_str += 'ENC '
        if num >= 4096:
            num -= 4096
            out_str += 'MAG '
        if num >= 2048:
            num -= 2048
            out_str += 'WIZ '
        if num >= 1024:
            num -= 1024
            out_str += 'NEC '
        if num >= 512:
            num -= 512
            out_str += 'SHM '
        if num >= 256:
            num -= 256
            out_str += 'ROG '
        if num >= 128:
            num -= 128
            out_str += 'BRD '
        if num >= 64:
            num -= 64
            out_str += 'MNK '
        if num >= 32:
            num -= 32
            out_str += 'DRU '
        if num >= 16:
            num -= 16
            out_str += 'SHD '
        if num >= 8:
            num -= 8
            out_str += 'RNG '
        if num >= 4:
            num -= 4
            out_str += 'PAL '
        if num >= 2:
            num -= 2
            out_str += 'CLR '
        if num >= 1:
            num -= 1
            out_str += 'WAR '
    return out_str.strip()


def get_slot_string(num):
    """Returns the classes that can use this item."""
    out_str = ''
    if num == 0:
        return 'NONE'
    while num > 0:
        if num >= 4194304:
            num -= 4194304
            out_str += 'Ammo '
        if num >= 1048576:
            num -= 1048576
            out_str += 'Waist '
        if num >= 524288:
            num -= 524288
            out_str += 'Feet '
        if num >= 262144:
            num -= 262144
            out_str += 'Legs '
        if num >= 131072:
            num -= 131072
            out_str += 'Chest '
        if num >= 65536:
            num -= 65536
        if num >= 32768:
            num -= 32768
            out_str += 'Finger '
        if num >= 16384:
            num -= 16384
            out_str += 'Secondary '
        if num >= 8192:
            num -= 8192
            out_str += 'Primary '
        if num >= 4096:
            num -= 4096
            out_str += 'Hands '
        if num >= 2048:
            num -= 2048
            out_str += 'Range '
        if num >= 1024:
            num -= 1024
        if num >= 512:
            num -= 512
            out_str += 'Wrist '
        if num >= 256:
            num -= 256
            out_str += 'Back '
        if num >= 128:
            num -= 128
            out_str += 'Arms '
        if num >= 64:
            num -= 64
            out_str += 'Shoulders '
        if num >= 32:
            num -= 32
            out_str += 'Neck '
        if num >= 16:
            num -= 16
        if num >= 8:
            num -= 8
            out_str += 'Face '
        if num >= 4:
            num -= 4
            out_str += 'Head '
        if num >= 2:
            num -= 2
            out_str += 'Ear '
        if num >= 1:
            num -= 1
            out_str += 'Charm '
    return out_str.strip()


def get_type_string(num):
    """Returns the appropriate item type based on id number."""
    if num == 0:
        return '1H Slashing'
    elif num == 1:
        return '2H Slashing'
    elif num == 2:
        return '1H Piercing'
    elif num == 3:
        return '1H Blunt'
    elif num == 4:
        return '2H Blunt'
    elif num == 35:
        return '2H Piercing'
    elif num == 27:
        return 'Arrow'
    elif num == 5:
        return 'Archery'
    elif num == 45:
        return 'Hand to Hand'
    elif num == 8:
        return 'Shield'
    else:
        return '__na__'


def lookup_class(name):
    if 'None' in name:
        return 0
    if 'Warrior' in name:
        return 1
    elif 'Cleric' in name:
        return 2
    elif 'Paladin' in name:
        return 4
    elif 'Ranger' in name:
        return 8
    elif 'Shadow Knight' in name:
        return 16
    elif 'Druid' in name:
        return 32
    elif 'Monk' in name:
        return 64
    elif 'Bard' in name:
        return 128
    elif 'Rogue' in name:
        return 256
    elif 'Shaman' in name:
        return 512
    elif 'Necromancer' in name:
        return 1024
    elif 'Wizard' in name:
        return 2048
    elif 'Magician' in name:
        return 4096
    elif 'Enchanter' in name:
        return 8192
    elif 'Beastlord' in name:
        return 16384
    elif 'Berserker' in name:
        return 32768


def lookup_weapon_types(name):
    if 'One Hand Slash' in name:
        return 0
    elif 'Two Hand Slash' in name:
        return 1
    elif 'One Hand Piercing' in name:
        return 2
    elif 'One Hand Blunt' in name:
        return 3
    elif 'Two Hand Blunt' in name:
        return 4
    elif 'Two Hand Piercing' in name:
        return 35
    elif 'Arrow' in name:
        return 27
    elif 'Bow' in name:
        return 5
    elif 'Hand to Hand' in name:
        return 45
    elif 'Shield' in name:
        return 8
    elif 'Thrown' in name:
        return 7
    else:
        return 10


def get_stat_weights(weights, item, bane_body=None):
    """Helper to calculate and return stat weights."""
    value = 0
    for weight in weights:
        # Fix the resist weights by adding their heroic counterpart

        if weight == 'pr':
            value += (item.pr + item.heroic_pr) * weights[weight]
        elif weight == 'mr':
            value += (item.mr + item.heroic_mr) * weights[weight]
        elif weight == 'cr':
            value += (item.cr + item.heroic_cr) * weights[weight]
        elif weight == 'dr':
            value += (item.dr + item.heroic_dr) * weights[weight]
        elif weight == 'fr':
            value += (item.fr + item.heroic_fr) * weights[weight]
        elif weight == 'w_eff':
            if not item.delay or item.delay == 0:
                continue
            value += round((item.damage / item.delay), 2) * weights[weight]
        elif 'bane_damage' in weight:
            if bane_body:
                value += item.banedmgamt * weights[weight]
            else:
                value += item.banedmgraceamt * weights[weight]
        else:
            value += int(getattr(item, weight)) * weights[weight]
    return value


def fix_npc_name(name):
    """Helper to fix names to readible standards"""
    if name.startswith('#'):
        name = name[1:]
    name = name.replace('_', ' ')
    return name.strip()


def lookup_slot(name):
    if 'Charm' in name:
        return 1
    elif 'Ear' in name:
        return 2
    elif 'Head' in name:
        return 4
    elif 'Face' in name:
        return 8
    elif 'Neck' in name:
        return 32
    elif 'Shoulders' in name:
        return 64
    elif 'Arms' in name:
        return 128
    elif 'Back' in name:
        return 256
    elif 'Wrist' in name:
        return 512
    elif 'Range' in name:
        return 2048
    elif 'Hands' in name:
        return 4096
    elif 'Primary' in name:
        return 8192
    elif 'Secondary' in name:
        return 16384
    elif 'Finger' in name:
        return 32768
    elif 'Chest' in name:
        return 131072
    elif 'Legs' in name:
        return 262144
    elif 'Feet' in name:
        return 524288
    elif 'Waist' in name:
        return 1048576
    elif 'Ammo' in name:
        return 4194304
    else:
        raise Exception(f'Unknown slot name: {name}.')


def get_focus_values(focus_type, sub_type, engine, SpellsNew):
    with Session(bind=engine) as session:
        ret_ids = []
        # "All" queries
        ignore_effects = []
        for i in range(2, 13):
            ignore_effects.append(getattr(SpellsNew, f'effectid{i}').not_in([137, 138]))
        ignore_params = and_(*ignore_effects)
        all_haste_query = session.query(SpellsNew.id). \
            filter(SpellsNew.effectid1 == 127). \
            filter(SpellsNew.effect_base_value1 > 0). \
            filter(ignore_params). \
            order_by(SpellsNew.id)

        all_range_query = session.query(SpellsNew.id). \
            filter(SpellsNew.effectid1 == 129). \
            filter(SpellsNew.effect_base_value1 > 0). \
            filter(ignore_params). \
            order_by(SpellsNew.id)

        add_effects = []
        ignore_effects = []
        for i in range(2, 13):
            add_effects.append(getattr(SpellsNew, f'effectid{i}').in_([139]))
            ignore_effects.append(getattr(SpellsNew, f'effectid{i}').not_in([138]))
        add_params = or_(*add_effects)
        ignore_params = and_(*ignore_effects)
        all_pres_query = session.query(SpellsNew.id). \
            filter(SpellsNew.effectid1 == 132). \
            filter(SpellsNew.effect_base_value1 > 0). \
            filter(ignore_params). \
            filter(add_params). \
            order_by(SpellsNew.id)

        if focus_type == 'Beneficial':
            add_effects = []
            for i in range(2, 13):
                add_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 138,
                                        getattr(SpellsNew, f'effect_base_value{i}') == 1))
            add_params = or_(*add_effects)

            if sub_type == 'Preservation':
                all_ids = all_pres_query.all()
                for entry in all_ids:
                    ret_ids.append(entry[0])

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 132). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Range':
                all_ids = all_range_query.all()
                for entry in all_ids:
                    ret_ids.append(entry[0])

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 129). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Haste':
                all_ids = all_haste_query.all()
                for entry in all_ids:
                    ret_ids.append(entry[0])

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 127). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Duration':
                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 128). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Healing':
                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 125). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            else:
                raise f'Unknown subtype: {sub_type}'
        elif focus_type == 'Detrimental':
            add_effects = []
            for i in range(2, 13):
                add_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 138,
                                        getattr(SpellsNew, f'effect_base_value{i}') == 0))
            add_params = or_(*add_effects)
            if sub_type == 'Preservation':
                all_ids = all_pres_query.all()
                for entry in all_ids:
                    ret_ids.append(entry[0])

                ignore_effects = []
                for i in range(2, 13):
                    ignore_effects.append(getattr(SpellsNew, f'effectid{i}').not_in([138]))
                ignore_params = and_(*ignore_effects)

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 132). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    filter(ignore_params). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Range':
                all_ids = all_range_query.all()
                for entry in all_ids:
                    ret_ids.append(entry[0])

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 129). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Haste':
                all_ids = all_haste_query.all()
                for entry in all_ids:
                    ret_ids.append(entry[0])

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 127). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Duration':
                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 128). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Damage (All)':
                ignore_effects = []
                for i in range(2, 13):
                    ignore_effects.append(getattr(SpellsNew, f'effectid{i}').not_in([135, 140]))
                ignore_params = and_(*ignore_effects)

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 124). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    filter(ignore_params). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Damage (Fire)':
                ignore_effects = []
                type_effects = []
                for i in range(2, 13):
                    ignore_effects.append(getattr(SpellsNew, f'effectid{i}').not_in([140]))
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 135,
                                             getattr(SpellsNew, f'effect_base_value{i}') == 2))
                ignore_params = and_(*ignore_effects)
                type_effects = or_(*type_effects)

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 124). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    filter(ignore_params). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Damage (Cold)':
                ignore_effects = []
                type_effects = []
                for i in range(2, 13):
                    ignore_effects.append(getattr(SpellsNew, f'effectid{i}').not_in([140]))
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 135,
                                             getattr(SpellsNew, f'effect_base_value{i}') == 3))
                ignore_params = and_(*ignore_effects)
                type_effects = or_(*type_effects)

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 124). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    filter(ignore_params). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Damage (Magic)':
                ignore_effects = []
                type_effects = []
                for i in range(2, 13):
                    ignore_effects.append(getattr(SpellsNew, f'effectid{i}').not_in([140]))
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 135,
                                             getattr(SpellsNew, f'effect_base_value{i}') == 1))
                ignore_params = and_(*ignore_effects)
                type_effects = or_(*type_effects)

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 124). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    filter(ignore_params). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Damage (Poison)':
                ignore_effects = []
                type_effects = []
                for i in range(2, 13):
                    ignore_effects.append(getattr(SpellsNew, f'effectid{i}').not_in([140]))
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 135,
                                             getattr(SpellsNew, f'effect_base_value{i}') == 4))
                ignore_params = and_(*ignore_effects)
                type_effects = or_(*type_effects)

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 124). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    filter(ignore_params). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Damage (Disease)':
                ignore_effects = []
                type_effects = []
                for i in range(2, 13):
                    ignore_effects.append(getattr(SpellsNew, f'effectid{i}').not_in([140]))
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 135,
                                             getattr(SpellsNew, f'effect_base_value{i}') == 5))
                ignore_params = and_(*ignore_effects)
                type_effects = or_(*type_effects)

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 124). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    filter(ignore_params). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Damage (DoT)':
                type_effects = []
                for i in range(2, 13):
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 140,
                                             getattr(SpellsNew, f'effect_base_value{i}') >= 4))
                type_effects = or_(*type_effects)

                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 124). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(add_params). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            else:
                raise f'Unknown subtype: {sub_type}'
        elif focus_type == 'Pet':
            if sub_type == 'Pet Power':
                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 167). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            else:
                raise f'Unknown subtype: {sub_type}'
        elif focus_type == 'Melee':
            if sub_type == 'Ferocity':
                return [3886, 3887, 3888, 6323, 6324, 7835, 9615, 15841, 20517]
            elif sub_type == 'Cleave':
                return [3883, 3884, 3885, 6321, 6322, 7834, 9614, 15840, 20516]
            elif sub_type == 'Dodging':
                return [3889, 3890, 3891, 7832, 9612, 15838, 20514]
            elif sub_type == 'Parry':
                return [3892, 3893, 3894, 6327, 6328, 6329, 7833, 7837, 9613, 9617, 15839, 20515]
            elif sub_type == 'Sharpshooting':
                return [3896, 3897, 3898, 6325, 6326, 7836, 9616, 15842, 20518]
            else:
                raise f'Unknown subtype: {sub_type}'
        elif focus_type == 'Bard':
            if sub_type == 'Wind':
                type_effects = []
                for i in range(2, 13):
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 414,
                                             getattr(SpellsNew, f'effect_base_value{i}') == 54))
                type_effects = or_(*type_effects)
                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 413). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Stringed':
                type_effects = []
                for i in range(2, 13):
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 414,
                                             getattr(SpellsNew, f'effect_base_value{i}') == 49))
                type_effects = or_(*type_effects)
                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 413). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Brass':
                type_effects = []
                for i in range(2, 13):
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 414,
                                             getattr(SpellsNew, f'effect_base_value{i}') == 12))
                type_effects = or_(*type_effects)
                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 413). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Percussion':
                type_effects = []
                for i in range(2, 13):
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 414,
                                             getattr(SpellsNew, f'effect_base_value{i}') == 70))
                type_effects = or_(*type_effects)
                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 413). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            elif sub_type == 'Singing':
                type_effects = []
                for i in range(2, 13):
                    type_effects.append(and_(getattr(SpellsNew, f'effectid{i}') == 414,
                                             getattr(SpellsNew, f'effect_base_value{i}') == 41))
                type_effects = or_(*type_effects)
                query = session.query(SpellsNew.id). \
                    filter(SpellsNew.effectid1 == 413). \
                    filter(SpellsNew.effect_base_value1 > 0). \
                    filter(type_effects). \
                    order_by(SpellsNew.id)
                ids = query.all()
                for entry in ids:
                    ret_ids.append(entry[0])
                return ret_ids
            else:
                raise Exception(f'Unknown sub_type: {sub_type}')
        else:
            raise Exception(f'Unknown focus type: {focus_type}')


def get_map_data(short_name):
    lines = []
    if short_name == 'Unknown':
        return lines
    with open(os.path.join(here, 'maps', f'{short_name}.txt'), 'r') as fh:
        data = fh.read()
        for line in data.split('\n'):
            if line.startswith('L'):
                split_line = line.split()
                lines.append({'x1': float(split_line[1].strip(',')),
                              'y1': float(split_line[2].strip(',')),
                              'z1': float(split_line[3].strip(',')),
                              'x2': float(split_line[4].strip(',')),
                              'y2': float(split_line[5].strip(',')),
                              'z2': float(split_line[6].strip(',')),
                              'rgb': f'{split_line[7].strip(",")}, {split_line[8].strip(",")}, {split_line[9].strip(",")}'})
    return lines


def get_map_poi(short_name):
    points = []
    if short_name == 'Unknown':
        return points
    with open(os.path.join(here, 'maps', f'{short_name}_1.txt'), 'r') as fh:
        data = fh.read()
        for line in data.split('\n'):
            if line.startswith('P'):
                split_line = line.split()
                points.append({'x': float(split_line[1].strip(',')),
                               'y': float(split_line[2].strip(',')),
                               'z': float(split_line[3].strip(',')),
                               'rgb': f'{split_line[4].strip(",")}, {split_line[5].strip(",")}, {split_line[6].strip(",")}',
                               'label': split_line[8].replace('_', ' ')})
    return points


def parse_skill(skill_num):
    if skill_num == -1:
        return 'All Skills'
    elif skill_num == 0:
        return '1H Blunt'
    elif skill_num == 1:
        return '1H Slashing'
    elif skill_num == 2:
        return '2H Blunt'
    elif skill_num == 3:
        return '2H Slashing'
    elif skill_num == 4:
        return 'Abjuration'
    elif skill_num == 5:
        return 'Alteration'
    elif skill_num == 6:
        return 'Apply Poison'
    elif skill_num == 7:
        return 'Archery'
    elif skill_num == 8:
        return 'Backstab'
    elif skill_num == 9:
        return 'Bind Wounds'
    elif skill_num == 10:
        return 'Bash'
    elif skill_num == 11:
        return 'Block'
    elif skill_num == 12:
        return 'Brass Instruments'
    elif skill_num == 13:
        return 'Channeling'
    elif skill_num == 14:
        return 'Conjuration'
    elif skill_num == 15:
        return 'Defense'
    elif skill_num == 16:
        return 'Disarm'
    elif skill_num == 17:
        return 'Disarm Traps'
    elif skill_num == 18:
        return 'Divination'
    elif skill_num == 19:
        return 'Dodge'
    elif skill_num == 20:
        return 'Double Attack'
    elif skill_num == 21:
        return 'Dragon Punch'
    elif skill_num == 22:
        return 'Dual Wield'
    elif skill_num == 23:
        return 'Eagle Strike'
    elif skill_num == 24:
        return 'Evocation'
    elif skill_num == 25:
        return 'Feign Death'
    elif skill_num == 26:
        return 'Flying Kick'
    elif skill_num == 27:
        return 'Forage'
    elif skill_num == 28:
        return 'Hand to Hand'
    elif skill_num == 29:
        return 'Hide'
    elif skill_num == 30:
        return 'Kick'
    elif skill_num == 31:
        return 'Meditate'
    elif skill_num == 32:
        return 'Mend'
    elif skill_num == 33:
        return 'Offense'
    elif skill_num == 34:
        return 'Parry'
    elif skill_num == 35:
        return 'Pick Locks'
    elif skill_num == 36:
        return 'Piercing'
    elif skill_num == 37:
        return 'Riposte'
    elif skill_num == 38:
        return 'Round Kick'
    elif skill_num == 39:
        return 'Safe Fall'
    elif skill_num == 40:
        return 'Sense Heading'
    elif skill_num == 41:
        return 'Singing'
    elif skill_num == 42:
        return 'Sneak'
    elif skill_num == 43:
        return 'Specialize Abjuration'
    elif skill_num == 44:
        return 'Specialize Alteration'
    elif skill_num == 45:
        return 'Specialize Conjuration'
    elif skill_num == 46:
        return 'Specialize Divination'
    elif skill_num == 47:
        return 'Specialize Evocation'
    elif skill_num == 48:
        return 'Pick Pockets'
    elif skill_num == 49:
        return 'Stringed Instruments'
    elif skill_num == 50:
        return 'Swimming'
    elif skill_num == 51:
        return 'Throwing'
    elif skill_num == 52:
        return 'Tiger Claw'
    elif skill_num == 53:
        return 'Tracking'
    elif skill_num == 54:
        return 'Wind Instruments'
    elif skill_num == 55:
        return 'Fishing'
    elif skill_num == 56:
        return 'Poison Making'
    elif skill_num == 57:
        return 'Tinkering'
    elif skill_num == 58:
        return 'Research'
    elif skill_num == 59:
        return 'Alchemy'
    elif skill_num == 60:
        return 'Baking'
    elif skill_num == 61:
        return 'Tailoring'
    elif skill_num == 62:
        return 'Sense Traps'
    elif skill_num == 63:
        return 'Blacksmithing'
    elif skill_num == 64:
        return 'Fletching'
    elif skill_num == 65:
        return 'Brewing'
    elif skill_num == 66:
        return 'Alcohol Tolerance'
    elif skill_num == 67:
        return 'Begging'
    elif skill_num == 68:
        return 'Jewel Crafting'
    elif skill_num == 69:
        return 'Pottery'
    elif skill_num == 70:
        return 'Percussion Instruments'
    elif skill_num == 71:
        return 'Intimidate'
    elif skill_num == 72:
        return 'Berserking'
    elif skill_num == 73:
        return 'Taunt'
    elif skill_num == 74:
        return 'Frenzy'
    elif skill_num == 75:
        return 'Non-Tradeskill'
    elif skill_num == 76:
        return 'Triple Attack'
    elif skill_num == 77:
        return '2H Piercing'
    elif skill_num == 255:
        return 'none'
    else:
        return 'Unknown skill'


def get_object_type(obj_id):
    if obj_id == 10:
        return 'Tool Box'
    elif obj_id == 11:
        return 'Research'
    elif obj_id == 12:
        return 'Mortar'
    elif obj_id == 13:
        return 'Self Dusting'
    elif obj_id == 14:
        return 'Baking'
    elif obj_id == 15:
        return 'Baking'
    elif obj_id == 16:
        return 'Tailoring'
    elif obj_id == 17:
        return 'Forge'
    elif obj_id == 18:
        return 'Fletching'
    elif obj_id == 19:
        return 'Brew Barrel'
    elif obj_id == 20:
        return 'Jewelcraft'
    elif obj_id == 21:
        return 'Pottery Wheel'
    elif obj_id == 22:
        return 'Pottery Kiln'
    elif obj_id == 24:
        return 'Wizard Only Research'
    elif obj_id == 25:
        return 'Mage Only Research'
    elif obj_id == 26:
        return 'Necromancer Only Research'
    elif obj_id == 27:
        return 'Enchanter Only Research'
    elif obj_id == 28:
        return 'Class/Race Limited'
    elif obj_id == 29:
        return 'Class/Race Limited'
    elif obj_id == 30:
        return 'Always Works'
    elif obj_id == 31:
        return 'High Elf Forge'
    elif obj_id == 32:
        return 'Dark Elf Forge'
    elif obj_id == 33:
        return 'Ogre Forge'
    elif obj_id == 34:
        return 'Dwarven Forge'
    elif obj_id == 35:
        return 'Gnome Forge'
    elif obj_id == 36:
        return 'Barbarian Forge'
    elif obj_id == 38:
        return 'Iksar Forge'
    elif obj_id == 39:
        return 'Human Forge'
    elif obj_id == 40:
        return 'Human Forge'
    elif obj_id == 41:
        return 'Halfling Tailoring Kit'
    elif obj_id == 42:
        return 'Erudite Tailoring Kit'
    elif obj_id == 43:
        return 'Wood Elf Tailoring Kit'
    elif obj_id == 44:
        return 'Wood Elf Fletching Kit'
    elif obj_id == 45:
        return 'Iksar Pottery Wheel'
    elif obj_id == 47:
        return 'Troll Forge'
    elif obj_id == 48:
        return 'Wood Elf Forge'
    elif obj_id == 49:
        return 'Halfling Forge'
    elif obj_id == 50:
        return 'Erudite Forge'
    elif obj_id == 53:
        return 'Augment'
    else:
        raise NotImplementedError(f'Unknown object id: {obj_id}')


def get_era_zones(era_name):
    if era_name == 'Classic':
        return [48, 55, 36, 17, 68, 58, 70, 22, 10, 15, 98, 24, 30, 16, 52, 29, 6, 5, 46, 64, 74, 20, 51, 33, 32,
                44, 42, 41, 40, 8, 67, 2, 34, 61, 37, 69, 49, 75, 76, 19, 31, 60, 1, 35, 62, 56, 77, 59, 65, 23,
                63, 47, 54, 39, 18, 27, 57, 11, 13, 73, 72, 186, 71, 45, 4, 50, 66, 14, 3, 12, 38, 21, 9, 25]
    elif era_name == 'Kunark':
        return [106, 82, 103, 84, 92, 88, 102, 97, 85, 87, 90, 104, 86, 94, 78, 105, 107, 93, 89, 91, 83, 81, 80,
                79, 96, 95, 108, 277, 225, 228, 227, 224, 226]
    elif era_name == 'LoY':
        return [277, 225, 228, 227, 224, 226]
    elif era_name == 'Velious':
        return [117, 123, 116, 129, 113, 125, 114, 115, 121, 118, 110, 127, 126, 128, 100, 124, 111, 119, 101, 120,
                109, 112]
    elif era_name == 'Luclin':
        return [163, 167, 166, 160, 168, 169, 161, 152, 159, 165, 150, 162, 154, 179, 155, 174, 164, 153, 157,
                171, 173, 156, 175, 172, 170, 176, 158]
    elif era_name == 'Planes':
        return [181, 278, 209, 214, 213, 200, 211, 221, 215, 205, 218, 222, 217, 206, 201, 202, 204, 210, 219, 223,
                203, 208, 216, 220, 212, 207]
    elif era_name == 'LDoN':
        return [264, 239, 229, 254, 259, 249, 244, 237, 275, 262, 247, 232, 242, 268, 263, 248, 238, 233, 272, 276,
                258, 253, 243, 270, 261, 274, 251, 246, 256, 236, 231, 266, 241, 234, 257, 252, 267, 269, 273, 265,
                230, 250, 255, 235, 260, 245, 240, 271]
    elif era_name == 'GoD':
        return [283, 284, 294, 296, 293, 280, 281, 295, 299, 282, 288, 286, 285, 287, 298, 279, 998, 289, 297, 292,
                290, 291]
    elif era_name == 'OoW':
        return [317, 328, 329, 330, 318, 319, 320, 302, 335, 304, 305, 306, 307, 308, 309, 316, 303, 334, 331, 332,
                333, 301, 336, 300]
    elif era_name == 'DoN':
        return [345, 344, 341, 339, 338, 346, 337, 343, 340, 342]
    elif era_name == 'DoDH':
        return [360, 359, 365, 367, 351, 348, 361, 357, 347, 364, 368, 363, 366, 358, 349, 356, 355, 354, 350, 362]
    elif era_name == 'PoR':
        return [385, 369, 388, 389, 381, 382, 387, 384, 391, 392, 375, 370, 376, 371, 393, 374, 386, 372, 378, 377,
                373, 380, 390, 379, 383]
    elif era_name == 'TSS':
        return [406, 411, 398, 395, 394, 405, 402, 397, 412, 407, 400, 410, 396, 403, 408, 413, 415, 409, 399, 414,
                401, 404]
    elif era_name == 'TBS':
        return [422, 428, 427, 424, 418, 416, 429, 425, 430, 420, 421, 426, 417, 423, 435, 431, 432, 433, 434, 419]
    elif era_name == 'SoF':
        return [445, 449, 446, 451, 442, 436, 440, 441, 444, 443, 437, 439, 447, 438, 448]
    elif era_name == 'SoD':
        return [468, 456, 471, 474, 452, 458, 454, 453, 470, 476, 455, 466, 467, 472, 457, 477, 469, 473, 459, 460, 461,
                462, 463, 464, 465, 475]
    elif era_name == 'UF':
        return [485, 492, 480, 490, 481, 484, 495, 487, 488, 491, 483, 486, 482, 489, 493, 494]
    elif era_name == 'HoT':
        return [709, 706, 711, 701, 702, 710, 707, 708, 712, 700, 703, 704, 705]
    elif era_name == 'VoA':
        return [724, 728, 732, 730, 727, 726, 734, 733, 735, 729, 725, 731]
    elif era_name == 'RoF':
        return [760, 755, 758, 759, 754, 752, 757, 756, 753]
    else:
        raise Exception(f'Unknown era: {era_name}')


def lookup_zone_name(item_id):
    if item_id == -1:
        return 'Quest'
    if item_id == -2:
        return 'Tradeskill'
    if item_id == -3:
        return 'Special Drop'
    zone_id = int(int(item_id) / 1000)
    with open(os.path.join(here, 'item_files/zonelist.txt'), 'r') as fh:
        zone_list = fh.read()
    for line in zone_list.split('\n'):
        if f'{zone_id}\t' in line:
            return line.split(str(zone_id))[1].strip()


def check_sympathetic(name):
    if 'Sympathetic Strike of Flames' in name:
        split_name = name.split('of Flames')
        return f'{split_name[0]}{split_name[1]}'
    elif 'Sympathetic Healing Burst' in name:
        split_name = name.split('Burst')
        return f'{split_name[0]}{split_name[1]}'
    else:
        return name


def get_era_name(era_id):
    if era_id == 0:
        return 'Classic'
    elif era_id == 1:
        return "Ruins of Kunark"
    elif era_id == 2:
        return "Scars of Velious"
    elif era_id == 3:
        return "Shadows of Luclin"
    elif era_id == 4:
        return "Planes of Power"
    elif era_id == 5:
        return "Legacy of Ykesha"
    elif era_id == 6:
        return "Lost Dungeons of Norrath"
    elif era_id == 7:
        return "Gates of Discord"
    elif era_id == 8:
        return "Omens of War"
    elif era_id == 9:
        return "Dragons of Norrath"
    elif era_id == 10:
        return "Depths of Darkhollow"
    elif era_id == 11:
        return "Prophecy of Ro"
    elif era_id == 12:
        return "The Serpents Spine"
    elif era_id == 13:
        return "The Buried Sea"
    elif era_id == 14:
        return "Secrets of Faydwer"
    elif era_id == 15:
        return "Seeds of Destruction"
    elif era_id == 16:
        return "Underfoot"
    elif era_id == 17:
        return "House of Thule"
    elif era_id == 18:
        return "Veil of Alaris"
    elif era_id == 19:
        return "Rain of Fear"
    else:
        return "Unknown Era"


def get_era_id(name):
    if name == 'Classic':
        return 0
    elif name == 'Kunark':
        return 1
    elif name == 'Velious':
        return 2
    elif name == 'Luclin':
        return 3
    elif name == 'Planes':
        return 4
    elif name == 'Ykesha':
        return 5
    elif name == 'LDoN':
        return 6
    elif name == 'GoD':
        return 7
    elif name == 'OoW':
        return 8
    elif name == 'DoN':
        return 9
    elif name == 'DoDH':
        return 10
    elif name == 'PoR':
        return 11
    elif name == 'TSS':
        return 12
    elif name == 'TBS':
        return 13
    elif name == 'SoF':
        return 14
    elif name == 'SoD':
        return 15
    elif name == 'UF':
        return 16
    elif name == 'HoT':
        return 17
    elif name == 'VoA':
        return 18
    elif name == 'RoF':
        return 19
    elif name == 'CoTF':
        return 20
    elif name == 'TDS':
        return 21
    elif name == 'TBM':
        return 22
    elif name == 'EoK':
        return 23
    elif name == 'RoS':
        return 24
    elif name == 'TBL':
        return 25
    elif name == 'ToV':
        return 26
    elif name == 'CoV':
        return 27
    elif name == 'ToL':
        return 28
    elif name == 'NoS':
        return 29
    elif name == 'LS':
        return 30
    elif name == 'TOB':
        return 31
    elif name == 'Unknown':
        return 999
    else:
        raise Exception(f'Unknown era name {name}')


def get_exclusion_list(name):
    with open(os.path.join(here, 'Exclusion', f'{name}.txt')) as fh:
        data = fh.read()
    return data.split('\n')


def get_stat_name(stat):
    if stat == 'hp':
        return 'Hit Points'
    elif stat == 'mana':
        return 'Mana'
    elif stat == 'endur':
        return 'Endurance'
    elif stat == 'ac':
        return 'Armor Class'
    elif stat == 'aagi':
        return 'Agility'
    elif stat == 'acha':
        return 'Charisma'
    elif stat == 'adex':
        return 'Dexterity'
    elif stat == 'aint':
        return 'Intelligence'
    elif stat == 'asta':
        return 'Stamina'
    elif stat == 'astr':
        return 'Strength'
    elif stat == 'awis':
        return 'Wisdom'
    elif stat == 'heroic_agi':
        return 'Heroic Agility'
    elif stat == 'heroic_cha':
        return 'Heroic Charisma'
    elif stat == 'heroic_dex':
        return 'Heroic Dexterity'
    elif stat == 'heroic_int':
        return 'Heroic Intelligence'
    elif stat == 'heroic_sta':
        return 'Heroic Stamina'
    elif stat == 'heroic_str':
        return 'Heroic Strength'
    elif stat == 'heroic_wis':
        return 'Heroic Wisdom'
    elif stat == 'cr':
        return 'Resist Cold'
    elif stat == 'dr':
        return 'Disease Resist'
    elif stat == 'fr':
        return 'Fire Resist'
    elif stat == 'mr':
        return 'Magic Resist'
    elif stat == 'pr':
        return 'Poison Resist'
    elif stat == 'attack':
        return 'Attack'
    elif stat == 'haste':
        return 'Haste'
    elif stat == 'regen':
        return 'HP Regeneration'
    elif stat == 'manaregen':
        return 'Mana Regeneration'
    elif stat == 'enduranceregen':
        return 'Endurance Regeneration'
    elif stat == 'healamt':
        return 'Healing Amount'
    elif stat == 'spelldmg':
        return 'Spell Damage'
    elif stat == 'accuracy':
        return 'Accuracy'
    elif stat == 'avoidance':
        return 'Avoidance'
    elif stat == 'combateffects':
        return 'Combat Effects'
    elif stat == 'damageshield':
        return 'Damage Shielding'
    elif stat == 'dotshielding':
        return 'DoT Shield'
    elif stat == 'shielding':
        return 'Shielding'
    elif stat == 'spellshield':
        return 'Spellshield'
    elif stat == 'strikethrough':
        return 'Strikethrough'
    elif stat == 'stunresist':
        return 'Stun Resist'
    else:
        return 'None'


def get_stats_of_interest():
    return [
        'aagi', 'ac', 'accuracy', 'acha', 'adex', 'aint', 'asta', 'astr', 'attack',
        'avoidance', 'awis', 'combateffects', 'cr', 'damageshield', 'dotshielding',
        'dr', 'endur', 'focuseffect', 'fr', 'hp', 'regen', 'mana', 'manaregen',
        'enduranceregen', 'mr', 'pr', 'shielding', 'clickeffect', 'spellshield',
        'strikethrough', 'stunresist', 'proceffect', 'worneffect', 'focustype',
        'dsmitigation', 'heroic_str', 'heroic_int', 'heroic_wis', 'heroic_agi',
        'heroic_dex', 'heroic_sta', 'heroic_cha', 'heroic_pr', 'heroic_dr',
        'heroic_fr', 'heroic_cr', 'heroic_mr', 'healamt', 'spelldmg', 'bardeffect'
    ]


def get_stat_translations():
    return {'aagi': 'Agility',
            'ac': 'AC',
            'accuracy': 'Accuracy',
            'acha': 'Charisma',
            'adex': 'Dexterity',
            'aint': 'Intelligence',
            'asta': 'Stamina',
            'astr': 'Strength',
            'avoidance': 'Avoidance',
            'awis': 'Wisdom',
            'combateffects': 'Combat Effects',
            'cr': 'Cold Resist',
            'damageshield': 'Damage Shielding',
            'dotshielding': 'DoT Shielding',
            'dr': 'Disease Resist',
            'endur': 'Endurance',
            'fr': 'Fire Resist',
            'hp': 'HP',
            'regen': 'HP Regeneration',
            'mana': 'Mana',
            'manaregen': 'Mana Regeneration',
            'enduranceregen': 'Endurance Regeneration',
            'mr': 'Magic Resist',
            'pr': 'Poison Resist',
            'shielding': 'Shielding',
            'spellshield': 'Spell Shielding',
            'strikethrough': 'Strikethrough',
            'stunresist': 'Stun Resist',
            'dsmitigation': 'Damage Shield Mitigation',
            'heroic_str': 'Heroic Strength',
            'heroic_int': 'Heroic Intelligence',
            'heroic_wis': 'Heroic Wisdom',
            'heroic_agi': 'Heroic Agility',
            'heroic_dex': 'Heroic Dexterity',
            'heroic_sta': 'Heroic Stamina',
            'heroic_cha': 'Heroic Charisma',
            'heroic_pr': 'Heroic Poison Resist',
            'heroic_dr': 'Heroic Disease Resist',
            'heroic_fr': 'Heroic Fire Resist',
            'heroic_cr': 'Heroic Cold Resist',
            'heroic_mr': 'Heroic Magic Resist',
            'healamt': 'Healing Amount',
            'spelldmg': 'Spell Damage',
            'attack': 'Attack'
            }
