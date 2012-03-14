What is Klein?
--------------

Klein is a fast, simple, production ready, lightweight web framework.

It builds on two widely used dependencies to enable production ready web apps
with as little of 2 lines of boilerplate.

Getting Started
===============

Example: "Hello World" in a klein bottle:

.. literalinclude:: examples/helloworld.py
    :linenos:
    :language: python

Can be launched with `python` and seen at http://localhost:8080/hello/Van%20Lindberg:
::

    $ python docs/examples/helloworld.py
    2012-03-14 14:27:36-0700 [-] Log opened.
    2012-03-14 14:27:36-0700 [-] Site starting on 8080
    2012-03-14 14:27:36-0700 [-] Starting factory <twisted.web.server.Site instance at 0x10677e440>
    2012-03-14 14:28:44-0700 [HTTPChannel,0,127.0.0.1] 127.0.0.1 - - [14/Mar/2012:21:28:43 +0000] "GET /hello/Van%20Lindberg HTTP/1.1" 200 26 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11"
    2012-03-14 14:28:44-0700 [HTTPChannel,0,127.0.0.1] 127.0.0.1 - - [14/Mar/2012:21:28:43 +0000] "GET /favicon.ico HTTP/1.1" 404 238 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11"


Example: "Hello World" with a KleinResource:

.. literalinclude:: examples/classyhelloworld.py
    :linenos:
    :language: python

Can be run with `twistd` and seen at http://localhost:8080/hello/Van%20Lindberg:
::

    $ PYTHONPATH="docs/examples" twistd -n web --class=classyhelloworld.MyKlein
    2012-03-14 14:31:48-0700 [-] Log opened.
    2012-03-14 14:31:48-0700 [-] twistd 12.0.0 (/Users/dreid/.virtualenvs/klein/bin/python 2.7.1) starting up.
    2012-03-14 14:31:48-0700 [-] reactor class: twisted.internet.selectreactor.SelectReactor.
    2012-03-14 14:31:48-0700 [-] Site starting on 8080
    2012-03-14 14:31:48-0700 [-] Starting factory <twisted.web.server.Site instance at 0x10fa2c320>
    2012-03-14 14:31:58-0700 [HTTPChannel,0,127.0.0.1] 127.0.0.1 - - [14/Mar/2012:21:31:58 +0000] "GET /hello/Van%20Lindberg HTTP/1.1" 200 27 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11"
    2012-03-14 14:31:58-0700 [HTTPChannel,0,127.0.0.1] 127.0.0.1 - - [14/Mar/2012:21:31:58 +0000] "GET /favicon.ico HTTP/1.1" 404 238 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11"


Example: "Hello World" with KleinResource and some static Files:

.. literalinclude:: examples/statichelloworld.py
    :linenos:
    :language: python

Can be run with `twistd`  and seen at http://localhost:8080/hello/Van%20Lindberg:
::

    $ PYTHONPATH="docs/examples" twistd -n web --class=statichelloworld.MyKlein
    2012-03-14 14:48:08-0700 [-] Log opened.
    2012-03-14 14:48:08-0700 [-] twistd 12.0.0 (/Users/dreid/.virtualenvs/klein/bin/python 2.7.1) starting up.
    2012-03-14 14:48:08-0700 [-] reactor class: twisted.internet.selectreactor.SelectReactor.
    2012-03-14 14:48:08-0700 [-] Site starting on 8080
    2012-03-14 14:48:08-0700 [-] Starting factory <twisted.web.server.Site instance at 0x109dc7ea8>
    2012-03-14 14:49:20-0700 [HTTPChannel,0,127.0.0.1] 127.0.0.1 - - [14/Mar/2012:21:49:20 +0000] "GET /hello/Van%20Lindberg HTTP/1.1" 200 50 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11"
    2012-03-14 14:49:21-0700 [HTTPChannel,0,127.0.0.1] 127.0.0.1 - - [14/Mar/2012:21:49:20 +0000] "GET /images/van-lindberg.png HTTP/1.1" 200 2806 "http://localhost:8080/hello/Van%20Lindberg" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11"
    2012-03-14 14:49:21-0700 [HTTPChannel,0,127.0.0.1] 127.0.0.1 - - [14/Mar/2012:21:49:20 +0000] "GET /favicon.ico HTTP/1.1" 404 238 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11"
