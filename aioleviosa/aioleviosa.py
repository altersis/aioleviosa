"""Classes containing the async http methods to connect to a 
Leviosa Motor Shades Zone Hub

These classes were built with Home Assistant in mind, but should work well
for other purposes """

import asyncio
from ipaddress import IPv4Address
import logging
from typing import Any, Mapping

import aiohttp
import async_timeout
from async_upnp_client.advertisement import SsdpAdvertisementListener

_LOGGER = logging.getLogger(__name__)


class LvsaApiError(Exception):
    """General Api error. Means we have a problem communication with
    the Leviosa hub."""

class LvsaApiResponseStatusError(LvsaApiError):
    """Wrong http response error."""

class LvsaApiConnectionError(LvsaApiError):
    """Problem connecting to Leviosa hub."""

async def discover_leviosa_zones() -> dict:
    """Listen for Zone advertisements. Leviosa Zones
       implement SSDP advertisements (do not respond to 
       M-SEARCH, no description document), so this custom 
       discovery process is necessary 
       20 seconds for discovery is enough, as Zones 
       advertise very frequently. 

       param: nothing needed 
       return: dictionary of UDNs and IPs of Zones
       (last segment of UDN contains Zone MAC address ) """
    _LOGGER.debug("setting up discovery for Leviosa Zone @0.0.0.0")
    ZonesFound = {}

    async def on_notify(data: Mapping[str, Any]) -> None:
        if (
            data.get("USN", "notfound").find("urn:leviosa:device:wiShadeController:1")
            > 0
        ) and (data.get("_udn", "notfound") not in ZonesFound.keys()):
            ip = data.get("_address", "NOADDR")  # IP of Zone normally comes in _address 
            if ip == "NOADDR":                   # Some OS' (like Ubuntu) return
                ip = data.get("_host", "0.0.0.0:1900") + ":" # _host
            ZonesFound[data["_udn"]] = ip[: ip.find(":")]
            _LOGGER.debug(
                "Found a Leviosa Zone %s @%s", data["_udn"], ZonesFound[data["_udn"]]
            )

    listener = SsdpAdvertisementListener(
        on_alive=on_notify,
        source=None, # This will bind to all addresses on the host
    )
    _LOGGER.debug("starting listener for Leviosa motor shades")
    await listener.async_start()
    try:
        _LOGGER.debug("Letting Zones discovery run for 20 secs")
        await asyncio.sleep(20)
    except:
        _LOGGER.debug("exception: ")
        raise
    finally:
        await listener.async_stop()
        _LOGGER.debug("stopped discovery for Leviosa motor shades")
    return ZonesFound

class LeviosaZoneHub:
    """Represents and manages the interaction with a Leviosa Zone Hub"""

    def __init__(self, hub_ip, hub_name, loop=None, websession=None, timeout=15):
        self.hub_ip = hub_ip
        self.hub_name = hub_name
        self.hub_fw_v = "0.0.0"
        self.timeout = timeout
        self.groups = []
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        if websession:
            self.websession = websession
        else:
            self.websession = aiohttp.ClientSession()

    @property
    def fwVer(self):
        return self.hub_fw_v

    @property
    def name(self):
        return self.hub_name

    @property
    def BlindGroups(self):
        return self.groups

    async def post(self, url_frag: str):
        """
        POST a request to the Leviosa Zone HUB

        :param url_frag: string with the command fragment
        :return: nothing (at this moment all POSTed reqs expect nothin')
        """
        response = None
        try:
            url = "http://" + self.hub_ip + url_frag
            with async_timeout.timeout(self.timeout):
                _LOGGER.debug("url: %s", url)
                response = await self.websession.post(url)
                _LOGGER.debug("return code is: %d", response.status)
        except (asyncio.TimeoutError, aiohttp.ClientError) as error:
            _LOGGER.error("Failed to communicate with Leviosa hub: %s", error)
            raise LvsaApiConnectionError
        finally:
            if response is not None:
                await response.release()

    async def get(self, url_frag: str) -> dict:
        """
        Get a resource.

        :param url_frag: string with the request fragment
        :return: a dictionary with the HUB info
        """
        response = None
        url = "http://" + self.hub_ip + "/" + url_frag
        try:
            _LOGGER.debug("Sending GET request to: %s" % url)
            with async_timeout.timeout(self.timeout):
                response = await self.websession.get(url)
            if response.status == 200:
                data = await response.json(content_type=None)
                return data
            else:
                raise LvsaApiResponseStatusError(response.status)
        except (asyncio.TimeoutError, aiohttp.ClientError) as error:
            _LOGGER.error("Failed to communicate with Leviosa hub: %s", error)
            raise LvsaApiConnectionError
        finally:
            if response is not None:
                await response.release()

    async def getHubInfo(self):
        _LOGGER.debug("Getting HUB info from: %s", self.hub_ip)
        hub_resp = await self.get("")  # Query the root doc of the Hub to get Hub info
        if hub_resp:
            self.hub_fw_v = hub_resp["firmware"]
        else:
            self.hub_fw_v = "invalid"

    def AddGroup(self, GroupName):
        newGroup = LeviosaShadeGroup(len(self.groups), GroupName, self)
        _LOGGER.debug(
            "Added new Group %s(%d) to Leviosa hub: %s",
            GroupName,
            len(self.groups),
            self.hub_name,
        )
        self.groups.append(newGroup)
        # print(len(self.groups) )
        return newGroup


class LeviosaShadeGroup:
    can_move = True
    can_tilt = False

    def __init__(self, number, name, Hub: LeviosaZoneHub):
        self.Hub = Hub
        self.Number = number
        self.Name = name
        self.Position = 0

    @property
    def name(self):
        return self.Name

    @property
    def number(self):
        return self.Number

    @property
    def position(self):
        return self.Position

    async def move(self, target_position):
        if target_position == 0:
            command = "close"
            self.Position = 0
        else:
            command = "open"
            self.Position = 100
        command = "/command/" + command + "/" + str(self.Number)
        _LOGGER.debug(
            "Setting cover.%s to position: %d",
            self.Name,
            self.Position,
        )
        result = await self.Hub.post(command)
        return result

    async def move_next_pos(self, direction):
        if direction:
            command = "down"
        else:
            command = "up"
        self.Position = 50
        _LOGGER.debug(
            "Moving cover.%s to next %s poisition",
            self.Name,
            self.Position,
        )
        command = "/command/" + command + "/" + str(self.Number)
        result = await self.Hub.post(command)
        return result

    async def close(self):
        return await self.move(0)

    async def down(self):
        return await self.move_next_pos(True)

    async def open(self):
        return await self.move(100)

    async def up(self):
        return await self.move_next_pos(False)

    async def stop(self):
        """Stop the shade."""
        command = "/command/stop/" + str(self.Number)
        _LOGGER.debug("stopping cover.%s", self.Name)
        return await self.Hub.post(command)
