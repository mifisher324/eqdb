from sqlalchemy import and_
from sqlalchemy.orm import Session

import utils
from logic import TradeskillRecipe, engine, TradeskillRecipeEntries, Item, expansion


def get_tradeskill_detail(ts_id):
    excl_list = utils.get_exclusion_list('tradeskill')
    if ts_id in excl_list:
        return None
    # Get the tradeskill base details
    base_data = {}
    with Session(bind=engine) as session:
        args = [TradeskillRecipe.name, TradeskillRecipe.tradeskill, TradeskillRecipe.skillneeded,
                TradeskillRecipe.trivial, TradeskillRecipe.nofail, TradeskillRecipe.replace_container,
                TradeskillRecipe.must_learn, TradeskillRecipe.enabled, TradeskillRecipe.min_expansion]
        query = session.query(*args).filter(TradeskillRecipe.id == ts_id)
        result = query.first()
    if not result:
        return None

    base_data.update({'name': result[0],
                      'skill': utils.parse_skill(result[1]),
                      'required': result[2],
                      'trivial': result[3],
                      'no_fail': result[4],
                      'replace_container': result[5],
                      'must_learn': result[6],
                      'enabled': result[7],
                      'min_expansion': result[8],
                      'expansion': expansion})

    # Get the items involved in making the recipe
    with Session(bind=engine) as session:
        args = [TradeskillRecipeEntries.item_id, Item.Name, TradeskillRecipeEntries.successcount,
                TradeskillRecipeEntries.failcount, TradeskillRecipeEntries.componentcount, Item.icon]
        query = session.query(*args).filter(TradeskillRecipeEntries.recipe_id == ts_id).\
            filter(TradeskillRecipeEntries.iscontainer <= 0).\
            filter(TradeskillRecipeEntries.item_id == Item.id)
        result = query.all()

    components = []
    success = []
    fail = []
    for entry in result:
        item_id = entry[0]
        item_name = entry[1]
        successcount = entry[2]
        failcount = entry[3]
        componentcount = entry[4]
        icon = entry[5]

        if successcount > 0:
            success.append({'item_id': item_id,
                            'item_name': item_name,
                            'count': successcount,
                            'icon': icon})
        if failcount > 0:
            fail.append({'item_id': item_id,
                         'item_name': item_name,
                         'count': failcount,
                         'icon': icon})
        if componentcount > 0:
            components.append({'item_id': item_id,
                               'item_name': item_name,
                               'count': componentcount,
                               'icon': icon})
    base_data.update({'components': components,
                      'success': success,
                      'fail': fail})

    # Get the containers
    containers = []
    with Session(bind=engine) as session:
        query = session.query(TradeskillRecipeEntries.item_id, TradeskillRecipeEntries.iscontainer).\
            filter(TradeskillRecipeEntries.recipe_id == ts_id).\
            filter(TradeskillRecipeEntries.iscontainer >= 1)
        result = query.all()

    for entry in result:
        try:
            containers.append({'container_type': utils.get_object_type(entry[0])})
        except NotImplementedError:
            with Session(bind=engine) as session:
                query = session.query(Item.Name).filter(Item.id == entry[0])
                sub_result = query.one()
            containers.append({'container_type': sub_result[0]})
    base_data.update({'containers': containers})

    return base_data


def get_tradeskills(name=None, trivial=None, tradeskill=None, remove_no_fail=False, trivial_min=None):
    filters = [TradeskillRecipe.enabled == 1]
    if name:
        partial = "%%%s%%" % name
        filters.append(TradeskillRecipe.name.like(partial))
    if trivial:
        filters.append(TradeskillRecipe.trivial <= int(trivial))
    if trivial_min:
        filters.append(TradeskillRecipe.trivial >= int(trivial_min))
    if tradeskill:
        filters.append(TradeskillRecipe.tradeskill == tradeskill)
    if remove_no_fail:
        filters.append(TradeskillRecipe.nofail != 1)

    params = and_(*filters)
    with Session(bind=engine) as session:
        query = session.query(TradeskillRecipe.id, TradeskillRecipe.name, TradeskillRecipe.trivial).filter(params)
        result = query.all()

    out_data = []
    for entry in result:
        excl_list = utils.get_exclusion_list('tradeskill')
        if entry[0] in excl_list:
            continue
        out_data.append({'ts_id': entry[0],
                         'ts_name': entry[1],
                         'trivial': entry[2]})
    return out_data


def get_tradeskill_json(ts_id=None, ts_name=None):
    excl_list = utils.get_exclusion_list('tradeskill')
    if ts_id in excl_list:
        return []
    with Session(bind=engine) as session:
        if ts_id:
            query = session.query(TradeskillRecipe).filter(TradeskillRecipe.id == ts_id)
            result = query.one()
            if not result:
                return {}
            ret_dict = result.__dict__
            ret_dict.pop('_sa_instance_state')
            query = session.query(TradeskillRecipeEntries).filter(TradeskillRecipeEntries.recipe_id == ts_id)
            result = query.all()
            entries = []
            for entry in result:
                entry = entry.__dict__
                entry.pop('_sa_instance_state')
                entries.append(entry)
            ret_dict.update({'tradeskill_entries': entries})
            return ret_dict
        else:
            query = session.query(TradeskillRecipe).filter(TradeskillRecipe.name.like('%%%s%%' % ts_name))
            result = query.limit(50).all()
            if not result:
                return {}
            ret_list = []
            for entry in result:
                entry = entry.__dict__
                entry.pop('_sa_instance_state')
                if entry['id'] in excl_list:
                    continue
                ret_dict = entry
                query = session.query(TradeskillRecipeEntries).\
                    filter(TradeskillRecipeEntries.recipe_id == ret_dict['id'])
                sub_result = query.all()
                entries = []
                for sub_entry in sub_result:
                    sub_entry = sub_entry.__dict__
                    sub_entry.pop('_sa_instance_state')
                    entries.append(sub_entry)
                ret_dict.update({'tradeskill_entries': entries})
                ret_list.append(ret_dict)
            return ret_list
