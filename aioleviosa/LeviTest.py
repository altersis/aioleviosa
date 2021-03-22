''' Test for the Leviosa Motor Shades base classes
    
    The below code will search for Leviosa Zones for 20 seconds, 
    then will connect to the first Zone found and iterate through
    all shade Groups, issuing Open/Close/Down/Up/Stop               '''

import asyncio
import time

import aiohttp
import aioleviosa as lev


async def Test(loop):
    session = aiohttp.ClientSession()
    print("Looking for Leviosa Zones (20 seconds)")
    zones_found = await lev.discover_leviosa_zones()
    print("Leviosa Zones found: ", zones_found)
    addresses = list(zones_found.values())
    if len(addresses) > 0:
        print("Testing with: ", addresses[0])
        hub = lev.LeviosaZoneHub(addresses[0], "FirstHubFound", loop, session)
        print("Hub created")
        await hub.getHubInfo()
        print("GetInfo should be done now")
        print("version:", hub.fwVer)
        hub.AddGroup("All groups") # Group 0 means all groups in the Zone hub
        hub.AddGroup("Group ONE")
        hub.AddGroup("Group TWO")
        hub.AddGroup("Group THREE")
        hub.AddGroup("Group FOUR")
        hub.AddGroup("Group FIVE")
        hub.AddGroup("Group SIX")
        BG_num = len(hub.groups)
        print("Number of Blind Groups: ", BG_num)
        for BlindGroup in hub.groups:
            print("\n")
            print(BlindGroup.name)
            print("Opening")
            await BlindGroup.open()
            time.sleep(2)
            print("Stopping")
            await BlindGroup.stop()
            time.sleep(2)
            print("Closing")
            await BlindGroup.close()
            print("Next up position")
            await BlindGroup.up()
            time.sleep(2)
            print("Next down position")
            await BlindGroup.down()
            time.sleep(5)
    else:
        print("No Zones found, nothing to test")
    print("End of run")
    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(Test(loop))
