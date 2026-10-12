import configparser
import json
import logging
import os

from flask import Flask, render_template, request, flash, redirect, url_for

import spell
import utils
import local
import logic
from routes import apis, pets, spells, zones, tradeskills, npcs, items, factions

# Application Setup
here = os.path.dirname(__file__)
site_config = configparser.RawConfigParser()
ini_path = os.path.join(here, 'configuration.ini')
site_config.read_file(open(ini_path))

SITE_TYPE = site_config.get('DEFAULT', 'site_type')
SITE_VERSION = site_config.get('DEFAULT', 'site_version')

app = Flask(__name__)
fh = logging.FileHandler(site_config.get('path', 'flask_log'))
app.logger.addHandler(fh)
app.secret_key = 'this_is_a_secret'
app.config['SITE_TYPE'] = SITE_TYPE
app.config['SITE_VERSION'] = SITE_VERSION
app.config['DISCORD_CLIENT_ID'] = site_config.get('discord', 'client_id')
app.config['DISCORD_CLIENT_SECRET'] = site_config.get('discord', 'client_secret')
if SITE_TYPE == 'Development':
    app.config['DISCORD_REDIRECT_URI'] = "http://localhost:5001/callback"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "true"
else:
    app.config['DISCORD_REDIRECT_URI'] = "https://eqdb.net/callback"
app.config['DISCORD_BOT_TOKEN'] = ""

app_path = site_config.get('path', 'app_log')
formatter = logging.Formatter(
    '%(asctime)s: %(levelname)s - %(funcName)s - %(message)s',
    '%m/%d/%Y-%I%M%S %p')

app_log = logging.getLogger('app_log')
afh = logging.FileHandler(app_path)
afh.setFormatter(formatter)
app_log.addHandler(afh)
app_log.setLevel(logging.DEBUG)
ALLOWED_EXTENSIONS = {'txt'}

""" BLUEPRINTS """
app.register_blueprint(apis.api_pages)
app.register_blueprint(pets.pet_pages)
app.register_blueprint(spells.spell_pages)
app.register_blueprint(zones.zone_pages)
app.register_blueprint(tradeskills.tradeskill_pages)
app.register_blueprint(npcs.npc_pages)
app.register_blueprint(items.item_pages)
app.register_blueprint(factions.faction_pages)


""" MAIN METHODS """


@app.route("/site_error")
@app.errorhandler(Exception)
def all_exception_handler(error):
    referrer = request.path
    if SITE_TYPE == 'Development':
        raise error
    logic.send_error_email(error, referrer)
    return render_template('site_error.html')


@app.route("/search/all", methods=['POST'])
def all_search():
    name = request.form['all_names']
    if len(name) > 50:
        flash('Search by name limited to 50 characters.')
        return redirect(url_for('main_page'))
    elif len(name) < 3:
        flash('Search by name requires at least 3 characters.')
        return redirect(url_for('main_page'))
    if not name.isascii():
        flash('Only ASCII characters are allowed.')
        return redirect(url_for('main_page'))
    data = logic.all_search(name=name)
    return render_template('all_search_result.html', search_txt=name, data=data)


@app.route("/tooltip/<item_id>", methods=['GET', 'POST'])
def tooltip(item_id):
    return render_template('tooltip.html', item=logic.get_item_data(item_id))


@app.route("/spell-tooltip/<spell_id>", methods=['GET', 'POST'])
def spell_tooltip(spell_id):
    _, slots = spell.get_spell_tooltip(spell_id)
    return render_template('spell_tooltip.html', slots=slots)


@app.route("/about", methods=['GET'])
def about():
    with open(os.path.join(here, 'about.txt'), 'r') as fh:
        data = fh.read()
    return render_template('changelog.html', data=data)


@app.route("/changelog", methods=['GET'])
def changelog():
    with open(os.path.join(here, 'changelog.txt'), 'r') as fh:
        data = fh.read()
    return render_template('changelog.html', data=data)


@app.route("/error", methods=['GET'])
def error():
    return render_template('blank.html')


@app.route("/", methods=['GET'])
def main_page():
    return render_template('main.html')


@app.route("/debug/tester", methods=['GET'])
def tester():
    if SITE_TYPE != 'Development':
        flash("Unauthorized")
        return redirect(url_for('error'))
    # data, slots = logic._debugger()
    return render_template('blank.html')


