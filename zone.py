"""EQDB Logic File for Zones."""
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

import utils
from logic import Zone, engine, Spawn2, SpawnEntry, SpawnGroup, NPCTypes, Item, expansion, \
    ZonePoints, LootTableEntries, LootDropEntries

from logic import expansion


def _get_link_filters():
    """Helper to return the basic link filters between zone, npc, and item"""
    return [NPCTypes.loottable_id == LootTableEntries.loottable_id,
            LootTableEntries.lootdrop_id == LootDropEntries.lootdrop_id,
            LootDropEntries.item_id == Item.id]


def get_zone_listing():
    era_list = {'Classic': 0, 'Ruins of Kunark': 1, 'Legacy of Ykesha': 5, 'Scars of Velious': 2, 'Shadows of Luclin': 3,
                'Planes of Power': 4, 'Lost Dungeons of Norrath': 6, 'Gates of Discord': 7}
    out_list = {}
    exclusion_list = ['cshome', 'hateplane', 'powar', 'soldungc', 'qvicb']
    # Massaging
    massage_list = {'nedaria': 7, 'bazaar': 3}
    add_to_later = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}}
    for era in era_list:
        if era_list[era] > expansion:
            continue
        with Session(bind=engine) as session:
            query = session.query(Zone.zoneidnumber, Zone.short_name, Zone.long_name, Zone.zone_exp_multiplier). \
                filter(Zone.expansion == era_list[era])
            result = query.all()
        era_zones = {}
        for entry in result:
            id_num = entry[0]
            excl_list = utils.get_exclusion_list('zone')
            if id_num in excl_list:
                continue
            short_name = entry[1]
            long_name = entry[2]
            zem = entry[3]
            if short_name in exclusion_list:
                continue
            if short_name in massage_list.keys() and massage_list[short_name] != era_list[era]:
                add_to_later.update({massage_list[short_name]: {long_name: {'id': id_num,
                                                                            'short_name': short_name,
                                                                            'zem': zem}}})
                continue

            era_zones.update({long_name: {'id': id_num,
                                          'short_name': short_name,
                                          'zem': zem}})
        for entry in add_to_later[era_list[era]]:
            era_zones.update({entry: add_to_later[era_list[era]][entry]})
        out_list.update({era: era_zones})
    return out_list


def get_zone_long_name(zone_short_name):
    with Session(bind=engine) as session:
        query = session.query(Zone.zoneidnumber, Zone.long_name).filter(Zone.short_name == zone_short_name)
        result = query.first()
    return result[0], result[1]


