from flask import jsonify, request, Flask, json
from helper import *
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import os
import logging
from downloader import HandlerFactory as handlersFactory
import downloader.urlHandler
from policies import policyFactory as policiesFactory
import policies.centralizedLock


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

app = Flask(__name__)

metrics = GunicornPrometheusMetrics(app)

policies = {
    "sre_centralized_lock": policiesFactory.PolicyFactory.make_policy(
        "sre_centralized_lock"
    )
}

cache_timeout = int(os.getenv("CACHE_TIMEOUT", "120"))

@timed_lru_cache(maxsize=None, seconds=cache_timeout)
def update_data():
    logging.info("Downloading data from {}".format(file_place))
    lockout_data = handler.download(file_place)
    global data
    data = parse_data(lockout_data)
    logging.info("Data Updated")

def validate_request(req_data):
    if not req_data:
        return False
    if not req_data.get("service"):
        return False
    return True

@app.route("/islocked", methods=["POST"])
def islocked():
    if request.headers["Content-Type"] == "application/json":
        req_data = json.loads(request.data)

        if not validate_request(req_data):
            logging.error("Invalid Request", req_data)
            return jsonify({"status": "Bad Request"}), 400

        service = req_data.get("service")
        update_data()
        status = "Not Locked"
        for policy in policies:
            logging.info("Evaluating %s on policy %s", service, policy)
            if policies[policy].is_locked(req_data=req_data, lock_data=data):
                status = "Locked"
                break

        logging.info("Service %s is %s", service, status)
        return jsonify({"status": status}), 200

    logging.error("Invalid Request", request.data)
    return jsonify({"status": "Bad Request"}), 400


@app.before_first_request
def setup():
    global handler, file_place
    lockout_place = os.getenv("LOCKOUT_PLACE", "url")
    file_place = os.getenv(
        "FILE_URL",
        "https://raw.githubusercontent.com/ThaSami/lockout-registry-test/main/services/lockout.yaml",
    )
    handler = handlersFactory.HandlerFactory.make_handler(lockout_place)
    update_data()


if __name__ == "__main__":
    port = os.getenv("API_PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
