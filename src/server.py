"""Components for running the raspberry pi in server mode

    Checks whether running on real Raspberry PI
    Only tries to command the servo if so.
    If not, just logs what the fraction of travel was.

"""

import os
import logging
from flask import Flask, jsonify, request
from utils import is_raspberrypi

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
on_pi = is_raspberrypi()

logging.info(f'Starting servo server, on_py = {on_pi}')

app = Flask(__name__)
if on_pi:
    from servo_controller import ServoController
    sc = ServoController()


@app.route('/')
def index():
    """API index route"""
    return jsonify({'status': 'ok'})


@app.route('/servo/')
def alarm():
    """Turn on the relay"""
    fraction = request.args.get('f')

    if not fraction:
        ret_status = 'no f'
    else:
        try:
            f_fraction = float(fraction)
            if (f_fraction < 0) or (f_fraction > 1.0):
                ret_status = 'f out of range [0, 1.0]'
            else:
                ret_status = f'f={f_fraction:4.2f}'
                if on_pi:
                    sc.set_servo_fraction(f_fraction)
                else:
                    logging.info(f'on_pi={on_pi}, set travel {f_fraction:4.2f}%')
        except ValueError:
            ret_status = 'non-numeric f'

    return jsonify({'status': ret_status})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
