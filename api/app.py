from flask import json, request, Flask
import toolz
from helper import *
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import os
import logging

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

app = Flask(__name__)

metrics = GunicornPrometheusMetrics(app)


def update_data():
    logging.info("Updating Repo")
    pull_new_data()
    logging.info("Repo Updated")
    global data
    data = update_dictionary(lockout_config_path)
    logging.info("Data Updated")


@app.route("/hook", methods=["POST"])
def hook_root():
    logging.info("Received Hook")
    if request.headers["content-type"] == "application/json":
        req_data = json.loads(request.data)

        if toolz.get_in(["ref"], req_data, None) == "refs/heads/main":
            logging.info("Hook Triggered on main push")
            update_data()
            return "Handled"

        if check_merged("main", req_data):
            logging.info("Hook Triggered on merge")
            update_data()
            return "Handled"

        else:
            logging.info("unknown event")
            return "500"


@app.route("/islocked", methods=["POST"])
def islocked():
    if request.headers["Content-Type"] == "application/json":
        req_data = json.loads(request.data)

        service = toolz.get_in(["service"], req_data, None)
        if service is None:
            logging.error("Invalid Request", req_data)
            return "400", "Bad Request"

        lock_all = toolz.get_in(["lockall"], data, None)
        whitelisted = toolz.get_in(["whitelist"], data, None)
        lockout = toolz.get_in(["lockout"], data, None)

        if service in whitelisted:
            logging.info("Service %s is whitelisted", service)
            return "Not Locked"

        elif service in lockout or lock_all:
            logging.info("Service %s is locked", service)
            return "Locked"

        logging.info("Service %s is not locked", service)
        return "Not Locked"

    logging.error("Invalid Request", request.data)
    return 400, "Bad Request"

## implement LRU Cache 

@app.before_first_request
def setup():
    global lockout_config_path
    lockout_config_path = os.getenv("LOCKOUT_CONFIG_PATH", "../services/lockout.yaml")
    update_data()


if __name__ == "__main__":
    port = os.getenv("API_PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
