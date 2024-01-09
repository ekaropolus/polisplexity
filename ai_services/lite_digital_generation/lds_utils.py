import random
import uuid
from datetime import datetime
import json
from . import cities, replicate_api_key
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
from flask import jsonify

import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.language_models import CodeGenerationModel
from vertexai.preview.generative_models import GenerativeModel, Part

import math
import replicate
import os
import requests




def check_collision(position_x, position_z, objects):
    """Check if there is a collision between the given position and existing objects."""
    if not objects:  # If objects list is empty, no collision can occur
        return False

    for obj in objects:
        obj_pos_x = obj.get("position_x", 0)
        obj_pos_z = obj.get("position_z", 0)
        obj_width = obj.get("width", 0)
        obj_depth = obj.get("depth", 0)

        if (
            position_x + obj_width >= obj_pos_x and
            position_x <= obj_pos_x + obj_width and
            position_z + obj_depth >= obj_pos_z and
            position_z <= obj_pos_z + obj_depth
        ):
            return True

    return False

def generate_house(position_x, position_z, objects):
    """Generate a house dictionary with random attributes at a valid position."""
    height = random.uniform(15, 25)
    width = random.uniform(8, 12)
    depth = random.uniform(8, 12)
    color = "#ffcc99"  # Light orange color

    rotation_y = random.randint(0, 3) * 90  # Rotate 0, 90, 180, or 270 degrees
    status = random.choice(["good state", "maintenance", "no data"])
    if status == "maintenance":
        file = "models/house_mantainance.obj"
    elif status == "good state":
        file = "models/house_good.obj"
    else:
        file = ""

    house = {
        "id": str(uuid.uuid4()),
        "height": height,
        "width": width,
        "depth": depth,
        "color": color,
        "position_x": position_x,
        "position_y": 0,
        "position_z": position_z,
        "rotation_y": rotation_y,
        "status": status,
        "file": file,
    }

    return house

def generate_store(position_x, position_z, objects):
    """Generate a store dictionary with random attributes at a valid position."""
    height = random.uniform(30, 50)
    width = random.uniform(12, 20)
    depth = random.uniform(12, 20)
    color = "#999999"  # Gray color

    rotation_y = random.randint(0, 3) * 90  # Rotate 0, 90, 180, or 270 degrees
    status = random.choice(["good state", "maintenance", "no data"])
    file = ""
    store = {
        "id": str(uuid.uuid4()),
        "height": height,
        "width": width,
        "depth": depth,
        "color": color,
        "position_x": position_x,
        "position_y": 0,
        "position_z": position_z,
        "rotation_y": rotation_y,
        "status": status,
        "file": file,
    }

    return store

def generate_building(building_type, objects):
    """Generate a building dictionary with random attributes based on building type."""
    if building_type == "house":
        position_x = random.uniform(-50, 50)
        position_z = random.uniform(-50, 50)
        while check_collision(position_x, position_z, objects):
            position_x = random.uniform(-50, 50)
            position_z = random.uniform(-50, 50)
        building = generate_house(position_x, position_z, objects)
    else:
        position_x = random.uniform(-50, 50)
        position_z = random.uniform(-50, 50)
        while check_collision(position_x, position_z, objects):
            position_x = random.uniform(-50, 50)
            position_z = random.uniform(-50, 50)
        building = generate_store(position_x, position_z, objects)

    return building

def generate_lamp(position_x, position_z, objects):
    """Generate a lamp dictionary with random attributes at a valid position."""
    height = 4
    color = "#FFD700"  # Gold color
    status = random.choice(["good state", "maintenance", "no data"])

    lamp = {
        "id": str(uuid.uuid4()),
        "height": height,
        "color": color,
        "position_x": position_x,
        "position_y": 0,
        "position_z": position_z,
        "status": status,
    }

    return lamp

