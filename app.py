from flask import (
    json,
    request,
    Flask
)
import toolz
from helpers.helper import *
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics
import os 

app = Flask(__name__)
metrics = GunicornPrometheusMetrics(app)


def update_data(lockout_config_path):
    pull_new_data()
    global data
    data = update_dictionary(lockout_config_path)


@app.route("/hook", methods=["POST"])
def hook_root():
    if request.headers["content-type"] == "application/json":
        data = json.loads(request.data)

        if toolz.get_in(["ref"], data, None) == "refs/heads/main":
            update_data()
            return "Handled"

        if check_merged("main", data):
            update_data()
            return "Handled"

        else:
            print("unknown event")
            return "500"

@app.route("/islocked", methods=["POST"])
def islocked():
    if request.headers["Content-Type"] == "application/json":
        req_data =  json.loads(request.data)
    
        service = toolz.get_in(["service"], req_data, None)
        if service is None:
            return "400", "Bad Request"        

        lock_all = toolz.get_in(["lockall"], data, None)
        whitelisted = toolz.get_in(["whitelist"], data, None)
        lockout = toolz.get_in(["lockout"], data, None)

        if service in whitelisted:
            return "Not Locked"
        elif service in lockout or lock_all:
            return "Locked"
        
        return "Not Locked"

    return 400, "Bad Request"

if __name__ == "__main__":

    port = os.getenv('API_PORT',5000)
    lockout_config_path = os.getenv('LOCKOUT_CONFIG_PATH', 'services/lockout.yaml')
    update_data(lockout_config_path)

    
    app.run(host='0.0.0.0', port=port, debug=False,threaded=True)
