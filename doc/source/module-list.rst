Description of the Modules
==========================

libdesktop has an array[] of different modules.

Here is a list of them, with descriptions.

libdesktop.applications
-----------------------

`Documentation <applications.html>`_

Use for interacting with the system's installed applications.

This handles things like launching/getting default/user-preffered apps. Also has a OS X-specific function: `mac_app_exists()`.


libdesktop.startup
------------------

`Documentation <startup.html>`_

Use for interacting with user startup.

This handles listing, adding and removing of applications to run at startup.

libdesktop.wallpaper
--------------------

`Documentation <wallpaper.html>`_

This handles getting and setting of the wallpaper.

libdesktop.system
-----------------

`Documentation <system.html>`_

Functions for the system in general.

This handles things like processes, executables, system name and configuration directories.

libdesktop.desktopfile
----------------------

`Documentation <desktopfile.html>`_

Use for processing .desktop files.

This handles execution, parsing, location and construction of .desktop files.

libdesktop.volume
-----------------

`Documentation <volume.html>`_

Functions for system volume.

Set, get, increase, decrease etc. the volume.

libdesktop.dialog
-----------------

`Documentation <dialog.html>`_

Native system dialogs for files, printing etc.
