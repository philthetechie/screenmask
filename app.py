from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request
from flask import redirect
from threading import Thread
import pystache
import RPi.GPIO as GPIO
import time
from config import config

GPIO.setmode(GPIO.BCM)

for pin in config['gpio_pins']:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, True)


app = Flask(__name__,  static_folder ='static')
mysql_string = f"{sql_credentials}/{sql_db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = mysql_string
# Increase performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def reset_curtain():
    t1 = Thread(target=roll_roller, args=('top', 'up', 6))
    t2 = Thread(target=roll_roller, args=('bottom', 'down', 6))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    return

def roll_roller(roller, direction, delay):
    # Ensure only one program can run at once per roller.
    lock = db.session.query(Lock).filter(Lock.roller == roller).first()
    if lock.lock == 1:
        return False
    lock.lock = 1
    db.session.commit()

    delay = float(delay)

    # Choose pins
    pinout = config['pinout']
    try:
        pins = [pinout[roller][direction], pinout[roller]["power"]]
    except:
        return False

    GPIO.output(pins[0], False)
    time.sleep(0.1)
    GPIO.output(pins[1], False)
    time.sleep(delay)
    GPIO.output(pins[1], True)
    time.sleep(0.1)
    GPIO.output(pins[0], True)
    
    # Unlock the lock
    lock.lock = 0
    db.session.commit()

    return True

# MODELS
class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(80))
    top = db.Column(db.Float)
    bottom = db.Column(db.Float)
    def __init__(self, identifier, top, bottom):
        self.identifier = identifier
        self.top=top
        self.bottom = bottom
        self.id = id

    def __repr__(self):
        return '<Program %r>' % self.identifier
        
# MODELS
class Lock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roller = db.Column(db.String(25))
    lock = db.Column(db.Integer)
    def __init__(self, id, roller, lock):
        self.id = id
        self.roller = roller
        self.lock=lock

    def __repr__(self):
        return '<Lock %r>' % self.id


def render(template, data={}):
    return pystache.render(
        open("templates/%s.html" % template).read(),
        data)


@app.route('/', methods=['get', 'post'])
def index():
    programs = db.session.query(Program).all()
    response = {
        'programs':
        [{'id': x.id, 'identifier': x.identifier} for x in programs]
    }
    return render('index', response)


@app.route('/manual_control', methods=['get', 'post'])
def manual_control():
    response ={}
    return render('manual', response)

@app.route('/settings', methods=['get', 'post'])
def settings():

    if 'action' in request.form and request.form['action'] == 'delete':
        prog = db.session.query(Program).filter(Program.id == request.form['program_id']).first()
        if prog:
            db.session.delete(prog)
            db.session.commit()
    programs = db.session.query(Program).all()
    response = {
        'programs':
        [{'id': x.id, 'identifier': x.identifier} for x in programs]
    }

    return render('settings', response)


@app.route('/new_program', methods=['get', 'post'])
def new_program():
    if 'action' in request.form and request.form['action'] == 'save':
        program=Program(
            identifier=request.form['identifier'],
            top=request.form['topcounter'],
            bottom=request.form['bottomcounter']
        )
        db.session.add(program)
        db.session.commit()
        return redirect("/", code=302)

    return render('new_program', {})


@app.route('/trigger_curtain', methods=['get', 'post'])
def trigger_curtain():
    if request.form['action'] == 'push_direction':
        roller = request.form['roller']
        direction = request.form['direction']
        time = request.form['time']
        success = roll_roller(roller, direction, time)
        return jsonify({
            'success':success, 'roller': roller,
            'direction': direction, 'time': time
        })

    return jsonify({'success': False})


@app.route('/runprogram', methods=['get', 'post'])
def runprogram():
    if 'id' in request.form:
        prog = db.session.query(Program).filter(
            Program.id == request.form['id']
        ).first()
        if prog:
            t1 = Thread(target=roll_roller, args=('top', 'down', prog.top))
            t2 = Thread(target=roll_roller, args=('bottom', 'up', prog.bottom))

            t1.start()
            t2.start()

            return jsonify({'success': True})
    return jsonify({'success': False})


@app.route('/reset', methods=['get', 'post'])
def reset():
    reset_curtain()
    return redirect("/", code=302)


if __name__ == '__main__':
    # Reset lock files on bootup
    for lock in db.session.query(Lock).all():
        lock.lock = 0
        db.session.commit()

    app.run(port=80, host='0.0.0.0', processes=10)


#db.create_all() # In case table doesn't exist already.