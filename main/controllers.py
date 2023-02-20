from flask import render_template


def main_controller():
    return render_template('main/index.html')