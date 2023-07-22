from typing import List
from cache import AsyncLRU  # pip install async-cache
from dataclasses import dataclass

import aiohttp

ENDPOINT = "https://www.1secmail.com/api/v1/"
# See https://www.1secmail.com/api/


@dataclass
class MessageNotFound(Exception):
    login: str
    domian: str
    id: int

    def __str__(self):
        return f"Message with id {self.id} not found on {self.login}@{self.domian}"


@AsyncLRU(maxsize=None)
async def get_domians(*args, **kwargs) -> List[str]:
    """Get list of active domains(cached)

    :param args: additional options for `aiohttp.ClientSession.get`
    :param kwargs: additional options for `aiohttp.ClientSession.get`

    :rtype: List[str]
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(ENDPOINT, params={
            "action": "getDomainList"
        }, *args, **kwargs) as response:
            return await response.json()


async def get_messages(login: str, domian: str, *args, **kwargs) -> dict:
    """Get list of messages on mailbox

    :param login: mailbox login
    :type login: str
    :param domian: mailbox domian
    :type domian: str
    :param args: additional options for `aiohttp.ClientSession.get`
    :param kwargs: additional options for `aiohttp.ClientSession.get`

    :rtype: dict
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(ENDPOINT, params={
            "action": "getMessages",
            "login": login,
            "domain": domian,
        }, *args, **kwargs) as response:
            pass

    return await response.json()


@AsyncLRU(maxsize=None)
async def get_message(login: str, domian: str, id: int, *args, **kwargs) -> dict:
    """Get list of messages on mailbox(cached)

    :param login: mailbox login
    :type login: str
    :param domian: mailbox domian
    :type domian: str
    :param id: message id
    :type id: id
    :param args: additional options for `aiohttp.ClientSession.get`
    :param kwargs: additional options for `aiohttp.ClientSession.get`

    :rtype: dict

    :exception MessageNotFound:
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(ENDPOINT, params={
            "action": "readMessage",
            "login": login,
            "domain": domian,
            "id": id
        }, *args, **kwargs):
            if await response.text() == "Message not found":
                raise MessageNotFound(login=login, domian=domian, id=id)

            return await response.json()


async def get_attachment(login: str, domian: str, id: int, file: str, *args, **kwargs) -> bytes:
    """Get list of messages on mailbox

    :param login: mailbox login
    :type login: str
    :param domian: mailbox domian
    :type domian: str
    :param id: message id
    :type id: id
    :param file: file name
    :type file: str
    :param args: additional options for `aiohttp.ClientSession.get`
    :param kwargs: additional options for `aiohttp.ClientSession.get`

    :rtype: byte
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(ENDPOINT, params={
            "action": "download",
            "login": login,
            "domain": domian,
            "id": id,
            "file": file
        }, *args, **kwargs):
            return await response.content