def generate_tree(position_x, position_z, objects):
    """Generate a tree dictionary with random attributes at a valid position."""
    height = 5
    radius_top = 1.5
    radius_bottom = 2.5
    color_trunk = "#8B4513"  # Brown color
    color_leaves = "#228B22"  # Green color

    status = random.choice(["good state", "maintenance", "no data"])

    tree = {
        "id": str(uuid.uuid4()),
        "height": height,
        "radius_top": radius_top,
        "radius_bottom": radius_bottom,
        "color_trunk": color_trunk,
        "color_leaves": color_leaves,
        "position_x": position_x,
        "position_y": 0,
        "position_z": position_z,
        "status": status,
    }

    return tree

def generate_human(position_x, position_z, objects):
    """Generate a human dictionary with random attributes at a valid position."""
    # Define human attributes here, e.g., scale, posture, color, etc.
    # For example:
    scale = [1, 1, 1]
    posture = "standing"
    color = "#FF0000"  # Red color

    status = random.choice(["healthy", "sick", "asleep", "mutated","Neo"])
    human_id = str(uuid.uuid4())
    if status == "mutated":
        file = "models/mutant.obj"
    elif status == "Neo":
        file = "models/" + create_neo_human(human_id)
    else:
        file = "models/human.obj"

    human = {
        "id": human_id,
        "scale": scale,
        "posture": posture,
        "color": color,
        "position_x": position_x,
        "position_y": 0,
        "position_z": position_z,
        "status": status,
        "file": file,
    }

    return human

def create_neo_human(human_id):

    download_directory = "/home/Admingania/portal_gain/ai_services/lite_digital_generation/static/models/"
    # Create a Replicate client instance
    client = replicate.Client(api_token=replicate_api_key)

    # Define the input data (prompt) for the Neo human
    input_data = {
        "prompt": "A human with Neo status",
        "save_mesh": True,
    }

    # Run the model to generate a Neo human mesh and get the generated file URL
    output = client.run(
        "cjwbw/shap-e:5957069d5c509126a73c7cb68abcddbb985aeefa4d318e7c63ec1352ce6da68c",
        input=input_data
    )

    # Extract the generated mesh URL from the output
    generated_mesh_url = output[1]

    # Download the OBJ mesh
    response = requests.get(generated_mesh_url)
    if response.status_code == 200:
        # Create the download directory if it doesn't exist
        os.makedirs(download_directory, exist_ok=True)

        # Extract the filename from the URL and save the mesh to the specified directory
        neo_human = "neo_" + human_id + ".obj"
        filename = os.path.join(download_directory, neo_human)
        with open(filename, "wb") as file:
            file.write(response.content)
        return neo_human
    else:
        return "human.obj"


def generate_city_random(app):
    num_buildings = random.randint(5, 45)
    num_lamps = random.randint(5, 45)
    num_trees = random.randint(5, 45)

    buildings = []
    lamps = []
    trees = []
    objects = []  # List of objects to check for collisions

    # Generate buildings
    for i in range(num_buildings):
        # Randomly choose between building types
        building_type = random.choice(["house", "store"])
        building = generate_building(building_type, objects)
        buildings.append(building)
        objects.append(building)

    # Generate lamps
    for i in range(num_lamps):
        position_x = random.uniform(-50, 50)
        position_z = random.uniform(-50, 50)
        while check_collision(position_x, position_z, objects):
            position_x = random.uniform(-50, 50)
            position_z = random.uniform(-50, 50)
        lamp = generate_lamp(position_x, position_z, objects)
        lamps.append(lamp)
        objects.append(lamp)

    # Generate trees
    for i in range(num_trees):
        position_x = random.uniform(-50, 50)
        position_z = random.uniform(-50, 50)
        while check_collision(position_x, position_z, objects):
            position_x = random.uniform(-50, 50)
            position_z = random.uniform(-50, 50)
        tree = generate_tree(position_x, position_z, objects)
        trees.append(tree)
        objects.append(tree)

    humans = []

    city_id = str(uuid.uuid4())
    current_datetime = datetime.now()

    cities[city_id] = {
        "buildings": buildings,
        "lamps": lamps,
        "trees": trees,
        "humans": humans,
    }

    app.db.cities.insert_one(cities[city_id])

    return city_id

