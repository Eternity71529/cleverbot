import requests
from .errors import CleverConfigurationError, CleverAPIError


class Client:
    '''Cleverbot Client:
    Notice:
        This is a Requests based wrapper for the Cleverbot.io API
        for more control over the wrapper in an event based loop,
        see the :AsyncClient: class
    Usage:
        >>> from cleverbot import *
        >>> bot = Client(api_key = "API TOKEN/KEY HERE", user_id = "User ID Here", nick = "Optional Parameter to pass the Nickname")
        >>> bot.ask("Hi")
        "You said that so."
    Parameters to pass to the :Client: class
        -api_key = the Key for the API
        -user_name = the User name you received from the API
        -nick = An Optional Parameter. Starts the Session with that nick
            If not specified, a random nick is given
    '''
    def __init__(self, **kwargs):
        self.api_key = kwargs.pop("api_key", None)
        self.user_id = kwargs.pop("user_id", None)
        self._nick = kwargs.pop("nick", None)
        self.check_credentials()
        self.nick = None
        self.create = "https://cleverbot.io/1.0/create"
        self._ask = "https://cleverbot.io/1.0/ask"
        self.create_session()

    def check_credentials(self):
        if self.api_key is None:
            raise CleverConfigurationError("You must pass an API Key. eg: client = Cleverbot(api_key = 'KEY HERE', user_id = 'ID HERE', nick = 'NICK HERE')")
        if self.user_id is None:
            raise CleverConfigurationError("You must pass the User Name. eg: client = Cleverbot(api_key = 'KEY HERE', user_id = 'ID HERE', nick = 'NICK HERE')")

    def create_session(self):
        """Initiates the Session with the Cleverbot API"""
        data = {
        "user" : self.user_id,
        "key" : self.api_key
        }
        if self._nick is not None:
            data["nick"] = self._nick
        post = requests.post(self.create, data = data)
        recv = post.json()
        if recv["status"] == "Error: reference name already exists":
            self.nick = self._nick
            return
        elif recv["status"] != "success":
            raise CleverAPIError("An Error occured while creating a session. Error: {}\nPayload: {}".format(recv["status"], data))
        elif post.status_code != 200:
            raise CleverAPIError("An Error occured while creating a session. Error: Bad Request (Status Code: 400)\nPayload: {}".format(data))
        else:
            self.nick = recv["nick"]
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
        post = requests.post(self._ask, data = data)
        recv = post.json()
        if recv["status"] != "success":
            raise CleverAPIError("An Error occured while asking a question to the API. Error: {}".format(recv["status"]))
        elif post.status_code != 200:
            raise CleverAPIError("An Error occured while asking a question to the API. Error: Bad Request (Status Code: 400)")
        else:
            answer = recv["response"]
        return answer



