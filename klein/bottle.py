import sys

from functools import wraps

from twisted.python.log import startLogging
from twisted.internet import reactor
from twisted.web.server import Site

from klein.decorators import expose
from klein.resource import KleinResource

global_routes = {}

def route(r, routes=global_routes):
    def deco(f):
        # Swallow self.
        # XXX hilariously, staticmethod would be *great* here.
        @wraps(f)
        def inner(self, *args, **kwargs):
            return f(*args, **kwargs)
        routes[f.__name__] = expose(r)(inner)
    return deco


def run(host=None, port=8080, reactor=reactor,
        routes=global_routes, site_factory=Site):
    # Invoke the metaclass directly.
    runner = type(KleinResource)("runner", (KleinResource,), routes)
    site = site_factory(runner())
    startLogging(sys.stdout)
    reactor.listenTCP(port, site, interface=host)
    reactor.run()


__all__ = ['route', 'run']