def generate_default_city(app):
    """Generate a default city with one tree, one house, one building, and one lamp."""
    objects = []  # List of objects to check for collisions

    buildings = [generate_building("house", objects), generate_building("store", objects)]
    lamps = [generate_lamp(-10, -10, objects)]  # Specify fixed position
    trees = [generate_tree(10, 10, objects)]
    humans = [generate_human(-20, -20, objects)]

    # Generate a unique UUID for the city
    city_id = str(uuid.uuid4())

    # Get the current date and time
    current_datetime = datetime.now()

    # Save the default city to the global dictionary
    cities[city_id] = {
        "buildings": buildings,
        "lamps": lamps,
        "trees": trees,
        "humans": humans,
        #"datetime": current_datetime,
    }

    app.db.cities.insert_one(cities[city_id])

def upload_city(city_data):
    # Parse the city_data as JSON
    city_data = json.loads(city_data)

    # Extract the city_id from the parsed JSON keys
    city_id = list(city_data.keys())[0]

    # Get the current date and time
    current_datetime = datetime.now()

    # Add the city data to the global dictionary
    cities[city_id] = {
        "buildings": city_data[city_id].get("buildings", []),
        "lamps": city_data[city_id].get("lamps", []),
        "trees": city_data[city_id].get("trees", []),
        "humans": city_data[city_id].get("humans",[]),
        "datetime": current_datetime
    }

    return f"City {city_id} uploaded successfully!"

def create_house(city_id):
    """Create a house for the specified city ID."""
    city = cities.get(city_id)
    if city:
        # Initialize empty lists if certain elements don't exist
        buildings = city.get("buildings", [])
        lamps = city.get("lamps", [])
        trees = city.get("trees", [])
        humans = city.get("humans", [])

        # Combine all elements
        objects = buildings + lamps + trees + humans

        # Generate and append the new building
        building = generate_building("house", objects)
        buildings.append(building)

        # Update the city data
        city["buildings"] = buildings
        return building
    else:
        return None


def create_store(city_id):
    """Create a store for the specified city ID."""
    city = cities.get(city_id)
    if city:
        # Initialize empty lists if certain elements don't exist
        buildings = city.get("buildings", [])
        lamps = city.get("lamps", [])
        trees = city.get("trees", [])
        humans = city.get("humans", [])

        # Combine all elements
        objects = buildings + lamps + trees + humans

        # Generate and append the new store
        store = generate_store(random.uniform(-50, 50), random.uniform(-50, 50), objects)
        buildings.append(store)

        # Update the city data
        city["buildings"] = buildings
        return store
    else:
        return None


def create_lamp(city_id):
    """Create a lamp for the specified city ID."""
    city = cities.get(city_id)
    if city:
        # Initialize empty lists if certain elements don't exist
        buildings = city.get("buildings", [])
        lamps = city.get("lamps", [])
        trees = city.get("trees", [])
        humans = city.get("humans", [])

        # Combine all elements
        objects = buildings + lamps + trees + humans

        # Generate and append the new lamp
        lamp = generate_lamp(random.uniform(-50, 50), random.uniform(-50, 50), objects)
        lamps.append(lamp)

        # Update the city data
        city["lamps"] = lamps
        return lamp
    else:
        return None


def create_tree(city_id):
    """Create a tree for the specified city ID."""
    city = cities.get(city_id)
    if city:
        # Initialize empty lists if certain elements don't exist
        buildings = city.get("buildings", [])
        lamps = city.get("lamps", [])
        trees = city.get("trees", [])
        humans = city.get("humans", [])

        # Combine all elements
        objects = buildings + lamps + trees + humans

        # Generate and append the new tree
        tree = generate_tree(random.uniform(-50, 50), random.uniform(-50, 50), objects)
        trees.append(tree)

        # Update the city data
        city["trees"] = trees
        return tree
    else:
        return None


def create_human(city_id):
    """Create a human for the specified city ID."""
    city = cities.get(city_id)
    if city:
        # Initialize empty lists if certain elements don't exist
        buildings = city.get("buildings", [])
        lamps = city.get("lamps", [])
        trees = city.get("trees", [])
        humans = city.get("humans", [])

        # Combine all elements
        objects = buildings + lamps + trees + humans

        # Generate and append the new human
        human = generate_human(random.uniform(-50, 50), random.uniform(-50, 50), objects)
        humans.append(human)

        # Update the city data
        city["humans"] = humans
        return human
    else:
        return None


