# aioleviosa
 ## Async communication with Leviosa Zone Hubs

 This module allows communication to Leviosa Motor Blinds Zone hubs. Mainly designed for Home Assistant, but should be usable for any other purpose. Exposed functionality is:
 
 **1. discover_leviosa_zones**: This function listens for 20 seconds for any available Leviosa Zones and returns a dictionary of all found hubs, composed of the hub's unique identifier (last part is the hub's MAC address) and the Hub's IP address. Receives no parameters. The Zone hub has a partial implementation of SSDP, as it only advertises, and does not respond to M-SEARCH, making this custom discovery function necessary. 

 **2. LeviosaZoneHub**. Instantiate this class to represent one Leviosa Zone, and then Add the Blind Group names to it using **AddGroup(GroupName)** This method will return a reference to an instance of a LeviosaShadeGroup. 

 **3. LeviosaShadeGroup**. There are methods to Open, Close and Stop the shades, as well as a methods to move to the next predefined step up or down. Do not instantiate this class, instead use AddGroup() from the LeviosaZoneHub class

 *See the included test file for more details on usage.*
