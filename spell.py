"""Utility file to convert SPA data into human readible information."""
import time
from math import ceil

from sqlalchemy import and_
from sqlalchemy.orm import Session

import item
import logic
import utils
import zone
from logic import SpellsNew, engine, Item

LEVEL_CAP = 65


def get_full_spell_data(spell_id):
    excl_list = utils.get_exclusion_list('spells')
    item_excl_list = utils.get_exclusion_list('item')
    if spell_id in excl_list:
        return None
    spell_data, slots = get_spell_data(spell_id, engine)
    if not spell_data:
        return spell_data, slots

    procs = []
    clicks = []
    focus = []
    worn = []
    bard = []
    scroll = []

    with Session(bind=engine) as session:
        # Find all the items that have this as a proc
        query = session.query(logic.Item.id, Item.Name, Item.icon).filter(Item.proceffect == spell_id)
        result = query.all()
        for entry in result:
            item_id = entry[0]
            if item_id in item_excl_list:
                continue
            item_name = entry[1]
            icon = entry[2]
            procs.append({'item_id': item_id,
                          'item_name': item_name,
                          'icon': icon})

        # Find all the items that have this as a click effect
        query = session.query(Item.id, Item.Name, Item.icon).filter(Item.clickeffect == spell_id)
        result = query.all()
        for entry in result:
            item_id = entry[0]
            if item_id in item_excl_list:
                continue
            item_name = entry[1]
            icon = entry[2]
            clicks.append({'item_id': item_id,
                          'item_name': item_name,
                           'icon': icon})

        # Find all the items that have this as a focus effect
        query = session.query(Item.id, Item.Name, Item.icon).filter(Item.focuseffect == spell_id)
        result = query.all()
        for entry in result:
            item_id = entry[0]
            if item_id in item_excl_list:
                continue
            item_name = entry[1]
            icon = entry[2]
            focus.append({'item_id': item_id,
                          'item_name': item_name,
                          'icon': icon})

        # Find all the items that have this as a worn effect
        query = session.query(Item.id, Item.Name, Item.icon).filter(Item.worneffect == spell_id)
        result = query.all()
        for entry in result:
            item_id = entry[0]
            if item_id in item_excl_list:
                continue
            item_name = entry[1]
            icon = entry[2]
            worn.append({'item_id': item_id,
                         'item_name': item_name,
                         'icon': icon})

        # Find all the items that have this as a bard effect
        query = session.query(Item.id, Item.Name, Item.icon).filter(Item.bardeffect == spell_id)
        result = query.all()
        for entry in result:
            item_id = entry[0]
            if item_id in item_excl_list:
                continue
            item_name = entry[1]
            icon = entry[2]
            bard.append({'item_id': item_id,
                         'item_name': item_name,
                         'icon': icon})

        # Find all the items that teach this.
        query = session.query(Item.id, Item.Name, Item.icon).filter(Item.scrolleffect == spell_id)
        result = query.all()
        for entry in result:
            item_id = entry[0]
            if item_id in item_excl_list:
                continue
            item_name = entry[1]
            icon = entry[2]
            scroll.append({'item_id': item_id,
                           'item_name': item_name,
                           'icon': icon})
    print(scroll)
    spell_data.update({'procs': procs,
                       'clicks': clicks,
                       'focus': focus,
                       'worn': worn,
                       'bard': bard,
                       'scroll': scroll})

    return spell_data, slots


def get_spell_tooltip(spell_id):
    excl_list = utils.get_exclusion_list('spells')
    if spell_id in excl_list:
        return None
    return get_spell_data(spell_id, basic_data=False)


def get_spells(spell_name):
    partial = "%%%s%%" % spell_name
    with Session(bind=engine) as session:
        query = session.query(SpellsNew.id, SpellsNew.name, SpellsNew.new_icon).\
            filter(SpellsNew.name.like(partial)).limit(50)
        result = query.all()

    with Session(bind=engine) as session:
        query = session.query(SpellsNew.id, SpellsNew.name, SpellsNew.new_icon).\
            filter(SpellsNew.name.like(partial)).limit(50)
        result2 = query.all()

    out_data = []
    known_spells = []
    for entry in result2 + result:
        spell_id = entry[0]
        excl_list = utils.get_exclusion_list('spells')
        if spell_id in excl_list:
            continue
        if spell_id in known_spells:
            continue
        name = entry[1]
        icon = entry[2]
        out_data.append({'spell_id': spell_id,
                         'name': name,
                         'icon': icon})
        known_spells.append(spell_id)
    return out_data


def get_spell_raw_data(spell_id=None, spell_name=None):
    excl_list = utils.get_exclusion_list('spells')
    if spell_id in excl_list:
        return None
    with Session(bind=engine) as session:
        if spell_id:
            query = session.query(SpellsNew).filter(SpellsNew.id == spell_id)
            result = query.first()
            if not result:
                return {}
            ret_dict = result.__dict__
            ret_dict.pop('_sa_instance_state')
            return ret_dict
        else:
            ret_list = []
            name = '%%%s%%' % spell_name
            query = session.query(SpellsNew).filter(SpellsNew.name.like(name))
            result = query.limit(50).all()
            if not result:
                return []
            for entry in result:
                entry = entry.__dict__
                entry.pop('_sa_instance_state')
                if entry['id'] in excl_list:
                    continue
                ret_list.append(entry)
            return ret_list


def translate_result(entry):
    entry = entry._mapping
    spell_id = entry.id
    excl_list = utils.get_exclusion_list('spells')
    if spell_id in excl_list:
        return None
    spell_name = entry.name
    skill = utils.parse_skill(entry.skill)
    target = parse_target_type(int(entry.targettype))
    icon = entry.new_icon
    slots = {}
    dot = False
    for idx in range(1, 13):
        if getattr(entry, f'effectid{idx}') != 254:
            slots.update({f'slot_{idx}': parse_slot_data(idx, entry, no_item_links=True)})
            if getattr(entry, f'effectid{idx}') == 0:
                dot = True
    if entry.buffduration > 0:
        instant = False
    else:
        instant = True
    if entry.goodEffect == 1:
        beneficial = True
    else:
        beneficial = False
    return {'spell_id': spell_id, 'skill': skill, 'spell_name': spell_name, 'dot': dot,
            'target': target, 'slots': slots, 'icon': icon, 'instant': instant, 'beneficial': beneficial}


def get_spells_by_class(class_id, min_level=1, max_level=65):
    filters = [getattr(SpellsNew, f'classes{class_id}') >= min_level,
               getattr(SpellsNew, f'classes{class_id}') <= max_level]
    params = and_(*filters)

    with Session(bind=engine) as session:
        args = [SpellsNew.id, SpellsNew.classes1, SpellsNew.classes2,
                SpellsNew.classes3, SpellsNew.classes4, SpellsNew.classes5,
                SpellsNew.classes6, SpellsNew.classes7, SpellsNew.classes8,
                SpellsNew.classes9, SpellsNew.classes10, SpellsNew.classes11,
                SpellsNew.classes12, SpellsNew.classes13, SpellsNew.classes14,
                SpellsNew.classes15, SpellsNew.classes16,
                SpellsNew.name, SpellsNew.skill, SpellsNew.targettype,
                SpellsNew.new_icon, SpellsNew.effectid1, SpellsNew.effectid2,
                SpellsNew.effectid3, SpellsNew.effectid4, SpellsNew.effectid5,
                SpellsNew.effectid6, SpellsNew.effectid7, SpellsNew.effectid8,
                SpellsNew.effectid9, SpellsNew.effectid10, SpellsNew.effectid11,
                SpellsNew.effectid12, SpellsNew.effect_base_value1,
                SpellsNew.effect_base_value2, SpellsNew.effect_base_value3,
                SpellsNew.effect_base_value4, SpellsNew.effect_base_value5,
                SpellsNew.effect_base_value6, SpellsNew.effect_base_value7,
                SpellsNew.effect_base_value8, SpellsNew.effect_base_value9,
                SpellsNew.effect_base_value10, SpellsNew.effect_base_value11,
                SpellsNew.effect_base_value12, SpellsNew.effect_limit_value1,
                SpellsNew.effect_limit_value2, SpellsNew.effect_limit_value3,
                SpellsNew.effect_limit_value4, SpellsNew.effect_limit_value5,
                SpellsNew.effect_limit_value6, SpellsNew.effect_limit_value7,
                SpellsNew.effect_limit_value8, SpellsNew.effect_limit_value9,
                SpellsNew.effect_limit_value10, SpellsNew.effect_limit_value11,
                SpellsNew.effect_limit_value12, SpellsNew.max1, SpellsNew.max2,
                SpellsNew.max3, SpellsNew.max4, SpellsNew.max5,
                SpellsNew.max6, SpellsNew.max7, SpellsNew.max8,
                SpellsNew.max9, SpellsNew.max10, SpellsNew.max11,
                SpellsNew.max12, SpellsNew.formula1, SpellsNew.formula2,
                SpellsNew.formula3, SpellsNew.formula4, SpellsNew.formula5,
                SpellsNew.formula6, SpellsNew.formula7, SpellsNew.formula8,
                SpellsNew.formula9, SpellsNew.formula10, SpellsNew.formula11,
                SpellsNew.formula12, SpellsNew.buffduration, SpellsNew.teleport_zone,
                SpellsNew.buffduration, SpellsNew.buffdurationformula, SpellsNew.RecourseLink,
                SpellsNew.goodEffect]
        query = session.query(*args).filter(params)
        result = query.all()

    data = {'game_class': utils.get_spell_class(int(class_id))}
    for entry in result:
        level = getattr(entry, f'classes{class_id}')
        if level in data:
            level_list = data[level]
        else:
            level_list = []
        parsed = translate_result(entry)
        level_list.append(parsed)

        if entry.RecourseLink > 0:
            with Session(bind=engine) as session:
                query = session.query(*args).filter(SpellsNew.id == entry.RecourseLink)
                sub_result = query.one()
            parsed = translate_result(sub_result)
            level_list.append(parsed)

        data.update({level: level_list})

    return data


def get_spell_data(spell_id, basic_data=True, skip_effect=False):
    """Returns human readible spell data."""
    excl_list = utils.get_exclusion_list('spells')
    if spell_id in excl_list:
        return None, None

    # Get the spell data
    with Session(bind=engine) as session:
        query = session.query(SpellsNew).filter(SpellsNew.id == spell_id)
        result = query.first()

        if not result:
            query = session.query(SpellsNew).filter(SpellsNew.id == spell_id)
            result = query.first()

            if not result:
                return None, None

    if basic_data:
        base = {'id': spell_id,
                'name': result.name,
                'on_you': result.cast_on_you,
                'on_other': result.cast_on_other,
                'on_fade': result.spell_fades,
                'range': result.range,
                'cast_time': result.cast_time / 1000,
                'recast_time': result.recast_time / 1000,
                'mana': result.mana,
                'resist': parse_resist(result.resisttype, result.ResistDiff),
                'skill': utils.parse_skill(result.skill),
                'classes': parse_classes(result),
                'target_type': parse_target_type(int(result.targettype)),
                'aoe_range': result.aoerange}
        if result.buffdurationformula > 0:
            base.update({'min_duration': parse_duration(result)}),
            base.update({'max_duration': parse_duration(result, min_val=False)})
        if skip_effect:
            return base
        components = []
        for idx in range(1, 5):
            item_id = getattr(result, f'components{idx}')
            if item_id != -1:
                item_name = item.get_item_name(item_id)
                components.append({'item_id': item_id,
                                   'name': item_name,
                                   'count': getattr(result, f'component_counts{idx}')})
        base.update({'components': components})

    else:
        base = {}

    slots = {}
    for idx in range(1, 13):
        if getattr(result, f'effectid{idx}') != 254:
            slots.update({f'slot_{idx}': parse_slot_data(idx, result)})

    if result.RecourseLink > 0:
        recourse_base, recourse_slots = get_spell_data(result.RecourseLink)
        base.update({'recourse_base': recourse_base,
                     'recourse_slots': recourse_slots})

    return base, slots


