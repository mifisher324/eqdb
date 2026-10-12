from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

import spell
import utils
from logic import engine, Item, LootTable, LootTableEntries, LootDrop, LootDropEntries, NPCTypes, get_era_items, \
    create_lookup_table, SpellsNew


def get_click_items(click_category, click_type, **kwargs):
    # Get the base items, tradeskill items, and quest items that drop from the zones in the eras requested.
    base_items, special_items, quest_items, tradeskill_items = get_era_items(kwargs)
    if not base_items and not tradeskill_items and not quest_items and not special_items:
        return [], False, False, False

    # Create the lookup table
    item_ids, lookup_table = create_lookup_table(base_items, tradeskill_items, quest_items, special_items)

    item_params = or_(*item_ids)
    filters = []
    effect_or_filters = []

    # Now, we need to do some additional filtering based on click type
    if click_category == 'Sympathetic':
        if click_type == 'SympatheticStrike':
            filters.append(Item.clickeffect >= 24356)
            filters.append(Item.clickeffect <= 24365)
        elif click_type == 'SympatheticHealing':
            filters.append(Item.clickeffect >= 24434)
            filters.append(Item.clickeffect <= 24443)
    elif click_category == 'Statistics':
        if click_type == 'AC':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 1,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
        elif click_type == 'ATK':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 2,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
        elif click_type == 'HPRegen':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 0,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
        elif click_type == 'ManaRegen':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 15,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
        elif click_type == 'MaxHP':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 69,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
        elif click_type == 'MaxMana':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 97,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
        elif click_type == 'Resists':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 46,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 47,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 48,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 49,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 50,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 111,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
        elif click_type == 'Haste':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 11,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 100))
        elif click_type == 'Overhaste':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 119,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 100))
        elif click_type == 'Stats':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 4,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 5,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 6,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 7,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 8,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 9,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 10,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
        elif click_type == 'Singing':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 118,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
        filters.append(SpellsNew.buffduration > 0)
        filters.append(SpellsNew.targettype != 14)
    elif click_category == 'Buffs':
        if click_type == 'Enduring Breath':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 14)
        elif click_type == 'SummonItems':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 32)
        elif click_type == 'Illusion':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 58)
        elif click_type == 'Invis':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 12)
        elif click_type == 'InvisToUndead':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 28)
        elif click_type == 'InvisToAnimal':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 29)
        elif click_type == 'Misc':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 65)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 87)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 67)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 75)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 66)
        elif click_type == 'ProcBuff':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 85)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 428)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 339)
        elif click_type == 'DamageShield':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 59)
        elif click_type == 'Levitate':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 57)
        elif click_type == 'MovementSpeed':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 3,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
        elif click_type == 'SeeInvis':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 13)
        elif click_type == 'Invuln':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 40)
        filters.append(SpellsNew.buffduration > 0)
    elif click_category == 'Defensive':
        if click_type == 'Heal':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 0,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 79,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                filters.append(SpellsNew.buffduration == 0)
        elif click_type == 'Mana':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 15,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
                filters.append(SpellsNew.buffduration == 0)
        elif click_type == 'CurePoison':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 36,
                                              getattr(SpellsNew, f'effect_base_value{idx}') < 0))
        elif click_type == 'CureDisease':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 35,
                                              getattr(SpellsNew, f'effect_base_value{idx}') < 0))
        elif click_type == 'CureCurse':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 116,
                                              getattr(SpellsNew, f'effect_base_value{idx}') < 0))
        elif click_type == 'Rune':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 55)
        elif click_type == 'SpellRune':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 78)
        elif click_type == 'Endurance':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 189,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 0))
    elif click_category == 'Offensive':
        if click_type == 'DispelBene':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 209)
        elif click_type == 'Dispel':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 27)
        elif click_type == 'DOT':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 0,
                                              getattr(SpellsNew, f'effect_base_value{idx}') < 0))
                filters.append(SpellsNew.buffduration > 0)
        elif click_type == 'Slow':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 11,
                                         getattr(SpellsNew, f'effect_base_value{idx}') < 100))
        elif click_type == 'SwarmPet':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 152)
        elif click_type == 'Root':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 99)
        elif click_type == 'DD':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 0,
                                              getattr(SpellsNew, f'effect_base_value{idx}') < 0))
                filters.append(SpellsNew.buffduration == 0)
        elif click_type == 'Lifetap':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 0,
                                              getattr(SpellsNew, f'effect_base_value{idx}') < 0))
                filters.append(SpellsNew.targettype == 13)
        elif click_type == 'Snare':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 3,
                                              getattr(SpellsNew, f'effect_base_value{idx}') < 0))
        elif click_type == 'Fear':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 23)
        elif click_type == 'Stun':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 21)
        elif click_type == 'Blind':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 20,
                                              getattr(SpellsNew, f'effect_base_value{idx}') == -1))
        elif click_type == 'Charm':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 22)
        elif click_type == 'DecreaseATK':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 2,
                                              getattr(SpellsNew, f'effect_base_value{idx}') < 0))
    elif click_category == 'Pets':
        filters.append(SpellsNew.targettype == 14)
    elif click_category == 'Misc':
        if click_type == 'Misc':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 68)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 61)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 42)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 91)
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 20,
                                              getattr(SpellsNew, f'effect_base_value{idx}') == 1))
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 33)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 56)
        elif click_type == 'SummonItem':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 32)
        elif click_type == 'Transport':
            for idx in range(1, 13):
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 26)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 83)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 104)
                effect_or_filters.append(getattr(SpellsNew, f'effectid{idx}') == 88)
        elif click_type == 'Shrink':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 89,
                                              getattr(SpellsNew, f'effect_base_value{idx}') < 100))
        elif click_type == 'Grow':
            for idx in range(1, 13):
                effect_or_filters.append(and_(getattr(SpellsNew, f'effectid{idx}') == 89,
                                              getattr(SpellsNew, f'effect_base_value{idx}') > 100))
    if 'charges' in kwargs:
        filters.append(Item.maxcharges < 0)

    filters.append(Item.clicklevel2 <= kwargs['min_level'])

    params = and_(*filters)
    effect_or_params = or_(*effect_or_filters)

    with Session(bind=engine) as session:
        query = session.query(Item.Name, Item.id, SpellsNew.id, SpellsNew.name).\
            filter(SpellsNew.id == Item.clickeffect).\
            filter(Item.id.in_(session.query(Item.id).filter(item_params))).\
            filter(params).\
            filter(effect_or_params)
        result = query.all()

    ret_data = []
    for entry in result:
        item_name = entry[0]
        item_id = entry[1]
        spell_id = entry[2]
        spell_name = entry[3]
        npc_id = lookup_table[item_id]['npc_id']
        npc_name = lookup_table[item_id]['npc_name']
        zone_name = utils.lookup_zone_name(npc_id)
        npc_name = utils.fix_npc_name(npc_name)

        # Get the spell effects
        _, effects = spell.get_spell_data(spell_id, basic_data=False)

        ret_data.append({'item_name': item_name,
                         'item_id': item_id,
                         'spell_id': spell_id,
                         'spell_name': spell_name,
                         'npc_id': npc_id,
                         'npc_name': npc_name,
                         'zone_name': zone_name,
                         'zone_id': int(npc_id / 1000),
                         'effects': effects})
    return ret_data


