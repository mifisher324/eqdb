import configparser
import logging
import os

import logic

from flask import Flask, render_template, request, flash, redirect, url_for

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
app.secret_key = ('\x1esN\x15X\xd8\xcc\xb1\x9a\xd2\xb4\x17\xa0`\x15?\x9b\x12'
                  '\x89\xeb\x88\x84\xe6\x00')
app.config['SITE_TYPE'] = SITE_TYPE
app.config['SITE_VERSION'] = SITE_VERSION

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

""" MAIN METHODS """


@app.route("/tooltip/<item_id>", methods=['GET', 'POST'])
def tooltip(item_id):
    return render_template('tooltip.html', item=logic.get_item_data(item_id))


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
    data = logic._debugger()
    return render_template('blank.html', data=data)


@app.route("/search/item", methods=['GET', 'POST'])
def item_search():
    if request.method == 'GET':
        return render_template('item_search.html')
    else:
        # Do some validations
        filters = {}
        g_slot = None
        show_dmg_delay = False
        show_focus = False
        full_detail = False
        show_click = False
        show_proc = False
        data = request.form

        # Make sure _something_ was provided
        if (request.form['g_class_1'] == 'None' and
                request.form['g_class_2'] == 'None' and
                request.form['g_class_3'] == 'None' and
                request.form['g_slot'] == 'None' and
                request.form['i_type'] == 'None' and
                request.form['spell_type'] == ''):
            flash('Must request a slot, class, item type other than all, or focus effect')
            return redirect(url_for('error'))

        if 'g_class_1' in request.form:
            filters.update({'g_class_1': request.form['g_class_1']})
        if 'g_class_2' in request.form:
            filters.update({'g_class_2': request.form['g_class_2']})
        if 'g_class_3' in request.form:
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
                if ('Bow' not in i_type and 'Any' not in i_type and 'Augment' not in i_type) and 'Range' in g_slot:
                    flash(f'Range slot can only search for "Bow" or "Any"')
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
                if i_type not in ['Any', 'Shield', 'Bow', 'Augment', 'Arrow'] and g_slot not in ['Primary', 'Secondary']:
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
        if 'True' in request.form['proc']:
            if g_slot:
                if g_slot == 'Primary' or g_slot == 'Secondary' or g_slot == 'Range':
                    filters.update({'proc': True})
                    show_proc = True
                    if 'proc_level' in data:
                        if int(data['proc_level']) > 0:
                            filters.update({'proclevel2': data['proc_level']})

        # Handle Click Effect Items
        if 'True' in data['click']:
            filters.update({'click': True})
            show_click = True
            if 'click_level' in data:
                if int(data['click_level']) > 0:
                    filters.update({'clicklevel2': data['click_level']})

        # Handle Sympathetics
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
            thing = 'stat_%s' % (i)
            thing_val = 'stat_val_%s' % (i)
            if thing in request.form:
                if request.form[thing] in filters:
                    flash('Cannot add the same item stat filter twice.')
                    return redirect(url_for('error'))
                if 'none' in request.form[thing]:
                    continue

                filters.update({
                    request.form[thing]: int(request.form[thing_val])})
                if 'reduce_restrict' in request.form:
                    reduce_changed = True
                    reduce_restrictions.update({request.form[thing]: True})
            else:
                continue

        # Handle Weights
        show_values = False
        weights = {}
        for i in range(1, 100):
            thing = 'weight_%s' % (i)
            thing_val = 'stat_weight_%s' % (i)
            if thing in request.form:
                show_values = True
                if request.form[thing] in weights:
                    flash('Cannot add the same item stat weight twice.')
                    return redirect(url_for('error'))
                if 'none' in request.form[thing]:
                    continue
                weights.update({
                    request.form[thing]: int(request.form[thing_val])})
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
        if 'add_no_rent' in request.form:
            filters.update({'no_rent': True})

        # Handle focus effects
        if 'spell_type' in request.form:
            if request.form['spell_type'] is not None and request.form['spell_type'] != '':
                filters.update({'focus_type': request.form['spell_type']})
                filters.update({'sub_type': request.form['focus_type']})
                show_focus = True

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
        ret_items = logic.get_items_with_filters(weights, ignore_zero, **filters)
        return render_template('item_search_results.html', data=ret_items, reduce=reduce_restrictions,
                               show_dmg_delay=show_dmg_delay, show_focus=show_focus, full_detail=full_detail,
                               show_values=show_values, show_click=show_click, show_proc=show_proc)


if __name__ == "__main__":
    app.debug = True
    app.run(port=5001)
