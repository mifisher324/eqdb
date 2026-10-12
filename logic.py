"""EQDB Logic File"""
import configparser
import datetime
import operator
import os

import utils

from sqlalchemy import create_engine, and_, or_, Column, Integer
from sqlalchemy.orm import Session, aliased
from sqlalchemy.ext.automap import automap_base

here = os.path.dirname(__file__)
site_config = configparser.RawConfigParser()
ini_path = os.path.join(here, 'configuration.ini')
site_config.read_file(open(ini_path))
expansion = site_config.getint('emu', 'expansion')

driver = site_config.get('database', 'driver')
user = site_config.get('database', 'user')
password = site_config.get('database', 'password')
database = site_config.get('database', 'database')
host = site_config.get('database', 'host')
port = site_config.get('database', 'port')

engine = create_engine(f'{driver}{user}:{password}@{host}:{port}/{database}')
Base = automap_base()


class ItemRedirection(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)


Base.prepare(autoload_with=engine)

Zone = Base.classes.zone
ZonePoints = Base.classes.zone_points
Item = ItemRedirection
Spawn2 = Base.classes.spawn2
SpawnEntry = Base.classes.spawnentry
SpawnGroup = Base.classes.spawngroup
NPCTypes = Base.classes.npc_types
NPCSpells = Base.classes.npc_spells
NPCSpellsEntries = Base.classes.npc_spells_entries
MerchantList = Base.classes.merchantlist
LootTable = Base.classes.loottable
LootTableEntries = Base.classes.loottable_entries
LootDropEntries = Base.classes.lootdrop_entries
LootDrop = Base.classes.lootdrop
SpellsNew = Base.classes.spells_new
FocusSpell = aliased(SpellsNew)
ClickSpell = aliased(SpellsNew)
ProcSpell = aliased(SpellsNew)
WornSpell = aliased(SpellsNew)
BardSpell = aliased(SpellsNew)
Forage = Base.classes.forage
GroundSpawns = Base.classes.ground_spawns
TradeskillRecipe = Base.classes.tradeskill_recipe
TradeskillRecipeEntries = Base.classes.tradeskill_recipe_entries
NPCFactionEntries = Base.classes.npc_faction_entries
FactionList = Base.classes.faction_list
Pets = Base.classes.pets


# Important that these goes here to stop circular import
import spell
import faction
import zone
import tradeskill
import npc
import item


def _debugger():
    return spell.get_spell_data(6561, engine)


def _get_link_filters():
    """Helper to return the basic link filters between zone, npc, and item"""
    return [NPCTypes.loottable_id == LootTableEntries.loottable_id,
            LootTableEntries.lootdrop_id == LootDropEntries.lootdrop_id,
            LootDropEntries.item_id == Item.id]


