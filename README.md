HTTPHandler
===========

This HTTPHandler is a replacement class for Pythons HTTP logging handler by Viany Sajip.
This class also supports HTTPS and basic authorization.


Usage
=====

```python
import logging
from httphandler import HTTPHandler


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('mylogger')
auth = ('username', 'password')
http_handler = HTTPHandler(
    'localhost:1337',
    '/api/logger',
    method='POST',
    secure=True,
    authorization=auth)
logger.addHandler(http_handler)
logger.debug('testing remote logging')
```
