from flask import Blueprint, request, render_template, flash, redirect, url_for

import spell

spell_pages = Blueprint('spells', __name__, template_folder='templates')


@spell_pages.route("/search/spell", methods=['GET', 'POST'])
def spell_search():
    if request.method == 'GET':
        return render_template('spell_search.html')
    else:
        spell_name = request.form['spell_name']
        if len(spell_name) > 50:
            flash('Search by name limited to 50 characters.')
            return redirect(url_for('spell_search'))
        elif len(spell_name) < 3:
            flash('Search by name requires at least 3 characters')
            return redirect(url_for('spell_search'))
        if not spell_name.isascii():
            flash('Only ASCII characters are allowed.')
            return redirect(url_for('spell_search'))
        data = spell.get_spells(spell_name)
        return render_template('spell_search_result.html', data=data)


@spell_pages.route("/spell/detail/<int:spell_id>")
def spell_detail(spell_id):
    base_data, slots = spell.get_full_spell_data(spell_id)
    return render_template('spell_detail.html', data=base_data, slots=slots)


@spell_pages.route("/spell/raw/<int:spell_id>")
def spell_raw(spell_id):
    raw_data = spell.get_spell_raw_data(spell_id)
    return render_template('raw_data.html', data=raw_data)


@spell_pages.route("/spell/listing", methods=['GET'])
def spell_listing():
    class_id = request.args.get('class_id')
    if not class_id:
        return render_template('spell_listing.html')
    else:
        data = spell.get_spells_by_class(class_id, min_level=1, max_level=65)
        return render_template('spell_listing_result.html', data=data)
