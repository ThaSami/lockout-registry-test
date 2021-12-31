class HandlerFactory:
  handlers = {}

  @classmethod
  def make_handler(cls, version):
    try:
      retval = cls.handlers[version]
    except KeyError as err:
      raise NotImplementedError(f"{version=} doesn't exist") from err
    return retval

  @classmethod
  def register(cls, type_name):
    def deco(deco_cls):
      cls.handlers[type_name] = deco_cls
      return deco_cls
    return deco
