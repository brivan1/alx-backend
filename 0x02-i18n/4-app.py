#!/usr/bin/env python3
'''
flask babel module
'''
from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    '''
    config class
    '''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale():
    '''
    get and return best match locale
    '''
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        print(locale)
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/")
def index():
    '''
    root route
    '''
    return render_template("3-index.html")


if __name__ == "__main__":
    app.run(port='5000', host='0.0.0.0', debug=True)
