#!/usr/bin/env python3
'''
flask babel module
'''
from flask import Flask, render_template, request, g
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

    if g.user:
        locale = g.user.get("locale")
        if locale and locale in app.config["LANGUAGES"]:
            return locale

    locale = request.headers.get("locale", None)
    if locale in app.config["LANGUAGES"]:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    '''
    return a dict or None
    '''
    login_id = request.args.get("login_as")
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request():
    '''
    set up user
    '''
    user = get_user()
    g.user = user


@app.route("/")
def index():
    '''
    root route
    '''
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(port='5000', host='0.0.0.0', debug=True)