def get_zone_detail(zone_id):
    excl_list = utils.get_exclusion_list('zone')
    if zone_id in excl_list:
        return None
    # Get some zone details
    with Session(bind=engine) as session:
        args = [Zone.expansion, Zone.short_name, Zone.long_name, Zone.safe_x, Zone.safe_y, Zone.canbind, Zone.canlevitate,
                Zone.castoutdoor]
        query = session.query(*args).filter(Zone.zoneidnumber == zone_id)
        result = query.first()

    if not result:
        return None

    base_data = {'expansion': utils.get_era_name(result[0]),
                 'short_name': result[1],
                 'long_name': result[2],
                 'safe_x': int(result[3]),
                 'safe_y': int(result[4]),
                 'can_bind': result[5],
                 'can_lev': result[6],
                 'outdoor': result[7]}

    # Get all the zones this zone connects to
    with Session(bind=engine) as session:
        query = session.query(ZonePoints.target_zone_id).distinct().filter(ZonePoints.zone == base_data['short_name'])
        result = query.all()

        if result:
            target_zone_ids = []
            for entry in result:
                target_zone_ids.append(Zone.zoneidnumber == entry[0])

            target_zone_params = or_(*target_zone_ids)
            query = session.query(Zone.zoneidnumber, Zone.long_name, Zone.expansion).filter(target_zone_params)
            result = query.all()
        else:
            result = []

    linked_zone_data = {}
    for entry in result:
        if int(entry[2]) > expansion:
            continue
        linked_zone_data.update({entry[0]: entry[1]})
    base_data.update({'linked_zones': linked_zone_data})

    # Get all the items that drop in this zone.
    known_ids = []
    link_filters = _get_link_filters()
    link_params = and_(*link_filters)
    with Session(bind=engine) as session:
        query = session.query(Item.id, Item.Name, Item.icon).filter(NPCTypes.id.like(f'{zone_id}___')).\
            filter(link_params)
        result = query.all()
    out_items = []
    for entry in result:
        if entry[0] not in known_ids:
            known_ids.append(entry[0])
            out_items.append({'item_id': entry[0],
                              'item_name': entry[1],
                              'icon': entry[2]})
    base_data.update({'dropped_items': out_items})

    # Parse the map files and add them to the returned data.
    short_name = base_data['short_name']
    base_data.update({'mapping': utils.get_map_data(short_name)})
    # base_data.update({'poi': utils.get_map_poi(short_name)})

    # Get all the NPCs for this zone
    spawn_groups = {}
    npc_list = []
    with Session(bind=engine) as session:
        query = session.query(NPCTypes.id, NPCTypes.name, NPCTypes.hp, NPCTypes.race, NPCTypes.level).\
            filter(NPCTypes.id.like(f'{zone_id}___'))
        result = query.all()
        for entry in result:
            npc_id = entry[0]
            npc_name = entry[1]
            npc_hp = entry[2]
            npc_race = utils.get_bane_dmg_race(entry[3])
            npc_level = entry[4]
            npc_list.append({'id': npc_id, 'name': utils.fix_npc_name(npc_name), 'hp': npc_hp, 'race': npc_race,
                             'level': npc_level})

        base_data['npcs'] = npc_list
        query = session.query(Spawn2.x, Spawn2.y, Spawn2.z, Spawn2.respawntime, SpawnGroup.name, NPCTypes.name,
                              NPCTypes.id, SpawnEntry.chance, Spawn2.id, Spawn2.spawngroupID).\
            filter(Spawn2.spawngroupID == SpawnGroup.id).\
            filter(SpawnEntry.spawngroupID == Spawn2.spawngroupID).\
            filter(Spawn2.zone == short_name). \
            filter(SpawnEntry.npcID == NPCTypes.id).\
            order_by(Spawn2.spawngroupID)
        result = query.all()
        for entry in result:
            x = entry[0]
            y = entry[1]
            z = entry[2]
            respawn = entry[3]
            name = entry[4]
            npc_name = entry[5]
            npc_id = entry[6]
            chance = entry[7]
            spawn_id = entry[8]
            group_id = entry[9]
            if name in spawn_groups:
                npc_list = spawn_groups[name]['npcs']
            else:
                npc_list = []
            if {'npc_name': npc_name, 'npc_id': npc_id, 'chance': chance} not in npc_list:
                npc_list.append({'npc_name': npc_name,
                                 'npc_id': npc_id,
                                 'chance': chance})
            spawn_groups.update({name: {'x': x,
                                        'y': y,
                                        'z': z,
                                        'respawn': utils.convert_time(respawn),
                                        'npcs': npc_list,
                                        'spawn_id': spawn_id,
                                        'group_id': group_id}})
    base_data['spawn_groups'] = spawn_groups

    # Get waypoint, assuming there is one
    base_data['waypoint'] = utils.get_zone_waypoint(short_name)

    return base_data


def get_zone(name):
    partial = "%%%s%%" % name
    with Session(bind=engine) as session:
        query = session.query(Zone.zoneidnumber, Zone.long_name).\
            filter(Zone.long_name.like(partial)).\
            filter(Zone.expansion <= expansion)
        result = query.all()

    out_zones = []
    for entry in result:
        excl_list = utils.get_exclusion_list('zone')
        if entry[0] in excl_list:
            return None
        out_zones.append({'zone_id': entry[0],
                          'zone_name': entry[1]})
    return out_zones


