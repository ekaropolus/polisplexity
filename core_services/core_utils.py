import os
ROOT_PATH = '/home/Admingania/portal_gain'
STATIC_DIR = 'static'
TEMPLATES_DIR = 'templates'
JS_DIR = os.path.join(STATIC_DIR ,'js')
CSS_DIR = os.path.join(STATIC_DIR ,'css')
DASH_DIR = 'dash'
AI_DIR = 'ai'

DIC_MDL = {'module': 'gtp_avatar', 'vertical':'ai_services', 'root_path' : ROOT_PATH }
DIC_DS = {'static': STATIC_DIR, 'templates': TEMPLATES_DIR, 'js': JS_DIR, 'css': CSS_DIR, 'dash': DASH_DIR, 'ai':AI_DIR }

DEV_MODULE = 'cdc_dev'
DEV_TEMPLATES_DIR =  'module_templates'
INIT_FILE_TEMPLATE = 'init_template.txt'
CORE = 'core_services'
INIT_FILE_NAME = '__init__.py'
PATH_TEMPLATE = os.path.join(ROOT_PATH, CORE,'templates',DEV_TEMPLATES_DIR)

def create_microservice():
    create_module()
    create_init()
    create_components('forms')
    create_components('utils')
    create_components('models')
    create_components('controllers')
    create_components('routes')


def create_module(dic_directories_structure=DIC_DS,dic_module=DIC_MDL):
    # Create the directory
    for key, value in dic_directories_structure.items():
        path = os.path.join(dic_module['root_path'], dic_module['vertical'], dic_module['module'],value)
        os.makedirs(path)

def create_init(dic_directories_structure=DIC_DS,dic_module=DIC_MDL):
    # Get the path to the template file
    path_template = PATH_TEMPLATE


    # Open the template file and read its contents
    try:
        with open(os.path.join(path_template, INIT_FILE_TEMPLATE), 'r') as f:
            code = f.read()
    except FileNotFoundError as e:
        error_dict = {
            "type": type(e).__name__,
            "message": str(e)
        }
        return error_dict

    # Replace placeholders in the code with actual values
    code = code.replace('#module_name', dic_module['module'])
    code = code.replace('#template_folder', dic_directories_structure['templates'])
    code = code.replace('#static_folder', dic_directories_structure['static'])

    # Get the path to the directory where the file will be created
    path = os.path.join(dic_module['root_path'], dic_module['vertical'], dic_module['module'])

    # Write the code to a file
    try:
        with open(os.path.join(path,INIT_FILE_NAME), 'w') as f:
            f.write(code)
    except IOError as e:
        error_dict = {
            "type": type(e).__name__,
            "message": str(e)
        }
        return error_dict

    # Return the path to the created file
    return os.path.join(path, INIT_FILE_NAME)


def create_components(name,dic_directories_structure=DIC_DS,dic_module=DIC_MDL):
    # Get the path to the template file
    path = os.path.join(dic_module['root_path'], dic_module['vertical'],dic_module['module'])

    code = ''
    code_file = dic_module['vertical'] + '_' + dic_module['module'] + '_' + name + '.py'
    # Write the code to a file
    try:
        with open(os.path.join(path,code_file), 'w') as f:
            f.write(code)
    except IOError as e:
        error_dict = {
            "type": type(e).__name__,
            "message": str(e)
        }
        return error_dict

    # Return the path to the created file
    return os.path.join(path, INIT_FILE_NAME)