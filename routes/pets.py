from flask import Blueprint, render_template

import pets

pet_pages = Blueprint('pets', __name__, template_folder='templates')


@pet_pages.route("/pet/listing/<int:class_id>", methods=['GET'])
def pet_listing_result(class_id):
    data, game_class = pets.get_all_class_pets(class_id)
    return render_template('pet_listing_result.html', data=data, g_class=game_class)


@pet_pages.route("/pet/listing", methods=['GET'])
def pet_listing():
    return render_template('pet_listing.html')


@pet_pages.route("/pet/detail/<pet_sum_name>")
def pet_detail(pet_sum_name):
    data = pets.get_pet_data(pet_sum_name)
    return render_template('pet_detail.html', data=data)
