from downloader.Handler import Handler
from downloader.HandlerFactory import HandlerFactory
import requests


@HandlerFactory.register("url")
class UrlHandler(Handler):
  def download(path):
    file = requests.get(path)
    return file.text