def _get_arg_list(tooltip=False):
    """Helper to return things we want to search for."""
    arg_list = [Item.id, Item.Name, Item.hp, Item.mana, Item.endur, Item.ac, Item.damage, Item.aagi, Item.acha,
                Item.adex, Item.aint, Item.asta, Item.astr, Item.awis, Item.heroic_agi, Item.heroic_cha,
                Item.heroic_dex, Item.heroic_int, Item.heroic_sta, Item.heroic_str, Item.heroic_wis, Item.cr, Item.dr,
                Item.fr, Item.mr, Item.pr, Item.heroic_cr, Item.heroic_dr, Item.heroic_fr, Item.heroic_mr,
                Item.heroic_pr, Item.attack, Item.haste, Item.regen, Item.manaregen, Item.enduranceregen, Item.healamt,
                Item.spelldmg, Item.accuracy, Item.avoidance, Item.combateffects, Item.damageshield, Item.dotshielding,
                Item.shielding, Item.spellshield, Item.strikethrough, Item.stunresist, Item.delay, Item.proceffect,
                Item.focuseffect, Item.clickeffect, Item.banedmgamt, Item.banedmgbody, Item.banedmgrace,
                Item.banedmgraceamt, Item.elemdmgamt, Item.elemdmgtype, Item.clicklevel2, Item.proclevel2,
                Item.backstabdmg, Item.bardeffect, Item.worneffect, Item.procrate, Item.lore, Item.bagtype,
                Item.bagslots, Item.bagwr, Item.bagsize, Item.skillmodvalue, Item.skillmodmax, Item.skillmodtype,
                Item.icon, Item.casttime, Item.maxcharges, Item.augtype, Item.augrestrict, Item.color, Item.scrolleffect]
    if tooltip:
        arg_list.append(Item.classes)
        arg_list.append(Item.slots)
        arg_list.append(Item.itemtype)
        arg_list.append(Item.proceffect)
        arg_list.append(Item.augslot1type)
        arg_list.append(Item.augslot2type)
        arg_list.append(Item.augslot3type)
        arg_list.append(Item.augslot4type)
        arg_list.append(Item.augslot5type)
    else:
        arg_list.append(FocusSpell.id.label('focus_id'))
        arg_list.append(FocusSpell.name.label('focus_spell_name'))
        arg_list.append(FocusSpell.effect_base_value1.label('focus_min_val'))
        arg_list.append(FocusSpell.effect_limit_value1.label('focus_max_val'))
        arg_list.append(ClickSpell.id.label('click_id'))
        arg_list.append(ClickSpell.name.label('click_name'))
        arg_list.append(ProcSpell.id.label('proc_id'))
        arg_list.append(ProcSpell.name.label('proc_name'))
        arg_list.append(ProcSpell.effect_base_value1.label('proc_max_damage'))
        arg_list.append(WornSpell.id.label('worn_id'))
        arg_list.append(WornSpell.name.label('worn_name'))
        arg_list.append(WornSpell.effect_base_value1.label('worn_value'))
        arg_list.append(BardSpell.id.label('inst_id'))
        arg_list.append(BardSpell.name.label('inst_name'))
        arg_list.append(BardSpell.effect_base_value1.label('inst_value'))

    return arg_list


def send_error_email(error, referrer):
    # See if this referrer exists in local text already.
    error_file = os.path.join(here, 'error_list.txt')
    if os.path.exists(error_file):
        with open(error_file, 'r') as fh:
            errors = fh.read()
        error_list = errors.split('\n')
        if referrer in error_list:
            return

    with open(error_file, 'a') as fh:
        fh.write(referrer)
        fh.write('\n')


def all_search(name=None):
    return {'tradeskill': tradeskill.get_tradeskills(name=name),
            'game_items': item.get_fast_item(name),
            'spells': spell.get_spells(name),
            'npcs': npc.get_npcs(name),
            'zones': zone.get_zone(name),
            'factions': faction.get_factions(name)}


