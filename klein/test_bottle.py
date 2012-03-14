from twisted.trial import unittest
from twisted.web.resource import IResource

from mock import Mock

from klein import route, run
from klein.test_resource import _render, requestMock

def fakeRoutes():
    my_routes = {}

    @route("/foo", routes=my_routes)
    def myroute(request):
        return "foo"

    return my_routes


class IResourceMatcher(object):
    def __init__(self):
        self.resource = None

    def __eq__(self, other):
        self.resource = other
        return IResource.providedBy(other)


class BottleTestCase(unittest.TestCase):
    def test_routeAddsRoutes(self):
        my_routes = fakeRoutes()

        self.assertIn("myroute", my_routes)
        self.assertTrue(hasattr(my_routes["myroute"], "__klein_exposed__"))

    def test_runRunsReactor(self):
        reactor = Mock()

        run(host="localhost", port=8080, reactor=reactor)

        self.assertTrue(reactor.run.called)

    def test_runListens(self):
        reactor = Mock()
        site_factory = Mock()
        run(host="localhost", port=8080, reactor=reactor, site_factory=site_factory)

        site = site_factory.return_value

        reactor.listenTCP.assert_called_with(8080, site, interface="localhost")

    def test_runConfiguresResource(self):
        reactor = Mock()
        site_factory = Mock()

        my_routes = fakeRoutes()

        run(host="localhost", port=8080, reactor=reactor,
            site_factory=site_factory, routes=my_routes)

        irm = IResourceMatcher()

        site_factory.assert_called_with(irm)

        request = requestMock("/foo")

        d = _render(irm.resource, request)

        @d.addCallback
        def _cb(result):
            request.write.assert_called_with('foo')

        return d

