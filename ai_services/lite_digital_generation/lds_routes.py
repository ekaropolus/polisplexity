from flask import Blueprint, jsonify, request, render_template, current_app, url_for
from .lds_controllers import lds_dg_gen_ctr, lds_dg_single_ctr
from .import cities
from .lds_utils import upload_city, create_store, create_house, create_tree, create_lamp, get_city_statistics, ask_city, create_human, simulate_city, generative_city
from .lds_gen_image import upload_image_util
from bson import ObjectId  # Import ObjectId from bson



lds = Blueprint('lds', __name__, template_folder='templates', static_folder='static', static_url_path='/static/')




@lds.route('/city/<city_id>/image/ai_ask/', methods=['POST'])
def upload_image_route(city_id):
    return upload_image_util(request,city_id)

@lds.route('/city/dashboard/', methods=['GET', 'POST'])
def dashboard():
    # Retrieve only the '_id' field from each document
    mongo_cities = list(current_app.db.cities.find({}, {'_id': 1}))
    # Convert each ObjectId to a string
    city_ids = [str(document['_id']) for document in mongo_cities]
    return render_template('lds_index.html', cities=city_ids)

@lds.route('/city/create/', methods=['POST'])
def lds_dg_gen():
    return jsonify(lds_dg_gen_ctr())

@lds.route('/city/GEN/<city_id>/', methods=['GET'])
def lds_dg_single(city_id):
    return lds_dg_single_ctr(city_id)

@lds.route('/city/get/mongo/cities/', methods=['GET'])
def get_all_cities_mongo():
    mongo_cities = list(current_app.db.cities.find({}))
    mongo_cities = [jsonify_dict(document) for document in mongo_cities]
    return jsonify(mongo_cities)

@lds.route('/city/get/mongo/cities/ids/', methods=['GET'])
def get_all_cities_ids_mongo():
    # Retrieve only the '_id' field from each document
    mongo_cities = list(current_app.db.cities.find({}, {'_id': 1}))
    # Convert each ObjectId to a string
    city_ids = [str(document['_id']) for document in mongo_cities]
    return jsonify(city_ids)

@lds.route('/city/get/mongo/city/<string:city_id>/', methods=['GET'])
def get_city_info_mongo(city_id):
    try:
        # Convert the city_id string to ObjectId
        city_object_id = ObjectId(city_id)

        # Query the MongoDB 'cities' collection using the ObjectId
        city_data = current_app.db.cities.find_one({"_id": city_object_id})

        if city_data is None:
            # If the city with the specified ObjectId is not found, return a 404 Not Found response
            return jsonify({"error": "City not found"}), 404

        # Assuming you have a `jsonify_dict` function to serialize the MongoDB document
        city_info = jsonify_dict(city_data)

        return jsonify(city_info)
    except ObjectId.InvalidId:
        # If the provided city_id is not a valid ObjectId, return a 400 Bad Request response
        return jsonify({"error": "Invalid city ID format"}), 400

@lds.route('/city/set/mongo/city/<string:city_id>/', methods=['GET'])
def set_city_from_mongo(city_id):
    # Query the MongoDB 'cities' collection for the specified city_id
    city_data = current_app.db.cities.find_one({"_id": ObjectId(city_id)})

    if city_data is None:
        # If the city with the specified ObjectId is not found, return a 404 Not Found response
        return jsonify({"error": "City not found in MongoDB"}), 404

    # Clear the existing cities global dictionary
    global cities
    cities.clear()

    # Set the retrieved city into the cities global dictionary
    cities[city_id] = jsonify_dict(city_data)

    return jsonify({"message": "City set successfully"})


# Function to convert ObjectId to string in a dictionary
def jsonify_dict(d):
    for key, value in d.items():
        if isinstance(value, ObjectId):
            d[key] = str(value)
    return d

@lds.route('/city/get/local/cities/', methods=['GET'])
def get_all_cities_local():
    print(cities)
    return "there are cities"

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

@lds.route('/city/<city_id>/generative/', methods=['GET'])
def city_generative_response(city_id):
    query = request.args.get('query', '')
    if city_id in cities:
        # Get the city response based on the query
        response = generative_city(city_id, query)
        return jsonify(response)
    else:
        # Return an error message in JSON format
        return jsonify({"error": "City not found"})

