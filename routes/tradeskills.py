from flask import Blueprint, request, render_template, flash, redirect, url_for

import tradeskill

tradeskill_pages = Blueprint('tradeskills', __name__, template_folder='templates')


@tradeskill_pages.route("/tradeskill/detail/<int:ts_id>")
def tradeskill_detail(ts_id):
    data = tradeskill.get_tradeskill_detail(ts_id)
    return render_template('tradeskill_detail.html', data=data)


@tradeskill_pages.route("/search/tradeskill", methods=['GET', 'POST'])
def tradeskill_search():
    if request.method == 'GET':
        return render_template('tradeskill_search.html')
    else:
        tradeskill_name = request.form['tradeskill_name']
        trivial = request.form.get('trivial')
        trivial_min = request.form.get('trivial_min')
        ts = request.form.get('tradeskill')
        remove_no_fail = request.form.get('no_fail')
        if ts == 'None':
            ts = None
        if len(tradeskill_name) > 50:
            flash('Search by name limited to 50 characters.')
            return redirect(url_for('tradeskill_search'))
        elif 0 < len(tradeskill_name) < 3:
            flash('Search by name requires at least 3 characters.')
            return redirect(url_for('tradeskill_search'))
        if not tradeskill_name.isascii():
            flash('Only ASCII characters are allowed.')
            return redirect(url_for('tradeskill_search'))
        data = tradeskill.get_tradeskills(name=tradeskill_name, trivial=trivial,
                                          tradeskill=ts, remove_no_fail=remove_no_fail,
                                          trivial_min=trivial_min)
        return render_template('tradeskill_search_result.html', data=data)
