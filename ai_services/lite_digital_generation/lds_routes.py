from flask import Blueprint, jsonify, request, render_template
from .lds_controllers import lds_dg_gen_ctr, lds_dg_single_ctr
from .import cities
from .lds_utils import upload_city, create_store, create_house, create_tree, create_lamp, get_city_statistics, ask_city, create_human, simulate_city


lds = Blueprint('lds', __name__, template_folder='templates', static_folder='static')

@lds.route('/city/dashboard/', methods=['GET', 'POST'])
def dashboard():
    return render_template('lds_index.html', cities=cities)

@lds.route('/lite/digital/GEN/', methods=['GET', 'POST'])
def lds_dg_gen():
    return lds_dg_gen_ctr()

@lds.route('/city/GEN/<city_id>/', methods=['GET'])
def lds_dg_single(city_id):
    return lds_dg_single_ctr(city_id)

@lds.route('/city/', methods=['GET'])
def get_all_cities():
    return jsonify(cities)

@lds.route('/city/<city_id>/', methods=['GET'])
def get_city(city_id):
    if city_id in cities:
        return jsonify(cities[city_id])
    else:
        return jsonify({"error": "City not found"})

@lds.route('/city/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        city_data = request.form.get('city_data')
        result = upload_city(city_data)
        return result

    return render_template('lds_upload_city.html')

@lds.route('/city/<city_id>/create_store/', methods=['POST'])
def post_create_store(city_id):
    store = create_store(city_id)
    if store:
        return jsonify(store)
    else:
        return "City not found"

@lds.route('/city/<city_id>/create_house/', methods=['POST'])
def post_create_house(city_id):
    house = create_house(city_id)
    if house:
        return jsonify(house)
    else:
        return "City not found"

@lds.route('/city/<city_id>/create_tree/', methods=['POST'])
def post_create_tree(city_id):
    tree = create_tree(city_id)
    if tree:
        return jsonify(tree)
    else:
        return "City not found"

@lds.route('/city/<city_id>/create_lamp/', methods=['POST'])
def post_create_lamp(city_id):
    lamp = create_lamp(city_id)
    if lamp:
        return jsonify(lamp)
    else:
        return "City not found"

@lds.route('/city/<city_id>/create_human/', methods=['POST'])
def post_create_human(city_id):
    human = create_human(city_id)
    if human:
        return jsonify(human)
    else:
        return "City not found"

@lds.route('/city/<city_id>/statistics/', methods=['GET'])
def city_statistics(city_id):
    if city_id in cities:
        # Get the city statistics
        statistics = get_city_statistics(city_id)
        return jsonify(statistics)
    else:
        # Return an error message in JSON format
        return jsonify({"error": "City not found"})

@lds.route('/city/<city_id>/geography/', methods=['GET'])
def city_geography(city_id):
    if city_id in cities:
        # Get the city statistics
        statistics = get_city_statistics(city_id)
        return jsonify(statistics)
    else:
        # Return an error message in JSON format
        return jsonify({"error": "City not found"})

@lds.route('/city/<city_id>/ask/', methods=['GET'])
def city_ask_response(city_id):
    query = request.args.get('query', '')
    if city_id in cities:
        # Get the city response based on the query
        response = ask_city(city_id, query)
        return jsonify(response)
    else:
        # Return an error message in JSON format
        return jsonify({"error": "City not found"})

@lds.route('/city/<city_id>/simulate/', methods=['GET'])
def city_simulate_response(city_id):
    query = request.args.get('query', '')
    if city_id in cities:
        # Get the city response based on the query
        response = simulate_city(city_id, query)
        return jsonify(response)
    else:
        # Return an error message in JSON format
        return jsonify({"error": "City not found"})



