CSV
===

Character Sheet Viewer allows you to focus on the rules you need for any RPG situation without carrying a briefcase of paper. Simply
by typing into the text box at the top, cards are filtered to provide only relevant rules in any situation.

Example:

* type `Powers Healing` to view powers with the healing keyword

* type `Pea Pro` to view cards relating to Peacemaker's Pronouncement

* type `feat` to view your feats, or `quest completed` to view completed quests.

Usage
=====

1. From the online D&D 4e Character Creator, select your character and export it. Convert it to JSON using any xml-to-json converter.

2. Navigate to the downloaded DND4e file and use the included converter python script to generate a reduced, focused, no-bs json file with
important character info.

3. Load `index.html` in a browser and load your character sheet file.

4. Cry when something doesn't work.

Alternatively, if you don't have your own character file,

1. Load `index.html` into a browser and load `pacha.json`.

IMPORTANT
=========

This is very much in alpha. Most of the code works barely according to some arcane rituals I performed getting the exported character sheet
into json, and converting that into smaller json, and then houseruling that into the current pacha.json file (My level 14 cleric is named
Pacha Rossa.)

LICENSES
========

* Packery used under GPL v3: http://packery.metafizzy.co/#commercial-licensing

* jQuery used under MIT License: https://jquery.org/license/

* D3 used under BSD License: d3js.org

* and other things too.
