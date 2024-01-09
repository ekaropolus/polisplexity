from flask import render_template, current_app
from .lds_utils import generate_city_random, generate_default_city
from . import cities

def lds_dg_gen_ctr():
    """
    Generate a city with buildings, lamps, and trees for visualization and save it to the global dictionary.

    Returns:
        str: The rendered template for displaying the generated city.
    """
    if not cities:
        generate_default_city(current_app)
        city_id = list(cities.keys())[0]
        city_data = cities[city_id]
    else:
        city_id = generate_city_random(current_app)
        # Retrieve the city data from the global dictionary excluding the datetime
        city_data = cities[city_id]
    return "city_data"


def lds_dg_single_ctr(city_id):
    """
    Retrieve the city data for a specific city ID from the global dictionary.

    Args:
        city_id (str): The ID of the city to retrieve data for.

    Returns:
        str: The rendered template for displaying the city data, or an error message if the city ID does not exist.
    """
    if city_id in cities:
        # Retrieve the city data from the global dictionary excluding the datetime
        city_data = cities[city_id]
        return render_template('lds_city_vr.html', city_data=city_data)
    else:
        return "City not found"
