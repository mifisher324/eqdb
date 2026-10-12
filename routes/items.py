from flask import Blueprint, render_template, request, flash, redirect, url_for

import item
import logic

item_pages = Blueprint('items', __name__, template_folder='templates')


@item_pages.route("/item/clicks", methods=['GET', 'POST'])
def click_item_search():
    if request.method == 'GET':
        return render_template('click_items.html')
    else:
        filters = {}
        if 'g_class_1' in request.form:
            if request.form['g_class_1'] != 'None':
                filters.update({'g_class_1': request.form['g_class_1']})
        if 'g_class_2' in request.form:
            if request.form['g_class_2'] != 'None':
                filters.update({'g_class_2': request.form['g_class_2']})
        if 'g_class_3' in request.form:
            if request.form['g_class_3'] != 'None':
                filters.update({'g_class_3': request.form['g_class_3']})
        base_era_list = ['Classic', 'Kunark', 'Velious', 'Luclin', 'Planes', 'LDoN']
        remove_era_list = request.form.getlist('eras')
        era_list = []
        for era in base_era_list:
            if era in remove_era_list:
                continue
            else:
                era_list.append(era)
        filters.update({'eras': era_list})
        click_category = request.form['click_category']
        if 'click_type' in request.form:
            click_type = request.form['click_type']
        else:
            click_type = 'None'
        if 'charges' in request.form:
            filters.update({'charges': False})
        filters.update({'min_level': request.form['level']})

        if click_category != 'All' and click_category != 'Pets' and click_type == 'None':
            flash('You must select a click type')
            return redirect(url_for('items.click_item_search'))

        data = item.get_click_items(click_category, click_type, **filters)
        return render_template('click_item_results.html', data=data)


@item_pages.route("/item/search", methods=['GET', 'POST'])
def item_fast_search():
    if request.method == 'GET':
        return render_template('item_fast_search.html')
    else:
        # Do some validation
        item_name = request.form.get('item_name')
        tradeskill = request.form.get('tradeskill')
        if tradeskill == 'none':
            tradeskill = None
        equippable = request.form.get('equippable')
        if equippable == 'none':
            equippable = None
        itype = request.form.get('itype')
        no_glamour = request.form.get('no_glamour')
        only_aug = request.form.get('only_aug')

        if len(item_name) > 50:
            flash('Search by name limited to 50 characters.')
            return redirect(url_for('item_fast_search'))
        if len(item_name) < 3:
            flash('Search by name requires at least 3 characters')
            return redirect(url_for('item_fast_search'))
        if not item_name.isascii():
            flash('Only ASCII characters are allowed.')
            return redirect(url_for('item_fast_search'))
        data = item.get_fast_item(item_name, tradeskill=tradeskill, equippable=equippable,
                                  itype=itype, no_glamours=no_glamour, only_aug=only_aug)
        return render_template('item_fast_search_result.html', data=data)


@item_pages.route("/item/detail/<int:item_id>")
def item_detail(item_id):
    data = logic.get_item_data(item_id, full=True)
    return render_template('item_detail.html', item=data, item_id=item_id)


@item_pages.route("/item/raw/<int:item_id>")
def item_raw(item_id):
    raw_data = item.get_item_raw_data(item_id)
    return render_template('raw_data.html', data=raw_data)
