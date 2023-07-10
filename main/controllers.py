from flask import render_template, current_app
from . import services, creation_steps
import random


def main_controller():
    with current_app.app_context():
        endpoint_list = []
        for rule in current_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                endpoint_list.append(str(rule))

    # Convert services dictionary to a list of tuples
    service_list = list(services.items())

    # Shuffle the service list randomly
    random.shuffle(service_list)

    # Convert the shuffled list back to a dictionary
    shuffled_services = dict(service_list)

    return render_template('main/index.html', services = shuffled_services, endpoint_list=endpoint_list, creation_steps=creation_steps)