def get_item_data(item_id, full=False):
    """Returns the basic data for an item, used for tooltips."""
    excl_list = utils.get_exclusion_list('item')
    if item_id in excl_list:
        return None

    with Session(bind=engine) as session:
        # Get the item
        args = _get_arg_list(tooltip=True)
        query = session.query(*args).filter(Item.id == item_id)
        result = query.all()
    if not result:
        return None
    ret_dict = dict(result[0]._mapping)

    proc = ret_dict['proceffect']
    click = ret_dict['clickeffect']
    focus = ret_dict['focuseffect']
    worn = ret_dict['worneffect']
    inst = ret_dict['bardeffect']
    banebody = ret_dict['banedmgbody']
    banerace = ret_dict['banedmgrace']
    elemtype = ret_dict['elemdmgtype']
    aug_slot_1 = ret_dict['augslot1type']
    aug_slot_2 = ret_dict['augslot2type']
    aug_slot_3 = ret_dict['augslot3type']
    aug_slot_4 = ret_dict['augslot4type']
    aug_slot_5 = ret_dict['augslot5type']
    skill_mod = ret_dict['skillmodtype']
    scrolleffect = ret_dict['scrolleffect']

    # An item can reference a spell id that is not in spells_new, e.g. when the spell
    # file is trimmed after the item data is imported. Indexing an empty result raised
    # IndexError and returned a 500 for the whole item page, so name it by id instead.
    def spell_name(spell_id):
        row = session.query(SpellsNew.name).filter(SpellsNew.id == spell_id).first()
        return row[0] if row else 'Spell %s' % spell_id

    if worn > 0:
        ret_dict['worn_name'] = spell_name(worn)
    if proc > 0:
        ret_dict['proc_name'] = spell_name(proc)
    if click > 0:
        ret_dict['click_name'] = utils.check_sympathetic(spell_name(click))
    if focus > 0:
        ret_dict['focus_name'] = spell_name(focus)
    if inst > 0:
        ret_dict['inst_name'] = spell_name(inst)
    if banebody > 0:
        ret_dict['bane_body_name'] = utils.get_bane_dmg_body(banebody)
        ret_dict['bane_body_amount'] = ret_dict['banedmgamt']
    if banerace > 0:
        ret_dict['bane_race_name'] = utils.get_bane_dmg_race(banerace)
        ret_dict['bane_race_amount'] = ret_dict['banedmgraceamt']
    if elemtype > 0:
        ret_dict['elem_dmg_name'] = utils.get_elem_dmg_type(elemtype)
        ret_dict['elem_dmg_amount'] = ret_dict['elemdmgamt']
    if aug_slot_1 > 0:
        ret_dict['aug_slot_1'] = utils.get_aug_slot_type(aug_slot_1)
    if aug_slot_2 > 0:
        ret_dict['aug_slot_2'] = utils.get_aug_slot_type(aug_slot_2)
    if aug_slot_3 > 0:
        ret_dict['aug_slot_3'] = utils.get_aug_slot_type(aug_slot_3)
    if aug_slot_4 > 0:
        ret_dict['aug_slot_4'] = utils.get_aug_slot_type(aug_slot_4)
    if aug_slot_5 > 0:
        ret_dict['aug_slot_5'] = utils.get_aug_slot_type(aug_slot_5)
    if skill_mod > 0:
        ret_dict['skillmodname'] = utils.parse_skill(int(skill_mod))
    if scrolleffect > 0:
        query = session.query(SpellsNew.name).filter(SpellsNew.id == scrolleffect)
        result = query.first()
        ret_dict['scrolleffectname'] = result[0]

    ret_dict['class_str'] = utils.get_class_string(ret_dict['classes'])
    ret_dict['slot_str'] = utils.get_slot_string(ret_dict['slots'])
    ret_dict['type_str'] = utils.get_type_string(ret_dict['itemtype'])
    if ret_dict['augtype'] > 0:
        ret_dict['augtype'] = utils.get_aug_types(ret_dict['augtype'])
        ret_dict['augrestrict'] = utils.get_aug_restrict(ret_dict['augrestrict'])
    if full:
        ret_dict['red'] = (int(ret_dict['color']) & 0x00FF0000) >> 16
        ret_dict['green'] = (int(ret_dict['color']) & 0x0000FF00) >> 8
        ret_dict['blue'] = (int(ret_dict['color']) & 0x000000FF)

        ret_dict['thj_enabled'] = False
        item_id = int(item_id)
        if item_id < 1000000:
            # See if Enchanted and Legendary exist
            with Session(bind=engine) as session:
                ench = item_id + 1000000
                lego = item_id + 2000000
                query = session.query(Item.id).filter(or_(Item.id == ench, Item.id == lego))
                result = query.all()
                if len(result) == 2:
                    ret_dict['thj_enabled'] = True
        elif item_id > 1000000:
            ret_dict['thj_enabled'] = True
        # Get mobs that drop this as loot
        droppers = []
        orig_item_id = item_id
        if item_id > 2000000:
            item_id = item_id - 2000000
        elif 2000000 > item_id > 1000000:
            item_id = item_id - 1000000
        known_zones = {}
        skip_zones = []
        with Session(bind=engine) as session:
            query = session.query(NPCTypes.id, NPCTypes.name, LootDropEntries.chance).filter(LootDropEntries.item_id == item_id).\
                filter(LootDropEntries.lootdrop_id == LootTableEntries.lootdrop_id).\
                filter(LootTableEntries.loottable_id == NPCTypes.loottable_id)
            result = query.all()
            for entry in result:
                zone_id = int(entry[0] / 1000)
                if zone_id in skip_zones:
                    continue
                if zone_id not in known_zones:
                    query = session.query(Zone.long_name, Zone.expansion).filter(Zone.zoneidnumber == zone_id)
                    sub_result = query.first()
                    if not sub_result:
                        # Walk through the spawn points instead
                        query = session.query(Zone.long_name, Zone.expansion, Zone.short_name). \
                            filter(SpawnEntry.npcID == entry[0]). \
                            filter(SpawnEntry.spawngroupID == Spawn2.spawngroupID). \
                            filter(Spawn2.zone == Zone.short_name)
                        sub_result = query.first()

                    if not sub_result:
                        zone_name = 'Unknown'
                    else:
                        if sub_result[1] > expansion:
                            skip_zones.append(zone_id)
                            continue
                        zone_name = sub_result[0]
                    known_zones.update({zone_id: zone_name})
                else:
                    zone_name = known_zones[zone_id]

                if {'npc_id': entry[0], 'npc_name': utils.fix_npc_name(entry[1]), 'zone_name': zone_name} in droppers:
                    continue
                droppers.append({'npc_id': entry[0],
                                 'npc_name': utils.fix_npc_name(entry[1]),
                                 'zone_name': zone_name,
                                 'zone_id': zone_id,
                                 'chance': entry[2]})
        ret_dict['droppers'] = droppers

        # Get vendors that sell this
        vendors = {}
        with Session(bind=engine) as session:
            query = session.query(NPCTypes.id, NPCTypes.name).filter(MerchantList.item == item_id).\
                filter(MerchantList.merchantid == NPCTypes.merchant_id).\
                filter(MerchantList.min_expansion <= expansion)
            result = query.all()
        lookup = {}
        for entry in result:
            zone_id = int(entry[0] / 1000)
            if zone_id in lookup:
                zone_name = lookup[zone_id]
            else:
                query = session.query(Zone.long_name, Zone.expansion).filter(Zone.zoneidnumber == zone_id)
                sub_result = query.first()
                if not sub_result:
                    query = session.query(Zone.long_name, Zone.expansion).\
                        filter(SpawnEntry.npcID == entry[0]).\
                        filter(SpawnEntry.spawngroupID == Spawn2.spawngroupID).\
                        filter(Zone.short_name == Spawn2.zone)
                    sub_result = query.first()
                    if not sub_result:
                        continue
                if sub_result[1] > expansion:
                    continue
                zone_name = sub_result[0]
                lookup.update({zone_id: zone_name})
            if zone_name in vendors:
                vendor_list = vendors[zone_name]
            else:
                vendor_list = []
            vendor_list.append({'npc_id': entry[0],
                                'npc_name': utils.fix_npc_name(entry[1])})
            vendors.update({zone_name: vendor_list})

        ret_dict['vendors'] = vendors

        # Get where this is foraged from
        foraged = []
        with Session(bind=engine) as session:
            query = session.query(Zone.zoneidnumber, Zone.long_name, Zone.expansion, Forage.chance).\
                filter(Forage.Itemid == item_id).\
                filter(Zone.zoneidnumber == Forage.zoneid)
            result = query.all()
        for entry in result:
            if int(entry[2]) > expansion:
                continue
            foraged.append({'zone_id': entry[0],
                            'zone_name': entry[1],
                            'chance': entry[3]})
        ret_dict['foraged'] = foraged

        # Get where this is a ground spawn
        ground = []
        with Session(bind=engine) as session:
            query = session.query(Zone.zoneidnumber, Zone.long_name, Zone.expansion,
                                  GroundSpawns.min_x, GroundSpawns.min_y, GroundSpawns.respawn_timer).\
                filter(GroundSpawns.zoneid == Zone.zoneidnumber).\
                filter(GroundSpawns.item == item_id)
            result = query.all()
        for entry in result:
            if int(entry[2]) > expansion:
                continue
            ground.append({'zone_id': entry[0],
                           'zone_name': entry[1],
                           'x': entry[3],
                           'y': entry[4],
                           'respawn': entry[5]})
        ret_dict['ground'] = ground

        # Get where this is made by tradeskills
        ts_result = []
        with Session(bind=engine) as session:
            query = session.query(TradeskillRecipeEntries.recipe_id, TradeskillRecipe.name).\
                filter(TradeskillRecipe.id == TradeskillRecipeEntries.recipe_id).\
                filter(TradeskillRecipeEntries.item_id == orig_item_id).\
                filter(TradeskillRecipeEntries.successcount >= 1). \
                filter(TradeskillRecipe.enabled == 1)
            result = query.all()

        for entry in result:
            ts_result.append({'ts_id': entry[0],
                              'ts_name': entry[1]})
        ret_dict['ts_result'] = ts_result

        # Get where this item is used in tradeskills
        ts_component = []
        with Session(bind=engine) as session:
            query = session.query(TradeskillRecipeEntries.recipe_id, TradeskillRecipe.name).\
                filter(TradeskillRecipe.id == TradeskillRecipeEntries.recipe_id).\
                filter(TradeskillRecipeEntries.item_id == orig_item_id).\
                filter(or_(TradeskillRecipeEntries.componentcount >= 1, TradeskillRecipeEntries.iscontainer >= 1)).\
                filter(TradeskillRecipe.enabled == 1)
            result = query.all()

        for entry in result:
            ts_component.append({'ts_id': entry[0],
                                 'ts_name': entry[1]})
        ret_dict['ts_component'] = ts_component

    return ret_dict


