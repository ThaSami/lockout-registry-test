from downloader.Handler import Handler
from downloader.HandlerFactory import HandlerFactory


@HandlerFactory.register('s3')
class S3Handler(Handler):
  def download(path):
    ...