def waypoint_listing():
    antonica = {}
    faydwer = {}
    odus = {}
    kunark = {}
    velious = {}
    luclin = {}
    planes = {}
    #taelosia = {}
    #kuua = {}
    entries = [Zone.short_name == 'blackburrow',
               Zone.short_name == 'commons',
               Zone.short_name == 'ecommons',
               Zone.short_name == 'feerrott',
               Zone.short_name == 'freportw',
               Zone.short_name == 'grobb',
               Zone.short_name == 'everfrost',
               Zone.short_name == 'halas',
               Zone.short_name == 'highkeep',
               Zone.short_name == 'lavastorm',
               Zone.short_name == 'neriakb',
               Zone.short_name == 'northkarana',
               Zone.short_name == 'eastkarana',
               Zone.short_name == 'oasis',
               Zone.short_name == 'oggok',
               Zone.short_name == 'oot',
               Zone.short_name == 'qey2hh1',
               Zone.short_name == 'qeynos2',
               Zone.short_name == 'qrg',
               Zone.short_name == 'rivervale',
               Zone.short_name == 'gukbottom',
               Zone.short_name == 'lakerathe',
               Zone.short_name == 'southkarana']
    entry_params = or_(*entries)
    with Session(bind=engine) as session:
        query = session.query(Zone.short_name, Zone.zoneidnumber, Zone.long_name).filter(entry_params)
        result = query.all()

    for entry in result:
        sub_data = utils.get_zone_waypoint(entry[0])
        sub_data.update({'zone_id': entry[1]})
        antonica.update({entry[2]: sub_data})

    entries = [Zone.short_name == 'akanon',
               Zone.short_name == 'cauldron',
               Zone.short_name == 'felwithea',
               Zone.short_name == 'gfaydark',
               Zone.short_name == 'kaladmina',
               Zone.short_name == 'mistmoore']
    entry_params = or_(*entries)
    with Session(bind=engine) as session:
        query = session.query(Zone.short_name, Zone.zoneidnumber, Zone.long_name).filter(entry_params)
        result = query.all()

    for entry in result:
        sub_data = utils.get_zone_waypoint(entry[0])
        sub_data.update({'zone_id': entry[1]})
        faydwer.update({entry[2]: sub_data})

    entries = [Zone.short_name == 'erudnext',
               Zone.short_name == 'hole',
               Zone.short_name == 'paineel',
               Zone.short_name == 'tox',
               Zone.short_name == 'stonebrunt',
               Zone.short_name == 'dulak',
               Zone.short_name == 'gunthak']
    entry_params = or_(*entries)
    with Session(bind=engine) as session:
        query = session.query(Zone.short_name, Zone.zoneidnumber, Zone.long_name).filter(entry_params)
        result = query.all()

    for entry in result:
        sub_data = utils.get_zone_waypoint(entry[0])
        sub_data.update({'zone_id': entry[1]})
        odus.update({entry[2]: sub_data})

    entries = [Zone.short_name == 'burningwood',
               Zone.short_name == 'cabeast',
               Zone.short_name == 'citymist',
               Zone.short_name == 'dreadlands',
               Zone.short_name == 'fieldofbone',
               Zone.short_name == 'firiona',
               Zone.short_name == 'frontiermtns',
               Zone.short_name == 'karnor',
               Zone.short_name == 'lakeofillomen',
               Zone.short_name == 'overthere',
               Zone.short_name == 'skyfire',
               Zone.short_name == 'timorous',
               Zone.short_name == 'trakanon',
               Zone.short_name == 'chardokb']
    entry_params = or_(*entries)
    with Session(bind=engine) as session:
        query = session.query(Zone.short_name, Zone.zoneidnumber, Zone.long_name).filter(entry_params)
        result = query.all()

    for entry in result:
        sub_data = utils.get_zone_waypoint(entry[0])
        sub_data.update({'zone_id': entry[1]})
        kunark.update({entry[2]: sub_data})

    entries = [Zone.short_name == 'cobaltscar',
               Zone.short_name == 'eastwastes',
               Zone.short_name == 'greatdivide',
               Zone.short_name == 'iceclad',
               Zone.short_name == 'wakening',
               Zone.short_name == 'westwastes',
               Zone.short_name == 'cobaltscar',
               Zone.short_name == 'sirens']
    entry_params = or_(*entries)
    with Session(bind=engine) as session:
        query = session.query(Zone.short_name, Zone.zoneidnumber, Zone.long_name).filter(entry_params)
        result = query.all()

    for entry in result:
        sub_data = utils.get_zone_waypoint(entry[0])
        sub_data.update({'zone_id': entry[1]})
        velious.update({entry[2]: sub_data})

    entries = [Zone.short_name == 'dawnshroud',
               Zone.short_name == 'fungusgrove',
               Zone.short_name == 'sharvahl',
               Zone.short_name == 'ssratemple',
               Zone.short_name == 'tenebrous',
               Zone.short_name == 'umbral',
               Zone.short_name == 'twilight',
               Zone.short_name == 'scarlet',
               Zone.short_name == 'paludal',
               Zone.short_name == 'bazaar']
    entry_params = or_(*entries)
    with Session(bind=engine) as session:
        query = session.query(Zone.short_name, Zone.zoneidnumber, Zone.long_name).filter(entry_params)
        result = query.all()

    for entry in result:
        sub_data = utils.get_zone_waypoint(entry[0])
        sub_data.update({'zone_id': entry[1]})
        luclin.update({entry[2]: sub_data})

    entries = [Zone.short_name == 'airplane',
               Zone.short_name == 'fearplane',
               Zone.short_name == 'hateplaneb',
               Zone.short_name == 'poknowledge',
               Zone.short_name == 'potranquility',
               Zone.short_name == 'potimea']
    entry_params = or_(*entries)
    with Session(bind=engine) as session:
        query = session.query(Zone.short_name, Zone.zoneidnumber, Zone.long_name).filter(entry_params)
        result = query.all()

    for entry in result:
        sub_data = utils.get_zone_waypoint(entry[0])
        sub_data.update({'zone_id': entry[1]})
        planes.update({entry[2]: sub_data})

    # entries = [Zone.short_name == 'barindu',
    #            Zone.short_name == 'kodtaz',
    #            Zone.short_name == 'natimbi',
    #            Zone.short_name == 'qvic',
    #            Zone.short_name == 'txevu']
    # entry_params = or_(*entries)
    # with Session(bind=engine) as session:
    #     query = session.query(Zone.short_name, Zone.zoneidnumber, Zone.long_name).filter(entry_params)
    #     result = query.all()
    #
    # for entry in result:
    #     sub_data = utils.get_zone_waypoint(entry[0])
    #     sub_data.update({'zone_id': entry[1]})
    #     taelosia.update({entry[2]: sub_data})
    #
    # entries = [Zone.short_name == 'wallofslaughter']
    # entry_params = or_(*entries)
    # with Session(bind=engine) as session:
    #     query = session.query(Zone.short_name, Zone.zoneidnumber, Zone.long_name).filter(entry_params)
    #     result = query.all()
    #
    # for entry in result:
    #     sub_data = utils.get_zone_waypoint(entry[0])
    #     sub_data.update({'zone_id': entry[1]})
    #     kuua.update({entry[2]: sub_data})

    return {'Antonica': antonica,
            'Faydwer': faydwer,
            'Odus': odus,
            'Kunark': kunark,
            'Velious': velious,
            'Luclin': luclin,
            'Planes': planes}
            #'Taelosia': taelosia,
            #'Kuua': kuua}