def calculate_distance(obj1, obj2):
    """Calculate the Euclidean distance between two objects."""
    x1, y1, z1 = obj1["position_x"], obj1["position_y"], obj1["position_z"]
    x2, y2, z2 = obj2["position_x"], obj2["position_y"], obj2["position_z"]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def get_city_statistics(city_id):
    city = cities.get(city_id)
    if city:
        buildings = city.get("buildings", [])
        lamps = city.get("lamps", [])
        trees = city.get("trees", [])
        humans = city.get("humans", [])

        buildings_count = len(buildings)
        stores = [b for b in buildings if b.get("type") == "store"]
        stores_count = len(stores)
        houses_count = sum(1 for b in buildings if b.get("type") == "house")
        lamps_count = len(lamps)
        trees_count = len(trees)

        building_heights = [b["height"] for b in buildings]
        building_widths = [b["width"] for b in buildings]
        building_depths = [b["depth"] for b in buildings]

        mean_building_height = sum(building_heights) / len(building_heights) if building_heights else 0
        mean_building_width = sum(building_widths) / len(building_widths) if building_widths else 0
        mean_building_depth = sum(building_depths) / len(building_depths) if building_depths else 0

        house_heights = [b["height"] for b in buildings if b.get("type") == "house"]
        house_widths = [b["width"] for b in buildings if b.get("type") == "house"]
        house_depths = [b["depth"] for b in buildings if b.get("type") == "house"]

        mean_house_height = sum(house_heights) / len(house_heights) if house_heights else 0
        mean_house_width = sum(house_widths) / len(house_widths) if house_widths else 0
        mean_house_depth = sum(house_depths) / len(house_depths) if house_depths else 0

        store_heights = [b["height"] for b in buildings if b.get("type") == "store"]
        store_widths = [b["width"] for b in buildings if b.get("type") == "store"]
        store_depths = [b["depth"] for b in buildings if b.get("type") == "store"]

        mean_store_height = sum(store_heights) / len(store_heights) if store_heights else 0
        mean_store_width = sum(store_widths) / len(store_widths) if store_widths else 0
        mean_store_depth = sum(store_depths) / len(store_depths) if store_depths else 0

        if buildings:
            x_positions = [b["position_x"] for b in buildings]
            y_positions = [b["position_y"] for b in buildings]
            z_positions = [b["position_z"] for b in buildings]

            min_x = min(x_positions)
            max_x = max(x_positions)
            min_y = min(y_positions)
            max_y = max(y_positions)
            min_z = min(z_positions)
            max_z = max(z_positions)

            block_size_x = max_x - min_x
            block_size_y = max_y - min_y
            block_size_z = max_z - min_z

            terrain_occupancy = block_size_x * block_size_y * block_size_z
        else:
            block_size_x = block_size_y = block_size_z = terrain_occupancy = 0


        trees_heights = [t["height"] for t in trees]
        lamps_heights = [l["height"] for l in lamps]

        mean_tree_height = sum(trees_heights) / len(trees_heights) if trees_heights else 0
        mean_lamp_height = sum(lamps_heights) / len(lamps_heights) if lamps_heights else 0

        lamps_closeness = 0
        trees_closeness = 0
        stores_closeness = 0
        houses_closeness = 0
        buildings_closeness = 0


        # Calculate lamps closeness
        if lamps_count > 1:
            total_distance = sum(calculate_distance(l1, l2) for i, l1 in enumerate(lamps) for l2 in lamps[i+1:])
            lamps_closeness = total_distance / (lamps_count * (lamps_count - 1) / 2)

        if trees_count > 1:
            total_distance = sum(calculate_distance(t1, t2) for i, t1 in enumerate(trees) for t2 in trees[i+1:])
            trees_closeness = total_distance / (trees_count * (trees_count - 1) / 2)

        # Calculate stores closeness
        if stores_count > 1:
            stores = [b for b in buildings if b.get("type") == "store"]
            total_distance = sum(calculate_distance(s1, s2) for i, s1 in enumerate(stores) for s2 in stores[i+1:])
            stores_closeness = total_distance / (stores_count * (stores_count - 1) / 2)

        # Calculate houses closeness
        if houses_count > 1:
            houses = [b for b in buildings if b.get("type") == "house"]
            total_distance = sum(calculate_distance(h1, h2) for i, h1 in enumerate(houses) for h2 in houses[i+1:])
            houses_closeness = total_distance / (houses_count * (houses_count - 1) / 2)

        # Calculate buildings closeness
        if buildings_count > 1:
            total_distance = sum(calculate_distance(b1, b2) for i, b1 in enumerate(buildings) for b2 in buildings[i+1:])
            buildings_closeness = total_distance / (buildings_count * (buildings_count - 1) / 2)

        buildings_status_summary = {}
        lamps_status_summary = {}
        trees_status_summary = {}
        houses_status_summary = {}
        stores_status_summary = {}

        stores = [b for b in buildings if b.get("type") == "store"]
        houses = [b for b in buildings if b.get("type") == "house"]

        for building in buildings:
            status = building.get("status")
            if status in buildings_status_summary:
                buildings_status_summary[status] += 1
            else:
                buildings_status_summary[status] = 1

        for lamp in lamps:
            status = lamp.get("status")
            if status in lamps_status_summary:
                lamps_status_summary[status] += 1
            else:
                lamps_status_summary[status] = 1

        for tree in trees:
            status = tree.get("status")
            if status in trees_status_summary:
                trees_status_summary[status] += 1
            else:
                trees_status_summary[status] = 1

        for house in houses:
            status = house.get("status")
            if status in houses_status_summary:
                houses_status_summary[status] += 1
            else:
                houses_status_summary[status] = 1

        for store in stores:
            status = store.get("status")
            if status in stores_status_summary:
                stores_status_summary[status] += 1
            else:
                stores_status_summary[status] = 1

        status_summary = {
            "buildings": buildings_status_summary,
            "lamps": lamps_status_summary,
            "trees": trees_status_summary,
            "houses": houses_status_summary,
            "stores": stores_status_summary
        }

        statistics = {
            "houses": houses_count,
            "stores": stores_count,
            "lamps": lamps_count,
            "trees": trees_count,
            "status_summary": status_summary,
            "block_size_x": block_size_x,
            "block_size_y": block_size_y,
            "block_size_z": block_size_z,
            "terrain_occupancy": terrain_occupancy,
            "mean_tree_height": mean_tree_height,
            "mean_lamp_height": mean_lamp_height,
            "mean_building_height": mean_building_height,
            "mean_building_width": mean_building_width,
            "mean_building_depth": mean_building_depth,
            "mean_house_height": mean_house_height,
            "mean_house_width": mean_house_width,
            "mean_house_depth": mean_house_depth,
            "mean_store_height": mean_store_height,
            "mean_store_width": mean_store_width,
            "mean_store_depth": mean_store_depth,
            "lamps_closeness": lamps_closeness,
            "trees_closeness": trees_closeness,
            "stores_closeness": stores_closeness,
            "houses_closeness": houses_closeness,
            "buildings_closeness": buildings_closeness
        }

        return statistics
    else:
        return None


