from flask import Blueprint, Response
from .ai_services_aith_controllers import aith_controller
from .ai_services_aith_utils import gen_frames

aith = Blueprint('aith',__name__, template_folder='templates', static_folder='static')

@aith.route('/video/SECURITY/', methods = ['GET', 'POST'])
def aith_home():
    return aith_controller()


@aith.route('/video/SECURITY/video_feed/', methods = ['GET', 'POST'])
def video_feed():
       return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')