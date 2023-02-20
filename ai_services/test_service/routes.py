from flask import Blueprint, render_template

test_service = Blueprint('test_service',__name__)

@test_service.route('/test_service/')
def test_service_route():
    return render_template('ai_services/test_service/test_service_view.html')