def initialize_api():
    json_credentials = "/home/Admingania/portal_gain/ai_services/lite_digital_generation/static/credentials/vivid-env-392205-8d28ffaba58a.json"
    with open(json_credentials) as f:
        service_account_info = json.load(f)
    my_credentials = service_account.Credentials.from_service_account_info(service_account_info)
    aiplatform.init(credentials=my_credentials)
    vertexai.init(project=service_account_info["project_id"], location="us-central1")

def ask_city_bison(city_id, query):
    initialize_api()
    city_statistics = get_city_statistics(city_id)
    text_prompt = f"This are the statistic of the city:\n{city_statistics}\n\nAnswer this question about the city: {query}"
    model = TextGenerationModel.from_pretrained("text-bison@001")
    parameters = {"temperature": 1, "max_output_tokens": 1028, "top_p": 0.8, "top_k": 40}
    response = model.predict(text_prompt, **parameters)
    return response.text

def ask_city_gemini(city_id, query):
    initialize_api()
    city_statistics = get_city_statistics(city_id)
    text_prompt = f"This are the statistic of the city:\n{city_statistics}\n\nAnswer this question about the city: {query}"
    config = {"temperature": 1, "max_output_tokens": 256, "top_p": 0.8, "top_k": 40}
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(text_prompt, generation_config=config)
    return response.candidates[0].content.parts[0].text