@app.route("/search/item", methods=['POST'])
def item_search():
    # Do some validations
    filters = {}
    g_slot = None
    show_dmg_delay = False
    show_spells = False
    full_detail = False
    show_click = False
    show_proc = False
    show_proc_max_dmg = False
    data = request.form

    # Make sure _something_ was provided
    if (request.form['g_class_1'] == 'None' and
        request.form['g_class_2'] == 'None' and
        request.form['g_class_3'] == 'None' and
        request.form['g_slot'] == 'None' and
        request.form['i_type'] == 'None' and
        ('spell_type' not in request.form or ('spell_type' in request.form and request.form['spell_type'] == '')) and
        'pet_search' not in data):
        flash('Must request a slot, class, item type other than all, or focus effect, or select Search for Pet Items')
        return redirect(url_for('error'))

    if 'g_class_1' in request.form:
        if request.form['g_class_1'] != 'None':
            filters.update({'g_class_1': request.form['g_class_1']})
    if 'g_class_2' in request.form:
        if request.form['g_class_2'] != 'None':
            filters.update({'g_class_2': request.form['g_class_2']})
    if 'g_class_3' in request.form:
        if request.form['g_class_3'] != 'None':
            filters.update({'g_class_3': request.form['g_class_3']})

    if 'g_slot' in request.form:
        if request.form['g_slot'] != 'None':
            filters.update({'g_slot': request.form['g_slot']})
            g_slot = request.form['g_slot']
            if 'Primary' in g_slot or 'Secondary' in g_slot or 'Range' in g_slot:
                show_dmg_delay = True

    # Handle Name
    if 'item_name' in request.form:
        if len(request.form['item_name']) > 0:
            filters.update({'item_name': request.form['item_name']})

    # Handle Skill Mod
    if request.form['skillmodtype'] != 'None':
        filters.update({'skillmodtype': request.form['skillmodtype']})

    # Handle Item Type
    if request.form['i_type'] != 'None':
        i_type = request.form['i_type']

        # Do some validations here to stop insanity
        if g_slot is not None:
            # Handle Bows not in Range
            if 'Bow' in i_type and 'Range' not in g_slot:
                flash(f'Cannot search for item type "Bow" in slot {g_slot}')
                return redirect(url_for('error'))

            # Handle ranged with other weapon types
            if (('Bow' not in i_type and 'Any' not in i_type and 'Augment' not in i_type and 'Thrown' not in i_type) and
                 'Range' in g_slot):
                flash(f'Range slot can only search for "Thrown", "Bow", or "Any"')
                return redirect(url_for('error'))

            # Handle Shield not in Secondary
            if 'Shield' in i_type and 'Secondary' not in g_slot and 'Back' not in g_slot:
                flash(f'Cannot search for item type "Shield" in slot {g_slot}')
                return redirect(url_for('error'))

            # Handle 2H not in Primary
            if (i_type in ['Two Hand Slash', 'Two Hand Blunt', 'Two Hand Piercing', 'Any 2H Weapon'] and
                    'Primary' not in g_slot):
                flash(f'Cannot search for Two-Handed items in slot {g_slot}')
                return redirect(url_for('error'))

            # Handle arrows in non-ammo slots
            if i_type == 'Arrow' and g_slot != 'Ammo':
                flash(f'Arrows can only go in the Ammo slot.')
                return redirect(url_for('error'))

            # Handle weapons in non-weapon slots
            if (i_type not in ['Any', 'Shield', 'Bow', 'Augment', 'Arrow', 'Thrown'] and
                g_slot not in ['Primary', 'Secondary']):
                flash(f'Cannot search for weapons in slot {g_slot}')
                return redirect(url_for('error'))

        filters.update({'i_type': i_type})

    # Handle Eras
    base_era_list = ['Classic', 'Kunark', 'Velious', 'Luclin', 'Planes']
    remove_era_list = request.form.getlist('eras')
    era_list = []
    for era in base_era_list:
        if era in remove_era_list:
            continue
        else:
            era_list.append(era)
    filters.update({'eras': era_list})

    # Handle Proc Weapon Items
    if 'proc' in data:
        if 'True' in data['proc']:
            if g_slot:
                if g_slot == 'Primary' or g_slot == 'Secondary' or g_slot == 'Range':
                    filters.update({'proc': True})
                    show_proc = True
                    if 'proc_level' in data:
                        if int(data['proc_level']) > 0:
                            filters.update({'proclevel2': data['proc_level']})
    if 'proc_type' in data and data['proc_type'] != 'None':
        filters.update({'proc_type': data['proc_type']})
        show_proc = True
        if data['proc_type'] == 'All':
            show_proc_max_dmg = True

    # Handle Click Effect Items
    if 'click' in data:
        if 'True' in data['click']:
            filters.update({'click': True})
            show_click = True
            if 'click_level' in data:
                if int(data['click_level']) > 0:
                    filters.update({'clicklevel2': data['click_level']})

    # Handle Sympathetics
    if 'sympathetic' in data:
        if data['sympathetic'] != 'None':
            filters.update({'sympathetic': data['sympathetic']})
            show_click = True

    # Handle Stat Requirements
    reduce_changed = False
    reduce_restrictions = {
        'ac': False,
        'hp': False,
        'mana': False,
        'astr': False,
        'asta': False,
        'aagi': False,
        'adex': False,
        'awis': False,
        'aint': False,
        'acha': False,
        'heroic_str': False,
        'heroic_sta': False,
        'heroic_agi': False,
        'heroic_dex': False,
        'heroic_wis': False,
        'heroic_int': False,
        'heroic_cha': False,
        'fr': False,
        'cr': False,
        'pr': False,
        'dr': False,
        'mr': False,
        'attack': False,
        'haste': False,
        'regen': False,
        'manaregen': False,
        'spelldmg': False,
        'healamt': False,
        'accuracy': False,
        'avoidance': False,
        'combateffects': False,
        'damageshield': False,
        'dotshielding': False,
        'shielding': False,
        'spellshield': False,
        'strikethrough': False,
        'stunresist': False,
    }
    for i in range(1, 100):
        thing = 'stat_%s' % i
        thing_val = 'stat_val_%s' % i
        if thing in request.form:
            if request.form[thing] in filters:
                flash('Cannot add the same item stat filter twice.')
                return redirect(url_for('error'))
            if 'none' in request.form[thing]:
                continue

            filters.update({
                request.form[thing]: float(request.form[thing_val])})
            if 'reduce_restrict' in request.form:
                reduce_changed = True
                reduce_restrictions.update({request.form[thing]: True})
        else:
            continue

    # Handle Weights
    show_values = False
    weights = {}
    for i in range(1, 100):
        thing = 'weight_%s' % i
        thing_val = 'stat_weight_%s' % i
        if thing in request.form:
            show_values = True
            if request.form[thing] in weights:
                flash('Cannot add the same item stat weight twice.')
                return redirect(url_for('error'))
            if 'none' in request.form[thing]:
                continue
            weights.update({
                request.form[thing]: float(request.form[thing_val])})
            if 'show_weight_detail' in request.form:
                reduce_changed = True
                reduce_restrictions.update({request.form[thing]: True})
        else:
            continue

    # Handle Show Table
    if 'show_full_detail' in request.form:
        full_detail = True

    if not reduce_changed:
        # Flip them all to true
        for entry in reduce_restrictions:
            reduce_restrictions[entry] = True

    # Handle Ignore Zero
    if 'ignore_zero' in request.form:
        if not show_values:
            flash('Include zero weight items requires at least one weight.')
            return redirect(url_for('error'))
        ignore_zero = False
    else:
        ignore_zero = True

    # Handle no rent
    if 'pet_search' in request.form:
        filters.update({'pet_search': True})

    # Handle focus effects
    if 'spell_type' in request.form:
        if request.form['spell_type'] is not None and request.form['spell_type'] != '':
            filters.update({'focus_type': request.form['spell_type']})
            filters.update({'sub_type': request.form['focus_type']})
            show_spells = True

    # Handle elem damage
    if 'elemdmgtype' in data:
        if g_slot:
            if g_slot == 'Primary' or g_slot == 'Secondary' or g_slot == 'Range':
                if data['elemdmgtype'] != 'all':
                    filters.update({'elemdmgtype': data['elemdmgtype']})

    # Handle bane damage
    if 'banetype' in data:
        if g_slot:
            if g_slot == 'Primary' or g_slot == 'Secondary' or g_slot == 'Range':
                if data['banetype'] != 'all':
                    bane_id = int(data['banetype'].split('_')[1])
                    if 'body' in data['banetype']:
                        filters.update({'banedmgbody': bane_id})
                    else:
                        filters.update({'banedmgrace': bane_id})

    # Oh god, we've got everything...lets get a list of items
    ret_items, focus, worn, inst = logic.get_items_with_filters(weights, ignore_zero, **filters)

    # Show damage and delay whenever the results actually contain weapons. show_dmg_delay
    # is otherwise set only when a Primary/Secondary/Range slot is chosen, so a search by
    # item type (Two Hand Slash, Bow, ...) lists no damage or delay at all.
    if not show_dmg_delay:
        show_dmg_delay = any(getattr(e, 'damage', 0) for e in ret_items)
    return render_template('item_search_results.html', data=ret_items, reduce=reduce_restrictions,
                           show_dmg_delay=show_dmg_delay, show_focus=focus, full_detail=full_detail,
                           show_values=show_values, show_click=show_click, show_proc=show_proc, show_worn=worn,
                           show_inst=inst, show_spells=show_spells, show_proc_max_dmg=show_proc_max_dmg)


@app.route("/search/weapon", methods=['GET', 'POST'])
def weapon_search():
    if request.method == 'GET':
        skills = utils.get_all_skills()
        return render_template('weapon_search.html',
                               skills=skills)
    else:
        return redirect(url_for('item_search'), code=307)


@app.route("/search/armor", methods=['GET', 'POST'])
def armor_search():
    if request.method == 'GET':
        skills = utils.get_all_skills()
        return render_template('item_search.html',
                               skills=skills)
    else:
        return redirect(url_for('item_search'), code=307)


if __name__ == "__main__":
    app.debug = True
    app.run(port=5001)
