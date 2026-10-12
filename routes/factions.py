from flask import Blueprint, request, render_template, redirect, flash, url_for

import faction

faction_pages = Blueprint('factions', __name__, template_folder='templates')


@faction_pages.route("/faction/detail/<int:faction_id>")
def faction_detail(faction_id):
    return render_template('faction_detail.html', data=faction.get_faction(faction_id))


@faction_pages.route("/search/faction", methods=['GET', 'POST'])
def faction_search():
    if request.method == 'GET':
        return render_template('faction_search.html')
    else:
        faction_name = request.form['faction_name']
        if len(faction_name) > 50:
            flash('Search by name limited to 50 characters.')
            return redirect(url_for('faction_search'))
        elif len(faction_name) < 3:
            flash('Search by name requires at least 3 characters')
            return redirect(url_for('faction_search'))
        if not faction_name.isascii():
            flash('Only ASCII characters are allowed.')
            return redirect(url_for('npc_search'))
        data = faction.get_factions(faction_name)
        return render_template('faction_search_result.html', data=data)