def parse_target_type(type_id):
    if type_id == 0:
        return "Rag'Zhezum Special"
    elif type_id == 1:
        return "Line of Sight"
    elif type_id == 2:
        return "Area of Effect over the caster"
    elif type_id == 3:
        return "Group V1"
    elif type_id == 4:
        return "Point Blank Area of Effect"
    elif type_id == 5:
        return 'Single'
    elif type_id == 6:
        return 'Self'
    elif type_id == 8:
        return 'Targeted Area of Effect'
    elif type_id == 9:
        return 'Animal'
    elif type_id == 10:
        return 'Undead'
    elif type_id == 11:
        return 'Summoned'
    elif type_id == 13:
        return 'Life Tap'
    elif type_id == 14:
        return 'Pet'
    elif type_id == 15:
        return 'Corpse'
    elif type_id == 16:
        return 'Plant'
    elif type_id == 17:
        return 'Uber Giants'
    elif type_id == 18:
        return 'Uber Dragons'
    elif type_id == 20:
        return "Targeted Area of Effect Life Tap"
    elif type_id == 24:
        return "Area of Effect Undead"
    elif type_id == 25:
        return "Area of Effect Summoned"
    elif type_id == 32:
        return "Area of Effect Caster"
    elif type_id == 33:
        return "NPC Hate List"
    elif type_id == 34:
        return "Dungeon Object"
    elif type_id == 35:
        return "Muramite"
    elif type_id == 36:
        return "Area - PC Only"
    elif type_id == 37:
        return "Area - NPC Only"
    elif type_id == 38:
        return "Summoned Pet"
    elif type_id == 39:
        return "Group No Pets"
    elif type_id == 40:
        return "Area of EffectPC V2"
    elif type_id == 41:
        return "Group v2"
    elif type_id == 42:
        return "Self(Directional)"
    elif type_id == 43:
        return "Group With Pets"
    elif type_id == 44:
        return "Beam"
    else:
        return f'Unknown target type: {type_id}'


def get_spell_min_level(data):
    min_level = 999
    for i in range(1, 16):
        check_val = getattr(data, f'classes{i}')
        if check_val < min_level:
            min_level = check_val
    if min_level == 254 or min_level == 255:
        min_level = 1
    return min_level


def parse_slot_data(idx, data, no_item_links=False):
    spa = getattr(data, f'effectid{idx}')
    min_val = getattr(data, f'effect_base_value{idx}')
    limit_val = getattr(data, f'effect_limit_value{idx}')
    max_val = getattr(data, f'max{idx}')
    formula = getattr(data, f'formula{idx}')
    min_level = get_spell_min_level(data)
    ret_data = {'spa': spa,
                'base_value': min_val,
                'max': max_val,
                'limit_value': limit_val,
                'formula': formula}
    ret_data.update({'desc': translate_spa(spa, min_val, limit_val, formula,
                                           max_val, min_level, data, no_item_links=no_item_links)})
    return ret_data


