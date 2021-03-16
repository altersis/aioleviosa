# aioleviosa
 ## Async communication with Leviosa Motor Shades

 This module allows communication to a Leviosa Motor Blinds Zone hub. Although mainly designed to be used with Home Assistant, should be usable for any other purpose. 
 
 **1. discover_leviosa_zones**: This function listens for 20 seconds for any available Leviosa Zones and returns a dictionary of all found hubs, composed of the hub's unique identifier (last part is the hub's MAC address) and the Hub's IP address. Receives no parameters.

 **2. LeviosaZoneHub**. Instantiate this class to represent one Leviosa Zone, and then Add the Blind Group names to it using **AddGroup(GroupName)** This method will return a reference to an instance of a LeviosaShadeGroup. 

 **3. LeviosaShadeGroup**. There are methods to Open, Close and Stop the shades, as well as a methods to move to the next predefined step up or down. Do not instantiate this class, instead use AddGroup() from the LeviosaZoneHub class
