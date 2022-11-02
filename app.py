from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import simple_websocket
import eventlet
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, URL
from flask_socketio import SocketIO, emit, send
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat_app.db"
bootstrap = Bootstrap(app)
db = SQLAlchemy()
db.init_app(app)
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# users db table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


# messages db table
class MessageTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, unique=False, nullable=False)
    session_id = db.Column(db.String, unique=False, nullable=False)
    message = db.Column(db.String, unique=False, nullable=False)
    time = db.Column(db.String, unique=False, nullable=False)


active_user_list = []

# multiroom
# private messages
# create encoding to passwords





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def if_logged(form, field):     # validator for logged users
    if field.data in active_user_list:
        raise ValidationError('You are already logged, please check your session')

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), if_logged])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Submit')


#


@socketio.on("disconnect")
def user_disconnected():
    active_user_list.remove(current_user.username)
    logout_user()
    emit("list_of_active_users", active_user_list, broadcast=True)


@socketio.on("message")
def handle_message(msg):
    global active_user_list
    if msg == "User-has_connected" and current_user.username not in active_user_list:
        active_user_list.append(current_user.username)
        emit("list_of_active_users", active_user_list, broadcast=True)
        print(active_user_list)
    elif msg != "User-has_connected" and msg != "":
        message = {"user": current_user.username,
                   "session_id": request.sid,
                   "message": msg,
                   "time": str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
                   }
        message_to_database = MessageTable(user=message["user"], session_id=message["session_id"],
                                           message=message["message"], time=message["time"])
        db.session.add(message_to_database)
        db.session.commit()
        send(message, broadcast=True)


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('session', user_name=user.username))
    return render_template("login.html", form=form)


@app.route('/session', methods=['GET', "POST"])
@login_required
def session():
    return render_template('session.html', logged_user=current_user.username, active_user_list=active_user_list,
                           message_history=MessageTable.query.all())


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # socketio.run(app,debug=True, allow_unsafe_werkzeug=True)
