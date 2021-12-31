class PolicyFactory:
  policies = {}

  @classmethod
  def make_policy(cls, policy):
    try:
      retval = cls.policies[policy]
    except KeyError as err:
      raise NotImplementedError(f"{policy=} doesn't exist") from err
    return retval

  @classmethod
  def register(cls, type_name):
    def deco(deco_cls):
      cls.policies[type_name] = deco_cls
      return deco_cls
    return deco
