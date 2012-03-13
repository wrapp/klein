from twisted.trial import unittest

from klein.decorators import expose
from klein.resource import KleinResource

from twisted.internet.defer import succeed, Deferred
from twisted.web import server
from twisted.web.resource import Resource
from twisted.web.template import Element, XMLString, renderer

from mock import Mock

def requestMock(path, method="GET", host="localhost", port=8080, isSecure=False):
    postpath = path.split('/')

    request = Mock()
    request.getRequestHostname.return_value = host
    request.getHost.return_value.port = port
    request.postpath = postpath
    request.prepath = []
    request.method = method
    request.isSecure.return_value = isSecure
    request.notifyFinish.return_value = Deferred()
    request.finished = False

    def render(resource):
        return _render(resource, request)

    def finish():
        request.notifyFinish.return_value.callback(None)
        request.finished = True

    def processingFailed(failure):
        request.failed = failure
        request.notifyFinish.return_value.errback(failure)

    request.finish.side_effect = finish
    request.render.side_effect = render
    request.processingFailed.side_effect = processingFailed

    return request

def _render(resource, request):
    result = resource.render(request)
    if isinstance(result, str):
        request.write(result)
        request.finish()
        return succeed(None)
    elif result is server.NOT_DONE_YET:
        if request.finished:
            return succeed(None)
        else:
            return request.notifyFinish()
    else:
        raise ValueError("Unexpected return value: %r" % (result,))


class SimpleElement(Element):
    loader = XMLString("""
    <h1 xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1" t:render="name" />
    """)

    def __init__(self, name):
        self._name = name

    @renderer
    def name(self, request, tag):
        return tag(self._name)


class SimpleKlein(KleinResource):
    def __init__(self):
        self.deferred = None

    @expose("/")
    def index(self, request):
        return 'ok'

    @expose("/trivial")
    def trivial(self, request):
        return "trivial"

    @expose("/deferred")
    def deferred(self, request):
        return self.deferred

    @expose("/element/<string:name>")
    def element(self, request, name):
        return SimpleElement(name)

    @expose("/resource/leaf")
    def resource(self, request):
        return LeafResource()

    @expose("/resource/children")
    def resource_children_index(self, request):
        return ChildrenResource()

    @expose("/resource/children/<path:rest>")
    def resource_children(self, request, rest):
        return ChildrenResource()


class ChildOfKlein(SimpleKlein):
    @expose("/")
    def index(self, request):
        return "child"


class LeafResource(Resource):
    isLeaf = True

    def render(self, request):
        return "I am a leaf in the wind."


class ChildResource(Resource):
    isLeaf = True
    def __init__(self, name):
        self._name = name

    def render(self, request):
        return "I'm a child named %s!" % (self._name,)


class ChildrenResource(Resource):
    def render(self, request):
        return "I have children!"

    def getChild(self, path, request):
        return ChildResource(path)


class KleinResourceTests(unittest.TestCase):
    def test_simpleRouting(self):
        kr = SimpleKlein()

        request = requestMock('/')

        d = _render(kr, request)

        def _cb(result):
            request.write.assert_called_with('ok')

        d.addCallback(_cb)

        return d

    def test_inheritedRouting(self):
        kr = ChildOfKlein()

        request = requestMock("/trivial")

        d = _render(kr, request)

        @d.addCallback
        def _cb(result):
            request.write.assert_called_with('trivial')

        return d

    def test_inheritedOverride(self):
        kr = ChildOfKlein()

        request = requestMock("/")

        d = _render(kr, request)

        @d.addCallback
        def _cb(result):
            request.write.assert_called_with('child')

        return d

    def test_deferredRendering(self):
        kr = SimpleKlein()
        kr.deferred = Deferred()

        request = requestMock("/deferred")

        d = _render(kr, request)

        def _cb(result):
            request.write.assert_called_with('ok')

        d.addCallback(_cb)
        kr.deferred.callback('ok')

        return d

    def test_elementRendering(self):
        kr = SimpleKlein()
        request = requestMock("/element/foo")

        d = _render(kr, request)

        def _cb(result):
            request.write.assert_called_with("<h1>foo</h1>")

        d.addCallback(_cb)

        return d

    def test_leafResourceRendering(self):
        kr = SimpleKlein()
        request = requestMock("/resource/leaf")

        d = _render(kr, request)
        def _cb(result):
            request.write.assert_called_with("I am a leaf in the wind.")

        d.addCallback(_cb)

        return d

    def test_childResourceRendering(self):
        kr = SimpleKlein()
        request = requestMock("/resource/children/betty")

        d = _render(kr, request)
        def _cb(result):
            request.write.assert_called_with("I'm a child named betty!")

        d.addCallback(_cb)

        return d

    def test_childrenResourceRendering(self):
        kr = SimpleKlein()
        request = requestMock("/resource/children")

        d = _render(kr, request)
        def _cb(result):
            request.write.assert_called_with("I have children!")

        d.addCallback(_cb)

        return d
