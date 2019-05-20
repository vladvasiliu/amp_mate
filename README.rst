|Travis badge| |Style badge| |Docs badge| |License badge|


AMP_MATE
========

This project's goal is to create an interface between HiFi amplifiers and various sources.

It will allow :
* Control of amplifier volume by the player (and its app).
* Turn the amp on/off or set the correct source on player events.
* Have the player know what the amplifier is doing, e.g. stop playback when the amplifier is turned off or the input is
changed.

This is mainly tested with a Rotel amp and Volumio players, but is designed to be an abstract bridge between the two and
handle plugins for other amps and players.


Why not use Command4 or other home automation systems?
------------------------------------------------------

This is supposed to be simple. The principle is that the player and the amplifier are supposed to be the same unit. Some
 manufacturers offer all-in-products, but if you happen to have higher-end equipment, this no longer works unless all
 your components are from the same manufacturer.

From a home automation standpoint, the combination of Player & Amp should be a single unit. The amp in this scenario is
basically "dumb". **amp_mate** is the glue that binds the player to the amp.


Useful documentation
--------------------
* `Volumio Websocket API <https://volumio.github.io/docs/Development_How_To/Overview.html>`_
* `Rotel command reference <http://rotel.com/manuals-resources/rs232-protocols>`_

.. |Travis badge| image:: https://img.shields.io/travis/vladvasiliu/amp_mate.svg
   :target: https://travis-ci.org/vladvasiliu/amp_mate
.. |Style badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
.. |License badge| image:: https://img.shields.io/github/license/vladvasiliu/amp_mate.svg
   :target: LICENSE
.. |Docs badge| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
   :target: https://amp-mate.readthedocs.io
