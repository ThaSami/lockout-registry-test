from typing import Protocol
from abc import abstractmethod

class Policy(Protocol):
  @abstractmethod
  def is_locked(self, **kwargs) -> bool:
    raise NotImplementedError
