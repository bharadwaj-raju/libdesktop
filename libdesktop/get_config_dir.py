# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import os

def get_config_dir(app_name=''):

		if 'XDG_CONFIG_HOME' in os.environ:

			config_home = os.getenv('XDG_CONFIG_HOME')

		elif 'APPDATA' in os.environ:  # On Windows

			config_home = os.getenv('APPDATA')

		else:

			try:

				from xdg import BaseDirectory
				config_home =  BaseDirectory.xdg_config_home

			except ImportError:  # Most likely a Linux/Unix system anyway

				config_home = os.path.expanduser('~/.config')

		if app_name == '':

			return config_home

		else:

			if os.path.isdir(os.path.join(config_home, app_name)):

				return os.path.join(config_home, app_name)

			else:

				return os.path.join(os.path.expanduser('~'), '.' + app_name)
