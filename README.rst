Squid buildout recipe
======================

This package provides buildout_ recipes for the configuration of squid.

We use the system squid, this recipe will not install squid for you.  If
you wish to install squid, use `zc.recipe.cmmi`_ perhaps.

.. _buildout: http://pypi.python.org/pypi/zc.buildout
.. _`zc.recipe.cmmi`: http://pypi.python.org/pypi/zc.recipe.cmmi


Mandatory Parameters
--------------------

port
    The port this squid should listen on


Optional Parameters
-------------------

localnet
    A list of addresses that are allowed to access this proxy
safe-ports
    A list of ports that can be proxied
connect-safe-ports
    A list of ports that CONNECT is allowed for
refresh-patterns
    A list of refresh_patterns (as they are in the squid config)
default-refresh
    Rules that govern how long an object is confisdered fresh when it doesn't have a refresh-pattern.


Repository
----------

This software is available from our `recipe repository`_ on github.

.. _`recipe repository`: http://github.com/isotoma/recipes


License
-------

Copyright 2010 Isotoma Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

