""" stack-ws API views. """
from flask import Flask, request, Response
from functools import wraps
from flask.ext.autodoc import Autodoc
from stackapi.stackFactory import AbstractStackFactory
from stackapi.application_config import get_config
import httplib as status

# APPLICATION definition
USER_CONFIG = get_config()
APPLICATION = Flask(__name__)
APPLICATION.config.update(USER_CONFIG)
APPLICATION.debug = APPLICATION.config['DEBUG']
AUTO = Autodoc(APPLICATION)

# Stack objects container
WSSTACKLIST = []
FACTORY = AbstractStackFactory.getStackFactory(APPLICATION.config['STACK'])


def check_auth(username, password):
    """
    This function is called to check if a username and password combination is
    valid.
    """
    return \
        username == APPLICATION.config['HTTP_AUTH_USERNAME'] and \
        password == APPLICATION.config['HTTP_AUTH_PASSWORD']


def authenticate():
    """ Return status code 401 Unauthorized to enable HTTP Basic Auth. """
    return Response(
        'Access denied..\n'
        'You must login with valid credentials', status.UNAUTHORIZED,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@APPLICATION.route('/')
@AUTO.doc()
def hello():
    """
    Test endpoint.
    GETs to this endpoint will retrieve the string 'Hello World'.
    """
    return 'Hello World'


# Manage the list of stack objs
@APPLICATION.route('/stack', methods=['GET', 'POST'])
@AUTO.doc()
@requires_auth
def stackMgr():
    """
    Manage stack objects.
    POSTs to this endpoint will create a new stack instance object. Any POST
    data sent with the request is discarded.

    GETs to this endpoint will retrieve all stack instance objects.

    All methods require authentication.
    """
    if request.method == 'GET':
        return str(WSSTACKLIST)
    elif request.method == 'POST':
        stack = FACTORY.getStackFactory()
        WSSTACKLIST.append(stack)
        return str(WSSTACKLIST.index(stack))


@APPLICATION.route('/stack/<int:id>', methods=['GET', 'POST', 'DELETE'])
@AUTO.doc()
@requires_auth
def stack(id):
    """
    Manage stack instance object operations.
    POSTs to this endpoint will insert a new element at the top of the stack
    instance object, above the current top element. The content of the new
    element is the POST data passed with the request.
    Effectively push'ing to the stack.

    DELETEs to this endpoint will remove the element at the top of the stack
    instance object, reducing its size by one.
    Effectively pop'ing the stack.

    GETs to this endpoint will retrieve the stack instance object. There is no
    equivalent replacement stack operation.

    All methods require authentication.

    All request methods return status code 500 Internal Server Error if an
    error is encountered.
    """
    if request.method == 'GET':
        try:
            return str(WSSTACKLIST[id])
        except (IndexError, ValueError) as exception:
            return str(exception), status.INTERNAL_SERVER_ERROR
    # Push to stack
    elif request.method == 'POST':
        try:
            WSSTACKLIST[id].push(request.get_data())
            return request.get_data()
        except (IndexError, ValueError) as exception:
            return str(exception), status.INTERNAL_SERVER_ERROR
    # Pop from stack
    elif request.method == 'DELETE':
        try:
            return WSSTACKLIST[id].pop()
        except (IndexError, ValueError) as exception:
            return str(exception), status.INTERNAL_SERVER_ERROR


@APPLICATION.route('/stack/<int:id>/size', methods=['GET'])
@AUTO.doc()
@requires_auth
def stackSize(id):
    """
    GETs to this endpoint will retrieve the number of elements in the stack
    instance object.

    All methods require authentication.
    """
    if request.method == 'GET':
        return str(WSSTACKLIST[id].size())


@APPLICATION.route('/stack/<int:id>/peek', methods=['GET'])
@AUTO.doc()
@requires_auth
def stackPeek(id):
    """
    GETs to this endpoint will retrieve the topmost element in the stack
    instance object.

    All methods require authentication.

    Returns status code 500 Internal Server Error if an error is encountered.
    """
    if request.method == 'GET':
        try:
            return str(WSSTACKLIST[id].peek())
        except (IndexError, ValueError) as exception:
            return str(exception), status.INTERNAL_SERVER_ERROR


@APPLICATION.route('/stack/<int:id>/clear', methods=['DELETE'])
@AUTO.doc()
@requires_auth
def stackClear(id):
    """
    Clear all elements of the stack.
    DELETEs to this endpoint will remove all elements from the stack object.
    Leaves the stack instance object in-place.

    All methods require authentication.

    Returns status code 500 Internal Server Error if an error is encountered.
    """
    if request.method == 'DELETE':
        try:
            return str(WSSTACKLIST[id].clear())
        except (IndexError, ValueError) as exception:
            return str(exception), status.INTERNAL_SERVER_ERROR


@APPLICATION.route('/documentation')
@AUTO.doc()
def documentation():
    """
    GETs to this endpoint will retrieve API documentation. Autogenerated with
    Flask-Autodoc.
    """
    return AUTO.html()


def run_application(arguments=None):
    print "Got Config:\n {}".format(USER_CONFIG)
    if arguments:
        # expansion for variable arguments for run_stack_app here
        # global FACTORY
        # global APPLICATION
        pass

    APPLICATION.run(
        host=APPLICATION.config['HOST'],
        port=APPLICATION.config['PORT'])

if __name__ == '__main__':
    run_application()