def translate_spa(spa, min_val, limit_val, formula, max_val, min_level, data, no_item_links=False):
    if spa == 0:
        # HP
        # Handle Formula = 122
        duration = parse_duration(data, min_val=False, raw_seconds=True)
        if formula == 122:
            min_mod = duration - 6
            min_dmg = min_val - (12 * (duration-min_mod))
            max_dmg = min_val
            return f'Decrease hitpoints by {abs(max_dmg)} per tick progressing to {abs(min_dmg)} per tick'

        if max_val == 0:
            minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level, ignore_max=True)
            max_val, _ = do_formula(abs(min_val), formula, max_val, level=LEVEL_CAP, ignore_max=True)
        else:
            minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level, ignore_max=False)
        if minimum < abs(min_val):
            minimum = abs(min_val)
        if min_val < 0:
            if (min_level == max_level) or min_level == 255:
                if duration:
                    return f'Decrease Hitpoints by {max_val} per tick'
                else:
                    return f'Decrease Hitpoints by {max_val}'
            else:
                if duration:
                    return f'Decrease Hitpoints by {minimum} (L{min_level}) to {max_val} (L{max_level}) per tick'
                else:
                    return f'Decrease Hitpoints by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if (min_level == max_level) or min_level == 255:
                if duration:
                    return f'Increase Hitpoints by {max_val} per tick'
                else:
                    return f'Increase Hitpoints by {max_val}'
            else:
                if duration:
                    return f'Increase Hitpoints by {minimum} (L{min_level}) to {max_val} (L{max_level}) per tick'
                else:
                    return f'Increase Hitpoints by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 1:
        # AC
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            int_min = int(round(minimum / 3))
            int_max = int(round(max_val / 3))  # This is correct
            reg_min = int(round(minimum / 4))
            reg_max = int(round(max_val / 4))  # This is correct
            if min_level == 255 or (min_level == max_level):
                return f'Decrease AC for cloth_casters by {int_min}, everyone else by {reg_min}'
            else:
                return (f'Decrease AC for cloth casters by {int_min} (L{min_level}) to {int_max} (L{max_level}), '
                        f'everyone else by {reg_min} (L{min_level}) to {reg_max} (L{max_level})')
        else:
            # TODO: Fix this
            int_min = int(round(minimum / 3))
            int_max = int(round(max_val / 3))  # This is correct
            reg_min = int(round(minimum / 4))
            reg_max = int(round(max_val / 4))  # This is correct
            if min_level == 255 or (min_level == max_level):
                return f'Increase AC for cloth casters by {int_min}, everyone else by {reg_min}'
            else:
                return (f'Increase AC for cloth casters by {int_min} (L{min_level}) to {int_max} (L{max_level}), '
                        f'everyone else by {reg_min} (L{min_level}) to {reg_max} (L{max_level})')
    elif spa == 2:
        # Attack Power
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if min_level == 255 or (max_level == min_level):
                return f'Decrease Attack Power by {minimum}'
            else:
                return f'Decrease Attack Power by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == 255 or (max_level == min_level):
                return f'Increase Attack Power by {minimum}'
            else:
                return f'Increase Attack Power by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 3:
        # Movement Rate
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if min_level == 255 or max_level == min_level:
                if minimum > max_val:
                    return f'Decrease Movement Speed by {minimum}%'
                else:
                    return f'Decrease Movement Speed by {max_val}%'
            else:
                return f'Decrease Movement Speed by {minimum}% (L{min_level}) to {max_val}% (L{max_level})'
        else:
            if min_level == 255 or max_level == min_level:
                if minimum > max_val:
                    return f'Increase Movement Speed by {minimum}%'
                else:
                    return f'Increase Movement Speed by {max_val}%'
            else:
                return f'Increase Movement Speed by {minimum}% (L{min_level}) to {max_val}% (L{max_level})'
    elif spa == 4:
        # STR
        # Handle formula 107 and 108:
        if formula == 107 or formula == 108:
            duration = parse_duration(data, min_val=False, raw_seconds=True)
            tics = duration / 6
            tic_diff = round(min_val / tics)
            max_eff = min_val
            if formula == 107:
                tic_final = tic_diff
                min_eff = int(min_val - (tics * tic_diff))
            else:
                tic_final = 2 * tic_diff
                min_eff = int(min_val - 2 * (tics * tic_diff))
            return f'Increase STR by {max_eff} decreasing by {tic_final} per tick to {min_eff}'
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if max_val == 0 or min_level == max_level:
                return f'Decrease STR by {minimum}'
            else:
                return f'Decrease STR by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if max_val == 0 or min_level == max_level:
                return f'Increase STR by {minimum}'
            else:
                return f'Increase STR by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 5:
        # DEX
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if max_val == 0 or min_level == max_level:
                return f'Decrease DEX by {minimum}'
            else:
                return f'Decrease DEX by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if max_val == 0 or min_level == max_level:
                return f'Increase DEX by {minimum}'
            else:
                return f'Increase DEX by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 6:
        # AGI
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if max_val == 0 or min_level == max_level:
                return f'Decrease AGI by {minimum}'
            else:
                return f'Decrease AGI by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if max_val == 0 or min_level == max_level:
                return f'Increase AGI by {minimum}'
            else:
                return f'Increase AGI by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 7:
        # STA
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if max_val == 0 or min_level == max_level:
                return f'Decrease STA by {minimum}'
            else:
                return f'Decrease STA by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if max_val == 0 or min_level == max_level:
                return f'Increase STA by {minimum}'
            else:
                return f'Increase STA by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 8:
        # INT
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if max_val == 0 or min_level == max_level:
                return f'Decrease INT by {minimum}'
            else:
                return f'Decrease INT by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if max_val == 0 or min_level == max_level:
                return f'Increase INT by {minimum}'
            else:
                return f'Increase INT by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 9:
        # WIS
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if max_val == 0 or min_level == max_level:
                return f'Decrease WIS by {minimum}'
            else:
                return f'Decrease WIS by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if max_val == 0 or min_level == max_level:
                return f'Increase WIS by {minimum}'
            else:
                return f'Increase WIS by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 10:
        # CHA
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        # SPA 10 is used as a sort of holding thing, if min/max are both 0, ignore this
        if minimum == max_val == 0 or max_val == 0:
            return None
        if min_val < 0:
            if max_val == 0 or min_level == max_level:
                return f'Decrease CHA by {minimum}'
            else:
                return f'Decrease CHA by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if max_val == 0 or min_level == max_level:
                return f'Increase CHA by {minimum}'
            else:
                return f'Increase CHA by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 11:
        # Melee Speed
        if min_val - 100 < 0:
            minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level, invert=True)
        else:
            minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val - 100 < 0 or min_level == 255:
            if min_level == 255 or (max_level == min_level):
                return f'Decrease Attack Speed by {abs(min_val - 100)}%'
            else:
                return (f'Decrease Attack Speed by {abs(min_val - 100)}% (L{min_level}) to '
                        f'{abs(max_val - 100)}% (L{max_level})')
        else:
            if min_level == 255 or (max_level == min_level):
                return f'Increase Attack Speed by {min_val - 100}%'
            else:
                return f'Increase Attack Speed by {minimum - 100}% (L{min_level}) to {max_val - 100}% (L{max_level})'
    elif spa == 12:
        # Invisiblity
        return 'Invisibility'
    elif spa == 13:
        # See Invis
        return 'See Invisibility'
    elif spa == 14:
        # Enduring Breath
        return 'Enduring Breath'
    elif spa == 15:
        # Mana
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        max_val, _ = do_formula(abs(min_val), formula, max_val, level=LEVEL_CAP, ignore_max=True)
        if min_val < 0:
            if min_level == max_level:
                if data.buffduration == 0:
                    return f'Decrease Mana by {minimum}'
                else:
                    return f'Decrease Mana by {minimum} per tick'
            else:
                if data.buffduration == 0:
                    return f'Decrease Mana by {minimum} (L{min_level}) to {max_val} (L{max_level})'
                else:
                    return f'Decrease Mana by {minimum} (L{min_level}) to {max_val} (L{max_level}) per tick'
        else:
            if min_level == max_level:
                if data.buffduration == 0:
                    return f'Increase Mana by {minimum}'
                else:
                    return f'Increase Mana by {minimum} per tick'
            else:
                if data.buffduration == 0:
                    return f'Increase Mana by {minimum} (L{min_level}) to {max_val} (L{max_level})'
                else:
                    return f'Increase Mana by {minimum} (L{min_level}) to {max_val} (L{max_level}) per tick'
    elif spa == 16:
        # Unused
        return 'SPA 16: Unused (tell the EQDB dev to fix me)'
    elif spa == 17:
        # Unused
        return 'SPA 17: Unused (tell the EQDB dev to fix me)'
    elif spa == 18:
        # NPC Aggro
        return 'Pacify'
    elif spa == 19:
        # NPC Faction
        return f'Increse Faction by {min_val}'
    elif spa == 20:
        # Blindness
        if min_val < 0:
            return 'Blindness'
        else:
            return 'Cure Blindness'
    elif spa == 21:
        # Stun
        return f'Stun ({min_val / 1000} sec)'
    elif spa == 22:
        # Charm
        return f'Charm up to level {max_val}'
    elif spa == 23:
        # Fear
        return f'Fear up to level {max_val}'
    elif spa == 24:
        # Fatigue
        return 'Non-Functional'
    elif spa == 25:
        # Bind Affinity
        return 'Create Bind Point'
    elif spa == 26:
        # Gate
        return 'Teleport to Bind Point'
    elif spa == 27:
        # Dispel Magic
        return f'Dispel Magic ({min_val})'
    elif spa == 28:
        # Invis Vs Undead
        return 'Invisibility versus Undead'
    elif spa == 29:
        # Invis Vs Animals
        return 'Invisibility versus Animals'
    elif spa == 30:
        # NPC-ReactRange
        return f'Reaction Radius ({min_val}/{max_val})'
    elif spa == 31:
        # Enthrall (Mez)
        return f'Mesmerize up to level {max_val}'
    elif spa == 32:
        # Create Item
        if no_item_links:
            if data.name.startswith('Summon '):
                return f'Summon item: {data.name.lstrip("Summon ")}'
            else:
                return f'Summon Item: {data.name}'
        item_name = item.get_item_name(min_val)
        return f'Summon item: <a href="/item/detail/{min_val}">{item_name}</a>'
    elif spa == 33:
        # Spawn NPC
        return f'Summon pet: <a href="/pet/detail/{data.teleport_zone}">{data.teleport_zone}</a>'
    elif spa == 34:
        # Confuse
        return f'SPA 34: Unused (tell the EQDB dev to fix me)'
    elif spa == 35:
        # Disease
        if min_val < 0:
            return f'Decrease Disease Counters by {abs(min_val)}'
        else:
            return f'Increase Disease Counters by {min_val}'
    elif spa == 36:
        # Poison
        if min_val < 0:
            return f'Decrease Poison Counters by {abs(min_val)}'
        else:
            return f'Increase Poison Counters by {min_val}'
    elif spa == 37:
        # DetectHostile
        return f'SPA 37: Unused (tell the EQDB dev to fix me)'
    elif spa == 38:
        # DetectMagic
        return f'SPA 38: Unused (tell the EQDB dev to fix me)'
    elif spa == 39:
        # NoTwincast
        return f'SPA 39: Unused (tell the EQDB dev to fix me)'
    elif spa == 40:
        # Invulnerability
        return 'Invulnerability'
    elif spa == 41:
        # Banish
        return 'Destroy Target'
    elif spa == 42:
        # Shadow Step
        return 'Shadowstep'
    elif spa == 43:
        # Berserk
        return f'SPA 43: Unused (tell the EQDB dev to fix me)'
    elif spa == 44:
        # Lycanthropy
        return 'Lycanthropy (buff blocker)'
    elif spa == 45:
        # Vampirism
        return f'SPA 45: Unused (tell the EQDB dev to fix me)'
    elif spa == 46:
        # Resist Fire
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if max_level == min_level:
            min_level = 255

        if min_val < 0:
            if min_level == 255:
                if abs(min_val) > max_val:
                    d_value = abs(min_val)
                else:
                    d_value = max_val
                return f'Decrease Fire Resist by {d_value}'
            else:
                return f'Decrease Fire Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == 255:
                if min_val > max_val:
                    d_value = min_val
                else:
                    d_value = max_val
                return f'Increase Fire Resist by {d_value}'
            else:
                return f'Increase Fire Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 47:
        # Resist Cold
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if max_level == min_level:
            min_level = 255

        if min_val < 0:
            if min_level == 255:
                if abs(min_val) > max_val:
                    d_value = abs(min_val)
                else:
                    d_value = max_val
                return f'Decrease Cold Resist by {d_value}'
            else:
                return f'Decrease Cold Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == 255:
                if min_val > max_val:
                    d_value = min_val
                else:
                    d_value = max_val
                return f'Increase Cold Resist by {d_value}'
            else:
                return f'Increase Cold Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 48:
        # Resist Poison
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if max_level == min_level:
            min_level = 255

        if min_val < 0:
            if min_level == 255:
                if abs(min_val) > max_val:
                    d_value = abs(min_val)
                else:
                    d_value = max_val
                return f'Decrease Poison Resist by {d_value}'
            else:
                return f'Decrease Poison Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == 255:
                if min_val > max_val:
                    d_value = min_val
                else:
                    d_value = max_val
                return f'Increase Poison Resist by {d_value}'
            else:
                return f'Increase Poison Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 49:
        # Resist Disease
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if max_level == min_level:
            min_level = 255

        if min_val < 0:
            if min_level == 255:
                if abs(min_val) > max_val:
                    d_value = abs(min_val)
                else:
                    d_value = max_val
                return f'Decrease Disease Resist by {d_value}'
            else:
                return f'Decrease Disease Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == 255:
                if min_val > max_val:
                    d_value = min_val
                else:
                    d_value = max_val
                return f'Increase Disease Resist by {d_value}'
            else:
                return f'Increase Disease Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 50:
        # Resist Magic
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if max_level == min_level:
            min_level = 255

        if min_val < 0:
            if min_level == 255:
                if abs(min_val) > max_val:
                    d_value = abs(min_val)
                else:
                    d_value = max_val
                return f'Decrease Magic Resist by {d_value}'
            else:
                return f'Decrease Magic Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == 255:
                if min_val > max_val:
                    d_value = min_val
                else:
                    d_value = max_val
                return f'Increase Magic Resist by {d_value}'
            else:
                return f'Increase Magic Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 51:
        # Detect (Switch) Traps
        return f'SPA 51: Unused (tell the EQDB dev to fix me)'
    elif spa == 52:
        # Detect Undead
        return 'Sense Undead'
    elif spa == 53:
        # Detect Elemental
        return 'Sense Elemental'
    elif spa == 54:
        # Detect Animals
        return 'Sense Animal'
    elif spa == 55:
        # Stoneskin
        # If there's no max_val for some reason, set it using level cap
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if max_val == 0:
            max_level = LEVEL_CAP
            max_val = min_val + int(LEVEL_CAP / 2)
        return f'Increase Absorb Damage by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 56:
        # True North
        return 'True North'
    elif spa == 57:
        # Levitation
        return 'Levitation'
    elif spa == 58:
        # Change Form
        return f'Illusion: {data.name}'
    elif spa == 59:
        # Damage Shield
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val > 0:
            return f'Decrease Damage Shield by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            return f'Increase Damage Shield by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 60:
        # Transfer Item
        return f'SPA 60: Unused (tell the EQDB dev to fix me)'
    elif spa == 61:
        # Identify
        return 'Identify Cursor Item'
    elif spa == 62:
        # Transfer Item
        return f'SPA 62: Unused (tell the EQDB dev to fix me)'
    elif spa == 63:
        # NPC-WipeHateList
        return f'Memblur ({min_val}%)'
    elif spa == 64:
        # Spin Stun
        return 'SpinStun'
    elif spa == 65:
        # Infravision
        return 'Infravision'
    elif spa == 66:
        # Ultravision
        return 'Ultravision'
    elif spa == 67:
        # NPC-POV
        return 'Eye of Zomm'
    elif spa == 68:
        # Reclaim Energy
        return "Reclaim Energy"
    elif spa == 69:
        # Maximum HP
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if max_level == min_level:
                return f'Decrease Max Hitpoints by {minimum}'
            else:
                return f'Decrease Max Hitpoints by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if max_level == min_level:
                return f'Increase Max Hitpoints by {minimum}'
            else:
                return f'Increase Max Hitpoints by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 70:
        # Corpsebomb
        return f'SPA 70: Unused (tell the EQDB dev to fix me)'
    elif spa == 71:
        # Create Undead
        return f'Summon undead pet: <a href="/pet/detail/{data.teleport_zone}">{data.teleport_zone}</a>'
    elif spa == 72:
        # PreserveCorpse
        return f'SPA 72: Unused (tell the EQDB dev to fix me)'
    elif spa == 73:
        # TargetsView
        return 'Bind Sight'
    elif spa == 74:
        # Feign Death
        return 'Feign Death'
    elif spa == 75:
        # Ventriloquism
        return 'Voice Graft'
    elif spa == 76:
        # Sentinel
        return 'Sentinel'
    elif spa == 77:
        # LocateCorpse
        return 'Locate Corpse'
    elif spa == 78:
        # Spell Shield
        return f'Increase Absorb Magic Damage by {min_val}'
    elif spa == 79:
        # Instant HP
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if min_level == 255 or (min_level == max_level):
                return f'Decrease Hitpoints when cast by {minimum}'
            else:
                return f'Decrease Hitpoints when cast by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == 255 or (min_level == max_level):
                return f'Increase Hitpoints when cast by {minimum}'
            else:
                return f'Increase Hitpoints when cast by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 80:
        # Enchant:Light
        return f'SPA 80: Unused (tell the EQDB dev to fix me)'
    elif spa == 81:
        # Resurrect
        return f'Resurrect and restore {min_val}% experience.'
    elif spa == 82:
        # Summon Target
        return 'Summon PC'
    elif spa == 83:
        # Portal
        if data.teleport_zone == 'same':
            return f'Teleport Group to Safe Spot'
        else:
            zone_id, zone_name = zone.get_zone_long_name(data.teleport_zone)
            return f'Teleport Group to <a href="/zone/detail/{zone_id}">{zone_name}</a>'
    elif spa == 84:
        # HP-NPC-ONLY (but really, its gravity flux)
        return f'Toss up by {abs(min_val)}'
    elif spa == 85:
        # Contact Ability (Melee Proc)
        spell_name = get_spell_name(min_val)
        return (f'Add Melee Proc: <a href="/spell/detail/{min_val}" data-url="{min_val}" class="spell-tooltip-link">'
                f'{spell_name}</a>')
    elif spa == 86:
        # NPC-Help-Radius
        return f'Reaction Radius ({min_val}/{max_val})'
    elif spa == 87:
        # Telescope
        return f'Increase Magnification by {min_val}%'
    elif spa == 88:
        # Evacuate
        if data.teleport_zone == 'same':
            return f'Evacuate Group to Safe Spot'
        else:
            zone_id, zone_name = zone.get_zone_long_name(data.teleport_zone)
            return f'Evacuate Group to <a href="/zone/detail/{zone_id}">{zone_name}</a>'
    elif spa == 89:
        # Change Size
        if min_val > 100:
            return f'Increase player size by {min_val - 100}%'
        else:
            return f'Decrease player size by {100 - min_val}%'
    elif spa == 90:
        # IgnorePet
        # This is only used by 2 spells, and has no effect.
        return None
    elif spa == 91:
        # SummonCorpse
        return 'Summon Corpse'
    elif spa == 92:
        # Hate (On Spell Land)
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if min_level == 255 or min_level == max_level:
                return f'Decrease Hate when cast by {minimum}'
            else:
                return f'Decrease Hate when cast by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == 255 or min_level == max_level:
                return f'Increase Hate when cast by {minimum}'
            else:
                return f'Increase Hate when cast by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 93:
        # WeatherControl
        return 'Stop Rain'
    elif spa == 94:
        # Fragile
        return 'Make Fragile (Remove Buff if Struck)'
    elif spa == 95:
        # Sacrifice
        return 'Sacrifice'
    elif spa == 96:
        # Silence
        return 'Silence'
    elif spa == 97:
        # Max Mana
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if min_level == 255:
                return f'Decrease Mana Pool by {minimum}'
            else:
                return f'Decrease Mana Pool by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == 255:
                return f'Increase Mana Pool by {minimum}'
            else:
                return f'Increase Mana Pool by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 98:
        # Bard Haste
        return f'Increase haste v2 by {min_val}%'
    elif spa == 99:
        # Root
        return 'Root'
    elif spa == 100:
        # DOT Heals
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if min_level == max_level:
                return f'Increase Hitpoints v2 by {minimum} per tick'
            else:
                return f'Decrease Hitpoints v2 by {minimum} (L{min_level}) to {max_val} (L{max_level}) per tick'
        else:
            if min_level == max_level:
                return f'Increase Hitpoints v2 by {minimum} per tick'
            else:
                return f'Increase Hitpoints v2 by {minimum} (L{min_level}) to {max_val} (L{max_level}) per tick'
    elif spa == 101:
        # Complete Heal from Donal's BP
        return 'Complete heal (with duration)'
    elif spa == 102:
        # Pet No Fear
        return 'Fear Immunity'
    elif spa == 103:
        # Summon Pet
        return 'Call Pet'
    elif spa == 104:
        # Translocate
        if not data.teleport_zone:
            return 'Translocate to Bind'
        else:
            zone_id, zone_name = zone.get_zone_long_name(data.teleport_zone)
            return f'Translocate to <a href="/zone/detail/{zone_id}">{zone_name}</a>'
    elif spa == 105:
        # Anti-Gate (NPC Only)
        return 'Prevent Gate Spell'
    elif spa == 106:
        # BeastLordPet
        return f'Summon Warder: <a href="/pet/detail/{data.teleport_zone}">{data.teleport_zone}</a>'
    elif spa == 107:
        # Alter Pet Level
        return f'SPA 107: Unused (tell the EQDB dev to fix me)'
    elif spa == 108:
        # Familiar
        return f'Summon Familiar: <a href="/pet/detail/{data.teleport_zone}">{data.teleport_zone}</a>'
    elif spa == 109:
        # CreateItemInBag
        item_name = item.get_item_name(min_val)
        if no_item_links:
            return f'Summon item: {item_name}'
        return f'Summon item (In Bag): <a href="/item/detail/{min_val}">{item_name}</a>'
    elif spa == 110:
        # Ranger Archery Accuracy %
        return f'SPA 110: Unused (tell the EQDB dev to fix me)'
    elif spa == 111:
        # Resistances
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level, ignore_max=True)
        if min_val < 0:
            if min_val >= max_val:
                return f'Decrease all resists by {minimum}'
            else:
                return f'Decrease all resists by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_val >= max_val:
                return f'Increase all resists by {minimum}'
            else:
                return f'Increase all resists by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 112:
        # Adjust Casting Skill (Fizzles)
        return f'Increase Effective Casting Level by {min_val}'
    elif spa == 113:
        # Summon Horse
        return f'Summon Horse: <a href="/pet/detail/{data.teleport_zone}">{data.teleport_zone}</a>'
    elif spa == 114:
        # Modify Hate
        if min_val < 0:
            return f'Decrease agro modifier by {min_val}%'
        else:
            return f'Increase agro modifier by {max_val}%'
    elif spa == 115:
        # Cornucopia
        return f'Remove food/water requirement'
    elif spa == 116:
        # Curse
        if min_val < 0:
            return f'Decrease Curse Counters by {abs(min_val)}'
        else:
            return f'Increase Curse Counters by {min_val}'
    elif spa == 117:
        # HitMagic
        return 'Make weapons magical'
    elif spa == 118:
        # Amplification
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        max_val, _ = do_formula(abs(min_val), formula, max_val, level=LEVEL_CAP)
        if min_val < 0:
            if min_level == max_level:
                return f'Increase Singing Skill by {minimum}'
            else:
                return f'Decrease Singing Skill by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == max_level:
                return f'Increase Singing Skill by {minimum}'
            else:
                return f'Increase Singing Skill by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 119:
        # BardHaste2
        return f'Increase haste v3 (Overhaste) by {min_val}%'
    elif spa == 120:
        # HealMod
        return f'Reduce Incoming Healing by {abs(min_val)}%'
    elif spa == 121:
        # IronMaiden aka Reverse DS
        return f'Reverse Damage Shield {abs(min_val)}'
    elif spa == 122:
        # ReduceSkill
        # Get the skill name
        skill_name = utils.parse_skill(min_val)
        minimum, _ = do_formula(abs(min_val), formula, max_val, level=min_level)
        return f"Reduce skill '{skill_name}' by {minimum}"
    elif spa == 123:
        # Immunity (actually a stack blocker)
        return 'Screech'
    elif spa == 124:
        # Focus: Damage %
        if min_val < 0:
            return f'Decrease Spell Damage by {abs(min_val)}%'
        else:
            return f'Increase Spell Damage by {min_val}% to {limit_val}%'
    elif spa == 125:
        # Focus: Healing %
        return f'Increase Spell Healing by {min_val}% to {limit_val}%'
    elif spa == 126:
        # Focus: Resist Reducer
        return f'Reduce Spell Resistance by {min_val} to {limit_val}'
    elif spa == 127:
        # Focus: Cast Time
        return f'Increase Spell Haste by {min_val}%'
    elif spa == 128:
        # Focus: Duration Modifier
        return f'Increase Spell Duration by {min_val}%'
    elif spa == 129:
        # Focus: Range Modifier
        return f'Increase Spell Range by {min_val}%'
    elif spa == 130:
        # Focus: Hate Modifier
        return f'Increase Spell/Bash Hate by {min_val}% to {limit_val}%'
    elif spa == 131:
        # Focus: Reagent Modifier
        return f'Decrease chance of using reagents by {min_val}% to {limit_val}%'
    elif spa == 132:
        # Focus: Mana Modifier
        return f'Decrease mana cost by {min_val}% to {limit_val}%'
    elif spa == 133:
        # Focus: Stun Time Modifier
        return f'SPA 110: Unused (tell the EQDB dev to fix me)'
    elif spa == 134:
        # Focus: Maximum Level
        return f'Limit: Maximum Level {min_val}'
    elif spa == 135:
        # Focus: Resist Type
        # Get the spell type
        resist = utils.get_elem_dmg_type(min_val)
        return f"Limit Spell Type '{resist}'"
    elif spa == 136:
        # Focus: Target Type
        # Get the target type
        t_type = parse_target_type(abs(min_val))
        if min_val < 0:
            return f"Limit: Exclude 'Target {t_type}'"
        else:
            return f"Limit: Only 'Target {t_type}'"
    elif spa == 137:
        # Focus: Which SPA?
        # Get the short name for the SPA
        spa_name = fast_spa_lookup(abs(min_val))
        if min_val >= 0:
            return f"Limit: Only Effect '{spa_name}'"
        else:
            return f"Limit: Exclude Effect '{spa_name}'"
    elif spa == 138:
        # Focus: Beneficial or Detrimental (w/o this, its all spells)
        if not min_val:
            return 'Limit: Beneficial Spells Only'
        else:
            return 'Limit: Detrimental Spells Only'
    elif spa == 139:
        # Focus: Which Spell ID?
        spell_name = get_spell_name(abs(min_val))
        if min_val >= 0:
            return (f'Limit: Only Spell <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                    f'class="spell-tooltip-link">{spell_name}</a>')
        else:
            return (f'Limit: Exclude Spell <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                    f'class="spell-tooltip-link">{spell_name}</a>')
    elif spa == 140:
        # Focus: Minimum Duration
        seconds = min_val * 6
        return f'Limit: Minimum {seconds} sec duration required.'
    elif spa == 141:
        # Focus: Instant Only
        return 'Limit: Instant Only'
    elif spa == 142:
        # Focus: Level Minimum
        return f'Limit: Minimum Level {min_val}'
    elif spa == 143:
        # Focus: Cast Time Min
        return f'Limit: Minimum cast time {min_val / 1000} sec'
    elif spa == 144:
        # Focus: Cast Time Max
        return f'Limit: Maximum cast time {min_val / 1000} sec'
    elif spa == 145:
        # Portal NPC Warder Banish
        return f'Banish to {data.teleport_zone}'
    elif spa == 146:
        # Portal Locations
        # Two spells use this, but it does nothing?  Return None
        # return f'SPA 146: Unused (tell the EQDB dev to fix me)'
        return None
    elif spa == 147:
        # Percent Heal
        return f'Increase Hitpoints by {max_val} (Limit: {min_val}%)'
    elif spa == 148:
        # StackingBlocker
        # Get the short name for the SPA
        spa_name = fast_spa_lookup(abs(min_val))
        if max_val > 0:
            return f"Stacking: Block Spell if any slot is 'Increase {spa_name}' with value < {max_val}"
        else:
            return f"Stacking: Block Spell if any slot is 'Decrease {spa_name}' with value < {max_val}"
    elif spa == 149:
        # StripVirtualSlot
        # Get the short name for the SPA
        # This is probably not right, but it looks more accurate than other sites.
        spa_name = fast_spa_lookup(abs(min_val))
        return f"Stacking: Overwrite Spell if any slot is '{spa_name}' with value < {abs(max_val - 1000)}"
    elif spa == 150:
        # DI/DP
        if min_val == 1:
            return 'Death Save - Restore Partial Health'
        else:
            return 'Death Save - Restore Full Health'
    elif spa == 151:
        # PocketPet
        return "Suspend Pet"
    elif spa == 152:
        # PetSwarm
        return f'Summon Swarm Pet(s): <a href="/pet/detail/{data.teleport_zone}">{data.teleport_zone}</a>'
    elif spa == 153:
        # Damage Balance
        return f'Balance group health with {min_val} penalty'
    elif spa == 154:
        # Cancel Negative
        return 'Remove Detrimental Effect'
    elif spa == 155:
        # PoP Resurrect
        return f'SPA 155: Unused (tell the EQDB dev to fix me)'
    elif spa == 156:
        # Mirror
        return 'Illusion Target'
    elif spa == 157:
        # Feedback
        return f'Increase spell damage shield by {min_val}'
    elif spa == 158:
        # Reflect
        return f'Increase chance to reflect spell by {min_val}%'
    elif spa == 159:
        # Mod all Stats
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=LEVEL_CAP)
        if min_val < 0:
            if min_level == 255:
                return f'Decrease All Stats by {minimum}'
            else:
                return f'Decrease All Stats by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            if min_level == 255:
                return f'Increase All Stats by {minimum}'
            else:
                return f'Increase All Stats by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 160:
        # Drunk
        return f'Drunk if Alcohol Tolerance < {min_val}'
    elif spa == 161:
        # Spell Guard
        return f'Mitigate spell damage by {min_val}% until {max_val} absorbed'
    elif spa == 162:
        # Melee Guard
        return f'Mitigate melee damage by {min_val}% until {max_val} absorbed'
    elif spa == 163:
        # Absorb Hit
        return f'Block next {min_val} melee or spell hits, up to {max_val} damage.'
    elif spa == 164:
        # Object - Sense Trap
        return 'Sense Traps'
    elif spa == 165:
        # Object - Disarm Trap
        return 'Disarm Traps'
    elif spa == 166:
        # Object - Picklock
        return 'Pick Lock'
    elif spa == 167:
        # Focus: Pet Power
        return f'Increase pet power by {min_val}'
    elif spa == 168:
        # Defensive
        if min_val < 0:
            return f'Increase Melee Mitigation by {abs(min_val)}%'
        else:
            return f'Decrease Melee Mitigation by {min_val}%'
    elif spa == 169:
        # Critical Melee (PC Only)
        skill_name = utils.parse_skill(limit_val)
        if min_val > 0:
            return f"Increase Skill '{skill_name}' Critical Strike Chance by {min_val}%"
        else:
            return f"Decrease Skill '{skill_name}' Critical Strike Chance by {min_val}%"
    elif spa == 170:
        # Spell Critical Damage
        if min_val > 0:
            return f'Increase Spell Critical Strike Chance by {min_val}%'
        else:
            return f'Decrease Spell Critical Strike Chance by {abs(min_val)}%'
    elif spa == 171:
        # Crippling BLow
        if min_val > 0:
            return f'Increase Crippling Blow Chance by {min_val}%'
        else:
            return f'Decrease Crippling Blow Chance by {abs(min_val)}%'
    elif spa == 172:
        # Evasion
        if min_val > 0:
            return f'Increase Chance to Avoid Melee by {min_val}%'
        else:
            return f'Decrease Chance to Avoid Melee by {abs(min_val)}%'
    elif spa == 173:
        # Riposte
        if min_val > 0:
            return f'Increase Chance to Riposte by {min_val}%'
        else:
            return f'Decrease Chance to Riposte by {abs(min_val)}%'
    elif spa == 174:
        # Dodge
        if min_val > 0:
            return f'Increase Chance to Dodge by {min_val}%'
        else:
            return f'Decrease Chance to Dodge by {abs(min_val)}%'
    elif spa == 175:
        # Parry
        if min_val > 0:
            return f'Increase Chance to Parry by {min_val}%'
        else:
            return f'Decrease Chance to Parry by {abs(min_val)}%'
    elif spa == 176:
        # Dual Wield
        if min_val > 0:
            return f'Increase Chance to Dual Wield by {min_val}%'
        else:
            return f'Decrease Chance to Dual Wield by {abs(min_val)}%'
    elif spa == 177:
        if min_val > 0:
            return f'Increase Chance to Double Attack by {min_val}%'
        else:
            return f'Decrease Chance to Double Attack by {abs(min_val)}%'
    elif spa == 178:
        # Lifetap from Melee
        return f'Lifetap from {min_val}% melee damage'
    elif spa == 179:
        # Puretone
        return f'Instrument Modifier {min_val}%'
    elif spa == 180:
        # Sanctification
        if min_val > 0:
            return f'Increase Spell Resistance by {min_val}%'
        else:
            return f'Decrease Spell Resistance by {abs(min_val)}%'
    elif spa == 181:
        # Fearless
        if min_val > 0:
            return f'Increase Fear Resistance by {min_val}%'
        else:
            return f'Decrease Fear Resistance by {abs(min_val)}%'
    elif spa == 182:
        # Hundred Hands
        if min_val < 0:
            return f'Hundred Hands (Reduce Delay by {(abs(min_val) / 10)}%)'
        else:
            return f'Hundred Hands (Increase Delay by {min_val / 10}%)'
    elif spa == 183:
        # UNUSED - Skill Increase Chance
        if min_val > 0:
            return f'Increase Chance to Hit with all skills by {min_val}%'
        else:
            return f'Decrease Chance to Hit with all skills by {abs(min_val)}%'
    elif spa == 184:
        # Accuracy %
        if min_val > 0:
            return f'Increase Chance to Hit with all skills by {min_val}%'
        else:
            return f'Decrease Chance to Hit with all skills by {abs(min_val)}%'
    elif spa == 185:
        # Skill Damage Mod 1
        if min_val > 0:
            return f'Increase All Skills Damage Modifier by {min_val}%'
        else:
            return f'Decrease All Skills Damage Modifier by {abs(min_val)}%'
    elif spa == 186:
        # Min Damage Done Mod
        if min_val > 0:
            return f'Increase All Skills Minimum Damage Modifier by {min_val}%'
        else:
            return f'Decrease All Skills Minimum Damage Modifier by {abs(min_val)}%'
    elif spa == 187:
        # Mana Balance
        return f'Balance Party Mana with {min_val}% penalty'
    elif spa == 188:
        # Block
        if min_val > 0:
            return f'Increase Chance to Block by {min_val}%'
        else:
            return f'Decrease Chance to Block by {abs(min_val)}%'
    elif spa == 189:
        # Endurance
        if min_val > 0:
            return f'Increase Endurance by {min_val}'
        else:
            return f'Decrease Endurance by {abs(min_val)}'
    elif spa == 190:
        # Max Endurance
        if min_val > 0:
            return f'Increase Endurance Pool by {min_val}'
        else:
            return f'Decrease Endurance Pool by {abs(min_val)}'
    elif spa == 191:
        # Amnesia
        return f'Silence Melee Ability'
    elif spa == 192:
        # Hate (Duration Only)
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            if min_level == 255:
                return f'Decrease Hate by {minimum} per tick'
            else:
                return f'Decrease Hate by {minimum} (L{min_level}) to {max_val} (L{max_level}) per tick'
        else:
            if min_level == 255 or max_level == min_level:
                return f'Increase Hate by {minimum} per tick'
            else:
                return f'Increase Hate by {minimum} (L{min_level}) to {max_val} (L{max_level}) per tick'
    elif spa == 193:
        # Skill Attack
        # TODO: Figure out what the numbers here do
        return f'Skill Attack'
    elif spa == 194:
        # Fade
        return f'Fading Memories (100% Agro Drop)'
    elif spa == 195:
        # Stun Resist (Melee+Spell)
        return f'Stun Resist {min_val}%'
    elif spa == 196:
        # Deprecated (Strikethrough)
        return 'Strikethrough'
    elif spa == 197:
        # Skill Damage Taken Incoming
        skill_name = utils.parse_skill(limit_val)
        return f"Skill '{skill_name}' Damage Taken {min_val}%"
    elif spa == 198:
        # Instant Endurance
        if min_val > 0:
            return f'Increase Endurance by {min_val}'
        else:
            return f'Decrease Endurance by {abs(min_val)}'
    elif spa == 199:
        # Taunt
        return f'Taunt with {min_val}% effectiveness'
    elif spa == 200:
        # Weapon Proc Chance
        return f'Increase Proc Chance by {min_val}%'
    elif spa == 201:
        # Ranged Proc
        return f'Increase Ranged Proc Modified by {min_val}%'
    elif spa == 202:
        # IllusionOther
        return f'Next illusion affects target PC'
    elif spa == 203:
        # MassBuff
        return f'Next buff spell affects all PC around caster'
    elif spa == 204:
        # Group Fear Immunity
        return f'Group Fear Immunity'
    elif spa == 205:
        # AE Rampage Instant
        return f'Melee attack all NPCs around caster'
    elif spa == 206:
        # AE Taunt
        return f'Taunt all NPCs around caster with {min_val}% chance to land'
    elif spa == 207:
        # Flesh to Bone
        return f'Flesh to Bone'
    elif spa == 208:
        # Purge Poison
        return f'SPA 208: Unused (tell the EQDB dev to fix me)'
    elif spa == 209:
        # Cancel Beneficial
        return f'Dispel Magic (Beneficial Only)'
    elif spa == 210:
        # Shield Caster
        return f'Pet Shield'
    elif spa == 211:
        # AE Melee (PC Only)
        return f'Area Effect Melee'
    elif spa == 212:
        # Focus: Frenzied Devastation
        return f'SPA 212: Unused (tell the EQDB dev to fix me)'
    elif spa == 213:
        # Pet % HP
        return f'SPA 213: Unused (tell the EQDB dev to fix me)'
    elif spa == 214:
        # HP Max Percent
        if min_val < 0:
            return f'Reduce maximum hp by {min_val / 100}%'
        else:
            return f'Increase maximum hp by {min_val / 100}%'
    elif spa == 215:
        # Pet Avoidance %
        return f'SPA 215: Unused (tell the EQDB dev to fix me)'
    elif spa == 216:
        # Melee Accuracy Amt
        if min_val > 0:
            return f'Increase Melee Accuracy by {min_val}%'
        else:
            return f'Decrease Melee Accuracy by {abs(min_val)}%'
    elif spa == 217:
        # Headshot
        return f'SPA 217: Unused (tell the EQDB dev to fix me)'
    elif spa == 218:
        # Pet Crit Melee Chance (Owner)
        return f'SPA 218: Unused (tell the EQDB dev to fix me)'
    elif spa == 219:
        # Slay Undead
        return f'Chance to trigger Slay Undead increased by {min_val}%'
    elif spa == 220:
        # Skill Min_damage Amt 1
        if min_val > 0:
            return f'Increase Skill Damage by {min_val}%'
        else:
            return f'Decrease Skill Damage by {min_val}%'
    elif spa == 221:
        # Reduce Weight
        # This is weird, only one spell uses it and Lucy thinks it corruption counters?
        return f'Increase Corruption Counter by {min_val}'
    elif spa == 222:
        # BlockBehind
        if min_val > 0:
            return f'Increase chance to block attacks from behind by {min_val}%'
        else:
            return f'Decrease chance to block attacks from behind by {min_val}%'
    elif spa == 223:
        # Double Riposte
        if min_val > 0:
            return f'Increase chance to double riposte by {min_val}%'
        else:
            return f'Decrease chance to double riposte by {min_val}%'
    elif spa == 224:
        # Add Riposte
        if min_val > 0:
            return f'Increase chance to double riposte by {min_val}%'
        else:
            return f'Decrease chance to double riposte by {min_val}%'
    elif spa == 225:
        # Give Double Attack
        if min_val > 0:
            return f'Increase chance to double attack by {min_val}%'
        else:
            return f'Decrease chance to double attack by {min_val}%'
    elif spa == 226:
        # 2HBash
        return f'SPA 226: Unused (tell the EQDB dev to fix me)'
    elif spa == 227:
        # ReduceSkillTimer
        return f'Reduce SKill Timer by {min_val}%'
    elif spa == 228:
        # ReduceFallDmg
        return f'SPA 228: Unused (tell the EQDB dev to fix me)'
    elif spa == 229:
        # CastThroughStun
        return f'SPA 229: Unused (tell the EQDB dev to fix me)'
    elif spa == 230:
        # Increase Shield Distance
        return f'SPA 230: Unused (tell the EQDB dev to fix me)'
    elif spa == 231:
        # StunBashChance
        return f'SPA 231: Unused (tell the EQDB dev to fix me)'
    elif spa == 232:
        # Divine Save
        return f'{min_val}% chance to return to life and gain invulnerability on death'
    elif spa == 233:
        # Metabolism
        return f'Reduce food/water usage by {min_val}%'
    elif spa == 234:
        # Poison Mastery
        return f'SPA 234: Unused (tell the EQDB dev to fix me)'
    elif spa == 235:
        # FocusChanneling
        return f'SPA 235: Unused (tell the EQDB dev to fix me)'
    elif spa == 236:
        # Free Pet
        return f'SPA 236: Unused (tell the EQDB dev to fix me)'
    elif spa == 237:
        # PetAffinity
        return f'SPA 237: Unused (tell the EQDB dev to fix me)'
    elif spa == 238:
        # Permanent Illusion
        return f'SPA 238: Unused (tell the EQDB dev to fix me)'
    elif spa == 239:
        # Stonewall
        return f'SPA 239: Unused (tell the EQDB dev to fix me)'
    elif spa == 240:
        # String Unbreakable
        return f'SPA 240: Unused (tell the EQDB dev to fix me)'
    elif spa == 241:
        # Improve Reclaim Energy
        return f'SPA 241: Unused (tell the EQDB dev to fix me)'
    elif spa == 242:
        # IncreaseChanceMemwipe
        return f'SPA 230: Unused (tell the EQDB dev to fix me)'
    elif spa == 243:
        # NoBreakCharmChance
        return f'Decrease charm break chance by {min_val}%'
    elif spa == 244:
        # Root Break Chance
        return f'Decrease root break chance by {min_val}%'
    elif spa == 245:
        # Trap Circumvention
        return f'SPA 245 Unused (tell the EQDB dev to fix me)'
    elif spa == 246:
        # Lung Capacity
        return f'Reduce lung capacity value by {abs(min_val)}'
    elif spa == 247:
        # IncreaseSkillCap
        return f'SPA 247 Unused (tell the EQDB dev to fix me)'
    elif spa == 248:
        # ExtraSpecialization
        return f'SPA 248: Unused (tell the EQDB dev to fix me)'
    elif spa == 249:
        # Offhand Weapon MinDamage Bonus
        return f'SPA 249: Unused (tell the EQDB dev to fix me)'
    elif spa == 250:
        # Increse ContactAbility Chance
        if min_val > 0:
            return f'Increase chance to spell proc by {min_val}%'
        else:
            return f'Decrease chance to spell proc by {min_val}%'
    elif spa == 251:
        # EndlessQuiver
        return f'SPA 251: Unused (tell the EQDB dev to fix me)'
    elif spa == 252:
        # Backstab FullDamage From Front
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 253:
        # Chaotic Stab
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 254:
        # NoSpell
        # This is the original "blank" spell slot
        return None
    elif spa == 255:
        # Shielding Duration Mod
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 256:
        # Shroud of Stealth
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 257:
        # DEPRECATED - GivePetHold
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 258:
        # Triple Backstab
        return f'Increase chance to triple backstab by {min_val}%'
    elif spa == 259:
        # ACLimitMod
        return f'Increase Melee Mitigation by {min_val}'
    elif spa == 260:
        # AddInstrumentMod
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 261:
        # SongModCap
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 262:
        # StatsCap
        return f'Increase Stats Cap by {max_val}'
    elif spa == 263:
        # TradeskillMasteries
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 264:
        # ReduceAATimer
        return f'Decrease reuse timer by {min_val}% on AA {limit_val}'
    elif spa == 265:
        # NoFizzle
        return f'Deactivate Mastery of the Past'
    elif spa == 266:
        # AddExtraAttackChance 2H
        return f'Extra Double Attack Chance by {min_val}%'
    elif spa == 267:
        # AddPetCommands
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 268:
        # AlcFailRate
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 269:
        # Bandage Max HP Limit %
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 270:
        # Bard Song beneficial Radius %
        return f'Increase Bard Song Range by {min_val}%'
    elif spa == 271:
        # BaseRunMod
        return f'Increase Base Movement Speed by {min_val}%'
    elif spa == 272:
        # Bard Song Level
        return f'Reduce Bard Instrument Level by {min_val}'
    elif spa == 273:
        # Critical DoT
        return f'Increase chance to critically strike with DoT damage by {min_val}'
    elif spa == 274:
        # Critical Heal
        return f'Increase chance to critically heal by {min_val}%'
    elif spa == 275:
        # Critical Mend %
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 276:
        # DualWieldAmt
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 277:
        # ExtraDIChance
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 278:
        # FinishingBlow
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 279:
        # FlurryChance (PC Only)
        return f'Increase chance to flurry by {min_val}%'
    elif spa == 280:
        # Pet Flurry Chance (Owner)
        return f'Increase chance for pet to flurry by {min_val}%'
    elif spa == 281:
        # GivePetFeign
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 282:
        # Increase Bandage Heal %
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 283:
        # SpecialAttackChain
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 284:
        # LoHSetHeal
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 285:
        # Allow Hide/Evade While Moving
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 286:
        # Focus: Damage Amount
        return f'Increase spell damage by {min_val}'
    elif spa == 287:
        # Focus: DurationMod (static)
        return f'Increaes spell duration by {min_val} tick(s)'
    elif spa == 288:
        # Add Proc Hit (AA)
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 289:
        # Doom Effect
        spell_name = get_spell_name(abs(min_val))
        return (f'Cast on Fade: <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" class="spell-tooltip-link">'
                f'{spell_name}</a>')
    elif spa == 290:
        # Increase Movement Cap
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 291:
        # Purify
        return f'Remove Detrimental {min_val}x'
    elif spa == 292:
        # Strikethrough
        return 'Enable Heroic Strikethrough'
    elif spa == 293:
        # StunResist2 (Melee)
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 294:
        # Spell Crit Chance
        if min_val > 0:
            return f'Increase chance to critically strike with spells by {min_val}%'
        else:
            return f'Decrease chance to critically strike with spells by {min_val}%'
    elif spa == 295:
        # ReduceTimerSpecial
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 296:
        # Focus: Spell Damage % Incoming
        if min_val == limit_val:
            return f'Increase Spell Damage Taken by {limit_val}%'
        else:
            return f'Increase Spell Damage Taken by {min_val}% to {limit_val}%'
    elif spa == 297:
        # Focus: Spell Damage Amt Incoming
        return f'Increase Spell Damage Taken by {min_val}'
    elif spa == 298:
        # Height (Small)
        return f'Shrink Pet'
    elif spa == 299:
        # Wake the Dead 1 (Corpse Class)
        return f'Summon Swarm Pet: <a href="/pet/detail/{data.teleport_zone}">{data.teleport_zone}</a>'
    elif spa == 300:
        # Doppelganger
        return f'Summon Swarm Pets: <a href="/pet/detail/{data.teleport_zone}">{data.teleport_zone}</a>'
    elif spa == 301:
        # Increase Range Damage
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 302:
        # Focus Damage % Crit
        return f'Increase Spell Critical Strike Damage by {min_val}%'
    elif spa == 303:
        # Focus Damage Amt Crit
        return f'Increase Spell Critical Stirke Damage by {min_val}'
    elif spa == 304:
        # Secondary Riposte Mod
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 305:
        # Mitigate Damage Shield Offhand
        return f'Reduce damage shield damage taken by {min_val}'
    elif spa == 306:
        # Wake the Dead 2 (File Class)
        return f'Summon Swarm Pets: <a href="/pet/detail/{data.teleport_zone}">{data.teleport_zone}</a>'
    elif spa == 307:
        # Appraisal
        return 'Show Sell Price of Item on Cursor'
    elif spa == 308:
        # Zone Suspend Minion
        return 'Enable Suspended Minion across Zone Lines'
    elif spa == 309:
        # Teleport Caster's Bindpoint
        return "Transport to Caster's Bindpoint"
    elif spa == 310:
        # Focus: Reuse Timer
        return f"Reduce reuse timer by {min_val / 1000} seconds"
    elif spa == 311:
        # Focus: Combat Skill
        if min_val == 0:
            return f'Limit: Exclude Combat Skills'
        else:
            return f'Limit: Only Combat Skills'
    elif spa == 312:
        # Observer
        return 'Enable Sanctuary Effect'
    elif spa == 313:
        # Forage Master
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 314:
        # Improved Invis
        return f'Improved (No Early Break) Invisibility'
    elif spa == 315:
        # Improved Invis Undead
        return f'Improved (No Early Break) Invisibility'
    elif spa == 316:
        # Improved Invis Animals
        return f'Improved (No Early Break) Invisibility'
    elif spa == 317:
        # Worn Regen Cap
        # Used by two debug spells
        return None
    elif spa == 318:
        # Worn Mana Regen Cap
        # Used by two debug spells
        return None
    elif spa == 319:
        # Critical HP Regen
        if min_val > 0:
            return f'Increase chance to critically strike with heal over time by {min_val}%'
        else:
            return f'Decrease chance to critically strike with heal over time by {min_val}%'
    elif spa == 320:
        # Shield Block Chance
        if min_val > 0:
            return f'Increase chance to block with a shield by {min_val}%'
        else:
            return f'Decrease chance to block with a shield by {min_val}%'
    elif spa == 321:
        # Reduce Target Hate
        return f'Reduce hate by {min_val}'
    elif spa == 322:
        # Gate Starting City
        return f'Teleport to Origin city'
    elif spa == 323:
        # Defensive Proc
        spell_name = get_spell_name(abs(min_val))
        return (f'Enable Defensive Proc: <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                f'class="spell-tooltip-link">{spell_name}</a>')
    elif spa == 324:
        # HP for Mana
        return f'Consume HP instead of mana ({min_val} percent cost)'
    elif spa == 325:
        # No Break AE Sneak
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 326:
        # Spell Slots
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 327:
        # Buff Slots
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 328:
        # Negative HP Limit
        return f'Increase negative health maximum by {min_val}'
    elif spa == 329:
        # Mana Absorb % Damage
        return f'Absorb {min_val}% damage from mana'
    elif spa == 330:
        # Critical Melee Damage Mod
        if min_val > 0:
            return f'Increase melee critical strike damage by {min_val}%'
        else:
            return f'Decrease melee critical strike damage by {min_val}%'
    elif spa == 331:
        # Alchemy Item Recovery
        return f'Increase chance to trigger Salvage by {min_val}%'
    elif spa == 332:
        # Summon to Corpse
        return f'Summon Player to Corpse'
    elif spa == 333:
        # Doom Rune Effect
        return f'Gain {min_val} Damage Rune on Fade'
    elif spa == 334:
        # HP No Move
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if max_val == 0:
            return f'Bard AoE DoT by {minimum}'
        else:
            return f'Bard AoE DoT by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 335:
        # Focus Immunity Focus
        return f'Block Next Applicable Spell'
    elif spa == 336:
        # Illusionary Target
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 337:
        # Increase EXP %
        return f'Increase XP gained by {min_val}%'
    elif spa == 338:
        # Expedient Recovery
        return f'Summon and Ressurect ({min_val}%) all corpses'
    elif spa == 339:
        # Focus: Proc on Cast
        spell_name = get_spell_name(abs(limit_val))
        return (f'{min_val}% chance to trigger on spell cast: <a href="/spell/detail/{abs(limit_val)}" '
                f'data-url="{min_val}" class="spell-tooltip-link">{spell_name}</a>')
    elif spa == 340:
        # Chance Spell
        spell_name = get_spell_name(abs(limit_val))
        return (f'{min_val}% chance to trigger on song cast: <a href="/spell/detail/{abs(limit_val)}" '
                f'data-url="{min_val}" class="spell-tooltip-link">{spell_name}</a>')
    elif spa == 341:
        # Worn Attack Cap
        # Used by two test spells
        return None
    elif spa == 342:
        # No Panic
        return 'Prevent NPC from Fleeing'
    elif spa == 343:
        # Spell Interrupt
        return f'{min_val}% chance to interrupt spell casting'
    elif spa == 344:
        # Item Channeling
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 345:
        # Assassinate Max Level / Chance
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 346:
        # Headshot Max
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 347:
        # Double Ranged Attack
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 348:
        # Focus: Mana Min
        return f'Limit: Minimum Mana {min_val}'
    elif spa == 349:
        # Increase Damage With Shield
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 350:
        # Manaburn
        return f'Convert {min_val} mana to damage'
    elif spa == 351:
        # Spawn Interactive Object
        return f'Summon Aura: <a href="/pet/detail/{data.teleport_zone}">{data.teleport_zone}</a>'
    elif spa == 352:
        # Increase Trap Count
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 353:
        # Increase SOI Count
        return f'Increase number of usable auras by {min_val}'
    elif spa == 354:
        # Deactivate All Traps
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 355:
        # Learn Trap
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 356:
        # Change Trigger Type
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 357:
        # Focus: Mute
        return f'{min_val}% chance to prevent damage or healing spell'
    elif spa == 358:
        # Instant Mana
        return f'Increase current mana by {min_val}'
    elif spa == 359:
        # Passive Sense Trap
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 360:
        # Proc on Kill Shot
        spell_name = get_spell_name(abs(limit_val))
        return (f'{min_val}% Chance to Proc Effect on Kill Shot: '
                f'<a href="/spell/detail/{abs(limit_val)}" data-url="{limit_val}" class="spell-tooltip-link">'
                f'{spell_name}</a>')
    elif spa == 361:
        # Proc on Death
        spell_name = get_spell_name(abs(limit_val))
        return (f'{min_val}% Chance to Proc Effect on death: '
                f'<a href="/spell/detail/{abs(limit_val)}" data-url="{limit_val}" class="spell-tooltip-link">'
                f'{spell_name}</a>')
    elif spa == 362:
        # Potion Belt
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 363:
        # Bandolier
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 364:
        # AddTripleAttackChance
        if min_val > 0:
            return f'Increase triple attack chance by {min_val}%'
        else:
            return f'Decrease triple attack chance by {min_val}%'
    elif spa == 365:
        # Proc On Spell Kill Shot
        spell_name = get_spell_name(abs(limit_val))
        return (f'{min_val}% Chance to Proc Effect on Spell Kill Shot: '
                f'<a href="/spell/detail/{abs(limit_val)}" data-url="{limit_val}" class="spell-tooltip-link">'
                f'{spell_name}</a>')
    elif spa == 366:
        # Group Shielding
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 367:
        # Modify Body Type
        body_type = utils.get_bane_dmg_body(min_val)
        return f'Set body type to {body_type}'
    elif spa == 368:
        # Modify Faction
        return f'Set faction <a href="/faction/detail/{min_val}">{min_val}</a> to {limit_val}'
    elif spa == 369:
        # Corruption
        if min_val < 0:
            return f'Decrease Corruption Counters by {abs(min_val)}'
        else:
            return f'Increase Corruption Counters by {min_val}'
    elif spa == 370:
        # Corruption Resist
        minimum, max_level = do_formula(abs(min_val), formula, max_val, level=min_level)
        if min_val < 0:
            return f'Decrease Corruption Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
        else:
            return f'Increase Corruption Resist by {minimum} (L{min_level}) to {max_val} (L{max_level})'
    elif spa == 371:
        # Slow
        return f'Slow melee attack speed by {min_val}%'
    elif spa == 372:
        # Grant Foraging
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 373:
        # Doom Always
        spell_name = get_spell_name(abs(min_val))
        return (f'Trigger on Fade: <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                f'class="spell-tooltip-link">{spell_name}</a>')
    elif spa == 374:
        # Trigger Spell
        spell_name = get_spell_name(abs(limit_val))
        return (f'{min_val}% chance to trigger: <a href="/spell/detail/{abs(limit_val)}" '
                f'data-url="{limit_val}" class="spell-tooltip-link">{spell_name}</a>')
    elif spa == 375:
        # Critical DoT Damage Mod %
        return f'Increase DoT Critical Damage by {min_val}%'
    elif spa == 376:
        # Fling
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 377:
        # Doom Entity
        spell_name = get_spell_name(abs(min_val))
        return (f'Cast on fade if not dispelled: <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                f'class="spell-tooltip-link">{spell_name}</a>')
    elif spa == 378:
        # Resist other SPA
        spa_name = fast_spa_lookup(limit_val)
        return f'{min_val}% chance to resist {spa_name}'
    elif spa == 379:
        # Directional Shadowstep
        return 'Blink'
    elif spa == 380:
        # Kockback Explosive (PC Only)
        return f'Knockback {min_val}'
    elif spa == 381:
        # Fling Target to Caster
        return f'Slow Pull Target to Caster'
    elif spa == 382:
        # Suppression
        spa_name = fast_spa_lookup(min_val)
        return f'Negate {spa_name} effects'
    elif spa == 383:
        # Focus: Cast Proc Normalized
        spell_name = get_spell_name(abs(limit_val))
        return (f'{min_val}% chance to proc on successful cast: '
                f'<a href="/spell/detail/{abs(limit_val)}" data-url="{limit_val}" class="spell-tooltip-link">'
                f'{spell_name}</a>')
    elif spa == 384:
        # Fling Caster to Target
        return f'Fling Caster to Target'
    elif spa == 385:
        # Focus: Which Spell Group?
        spell_id, spell_name = get_spell_group_name(abs(min_val))
        return (f'Limit: Spell Group <a href="/spell/detail/{spell_id}" data-url="{spell_id}" '
                f'class="spell-tooltip-link">{spell_name}</a> Only')
    elif spa == 386:
        # Doom Dispeller
        spell_name = get_spell_name(abs(min_val))
        return (f'Trigger on Dispeller: <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                f'class="spell-tooltip-link">{spell_name}</a>')
    elif spa == 387:
        # Doom Dispellee
        spell_name = get_spell_name(abs(min_val))
        return (f'Trigger on Dispel: <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                f'class="spell-tooltip-link">{spell_name}</a>')
    elif spa == 388:
        # Summon All Corpses
        return f'Summon all corpses in zone to caster'
    elif spa == 389:
        # Focus: Timer Refresh
        return f'FC Timer Refresh {min_val}'
    elif spa == 390:
        # Focus: Timer Lockout
        return f'Trigger {min_val/1000} sec lockout on spell type'
    elif spa == 391:
        # Focus: Max Mana
        return f'Limit: Maximum mana cost {min_val}'
    elif spa == 392:
        # Focus: Heal Amt
        return f'Increase amount healed by {min_val}'
    elif spa == 393:
        # Focus: Heal % Incoming
        return f'Reduce incoming healing by {min_val}%'
    elif spa == 394:
        # Focus: Heal Amt Incoming
        if min_val < 0:
            return f'Decrease healing recieved by {abs(min_val)}'
        else:
            return f'Increase healing received by {min_val}'
    elif spa == 395:
        # Focus Heal % Crit
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 396:
        # Focus Heal Amt Crit
        if min_val < 0:
            return f'Decrease critical healing amount by {abs(min_val)}'
        else:
            return f'Increase critical healing amount by {min_val}'
    elif spa == 397:
        # Pet Add AC
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 398:
        # Focus: Swarm Pet Duration
        return f'Increase swarm pet duration by {min_val/1000} sec'
    elif spa == 399:
        # Focus: Twincast
        return f'Increase chance to Twincast by {min_val}'
    elif spa == 400:
        # Focus: Healburn
        return f'Convert {min_val} mana in healing'
    elif spa == 401:
        # Mana Ignite
        return f'Drain {min_val} mana and deal amount in damage'
    elif spa == 402:
        # Endurance Ignite
        return f'Drain {min_val} endurance and deal amount in damage'
    elif spa == 403:
        # Focus: Spell Class
        return f'Limit: Spell Class {min_val}'
    elif spa == 404:
        # Focus: Spell Sub Class
        return f'Limit: Spell Sub Class {min_val}'
    elif spa == 405:
        # Staff Block Chance
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 406:
        # Doom Limit Use
        spell_name = get_spell_name(abs(min_val))
        return (f'Cast <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" class="spell-tooltip-link">'
                f'{spell_name}</a> when maximum hits reached')
    elif spa == 407:
        # Doom Focus Used
        spell_name = get_spell_name(abs(min_val))
        return (f'Cast <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" class="spell-tooltip-link">'
                f'{spell_name}</a> when focus triggered')
    elif spa == 408:
        # Limit HP
        return f'Set HP Maximum to {min_val}%'
    elif spa == 409:
        # Limit Mana
        return f'Set Mana Maximum to {min_val}%'
    elif spa == 410:
        # Limit Endurance
        return f'Set Endurance Maximum to {min_val}%'
    elif spa == 411:
        # Focus: Class Player
        # For some reason, this is off by one.  Divide the min_val in half
        playerclass = utils.get_class_string(min_val / 2)
        return f"Limit: Player Class '{playerclass}' only"
    elif spa == 412:
        # Focus: Race
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 413:
        # Focus: Base Effect
        return f'Increase base spell effectiveness by {min_val}%'
    elif spa == 414:
        # focus: Casting Skill
        return f'Increase Spell Power by {min_val}0%'
    elif spa == 415:
        # Focus: Item Class
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 416:
        # AC_2
        return f'New AC {min_val}'
    elif spa == 417:
        # Mana_2
        return f'New Mana {min_val}'
    elif spa == 418:
        # Skill Min_Damage Amt 2
        if min_val < 0:
            return f'Decrease skill damage amount 2 by {abs(min_val)}'
        else:
            return f'Increase skill damage amount 2 by {min_val}'
    elif spa == 419:
        # Contact Ability 2 (Melee Proc)
        spell_name = get_spell_name(abs(min_val))
        return (f'Add Melee Proc: <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                f'class="spell-tooltip-link">{spell_name}</a>')
    elif spa == 420:
        # Limit: Use
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 421:
        # Limit: Use Amt
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 422:
        # Limit: Use Min
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 423:
        # Limit: Use Type
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 424:
        # Gravitate
        if min_val < 0:
            return f'Slow Push {abs(min_val)}'
        else:
            return f'Slow Pull {min_val}'
    elif spa == 425:
        # Fly
        return 'Illusion: Flying Dragon'
    elif spa == 426:
        # AddExtTargetSlots
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 427:
        # Skill Proc (Attempt)
        spell_name = get_spell_name(abs(min_val))
        return (f'Trigger effect <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                f'class="spell-tooltip-link">{spell_name}</a> on fade')
    elif spa == 428:
        # Proc Skill Modifier
        return f'Increase proc chance of this spell by {min_val}%'
    elif spa == 429:
        # Skill Proc (Success)
        spell_name = get_spell_name(abs(min_val))
        return (f'Trigger effect <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                f'class="spell-tooltip-link">{spell_name}</a> on successful hit')
    elif spa == 430:
        # PostEffect
        return f'Post Effect {min_val}'
    elif spa == 431:
        # PostEffectData
        return f'Post Effect Data {min_val}'
    elif spa == 432:
        # ExpandMaxActiveTrophyBenefits
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 433:
        # Normalized Skill Min Dmg Amt 1
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 434:
        # Normalized SKill Min Dmg Amt 2
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 435:
        # Fragile Defense
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 436:
        # Toggle Freeze Buff Timers
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 437:
        # Teleport to Anchor
        return f'Teleport to Anchor'
    elif spa == 438:
        # Translocate to Anchor
        return f'Translocate target to Anchor'
    elif spa == 439:
        # Assassinate Chance / DMG
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 440:
        # FinishingBlowMax
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 441:
        # Distance Removal
        return f'Distance Removal {min_val}'
    elif spa == 442:
        # Doom Req Target
        spell_name = get_spell_name(abs(min_val))
        return (f'Trigger <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" class="spell-tooltip-link">'
                f'{spell_name}</a> on requirement {limit_val}')
    elif spa == 443:
        # Doom Req Caster
        spell_name = get_spell_name(abs(min_val))
        return (f'Trigger <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" class="spell-tooltip-link">'
                f'{spell_name}</a> on caster requirement {limit_val}')
    elif spa == 444:
        # Improved Taunt
        return f'{min_val}% chance to taunt and hold threat for duration'
    elif spa == 445:
        # Add Merc Slot
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    elif spa == 446:
        # A_Stacker
        return f'Stacker A'
    elif spa == 447:
        # B_stacker
        return f'Stacker B'
    elif spa == 448:
        # C_stacker
        return f'Stacker C'
    elif spa == 449:
        # D_stacker
        return f'Stacker D'
    elif spa == 450:
        # DoT Guard
        if min_val < 0:
            return f'Decrease DoT damage mitigation by {abs(min_val)}%'
        else:
            return f'Increase DoT damage mitigation by {min_val}%'
    elif spa == 451:
        # Melee Threshold Guard
        return f'Reduce melee damage by {min_val}% on melee hits over {limit_val} until {max_val} absorbed'
    elif spa == 452:
        # Spell Threshold Guard
        return f'Reduce spell damage by {min_val}% on melee hits over {limit_val} until {max_val} absorbed'
    elif spa == 453:
        # Doom Melee Threshold
        spell_name = get_spell_name(abs(min_val))
        return (f'Trigger effect <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                f'class="spell-tooltip-link">{spell_name}</a> on {limit_val} melee damage taken')
    elif spa == 454:
        # Doom Spell Threshold
        spell_name = get_spell_name(abs(min_val))
        return (f'Trigger effect <a href="/spell/detail/{abs(min_val)}" data-url="{min_val}" '
                f'class="spell-tooltip-link">{spell_name}</a> on {limit_val} spell damage taken')
    elif spa == 455:
        # Add Hate %
        return f'Increase Hate by {min_val}%'
    elif spa == 456:
        # Add Hate Over Time %
        return f'Increase Hate over Time by {min_val}%'
    elif spa == 457:
        # Resource Tap
        return f'Return {min_val} as hitpoints'
    elif spa == 458:
        # Faction Mod %
        return f'Lock Faction at {min_val}% of current'
    elif spa > 459:
        return f'SPA {spa}: Unused (tell the EQDB dev to fix me)'
    else:
        return f'Unknown SPA: {spa}'


def get_spell_name(spell_id):
    excl_list = utils.get_exclusion_list('spells')
    if spell_id in excl_list:
        return None
    with Session(bind=engine) as session:
        query = session.query(SpellsNew.name).filter(SpellsNew.id == spell_id)
        result = query.first()

    if not result:
        query = session.query(SpellsNew.name).filter(SpellsNew.id == spell_id)
        result = query.first()
    return result[0]


def get_spell_group_name(group_id):
    excl_list = utils.get_exclusion_list('spells')
    with Session(bind=engine) as session:
        query = session.query(SpellsNew.id, SpellsNew.name).filter(SpellsNew.spellgroup == group_id)
        result = query.first()

    spell_id = result[0]
    spell_name = result[1]

    if spell_id in excl_list:
        return None

    return spell_id, spell_name


def fast_spa_lookup(spa):
    if spa == 0:
        return 'Hitpoints'
    elif spa == 2:
        return 'Attack Power'
    elif spa == 3:
        return 'Movement Speed'
    elif spa == 4:
        return 'Strength'
    elif spa == 5:
        return 'Dexterity'
    elif spa == 6:
        return 'Agility'
    elif spa == 7:
        return 'Stamina'
    elif spa == 8:
        return 'Intelligence'
    elif spa == 9:
        return 'Wisdom'
    elif spa == 10:
        return 'Charisma'
    elif spa == 11:
        return 'Melee Attack Speed'
    elif spa == 15:
        return 'Mana'
    elif spa == 18:
        return 'NPC Aggro'
    elif spa == 21:
        return 'Stun'
    elif spa == 22:
        return 'Charm'
    elif spa == 23:
        return 'Fear'
    elif spa == 25:
        return 'Bind Affinity'
    elif spa == 26:
        return 'Gate'
    elif spa == 27:
        return 'Dispel Magic'
    elif spa == 31:
        return 'Mesmerize'
    elif spa == 32:
        return 'Create Item'
    elif spa == 33:
        return 'Summon Pet'
    elif spa == 35:
        return 'Disease'
    elif spa == 36:
        return 'Poison'
    elif spa == 40:
        return 'Invulnerability'
    elif spa == 42:
        return 'Shadow Step'
    elif spa == 50:
        return 'Magic Resist'
    elif spa == 55:
        return 'Absorb Damage'
    elif spa == 61:
        return 'Identify'
    elif spa == 63:
        return 'NPC Wipe Hate List'
    elif spa == 64:
        return 'Spin Stun'
    elif spa == 69:
        return 'Max Hitpoints'
    elif spa == 71:
        return 'Summon Undead'
    elif spa == 74:
        return 'Feign Death'
    elif spa == 79:
        return 'HP When Cast'
    elif spa == 81:
        return 'Resurrection'
    elif spa == 83:
        return 'Portal'
    elif spa == 85:
        return 'Add Melee Proc'
    elif spa == 86:
        return 'NPC Help Radius'
    elif spa == 88:
        return 'Evacuate'
    elif spa == 99:
        return 'Root'
    elif spa == 100:
        return 'Heal Over Time'
    elif spa == 101:
        return 'Complete Heal with duration'
    elif spa == 113:
        return 'Summon Mount'
    elif spa == 116:
        return 'Curse'
    elif spa == 147:
        return 'Percent Heal'
    elif spa == 152:
        return 'Swarm Pet'
    elif spa == 154:
        return 'Cancel Negative'
    elif spa == 185:
        return 'Skill Damage Mod'
    elif spa == 192:
        return 'Duration Hate'
    elif spa == 193:
        return 'Skill Attack'
    elif spa == 194:
        return 'Fade'
    elif spa == 199:
        return 'Taunt'
    elif spa == 291:
        return 'Purify'
    elif spa == 296:
        return 'Incoming Spell Damage %'
    elif spa == 321:
        return 'Reduce Target Hate'
    elif spa == 322:
        return 'Origin'
    elif spa == 324:
        return 'HP to Mana'
    elif spa == 339:
        return 'Cast Proc'
    elif spa == 350:
        return 'Manaburn'
    elif spa == 369:
        return 'Corruption'
    elif spa == 371:
        return 'Slow'
    elif spa == 379:
        return 'Blink'
    elif spa == 388:
        return 'Summon All Corpses'
    elif spa == 400:
        return 'Healburn'
    elif spa == 437:
        return 'Teleport to Anchor'
    elif spa == 438:
        return 'Translocate to Anchor'
    elif spa == 999:
        return 'Unknown'
    else:
        return f'Unknown SPA {spa}, tell the EQDB dev'


def calculate_values(base_value, level, max_val, test_value_func, ignore_max=False, invert=False):
    ret_val = test_value_func(base_value, level)
    # Find the max_level
    new_level = level
    while new_level < LEVEL_CAP:
        test_val = test_value_func(base_value, new_level)
        if not invert:
            if test_val >= max_val and not ignore_max:
                break
        else:
            if test_val <= max_val and not ignore_max:
                break
        new_level += 1
    max_level = new_level
    return ret_val, max_level


def do_formula(base_value, formula_id, max_val, level=1, ignore_max=False, invert=False):
    """Helper to do formula stuff."""
    if level == 255:
        max_level = 0
        level = 0
    else:
        max_level = level
    if formula_id == 1:
        ret_val = base_value
    elif formula_id == 60:
        ret_val = base_value / 100
    elif formula_id == 100:
        ret_val = base_value
    elif formula_id == 101:
        def test_value_func(base, level):
            return base + (level / 2)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func, invert=invert)
    elif formula_id == 102:
        def test_value_func(base, level):
            return base + level
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 103:
        def test_value_func(base, level):
            return base + (level * 2)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 104:
        def test_value_func(base, level):
            return base + (level * 3)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 105:
        def test_value_func(base, level):
            return base + (level * 4)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 107 or formula_id == 108:
        return -1, -1
    elif formula_id == 109:
        def test_value_func(base, level):
            return base + (level / 4)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 110:
        def test_value_func(base, level):
            return base + (level / 6)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 111:
        def test_value_func(base, level):
            return base + 6 * (level - 16)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 112:
        def test_value_func(base, level):
            return base + 8 * (level - 24)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 113:
        def test_value_func(base, level):
            return base + 10 * (level - 34)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 114:
        def test_value_func(base, level):
            return base + 15 * (level - 44)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 115:
        def test_value_func(base, level):
            if level > 15:
                return base + (7 * (level - 15))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 116:
        def test_value_func(base, level):
            if level > 24:
                return base + (10 * (level - 15))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 117:
        def test_value_func(base, level):
            if level > 34:
                return base + (13 * (level - 34))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 118:
        def test_value_func(base, level):
            if level > 44:
                return base + (20 * (level - 44))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 119:
        def test_value_func(base, level):
            return base + (level / 8)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 120:
        # TODO: Fix me (?)
        ret_val = base_value
    elif formula_id == 121:
        def test_value_func(base, level):
            return base + (level / 3)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 122:
        # TODO: Fix me
        # Calculate buff duration
        ret_val = base_value
    elif formula_id == 123:
        ret_val = base_value
    elif formula_id == 124:
        def test_value_func(base, level):
            if level > 50:
                return base + (level - 50)
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 125:
        def test_value_func(base, level):
            if level > 50:
                return base + (2 * (level - 50))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 126:
        def test_value_func(base, level):
            if level > 50:
                return base + (3 * (level - 50))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 127:
        def test_value_func(base, level):
            if level > 50:
                return base + (4 * (level - 50))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 128:
        def test_value_func(base, level):
            if level > 50:
                return base + (5 * (level - 50))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 129:
        def test_value_func(base, level):
            if level > 50:
                return base + (10 * (level - 50))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 130:
        def test_value_func(base, level):
            if level > 50:
                return base + (15 * (level - 50))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 131:
        def test_value_func(base, level):
            if level > 50:
                return base + (20 * (level - 50))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 132:
        def test_value_func(base, level):
            if level > 50:
                return base + (25 * (level - 50))
            else:
                return base
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 137:
        ret_val = base_value
    elif formula_id == 138:
        ret_val = base_value
    elif formula_id == 139:
        def test_value_func(base, level):
            if level > 30:
                return base + ((level - 30) / 2)
            else:
                return 0
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 140:
        def test_value_func(base, level):
            if level > 30:
                return base + (level - 30)
            else:
                return 0
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 141:
        def test_value_func(base, level):
            if level > 30:
                return base + ((3 * level - 90) / 2)
            else:
                return 0
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 142:
        def test_value_func(base, level):
            if level > 30:
                return base + (2 * level - 60)
            else:
                return 0
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 143:
        def test_value_func(base, level):
            if level > 30:
                return base + (3 * level / 4)
            else:
                return 0
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 144:
        def test_value_func(base, level):
            if level > 30:
                return base + (level * 10) + (level - 40) * 20
            else:
                return 0
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    elif formula_id == 201 or formula_id == 203:
        ret_val = max_val
    elif formula_id < 100:
        def test_value_func(base, level):
            return base + (level * formula_id)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func, ignore_max=ignore_max)
    elif 1999 > formula_id > 1000:
        raise Exception('Not supported')
    elif 2650 >= formula_id >= 2000:
        def test_value_func(base, level):
            return base * (level * (formula_id - 2000) + 1)
        ret_val, max_level = calculate_values(base_value, level, max_val, test_value_func)
    else:
        raise Exception('Unknown Formula')
    return int(ret_val), max_level


def parse_classes(data):
    classes = []
    if data.classes1 != 255:
        classes.append(f'Warrior ({data.classes1})')
    if data.classes2 != 255:
        classes.append(f'Cleric ({data.classes2})')
    if data.classes3 != 255:
        classes.append(f'Paladin ({data.classes3})')
    if data.classes4 != 255:
        classes.append(f'Ranger ({data.classes4})')
    if data.classes5 != 255:
        classes.append(f'Shadow Knight ({data.classes5})')
    if data.classes6 != 255:
        classes.append(f'Druid ({data.classes6})')
    if data.classes7 != 255:
        classes.append(f'Monk ({data.classes7})')
    if data.classes8 != 255:
        classes.append(f'Bard ({data.classes8})')
    if data.classes9 != 255:
        classes.append(f'Rogue ({data.classes9})')
    if data.classes10 != 255:
        classes.append(f'Shaman ({data.classes10})')
    if data.classes11 != 255:
        classes.append(f'Necromancer ({data.classes11})')
    if data.classes12 != 255:
        classes.append(f'Wizard ({data.classes12})')
    if data.classes13 != 255:
        classes.append(f'Magician ({data.classes13})')
    if data.classes14 != 255:
        classes.append(f'Enchanter ({data.classes14})')
    if data.classes15 != 255:
        classes.append(f'Beastlord ({data.classes15})')
    if data.classes16 != 255:
        classes.append(f'Berserker ({data.classes16})')

    return classes


def parse_resist(resist_num, resist_diff):
    """Helper to return the correct resist type."""
    if resist_num == 0:
        return 'Unresistable'
    elif resist_num == 1:
        return f'Magic ({resist_diff})'
    elif resist_num == 2:
        return f'Fire ({resist_diff})'
    elif resist_num == 3:
        return f'Cold ({resist_diff})'
    elif resist_num == 4:
        return f'Fire ({resist_diff})'
    elif resist_num == 4:
        return f'Poison ({resist_diff})'
    elif resist_num == 5:
        return f'Disease ({resist_diff})'
    elif resist_num == 6:
        return f'Chromatic ({resist_diff})'
    elif resist_num == 7:
        return f'Prismatic ({resist_diff})'
    elif resist_num == 8:
        return f'Physical ({resist_diff})'
    elif resist_num == 9:
        return f'Corruption ({resist_diff})'
    else:
        raise Exception(f'Unknown resist number: {resist_num}')


def parse_duration(data, min_val=True, raw_seconds=False):
    """Helper to parse the duration of the spell"""
    seconds = 0
    if not min_val:
        if data.buffduration == 0:
            return False
        if data.buffdurationformula == 50 or data.buffdurationformula == 51:
            return 'Permanent'
        seconds = data.buffduration * 6
        if raw_seconds:
            return seconds
    else:
        max_seconds = data.buffduration * 6
        if data.buffdurationformula == 1:
            seconds = 6
        elif data.buffdurationformula == 2:
            seconds = 36
        elif data.buffdurationformula == 3:
            seconds = 180 if max_seconds > 180 else max_seconds
        elif data.buffdurationformula == 4:
            seconds = 300 if max_seconds > 300 else max_seconds
        elif data.buffdurationformula == 5:
            seconds = 12 if max_seconds > 12 else max_seconds
        elif data.buffdurationformula == 6:
            seconds = 12 if max_seconds > 12 else max_seconds
        elif data.buffdurationformula == 7:
            seconds = 6 if max_seconds > 6 else max_seconds
        elif data.buffdurationformula == 8:
            seconds = 66 if max_seconds > 66 else max_seconds
        elif data.buffdurationformula == 9:
            seconds = 72 if max_seconds > 72 else max_seconds
        elif data.buffdurationformula == 10:
            seconds = 78 if max_seconds > 78 else max_seconds
        elif data.buffdurationformula == 11:
            seconds = 720 if max_seconds > 720 else max_seconds
        elif data.buffdurationformula == 12:
            seconds = 6
        elif data.buffdurationformula == 13:
            seconds = 264 if max_seconds > 264 else max_seconds
        elif data.buffdurationformula == 14:
            seconds = 90 if max_seconds > 90 else max_seconds
        elif data.buffdurationformula == 15:
            seconds = 660 if max_seconds > 660 else max_seconds
        elif data.buffdurationformula == 50 or data.buffdurationformula == 51:
            return 'Permanent'

    # Translate this into human readible
    return utils.convert_time(seconds)
