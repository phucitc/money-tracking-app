class Constant:
    HTTP_OK = 200
    HTTP_CREATED = 201
    HTTP_ACCEPTED = 202
    HTTP_NO_CONTENT = 204
    HTTP_BAD_REQUEST = 400
    HTTP_UNAUTHORIZED = 401
    HTTP_FORBIDDEN = 403
    HTTP_NOT_FOUND = 404
    HTTP_METHOD_NOT_ALLOWED = 405
    HTTP_CONFLICT = 409
    HTTP_INTERNAL_SERVER_ERROR = 500
    HTTP_NOT_IMPLEMENTED = 501
    HTTP_BAD_GATEWAY = 502
    HTTP_SERVICE_UNAVAILABLE = 503
    HTTP_GATEWAY_TIMEOUT = 504
    HTTP_MSG = {
        HTTP_OK: 'OK',
        HTTP_CREATED: 'Created',
        HTTP_ACCEPTED: 'Accepted',
        HTTP_NO_CONTENT: 'No Content',
        HTTP_BAD_REQUEST: 'Bad Request',
        HTTP_UNAUTHORIZED: 'Unauthorized',
        HTTP_FORBIDDEN: 'Forbidden',
        HTTP_NOT_FOUND: 'Not Found',
        HTTP_METHOD_NOT_ALLOWED: 'Method Not Allowed',
        HTTP_CONFLICT: 'Conflict',
        HTTP_INTERNAL_SERVER_ERROR: 'Internal Server Error',
        HTTP_NOT_IMPLEMENTED: 'Not Implemented',
        HTTP_BAD_GATEWAY: 'Bad Gateway',
        HTTP_SERVICE_UNAVAILABLE: 'Service Unavailable',
        HTTP_GATEWAY_TIMEOUT: 'Gateway Timeout'
    }
    ADMIN_EMAILS = ['dhoangphuc237@gmail.com']
    VUEJS_PAGES = [
        'home', 'login', 'signup',
        'logout', 'profile', 'dashboard',
        'about', 'callback', 'beta'
    ]

    VUEJS_ADMIN_PAGES = ['login', 'urls']
