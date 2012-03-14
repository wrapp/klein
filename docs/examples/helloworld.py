from klein import route, run

@route('/hello/<string:name>')
def index(request, name="World!"):
    return '<b>Hello, %s!</b>' % (name.encode('utf-8'),)

run(host='localhost', port=8080)