def get_era_items(kwargs):
    """Returns all base items with NPC names and IDs, as well as Tradeskill and Quest items."""
    # We need to link through to all the NPCs in all the zones of the era to get all the items they drop.
    zone_or_filters = []
    quest_item_ids = []
    special_item_ids = []
    ts_item_ids = []
    quest_items = []
    for era in kwargs['eras']:
        zone_id_list = utils.get_era_zones(era)
        for zone_id in zone_id_list:
            zone_or_filters.append(NPCTypes.id.like(f'{zone_id}___'))
        # Now, we need to get the quest items.  These are stored in files
        with open(os.path.join(here, 'item_files', f'{era}.txt'), 'r') as fh:
            file_data = fh.read()
        quest_item_ids += file_data.split('\n')

        if era == 'Kunark':
            # Add LoY
            if os.path.exists(os.path.join(here, f'item_files/LoY.txt')):
                with open(os.path.join(here, 'item_files', f'LoY.txt'), 'r') as fh:
                    file_data = fh.read()
                quest_item_ids += file_data.split('\n')
            if os.path.exists(os.path.join(here, f'item_files/LoY_ts.txt')):
                with open(os.path.join(here, f'item_files/LoY_ts.txt'), 'r') as fh:
                    file_data = fh.read()
                ts_item_ids += file_data.split('\n')

        # Certain expansions have tradeskill items at the highest level, add those
        if os.path.exists(os.path.join(here, f'item_files/{era}_ts.txt')):
            with open(os.path.join(here, f'item_files/{era}_ts.txt'), 'r') as fh:
                file_data = fh.read()
            ts_item_ids += file_data.split('\n')

        if os.path.exists(os.path.join(here, f'item_files/{era}_special.txt')):
            with open(os.path.join(here, f'item_files/{era}_special.txt'), 'r') as fh:
                file_data = fh.read()
            special_item_ids += file_data.split('\n')

    filters = []
    class_or_filters = []
    weapon_or_filters = []
    symp_or_filters = []
    aug_search = False
    no_rent = False
    # Now, add the filters that can be applied at all levels to save time.
    if 'item_name' in kwargs:
        partial = "%%%s%%" % (kwargs['item_name'])
        filters.append(Item.Name.like(partial))
    if 'g_class_1' in kwargs:
        class_value = utils.lookup_class(kwargs['g_class_1'])
        class_or_filters.append(Item.classes.op('&')(class_value) == class_value)
    if 'g_class_2' in kwargs:
        class_value = utils.lookup_class(kwargs['g_class_2'])
        class_or_filters.append(Item.classes.op('&')(class_value) == class_value)
    if 'g_class_3' in kwargs:
        class_value = utils.lookup_class(kwargs['g_class_3'])
        class_or_filters.append(Item.classes.op('&')(class_value) == class_value)
    if 'g_slot' in kwargs:
        slot_value = utils.lookup_slot(kwargs['g_slot'])
        filters.append(Item.slots.op('&')(slot_value) == slot_value)
    if 'skillmodtype' in kwargs:
        if kwargs['skillmodtype'] == 'All':
            filters.append(Item.skillmodtype >= 0)
        else:
            filters.append(Item.skillmodtype == kwargs['skillmodtype'])
    if 'i_type' in kwargs:
        if kwargs['i_type'] == 'Augment':
            aug_search = True
        elif kwargs['i_type'] == 'Any 1H Weapon':
            weapon_or_filters.append(Item.itemtype == utils.lookup_weapon_types('One Hand Slash'))
            weapon_or_filters.append(Item.itemtype == utils.lookup_weapon_types('One Hand Blunt'))
            weapon_or_filters.append(Item.itemtype == utils.lookup_weapon_types('One Hand Piercing'))
            weapon_or_filters.append(Item.itemtype == utils.lookup_weapon_types('Hand to Hand'))
        elif kwargs['i_type'] == 'Any 2H Weapon':
            weapon_or_filters.append(Item.itemtype == utils.lookup_weapon_types('Two Hand Slash'))
            weapon_or_filters.append(Item.itemtype == utils.lookup_weapon_types('Two Hand Blunt'))
            weapon_or_filters.append(Item.itemtype == utils.lookup_weapon_types('Two Hand Piercing'))
        elif kwargs['i_type'] == 'Exclude 1H Weapon':
            filters.append(Item.itemtype != utils.lookup_weapon_types('One Hand Slash'))
            filters.append(Item.itemtype != utils.lookup_weapon_types('One Hand Blunt'))
            filters.append(Item.itemtype != utils.lookup_weapon_types('One Hand Piercing'))
            filters.append(Item.itemtype != utils.lookup_weapon_types('Hand to Hand'))
        elif kwargs['i_type'] == 'Exclude 2H Weapon':
            filters.append(Item.itemtype != utils.lookup_weapon_types('Two Hand Slash'))
            filters.append(Item.itemtype != utils.lookup_weapon_types('Two Hand Blunt'))
            filters.append(Item.itemtype != utils.lookup_weapon_types('Two Hand Piercing'))
        else:
            filters.append(Item.itemtype == utils.lookup_weapon_types(kwargs['i_type']))
    if 'pet_search' in kwargs:
        no_rent = True

    # Apply universal filters
    if aug_search:
        filters.append(Item.augtype > 0)

    if not no_rent:
        filters.append(Item.norent == 1)

    # Run the base query to get item IDs for the
    zone_or_params = or_(*zone_or_filters)
    link_filters = _get_link_filters()
    link_params = and_(*link_filters)
    params = and_(*filters)
    class_or_params = or_(*class_or_filters)
    weapon_or_params = or_(*weapon_or_filters)
    symp_or_params = or_(*symp_or_filters)

    base_items = []
    with Session(bind=engine) as session:
        query = session.query(Item.id, NPCTypes.id.label('npc_id'), NPCTypes.name.label('npc_name')).\
            filter(zone_or_params).\
            filter(link_params).\
            filter(params).\
            filter(class_or_params).\
            filter(weapon_or_params).\
            filter(symp_or_params).\
            group_by(Item.id)
        result = query.all()

    for entry in result:
        new_item = dict(entry._mapping)
        new_item['id'] = new_item['id'] + 2000000
        base_items.append(new_item)

    if quest_item_ids:
        item_id_filters = []
        for entry in quest_item_ids:
            item_id_filters.append(Item.id == entry)
        item_id_params = or_(*item_id_filters)
        with Session(bind=engine) as session:
            query = session.query(Item.id).\
                filter(item_id_params).\
                filter(params).\
                filter(class_or_params).\
                filter(weapon_or_params).\
                group_by(Item.id)
            result = query.all()
        for entry in result:
            quest_items.append({'id': entry[0], 'npc_id': -1, 'npc_name': 'Quested'})

    special_items = []
    if special_item_ids:
        item_id_filters = []
        for entry in special_item_ids:
            item_id_filters.append(Item.id == entry)
        item_id_params = or_(*item_id_filters)
        with Session(bind=engine) as session:
            query = session.query(Item.id).\
                filter(item_id_params).\
                filter(params).\
                filter(class_or_params).\
                filter(weapon_or_params).\
                group_by(Item.id)
            result = query.all()
        for entry in result:
            special_items.append({'id': entry[0], 'npc_id': -3, 'npc_name': 'Special Drop'})

    ts_items = []
    if ts_item_ids:
        item_id_filters = []
        for entry in ts_item_ids:
            item_id_filters.append(Item.id == entry)
        item_id_params = or_(*item_id_filters)
        with Session(bind=engine) as session:
            query = session.query(Item.id).\
                filter(item_id_params).\
                filter(params).\
                filter(class_or_params).\
                filter(weapon_or_params).\
                group_by(Item.id)
            result = query.all()
        for entry in result:
            ts_items.append({'id': entry[0], 'npc_id': -2, 'npc_name': 'Tradeskills'})
    return base_items, special_items, quest_items, ts_items