def get_fast_item(item_name, tradeskill=None, equippable=None, itype='Base', no_glamours=False, only_aug=False):
    filters = []
    or_filters = []
    if len(item_name) > 0:
        partial = "%%%s%%" % item_name
        filters.append(Item.Name.like(partial))
    if tradeskill:
        filters.append(Item.tradeskills == 1)
        equippable = None
        itype = 'Base'
        no_glamours = True
        only_aug = False
    if equippable:
        or_filters = [Item.itemtype == 0, Item.itemtype == 1, Item.itemtype == 2, Item.itemtype == 3,
                      Item.itemtype == 4, Item.itemtype == 5, Item.itemtype == 7, Item.itemtype == 8,
                      Item.itemtype == 10, Item.itemtype == 19, Item.itemtype == 23, Item.itemtype == 24,
                      Item.itemtype == 25, Item.itemtype == 26, Item.itemtype == 27, Item.itemtype == 29,
                      Item.itemtype == 35, Item.itemtype == 54, Item.itemtype == 52]
    if itype == 'Base':
        filters.append(Item.id < 1000000)
    if itype == 'Enchanted':
        filters.append(Item.id > 1000000)
        filters.append(Item.id < 2000000)
    if itype == 'Legendary':
        filters.append(Item.id > 2000000)
    if only_aug:
        filters.append(Item.augtype > 0)

    params = and_(*filters)
    with Session(bind=engine) as session:
        if or_filters:
            or_params = or_(*or_filters)
            query = session.query(Item.id, Item.Name, Item.icon).filter(params).filter(or_params).limit(50)
        else:
            query = session.query(Item.id, Item.Name, Item.icon).filter(params).limit(50)
        result = query.all()

    out_data = []
    for entry in result:
        item_id = entry[0]
        excl_list = utils.get_exclusion_list('item')
        if item_id in excl_list:
            return None
        name = entry[1]
        icon = entry[2]
        if no_glamours and 'glamour' in name.lower():
            continue
        out_data.append({'item_id': item_id,
                         'name': name,
                         'icon': icon})
    return out_data


