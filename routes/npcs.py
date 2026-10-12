from flask import Blueprint, render_template, request, flash, redirect, url_for

import npc

npc_pages = Blueprint('npcs', __name__, template_folder='templates')


@npc_pages.route("/search/npc", methods=['GET', 'POST'])
def npc_search():
    if request.method == 'GET':
        return render_template('npc_search.html')
    else:
        npc_name = request.form['npc_name']
        if len(npc_name) > 50:
            flash('Search by name limited to 50 characters.')
            return redirect(url_for('npc_search'))
        elif len(npc_name) < 3:
            flash('Search by name requires at least 3 characters')
            return redirect(url_for('npc_search'))
        if not npc_name.isascii():
            flash('Only ASCII characters are allowed.')
            return redirect(url_for('npc_search'))
        data = npc.get_npcs(npc_name)
        return render_template('npc_search_result.html', data=data)


@npc_pages.route("/npc/raw/<int:npc_id>")
def npc_raw(npc_id):
    raw_data = npc.get_npc_raw_data(npc_id)
    return render_template('raw_data.html', data=raw_data)


@npc_pages.route("/npc/detail/<int:npc_id>")
def npc_detail(npc_id):
    return render_template('npc_detail.html', data=npc.get_npc_detail(npc_id))
