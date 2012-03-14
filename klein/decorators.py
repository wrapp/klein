from functools import wraps

def expose(url, *a, **kw):
    """
    Mark a ``KleinResource`` method as exposing a certain URL.

    URLs may have Werkzeug-style parameters in them, since they are
    essentially Werkzeug routes; see http://werkzeug.pocoo.org/docs/routing/
    for the details.

    >>> class SimpleResource(KleinResource):
    ...  @expose("/")
    ...  def index(self, request):
    ...   pass
    ...  @expose("/pages/<int:page_id>")
    ...  def pages(self, request, page_id):
    ...   pass

    Exposed methods will be called with at least two parameters. ``self`` is
    the explicit self. ``request`` is a ``twisted.web.request.Request``. The
    request will have two attributes: ``mapper``, the Werkzeug mapper used for
    the request, and ``url_for``, a callable which can build URLs for routes.
    """

    def deco(f):
        kw.setdefault('endpoint', '-'.join([f.__name__, url]))
        f.__klein_exposed__ = getattr(f, '__klein_exposed__', [])
        f.__klein_exposed__.append((url, a, kw))
        return f

    return deco


def expose_branch(baseurl, *a, **kw):
    """
    Mark a ``KleinResource`` method as exposing a branch at the given URL.
    A branch is a URL which may have children to an arbitrary depth and should
    match both /url/ and /url/<path:rest>.
    """

    if not baseurl.endswith('/'):
        baseurl += '/'

    pathurl = baseurl + '<path:__branch_rest__>'
    def deco(f):
        expose(pathurl, *a, **kw)(f)
        expose(baseurl, *a, **kw)(f)

        @wraps(f)
        def without_branch_rest(self, request, *a, **kw):
            if '__branch_rest__' in kw:
                branch_rest = kw.pop('__branch_rest__', '')
                branch_segments = branch_rest.split('/')
                request.__klein_branch_segments__ = branch_segments

            return f(self, request, *a, **kw)

        return without_branch_rest

    return deco
