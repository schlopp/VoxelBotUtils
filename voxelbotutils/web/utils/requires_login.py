import functools

import aiohttp_session
from aiohttp.web import HTTPFound, Request


def requires_login():
    """This function is a wrapper around all routes. It takes the output and
    adds the user info and request to the returning dictionary
    It must be applied before the template decorator"""

    def inner_wrapper(func):
        """An inner wrapper so I can get args at the outer level"""

        @functools.wraps(func)
        async def wrapper(request:Request):
            """This is the wrapper that does all the heavy lifting"""

            # See if we have token info
            session = await aiohttp_session.get_session(request)
            if session.new or session.get('logged_in', False) is False:
                session['redirect_on_login'] = str(request.url)
                if session['redirect_on_login'] == request.app['config']['login_url'] or '/login_processor' in str(request.url):
                    session['redirect_on_login'] = '/'
                return HTTPFound(location=request.app['config']['login_url'])

            # We're already logged in
            return await func(request)

        return wrapper
    return inner_wrapper
