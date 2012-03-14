from klein.decorators import expose
from klein.resource import KleinResource

class MyKlein(KleinResource):
    @expose("/hello/<string:name>")
    def hello(self, request, name='World'):
        return "<b>Hello, %s!</b>" % (name.encode('utf-8'),)
