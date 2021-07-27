"""Routes"""

from datetime import datetime
import logging, platform
from os import error
from flask import (
    flash,
    sessions,
    url_for,
    render_template,
    redirect,
    request,
    session
)
from flask.logging import default_handler
from werkzeug.exceptions import BadRequest
from wtforms.validators import HostnameValidation

from app.app import app
from app.forms import PasswordForm, SignupForm, LoginForm
from app.registration import register_pass, register_user
from app.authorizations import auth_user
from app.users import User

timestamp = datetime.now().strftime('%H:%M')
date_timestamp = datetime.now().strftime('%m-%d %H:%M')
app_user = User() # User object for page access

@app.route('/authorized/<path:page>/')
def authorized(page):
    """Authorized Routes"""

    if app_user.is_updated():
        flash(app_user.get_update())
        app_user.clear_update()

    if app_user.is_authorized(): # ensure user authorized
        return render_template(
            '%s.html' % page,
            time = timestamp,
            auth_home=True,
            user = app_user.get_user()
        )
    
    # if user not authorized deny access
    raise BadRequest('User Not Authorized')

@app.route("/")
@app.route("/home")
def home():
    """Home/Landing"""
    return render_template(
        'common/home.html',
        time = timestamp,
        auth_home = False
    )

@app.route('/<path:page>')
def show(page):
    """Common Routes"""
    return render_template(
        '%s.html' % page,
        time = timestamp,
        user = app_user.get_user()
    )

# @app.route("/forms/login", defaults=['attempts'==0])
@app.route("/forms/login", methods=["GET", 'POST'])
def login():
    """Login form"""
    form = LoginForm()

    login_attempt = int(request.args.get('attempts')) if request.args.get('attempts') is not None else 3
    
    if form.validate_on_submit():
        # check user authorization
        if auth_user(request.form['username'], request.form['password']) is True:

            # ensure user authorized
            app_user.set_user(request.form['username'])
            app_user.authorize(True)

            # new authorized route
            return redirect(
                url_for(
                    'authorized',
                    page='authorized/auth_home',
                    user = app_user.get_user(),
                    category = 'message'
                )
            )

        # Logger Setup
        format_s = '[%(asctime)s] | IP Address: [{}] | Error: Failed Login Attempt'.format(request.remote_addr)
        logging.basicConfig( # logger config
            format = format_s, 
            filename = "logins.log", 
            level=logging.ERROR
        )
        formatter = logging.Formatter(format_s) # day/time format
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        app.logger.addHandler(streamHandler)

        # count login attempt
        login_attempt = login_attempt - 1

        if login_attempt == 0:
            flash('Too Many Login Attempts. Try Again Later', 'error')
        else:
            flash('Username or Password Incorrect', 'error')
        return redirect(url_for('login', attempts = login_attempt))

    return render_template(
        "forms/login.html",
        form=form,
        template="login",
        time = timestamp,
        user = app_user.get_user(),
        attempts = login_attempt,
        category = 'error'
    )

@app.route('/logout')
def logout():
    """Logout"""
    # downgrade User
    app_user.set_user('unregistered')
    app_user.authorize(False)
    return redirect(
        url_for(
            'home',
            user = app_user.get_user()
        )
    )

@app.route('/forms/signup', methods=["GET", "POST"])
def signup():
    """Signup form"""
    form = SignupForm()

    if form.validate_on_submit():

        # register new user data in database (csv)
        register_user(
            request.form['username'],
            request.form['password']
        )

        # authorize user
        app_user.set_user(request.form['username'])
        app_user.authorize(True)
        # user confirmation
        app_user.update(f'Signup Successful! Welcome {request.form["username"]}!')

        # redirect to authorized routes
        return redirect(
            url_for(
                'authorized',
                page='authorized/auth_home',
                user = app_user.get_user()
            )
        )

    return render_template(
        'forms/signup.html',
        form=form,
        template="signup",
        time = timestamp,
        user = app_user.get_user()
    )

@app.route('/authorized/forms/password', methods=["GET", "POST"])
def password():
    """Signup form"""
    form = PasswordForm()

    if form.validate_on_submit():
        if app_user.is_authorized():
            print('AUTHORIZED') # TODO: remove
            # register new password
            register_pass(
                app_user,
                request.form['new_password']
            )

            # user confirmation
            app_user.update('Password Updated Successfully!')

            # redirect home
            return redirect(
                url_for(
                    'authorized',
                    page='authorized/auth_home',
                    user = app_user.get_user()
                )
            )

    return render_template(
        'authorized/forms/password.html',
        form=form,
        template="password",
        time = timestamp,
        auth_home=True,
        user = app_user.get_user()
    )
