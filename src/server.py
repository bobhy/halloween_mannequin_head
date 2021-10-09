"""Components for running the raspberry pi in server mode

    Checks whether running on real Raspberry PI
    Only tries to command the servo if so.
    If not, just logs what the percentage was.

    bugbug: need some range checking on percentage.  What if it's < 0 or > 100?
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
    percentage = request.args.get('p')

    if not percentage:
        ret_status = 'no p'
    else:
        try:
            f_pct = float(percentage)
            if (f_pct < 0) or (f_pct > 100):
                ret_status = 'p out of range [0,100]'
            else:
                ret_status = f'p={f_pct:5.2f}'
                if on_pi:
                    sc.set_servo_percent(f_pct)
                else:
                    logging.info(f'on_pi={on_pi}, set position {f_pct:5.2f}%')
        except ValueError:
            ret_status = 'non-numeric p'

    return jsonify({'status': ret_status})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', '8000')))