def create_lookup_table(base_items, tradeskill_items, quest_items, special_items):
    """Returns item id filters and an associated lookup table."""
    lookup = {}
    item_ids = []
    for entry in base_items + tradeskill_items + quest_items + special_items:
        item_ids.append(Item.id == entry['id'])
        lookup.update({entry['id']: {'npc_id': entry['npc_id'], 'npc_name': entry['npc_name']}})
    return item_ids, lookup


def get_items_with_filters(weights, ignore_zero, **kwargs):
    """Returns all items with filters provided"""
    # Get the base items, tradeskill items, and quest items that drop from the zones in the eras requested.
    base_items, special_items, quest_items, tradeskill_items = get_era_items(kwargs)
    if not base_items and not tradeskill_items and not quest_items and not special_items:
        return [], False, False, False

    # Create the lookup table
    item_ids, lookup_table = create_lookup_table(base_items, tradeskill_items, quest_items, special_items)

    # Set up basic database filters
    filters = []
    focus_or_filters = []

    skip_filters = ['item_name', 'g_class_1', 'g_class_2', 'g_class_3', 'g_slot', 'i_type', 'no_rent', 'sub_type',
                    'sympathetic', 'eras', 'w_eff', 'pet_search', 'skillmodtype']
    bane_body = False
    for entry in kwargs:
        if entry in skip_filters:
            continue
        elif entry == 'proc_type':
            filters.append(Item.proceffect == SpellsNew.id)
            if kwargs['proc_type'] == 'Lifetap':
                filters.append(SpellsNew.targettype == 13)
            elif kwargs['proc_type'] == 'All':
                filters.append(SpellsNew.effectid1 == 0)
                filters.append(SpellsNew.effect_base_value1 < 0)
            elif kwargs['proc_type'] == 'Debuff':
                filters.append(SpellsNew.buffduration > 0)
                filters.append(SpellsNew.effectid1 == 0)
            elif kwargs['proc_type'] == 'Rune':
                filters.append(SpellsNew.effectid1 == 55)
            elif kwargs['proc_type'] == 'Healing':
                filters.append(SpellsNew.effectid1 == 0)
                filters.append(SpellsNew.effect_base_value1 > 0)
            else:
                filters.append(SpellsNew.resisttype == kwargs['proc_type'])
                filters.append(SpellsNew.effectid1 == 0)
                filters.append(SpellsNew.effect_base_value1 < 0)
        elif entry == 'proc':
            filters.append(Item.proceffect >= 1)
        elif 'proclevel2' in entry:
            filters.append(Item.proclevel2 <= kwargs['proclevel2'])
        elif entry == 'click':
            filters.append(Item.clickeffect >= 1)
        elif 'clicklevel2' in entry:
            filters.append(Item.clicklevel2 <= kwargs['clicklevel2'])
        elif 'elemdmgtype' in entry:
            filters.append(Item.elemdmgtype == kwargs['elemdmgtype'])
        elif 'banedmgbody' in entry:
            bane_body = True
            filters.append(Item.banedmgbody == kwargs['banedmgbody'])
        elif 'banedmgrace' in entry:
            bane_body = False
            filters.append(Item.banedmgrace == kwargs['banedmgrace'])
        elif 'focus_type' in entry:
            ids = utils.get_focus_values(kwargs['focus_type'], kwargs['sub_type'], engine, SpellsNew)
            for focus_id in ids:
                focus_or_filters.append(Item.focuseffect == focus_id)
            if kwargs['focus_type'] == 'Melee':
                for worn_id in ids:
                    focus_or_filters.append(Item.worneffect == worn_id)
            if kwargs['focus_type'] == 'Bard':
                for bard_id in ids:
                    focus_or_filters.append(Item.bardeffect == bard_id)
        elif 'delay' in entry:
            filters.append(Item.delay <= kwargs['delay'])
        elif 'procrate' in entry:
            filters.append(Item.procrate >= int(kwargs[entry]))
        else:
            filters.append(getattr(Item, entry) >= kwargs[entry])

    # Filters are set, run them!
    and_params = and_(*filters)
    focus_or_params = or_(*focus_or_filters)
    item_params = or_(*item_ids)

    arg_list = _get_arg_list()

    # BEHOLD, THE QUERY
    with Session(bind=engine) as session:
        query = session.query(*arg_list). \
            join(FocusSpell, FocusSpell.id == Item.focuseffect, isouter=True). \
            join(ClickSpell, ClickSpell.id == Item.clickeffect, isouter=True). \
            join(ProcSpell, ProcSpell.id == Item.proceffect, isouter=True). \
            join(WornSpell, WornSpell.id == Item.worneffect, isouter=True). \
            join(BardSpell, BardSpell.id == Item.bardeffect, isouter=True). \
            filter(Item.id.in_(session.query(Item.id).filter(item_params))). \
            filter(and_params). \
            filter(focus_or_params). \
            group_by(Item.id)
        all_items = query.all()

    out_items = []
    # If we don't have any items, that's it, return early.
    if not lookup_table:
        return out_items
    show_worn = False
    show_inst = False
    show_focus = False
    for entry in all_items:
        excl_list = utils.get_exclusion_list('item')
        if entry.id in excl_list:
            continue
        entry = utils.ReducedItem((dict(entry._mapping)))
        entry.npc_id = lookup_table[entry.id]['npc_id']
        entry.npc_name = lookup_table[entry.id]['npc_name']
        entry.focus_type = kwargs.get('focus_type')
        entry.sub_focus = kwargs.get('sub_type')
        if entry.focuseffect > 0:
            show_focus = True
        if entry.worneffect > 0:
            show_worn = True
        if entry.bardeffect > 0:
            show_inst = True

        if 'pet_search' in kwargs:
            pet_search = True
        else:
            pet_search = False

        if weights:
            entry.weight = utils.get_stat_weights(weights, entry, bane_body=bane_body)
            if ignore_zero and entry.weight == 0:
                continue
        else:
            entry.weight = 0

        # Add the weapon efficiency
        if entry.delay > 0:
            w_eff = '%.2f' % round(entry.damage / entry.delay, 2)
        else:
            w_eff = 0
        entry.w_eff = w_eff
        entry.zone_name = utils.lookup_zone_name(entry.npc_id)
        entry.npc_name = utils.fix_npc_name(entry.npc_name)
        
        out_items.append(entry)

    out_items.sort(key=operator.attrgetter('weight'), reverse=True)
    return out_items, show_focus, show_worn, show_inst
