from sqlalchemy.orm import Session

from logic import FactionList, engine, NPCFactionEntries, NPCTypes, Zone


def get_factions(name):
    partial = "%%%s%%" % name
    with Session(bind=engine) as session:
        query = session.query(FactionList.name, FactionList.id).filter(FactionList.name.like(partial))
        result = query.all()

    out_factions = []
    for entry in result:
        out_factions.append({'faction_name': entry[0],
                             'faction_id': entry[1]})
    return out_factions


def get_faction(faction_id):
    # Get name
    if faction_id == 5013 or faction_id == 242:
        return []
    base_data = {}
    with Session(bind=engine) as session:
        query = session.query(FactionList.name).filter(FactionList.id == faction_id)
        result = query.first()
    if not result:
        return None

    base_data.update({'name': result[0]})

    # Get all the NPCs associated with this faction
    pos_zones = {}
    neg_zones = {}
    zone_lookup = {}
    with Session(bind=engine) as session:
        query = session.query(NPCFactionEntries.value, NPCTypes.id, NPCTypes.name).\
            filter(NPCFactionEntries.faction_id == faction_id).\
            filter(NPCFactionEntries.npc_faction_id == NPCTypes.npc_faction_id)
        result = query.all()

    for entry in result:
        value = entry[0]
        npc_id = entry[1]
        npc_name = entry[2]
        zone = int(npc_id / 1000)
        npc = {'npc_id': npc_id,
               'npc_name': npc_name,
               'value': value}
        if zone not in zone_lookup:
            with Session(bind=engine) as session:
                query = session.query(Zone.long_name).filter(Zone.zoneidnumber == zone)
                result = query.first()
                if not result:
                    zone_name = "Unknown"
                else:
                    zone_name = result[0]
                zone_lookup.update({zone: zone_name})
        else:
            zone_name = zone_lookup[zone]

        if value < 0:
            if zone_name in neg_zones:
                zone_list = neg_zones[zone_name]
            else:
                zone_list = []
            zone_list.append(npc)
            neg_zones.update({zone_name: zone_list})
        else:
            if zone_name in pos_zones:
                zone_list = pos_zones[zone_name]
            else:
                zone_list = []
            zone_list.append(npc)
            pos_zones.update({zone_name: zone_list})
    base_data.update({'positive': pos_zones})
    base_data.update({'negative': neg_zones})

    return base_data