def get_item_raw_data(item_id):
    excl_list = utils.get_exclusion_list('item')
    if item_id in excl_list:
        return None

    with Session(bind=engine) as session:
        query = session.query(Item).filter(Item.id == item_id)
        result = query.one()

    ret_dict = result.__dict__
    ret_dict.pop('_sa_instance_state')
    return ret_dict


def get_loot_json(loot_id=None, npc_id=None):
    excl_list = utils.get_exclusion_list('loottable')
    if loot_id in excl_list:
        return []
    npc_excl_list = utils.get_exclusion_list('npcs')
    if npc_id in npc_excl_list:
        return []

    with Session(bind=engine) as session:
        if npc_id:
            query = session.query(NPCTypes.loottable_id).filter(NPCTypes.id == npc_id)
            result = query.one()
            if not result:
                return {}
            loot_id = result[0]

        query = session.query(LootTable).filter(LootTable.id == loot_id)
        result = query.one()
        ret_dict = result.__dict__
        ret_dict.pop('_sa_instance_state')

        query = session.query(LootTableEntries).filter(LootTableEntries.loottable_id == loot_id)
        result = query.all()

        lt_entries = []
        for entry in result:
            lt_entry = entry.__dict__
            lt_entry.pop('_sa_instance_state')

            query = session.query(LootDrop).filter(LootDrop.id == lt_entry['lootdrop_id'])
            sub_result = query.one()
            drop = sub_result.__dict__
            drop.pop('_sa_instance_state')

            query = session.query(LootDropEntries).filter(LootDropEntries.lootdrop_id == lt_entry['lootdrop_id'])
            sub_result = query.all()
            ld_entries = []
            for sub_entry in sub_result:
                ld_entry = sub_entry.__dict__
                ld_entry.pop('_sa_instance_state')
                ld_entries.append(ld_entry)
            lt_entry.update({'lootdrop_entries': ld_entries})
            lt_entry.update({'lootdrop': drop})
            lt_entries.append(lt_entry)
        ret_dict.update({'loottable_entries': lt_entries})
        return ret_dict


def get_item_json(name=None, item_id=None, i_type=None):
    excl_list = utils.get_exclusion_list('item')
    if item_id in excl_list:
        return []
    with Session(bind=engine) as session:
        if item_id:
            query = session.query(Item).filter(Item.id == item_id)
            result = query.first()
            if not result:
                return {}
            ret_dict = result.__dict__
            ret_dict.pop('_sa_instance_state')
            return ret_dict
        else:
            ret_list = []
            partial = "%%%s%%" % name
            if i_type is None:
                query = session.query(Item).filter(Item.Name.like(partial))
            elif i_type.lower() == 'base':
                query = session.query(Item).filter(Item.Name.like(partial)).filter(Item.id < 1000000)
            elif i_type.lower() == 'ench':
                query = session.query(Item).filter(Item.Name.like(partial)).\
                    filter(and_(1000000 < Item.id, Item.id < 2000000))
            elif i_type.lower() == 'legend':
                query = session.query(Item).filter(Item.Name.like(partial)).filter(Item.id > 2000000)
            else:
                query = session.query(Item).filter(Item.Name.like(partial))

            result = query.limit(50).all()
            if not result:
                return {}
            for entry in result:
                entry = entry.__dict__
                entry.pop('_sa_instance_state')
                if entry['id'] in excl_list:
                    continue
                ret_list.append(entry)
            return ret_list


def get_item_name(item_id):
    excl_list = utils.get_exclusion_list('item')
    if item_id in excl_list:
        return None
    with Session(bind=engine) as session:
        query = session.query(Item.Name).filter(Item.id == item_id)
        result = query.one()
    return result[0]
