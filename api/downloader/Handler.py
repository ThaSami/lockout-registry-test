from typing import Protocol
from abc import abstractmethod

class Handler(Protocol):
  @abstractmethod
  def download(self, path: str) -> bytes:
    raise NotImplementedError
