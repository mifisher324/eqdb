from flask import Blueprint, render_template

import zone

zone_pages = Blueprint('zones', __name__, template_folder='templates')


@zone_pages.route("/zone/detail/<int:zone_id>")
def zone_detail(zone_id):
    return render_template('zone_detail.html', data=zone.get_zone_detail(zone_id))


@zone_pages.route("/zone/listing")
def zone_listing():
    return render_template('zone_listing.html', data=zone.get_zone_listing())


@zone_pages.route("/zone/waypoint/listing")
def waypoint_listing():
    return render_template('waypoint_listing.html', data=zone.waypoint_listing())