def ask_city(city_id, query):
    return ask_city_gemini(city_id, query)

def generate_code_with_bison(city_statistics, query):
    text_prompt = f"This are the statistic of the city:\n{city_statistics}\n\nCreate a program using simpy in python to simulate and resolve this inquiry: {query}"
    parameters = {"temperature": 0.2, "max_output_tokens": 8192}
    model = CodeGenerationModel.from_pretrained("code-bison-32k")
    response = model.predict(text_prompt, **parameters)
    return response.text

def refine_code_with_huggingface(code):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stablecode-completion-alpha-3b-4k"
    headers = {"Authorization": "Bearer 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"}
    payload = {"inputs": code, "parameters": {"max_new_tokens": 100}}
    response = requests.post(API_URL, headers=headers, json=payload).json()
    return response

def simulate_city(city_id, query):
    initialize_api()
    city_statistics = get_city_statistics(city_id)

    # Generate initial code with Bison AI model
    bison_response = generate_code_with_bison(city_statistics, query)

    # # Refine the code with Hugging Face API
    # hf_response = refine_code_with_huggingface(bison_response)

    # # Handle the response
    # if "error" in hf_response:
    #     return bison_response  # Return original response if there's an error
    # else:
    #     return hf_response  # Return refined response

    return bison_response.text


def create_generative_object(city_id, prompt):
    """Create a generative object for the specified city ID."""
    city = cities.get(city_id)
    if not city:
        return None

    objects = city.get("buildings", []) + city.get("lamps", []) + city.get("trees", []) + city.get("humans", [])
    human = generate_generative(random.uniform(-50, 50), random.uniform(-50, 50), objects, prompt)
    city.setdefault("humans", []).append(human)
    return human

def generate_generative(position_x, position_z, objects, prompt):
    """Generate a human dictionary with random attributes at a valid position."""
    human_id = str(uuid.uuid4())
    file = download_model_mesh(human_id, prompt)
    return {
        "id": human_id,
        "scale": [1, 1, 1],
        "posture": "standing",
        "color": "#FF0000",
        "position_x": position_x,
        "position_y": 0,
        "position_z": position_z,
        "status": random.choice(["healthy", "sick", "asleep", "mutated", "Neo"]),
        "file": file,
    }

def download_model_mesh(human_id, prompt):
    download_directory = "/home/Admingania/portal_gain/ai_services/lite_digital_generation/static/models/"
    client = replicate.Client(api_token=replicate_api_key)
    input_data = {"prompt": prompt, "save_mesh": True}
    output = client.run("cjwbw/shap-e:5957069d5c509126a73c7cb68abcddbb985aeefa4d318e7c63ec1352ce6da68c", input=input_data)
    generated_mesh_url = output[1]
    response = requests.get(generated_mesh_url)
    if response.status_code != 200:
        return "human.obj"
    os.makedirs(download_directory, exist_ok=True)
    neo_human = f"generative_{human_id}.obj"
    filename = os.path.join(download_directory, neo_human)
    with open(filename, "wb") as file:
        file.write(response.content)
    return neo_human

def generative_city_gemini(city_id, query):
    initialize_api()
    city_statistics = get_city_statistics(city_id)
    text_prompt = f"This are the statistic of the city:\n{city_statistics}\n\nAccording to the statistics, define a new object that the city needs in 4 words based on the: {query}"
    config = {"temperature": 1, "max_output_tokens": 100, "top_p": 0.8, "top_k": 40}
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(text_prompt, generation_config=config)
    prompt = response.candidates[0].content.parts[0].text
    create_generative_object(city_id, prompt)
    return prompt


def generative_city(city_id, query):
    return generative_city_gemini(city_id, query)


