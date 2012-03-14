import os
from klein.decorators import expose, expose_branch
from klein.resource import KleinResource

from twisted.web.static import File

class MyKlein(KleinResource):
    @expose("/hello/<string:name>")
    def hello(self, request, name='World'):
        if name.lower() != "van lindberg":
            return "<b>Hello, %s!</b>" % (name.encode('utf-8'),)
        else:
            return "<b>Hello, <img src=\"/static/van-lindberg.png\"></b>"

    @expose_branch("/static")
    def van_lindberg_png(self, request):
        return File(os.path.join(os.path.dirname(__file__), "static"))
