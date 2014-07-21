import logging
import logging.handlers


class HTTPHandler(logging.Handler):
    """
    A class Based on Vinay Sajip HTTPHandler-class which sends records to a Web server,
    using either GET or POST semantics. It supports HTTP, HTTPS and basic authorization.
    """
    def __init__(self, host, url, method="GET", secure=False, authorization=None):
        """
        Initialize the instance with the host, the request URL, the method ("GET" or "POST"), the secure-flag
        (to use HTTPS), and HTTP basic auth credentials as a tuple of username and password.
        """
        logging.Handler.__init__(self)
        method = method.upper()
        if method not in ["GET", "POST"]:
            raise ValueError("method must be GET or POST")
        self.host = host
        self.url = url
        self.method = method
        self.secure = secure
        self.authorization = authorization

    def mapLogRecord(self, record):
        """
        Default implementation of mapping the log record into a dict
        that is sent as the CGI data. Overwrite in your class.
        Contributed by Franz  Glasner.
        """
        import socket
        record.__dict__.update(hostname=socket.gethostname())
        return record.__dict__

    def emit(self, record):
        """
        Emit a record.

        Send the record to the Web server as a percent-encoded dictionary
        """
        try:
            import httplib, urllib
            host = self.host
            if self.secure:
                h = httplib.HTTPS(host)
            else:
                h = httplib.HTTP(host)
            url = self.url
            data = urllib.urlencode(self.mapLogRecord(record))
            if self.method == "GET":
                if (url.find('?') >= 0):
                    sep = '&'
                else:
                    sep = '?'
                url = url + "%c%s" % (sep, data)
            h.putrequest(self.method, url)
            # support multiple hosts on one IP address...
            # need to strip optional :port from host, if present
            i = host.find(":")
            if i >= 0:
                host = host[:i]
            h.putheader("Host", host)
            if self.authorization:
                import base64
                auth = base64.encodestring("%s:%s" % self.authorization).replace('\n', '')
                h.putheader("Authorization",
                            "Basic %s" % auth)
            if self.method == "POST":
                h.putheader("Content-type",
                            "application/x-www-form-urlencoded")
                h.putheader("Content-length", str(len(data)))
            if self.method == "POST":
                h.endheaders()
                h.send(data)
            else:
                h.endheaders()
            h.getreply()    #can't do anything with the result
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
