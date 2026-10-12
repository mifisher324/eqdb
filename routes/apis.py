from flask import Blueprint, request, jsonify

import item
import npc
import spell
import tradeskill

api_pages = Blueprint('apis', __name__, template_folder='templates')


@api_pages.route("/api/v1/loot")
def get_loot_json():
    loot_id = request.args.get('id')
    npc_id = request.args.get('npc_id')
    data = items.get_loot_json(loot_id=loot_id, npc_id=npc_id)
    return jsonify(data)


@api_pages.route("/api/v1/trades")
def get_tradeskill_json():
    name = request.args.get('name')
    ts_id = request.args.get('id')
    data = tradeskill.get_tradeskill_json(ts_id=ts_id, ts_name=name)
    return jsonify(data)


@api_pages.route("/api/v1/npcs")
def get_npc_json():
    name = request.args.get('name')
    npc_id = request.args.get('id')
    zone = request.args.get('zone')
    data = npc.get_npc_raw_data(npc_id=npc_id, name=name, zone=zone)
    return jsonify(data)


@api_pages.route("/api/v1/items")
def get_item_json():
    name = request.args.get('name')
    item_id = request.args.get('id')
    i_type = request.args.get('type')
    data = items.get_item_json(name=name, item_id=item_id, i_type=i_type)
    return jsonify(data)


@api_pages.route("/api/v1/spells")
def get_spell_json():
    name = request.args.get('name')
    spell_id = request.args.get('id')
    data = spell.get_spell_raw_data(spell_id=spell_id, spell_name=name)
    return jsonify(data)
