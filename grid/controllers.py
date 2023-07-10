from flask import render_template, current_app
from . import services


def main_controller():
    with current_app.app_context():
        endpoint_list = []
        for rule in current_app.url_map.iter_rules():
            if rule.endpoint != 'static':
                endpoint_list.append(str(rule))

    return render_template('main/index.html', services = services, endpoint_list=endpoint_list)

