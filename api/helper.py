import toolz
import yaml
import git
import os


def check_merged(basebranch, data):
    return (
        toolz.get_in(["pull_request", "base", "ref"], data, "unknown") == basebranch
        and toolz.get_in(["action"], data, "False") == "closed"
        and toolz.get_in(["pull_request", "merged"], data, False)
    )


def read_yaml(filepath):
    with open(filepath, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def format_service_dictionary(dictionary):
    return {
        "lockall": dictionary["lockall"],
        "lockout": set(dictionary["lockout"]) - set(dictionary["whitelist"]),
        "whitelist": set(dictionary["whitelist"]),
    }


def pull_new_data(branch_name):
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    repo = git.Repo(repo_path)
    repo.remotes.origin.pull(branch_name)


def update_dictionary(filepath):
    return format_service_dictionary(read_yaml(filepath))