import logging
from httphandler import HTTPHandler


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

simple_handler = HTTPHandler('localhost', '/api/logger')
https_handler = HTTPHandler('localhost:443', '/api/logger', method='POST', secure=True)
auth_handler = HTTPHandler('localhost:443', '/api/logger', method='POST', secure=True,
                           authorization=('username', 'password'))

logger.addHandler(simple_handler)
logger.addHandler(https_handler)
logger.addHandler(auth_handler)

logger.debug('some debug message')