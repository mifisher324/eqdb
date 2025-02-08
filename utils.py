"""Utilities for EQDB"""
import os

here = os.path.dirname(__file__)


class FileItem:
    # TODO: These may be deprecated now
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


class ReducedItem:
    # TODO: These may be deprecated now
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


def get_class_string(num):
    """Returns the classes that can use this item."""
    out_str = ''
    if num == 65536:
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
        if num >= 2097152:
            num -= 2097152
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
    else:
        return 10


def get_stat_weights(weights, item):
    """Helper to calculate and return stat weights."""
    value = 0
    for weight in weights:
        # Fix the resist weights by adding their heroic counterpart

        if 'pr' in weight:
            value += (item.pr + item.heroic_pr) * weights[weight]
        elif 'mr' in weight:
            value += (item.mr + item.heroic_mr) * weights[weight]
        elif 'cr' in weight:
            value += (item.cr + item.heroic_cr) * weights[weight]
        elif 'dr' in weight:
            value += (item.dr + item.heroic_dr) * weights[weight]
        elif 'fr' in weight:
            value += (item.fr + item.heroic_fr) * weights[weight]
        elif 'w_eff' in weight:
            if not item.delay or item.delay == 0:
                continue
            value += round((item.damage / item.delay), 2) * weights[weight]
        else:
            value += getattr(item, weight) * weights[weight]
    return value


def fix_item_name(name, item_id):
    """Helper to fix names to THJ standards"""
    if item_id < 1000000:
        return name
    elif 1000000 <= item_id < 2000000:
        base_name = name.split('Rose Colored')[1].strip()
        return f'{base_name} (Enchanted)'
    else:
        base_name = name.split('Apocryphal')[1].strip()
        return f'{base_name} (Legendary)'


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


def get_focus_values(focus_type, sub_type):
    # TODO: This needs to get made into a dynamic method
    if focus_type == 'Beneficial':
        if sub_type == 'Preservation':
            return [2342, 2343, 2344, 3537, 6419, 3114, 3113, 3117, 3122, 3112, 3116, 3543, 3544, 3545, 3538, 3539]
        elif sub_type == 'Range':
            return [3109, 3111, 2348, 2349, 2350, 3510, 6413, 3511, 3512]
        elif sub_type == 'Haste':
            return [3118, 3123, 3125, 3124, 2339, 2340, 2341, 3525, 6415, 3531, 3532, 3533]
        elif sub_type == 'Duration':
            return [3106, 2333, 2334, 2335, 3504, 6411, 3506, 3845, 3846]
        elif sub_type == 'Healing':
            return [3110, 2345, 2346, 2347, 3501, 6410, 3502, 3503]
        else:
            raise f'Unknown subtype: {sub_type}'
    elif focus_type == 'Detrimental':
        if sub_type == 'Preservation':
            return [2342, 2343, 2344, 3537, 6419, 3114, 3113, 3112, 3120, 3121, 3119, 3538, 3539, 3540, 3541, 3542,
                    3547]
        elif sub_type == 'Range':
            return [3109, 3111, 2349, 2350, 3510, 6413, 3511, 3512]
        elif sub_type == 'Haste':
            return [3118, 3123, 3128, 3124, 3127, 2339, 2340, 2341, 3525, 6415, 2339, 2340, 2341, 3525, 6415, 3528,
                    3529, 3530]
        elif sub_type == 'Duration':
            return [3106, 3843, 3844]
        elif sub_type == 'Damage (All)':
            return [3108, 3101, 3104, 2336, 2337, 2338, 3513, 6414, 3514, 3515]
        elif sub_type == 'Damage (Fire)':
            return [3102, 3516, 3517, 3518]
        elif sub_type == 'Damage (Cold)':
            return [3103, 3519, 3520, 3521]
        elif sub_type == 'Damage (Magic)':
            return [3105, 3522, 3523, 3524]
        elif sub_type == 'Damage (Poison)':
            return []
        elif sub_type == 'Damage (Disease)':
            return [3923]
        elif sub_type == 'Damage (DoT)':
            return [2366, 2367, 2368, 3507, 6412]
        else:
            raise f'Unknown subtype: {sub_type}'
    elif focus_type == 'Pet':
        if sub_type == 'Pet Power':
            return [4406, 4407, 4399, 4398, 4397, 4396, 4404, 4403, 4402, 4401, 4400, 4409, 5062, 5124, 5123, 5122,
                    5121, 4405, 4410, 5061, 6089]
        else:
            raise f'Unknown subtype: {sub_type}'
    else:
        raise f'Unknown focus type: {focus_type}'


def get_era_zones(era_name):
    if era_name == 'Classic':
        return [48, 55, 36, 17, 68, 58, 70, 22, 10, 15, 98, 24, 30, 16, 52, 29, 6, 5, 46, 64, 74, 20, 51, 33, 32,
                44, 42, 41, 40, 8, 67, 2, 34, 61, 37, 69, 49, 75, 76, 19, 31, 60, 1, 35, 62, 56, 77, 59, 65, 23,
                63, 47, 54, 39, 18, 27, 57, 11, 13, 73, 72, 186, 71, 45, 4, 50, 66, 14, 3, 12, 38, 21, 9, 25]
    elif era_name == 'Kunark':
        return [106, 82, 103, 84, 92, 88, 102, 97, 85, 87, 90, 104, 86, 94, 78, 105, 107, 93, 89, 91, 83, 81, 80,
                79, 96, 95, 108, 277, 225, 228, 227, 224, 226]
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
    zone_id = int(int(item_id) / 1000)
    with open(os.path.join(here, 'item_files/zonelist.txt'), 'r') as fh:
        zone_list = fh.read()
    for line in zone_list.split('\n'):
        if f'{zone_id}\t' in line:
            return line.split(str(zone_id))[1].strip()
