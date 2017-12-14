import aiohttp
import asyncio
from .errors import CleverConfigurationError, CleverAPIError
class AsyncClient:
    '''Cleverbot AsyncClient:
    Notice:
        This is an Asyncio based wrapper for the Cleverbot.io API
        for more control over the wrapper in an sync based program,
        see the :Client: class
    Usage:
        >>> import asyncio
        >>> from cleverbot import *
        >>> loop = asyncio.get_event_loop()
        >>> bot = AsyncClient(api_key = "API TOKEN/KEY HERE", user_id = "User ID Here", nick = "Optional Parameter to pass the Nickname", loop = loop)
        >>> loop.run_until_complete(bot.ask("Hi"))
        "You said that so."
    Parameters to pass to the :Client: class
        -api_key = the Key for the API
        -user_name = the User name you received from the API
        -nick = An Optional Parameter. Starts the Session with that nick
            If not specified, a random nick is given
        -loop = An Partially Optional Parameter. Initiates the Session in that loop
           If not specified, the default loop is chosen
    '''
    def __init__(self, **kwargs):
        self.api_key = kwargs.pop("api_key", None)
        self.user_id = kwargs.pop("user_id", None)
        self._nick = kwargs.pop("nick", None)
        self.loop = kwargs.pop("loop", asyncio.get_event_loop())
        self.check_credentials()
        self.nick = None
        self.session = aiohttp.ClientSession(loop = self.loop)
        self.create = "https://cleverbot.io/1.0/create"
        self._ask = "https://cleverbot.io/1.0/ask"
        self.loop.create_task(self.create_session())

    def check_credentials(self):
        if self.api_key is None:
            raise CleverConfigurationError("You must pass an API Key. eg: client = Cleverbot(api_key = 'KEY HERE', user_id = 'ID HERE', nick = 'NICK HERE')")
        if self.user_id is None:
            raise CleverConfigurationError("You must pass the User Name. eg: client = Cleverbot(api_key = 'KEY HERE', user_id = 'ID HERE', nick = 'NICK HERE')")

    @asyncio.coroutine
    def post(self, link, data):
        try:
            with aiohttp.Timeout(5):
                resp = yield from self.session.post(link, data = data)
                foo = yield from resp.json()
                return [foo, resp.status]
        except asyncio.TimeoutError:
            raise CleverAPIError("The API Timed out while POSTing this data")
        else:
            pass

    @asyncio.coroutine
    def create_session(self):
        data = {
        "user" : self.user_id,
        "key" : self.api_key
        }
        if self._nick is not None:
            data["nick"] = self._nick
        post = yield from self.post(self.create, data = data)
        recv = post[0]
        if recv["status"] == "Error: reference name already exists":
            self.nick = self._nick
            return
        if recv["status"] != "success":
            raise CleverAPIError("An Error occured while creating a session. Error: {}".format(recv["status"]))
        elif post[1] != 200:
            raise CleverAPIError("An Error occured while creating a session. Error: Bad Request (Status Code: {})".format(post[1]))
        else:
            self.nick = recv["nick"]
    @asyncio.coroutine
    def ask(self, question):
        """Ask the Instance a question
        Params:
            question: the question you are asking
        Returns:
            answer
        """
        answer = ""
        data = {
        "user" : self.user_id,
        "key" : self.api_key,
        "nick" : self.nick,
        "text" : question
        }
        post = yield from self.post(self._ask, data = data)
        recv = post[0]
        if recv["status"] != "success":
            raise CleverAPIError("An Error occured while asking a question to the API. Error: {} (Status Code: {})".format(recv["status"], post[1]))
        elif post[1] != 200:
            raise CleverAPIError("An Error occured while asking a question to the API. Error: Bad Request (Status Code: {})".format(post[1]))
        else:
            answer = recv["response"]
        return answer       
