from distutils.core import setup
setup(
  name = 'aioleviosa',         # How you named your package folder (MyLib)
  packages = ['aioleviosa'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='APACHE 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'AsyncIO compatible library to talk to a Leviosa Motor Shades Zone',   # Give a short description about your library
  author = 'Gerardo Castillo',                   # Type in your name
  author_email = 'gcastillo@integrahome.net',      # Type in your E-Mail
  url = 'https://github.com/altersis/aioleviosa',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/altersis/aioleviosa/aioleviosa_01.tar.gz',    # I explain this later on
  keywords = ['AIO', 'AsyncIO', 'Leviosa Zone'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'asyncio',
          'ipaddress',
          'logging',
          'typing',
          'aiohttp',
          'async_timeout',
          'async_upnp_client'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)


import asyncio
from ipaddress import IPv4Address
import logging
from typing import Any, Mapping, Optional, Sequence, Tuple, Union

import aiohttp
import async_timeout
from async_upnp_client.advertisement 