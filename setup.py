from distutils.core import setup
setup(
  name = 'aioleviosa',         # This package talks to a Leviosa Zone hub
  packages = ['aioleviosa'],   
  version = '0.3.5',           # Use source param in SsdpAdvertisementListener()
  license='APACHE 2.0',        # https://help.github.com/articles/licensing-a-repository
  description = 'AsyncIO compatible library to talk to a Leviosa Motor Shades Zone',   
  author = 'Gerardo Castillo',
  author_email = 'gcastillo@integrahome.net',
  url = 'https://github.com/altersis/aioleviosa',   
  download_url = 'https://github.com/altersis/aioleviosa/archive/refs/tags/0.3.0.tar.gz',
  keywords = ['Communication', 'AsyncIO', 'Leviosa Zone'],   
  install_requires=[
          'aiohttp>=3.7.4',
          'async_timeout>=3.0',
          'async_upnp_client>=0.22.11' # This package is also used by HASS for SSDP
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',   # "3 - Alpha", "4 - Beta" or "5 - Production/Stable" 
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
