Modules in libdesktop
=====================

libdesktop has an array[] of different modules.

Here is a list of them, with descriptions.

libdesktop.applications
-----------------------

Use for interacting with the system's installed applications.

This handles things like launching/getting default/user-preffered apps. Also has a OS X-specific function: `mac_app_exists()`.


libdesktop.startup
------------------

Use for interacting with user startup.

This handles listing, adding and removing of applications to run at startup.

libdesktop.wallpaper
--------------------

This handles getting and setting of the wallpaper.

libdesktop.system
-----------------

Functions for the system in general.

This handles things like processes, executables, system name and configuration directories.

libdesktop.desktopfile
----------------------

Use for processing .desktop files.

This handles execution, parsing, location and construction of .desktop files.
