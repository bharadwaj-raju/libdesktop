# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import sys
import os
from .is_running import is_running

def get_desktop_environment():

	if sys.platform in ['win32', 'cygwin']:

		return 'windows'

	elif sys.platform == 'darwin':

		return 'mac'

	else:

		desktop_session = os.environ.get('XDG_CURRENT_DESKTOP') or os.environ.get('DESKTOP_SESSION')

		if desktop_session is not None:

			desktop_session = desktop_session.lower()

			# Fix for X-Cinnamon etc

			if desktop_session.startswith('x-'):

				desktop_session = desktop_session.replace('x-', '')

			if desktop_session in ['gnome','unity', 'cinnamon', 'mate',
									'xfce4', 'lxde', 'fluxbox',
								   'blackbox', 'openbox', 'icewm', 'jwm',
								   'afterstep','trinity', 'kde', 'pantheon',
								   'i3', 'lxqt', 'awesome', 'enlightenment']:

				return desktop_session

			#-- Special cases --#

			# Canonical sets environment var to Lubuntu rather than
			# LXDE if using LXDE.
			# There is no guarantee that they will not do the same
			# with the other desktop environments.

			elif 'xfce' in desktop_session:

				return 'xfce4'

			elif desktop_session.startswith('ubuntu'): return 'unity'

			elif desktop_session.startswith('xubuntu'): return 'xfce4'

			elif desktop_session.startswith('lubuntu'): return 'lxde'

			elif desktop_session.startswith('kubuntu'):  return 'kde'

			elif desktop_session.startswith('razor'): return 'razor-qt'

			elif desktop_session.startswith('wmaker'): return 'windowmaker'

		if os.environ.get('KDE_FULL_SESSION') == 'true':

			return 'kde'

		elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):

			if not 'deprecated' in os.environ.get('GNOME_DESKTOP_SESSION_ID'):

				return 'gnome2'

		elif is_running('xfce-mcs-manage'): return 'xfce4'
		elif is_running('ksmserver'): return 'kde'

	return 'unknown'
