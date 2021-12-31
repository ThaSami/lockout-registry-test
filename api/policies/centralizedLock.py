from policies.policy import Policy
from policies.policyFactory import PolicyFactory
import toolz

@PolicyFactory.register("sre_centralized_lock")
class CentralizedLock(Policy):
  def is_locked(**kwargs):
    req_data = kwargs.get("req_data")
    service = toolz.get_in(["service"], req_data, None)
    lock_data = kwargs.get("lock_data")    
    lock_all = toolz.get_in(["lockall"], lock_data, None)
    whitelisted = toolz.get_in(["whitelist"], lock_data, None)
    lockout = toolz.get_in(["lockout"], lock_data, None)

    if service in whitelisted:
        return False

    elif service in lockout or lock_all:
        return True

    return True