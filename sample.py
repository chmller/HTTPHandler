import logging
from httphandler import HTTPHandler


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


simple_handler = HTTPHandler(
    'localhost',
    '/api/logger'
)
simple_handler.debug('some debug message')

https_handler = HTTPHandler(
    'localhost:443',
    '/api/logger',
    secure=True
)
https_handler.debug('some debug message over https')

auth_handler = HTTPHandler(
    'localhost:443',
    '/api/logger',
    method='POST',
    secure=True,
    authorization=('username', 'password')
)
auth_handler.debug('super secure debug message posted over https')



