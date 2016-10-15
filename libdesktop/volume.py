# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import subprocess as sp
from libdesktop import system

def set(percentage):

	'''Set the volume.

	Sets the volume to a given percentage (integer between 0 and 100).

	Args:
		percentage (int): The percentage (as a 0 to 100 integer) to set the volume to.
	'''

	if system.get_name() == 'windows':
		pass  # TODO: Implement volume for Windows. Looks like WinAPI is the solution...

	elif system.get_name() == 'mac':
		# OS X uses 0-10 instead of percentage
		volume_int = percentage / 10

		sp.Popen(['osascript', '-e', 'set Volume %d' % volume_int]).wait()

	else:
		# Linux/Unix
		formatted = str(percentage) + '%'
		sp.Popen(['amixer', '--quiet', 'sset', 'Master', formatted]).wait()

def get():

	'''Get the volume.

	Get the current volume.

	Returns:
		int: The current volume (percentage, between 0 and 100).
	'''

	if system.get_name() == 'windows':
		pass  # TODO: Implement volume for Windows. Looks like WinAPI is the solution...

	elif system.get_name() == 'mac':
		volume = system.get_cmd_out(['osascript', '-e', 'set ovol to output volume of (get volume settings); return the quoted form of ovol'])
		return int(volume) * 10

	else:
		# Linux/Unix
		volume = system.get_cmd_out('amixer get Master |grep % |awk \'{print $5}\'|sed -e \'s/\[//\' -e \'s/\]//\' | head -n1')
		return int(volume.replace('%', ''))

def increase(percentage):

	'''Increase the volume.

	Increase the volume by a given percentage.

	Args:
		percentage (int): The percentage (as an integer between 0 and 100) to increase the volume by.
	'''

	if system.get_name() == 'windows':
		pass  # TODO: Implement volume for Windows. Looks like WinAPI is the solution...

	elif system.get_name() == 'mac':
		volume_int = percentage / 10
		old_volume = get()

		new_volume = old_volume + volume_int

		if new_volume > 10:
			new_volume = 10

		set(new_volume * 10)

	else:
		# Linux/Unix
		formatted = '%d%%+' % percentage  # + or - increases/decreases in amixer

		sp.Popen(['amixer', '--quiet', 'sset', 'Master', formatted]).wait()

def decrease(percentage):

	'''Decrease the volume.

	Decrease the volume by a given percentage.

	Args:
		percentage (int): The percentage (as an integer between 0 and 100) to decrease the volume by.
	'''

	if system.get_name() == 'windows':
		pass  # TODO: Implement volume for Windows. Looks like WinAPI is the solution...

	elif system.get_name() == 'mac':
		volume_int = percentage / 10
		old_volume = get()

		new_volume = old_volume - volume_int

		if new_volume < 0:
			new_volume = 0

		set(new_volume * 10)

	else:
		# Linux/Unix
		formatted = '%d%%-' % percentage  # + or - increases/decreases in amixer

		sp.Popen(['amixer', '--quiet', 'sset', 'Master', formatted]).wait()

def unix_is_pulseaudio():

	'''Check if PulseAudio is running as sound server.

	Checks if `PulseAudio <https://www.freedesktop.org/wiki/Software/PulseAudio/>`_ is running as the sound server.

	Returns:
		bool: Is PulseAudio the sound server?
	'''

	return bool(system.is_running('pulseaudio'))

def mute():

	'''Mute the volume.

	Mutes the volume.
	'''

	# NOTE: mute != 0 volume

	if system.get_name() == 'windows':
		pass  # TODO: Implement volume for Windows. Looks like WinAPI is the solution...

	elif system.get_name() == 'mac':
		sp.Popen(['osascript', '-e', 'set volume output muted true']).wait()

	else:
		# Linux/Unix
		if unix_is_pulseaudio():
			sp.Popen(['amixer', '--quiet', '-D', 'pulse', 'sset', 'Master', 'mute']).wait()  # sset is *not* a typo

		else:
			sp.Popen(['amixer', '--quiet', 'sset', 'Master', 'mute']).wait()

def unmute():

	'''Unmute the volume.

	Unmutes the system volume.

	Note:
		On some systems, volume is restored to its previous level after unmute, or set to 100.
	'''

	if system.get_name() == 'windows':
		pass  # TODO: Implement volume for Windows. Looks like WinAPI is the solution...

	elif system.get_name() == 'mac':
		sp.Popen(['osascript', '-e', 'set volume output muted false']).wait()

	else:
		# Linux/Unix
		if unix_is_pulseaudio():
			sp.Popen(['amixer', '--quiet', '-D', 'pulse', 'sset', 'Master', 'unmute']).wait()  # sset is *not* a typo

		else:
			sp.Popen(['amixer', '--quiet', 'sset', 'Master', 'unmute']).wait()

def is_muted():

	'''Check if volume is muted.

	Checks if the volume is muted.

	Note:
		This does *not* check for volume == 0.

	Returns:
		bool: Is the volume muted?
	'''

	if system.get_name() == 'windows':
		pass  # TODO: Implement volume for Windows. Looks like WinAPI is the solution...

	elif system.get_name() == 'mac':
		return system.get_cmd_out(['osascript', '-e', 'set ismuted to volume output muted; return ismuted']) == 'true'

	else:
		# Linux/Unix
		return system.get_cmd_out('amixer get Master | awk \'$0~/%/{print $6}\' | tr -d \'[]\' | head -n1') != 'on'

