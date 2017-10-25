"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    # Get drop down menu brevet distance
    dist = request.args.get('dist')
    # Get beginning time/date and convert to ISO
    begin_time_base = request.args.get('time')
    begin_time_split = begin_time_base.split(":")

    # Scratch together an isoformat for acp_times to process
    begin_date_base = request.args.get('date') + "-" + begin_time_split[0] + "-" + begin_time_split[1]
    begin_date_arrow = arrow.get(begin_date_base, "YYYY-MM-DD-HH-mm")
    begin_date_iso = begin_date_arrow.isoformat()
    
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    
    open_time = acp_times.open_time(km, dist, begin_date_iso)
    close_time = acp_times.close_time(km, dist, begin_date_iso)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
