# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>


# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import os
import sys
import subprocess as sp

try:
	import configparser
except ImportError:
	import ConfigParser as configparser

import traceback
import ctypes
from libdesktop import system
import tempfile
import shutil
import subprocess as sp

def get():

	'''Get the desktop wallpaper.

	Get the current desktop wallpaper.

	Returns:
		str: The path to the current wallpaper.
	'''

	desktop_env = system.get_name()

	if desktop_env in ['gnome', 'unity', 'cinnamon', 'pantheon', 'mate']:
		SCHEMA = 'org.gnome.desktop.background'
		KEY = 'picture-uri'

		if desktop_env == 'mate':
			SCHEMA = 'org.mate.background'
			KEY = 'picture-filename'

		try:
			from gi.repository import Gio

			gsettings = Gio.Settings.new(SCHEMA)
			return gsettings.get_string(KEY).replace('file://', '')
		except ImportError:
			try:
				return system.get_cmd_out(['gsettings', 'get', SCHEMA, KEY]).replace('file://', '')
			except:  # MATE < 1.6
				return system.get_cmd_out(['mateconftool-2', '-t', 'string', '--get', '/desktop/mate/background/picture_filename']).replace('file://', '')

	elif desktop_env == 'gnome2':
		args = ['gconftool-2', '-t', 'string', '--get', '/desktop/gnome/background/picture_filename']
		return system.get_cmd_out(args).replace('file://', '')

	elif desktop_env == 'kde':
		pass  # TODO: Implement wallpaper.get() for KDE. Possibly derive from set()

	elif desktop_env=='xfce4':
		# XFCE4's image property is not image-path but last-image (What?)

		list_of_properties = system.get_cmd_out(['xfconf-query', '-R', '-l', '-c', 'xfce4-desktop', '-p', '/backdrop'])

		for i in list_of_properties.split('\n'):
			if i.endswith('last-image') and 'workspace' in i:
				# The property given is a background property
				return system.get_cmd_out(['xfconf-query', '-c', 'xfce4-desktop', '-p', i])

	elif desktop_env=='razor-qt':
		desktop_conf = configparser.ConfigParser()
		# Development version

		desktop_conf_file = os.path.join(get_config_dir('razor')[0], 'desktop.conf')

		if os.path.isfile(desktop_conf_file):
			config_option = r'screens\1\desktops\1\wallpaper'

		else:
			desktop_conf_file = os.path.join(os.path.expanduser('~'),'.razor/desktop.conf')
			config_option = r'desktops\1\wallpaper'

		desktop_conf.read(os.path.join(desktop_conf_file))
		try:
			if desktop_conf.has_option('razor', config_option):  # only replacing a value
				return desktop_conf.get('razor',config_option)
		except:
			pass


	elif desktop_env in ['fluxbox', 'jwm', 'openbox', 'afterstep', 'i3']:
		# feh stores last feh command in '~/.fehbg'
		# parse it
		with open(os.path.expanduser('~/.fehbg')) as f:
			fehbg = f.read()

		fehbg = fehbg.split('\n')

		for line in fehbg:
			if '#!' in line:
				fehbg.remove(line)

		fehbg = fehbg[0]

		for i in fehbg.split(' '):
			if not i.startswith("-"):
				if not i.startswith('feh'):
					if not i in ['', ' ', '  ', '\n']:
						return(i.replace("'", ''))

	# TODO: way to get wallpaper for desktops which are commented-out below
	# elif desktop_env == 'icewm':
	# 	args = ['icewmbg', image]
	# 	sp.Popen(args)
	#
	# elif desktop_env == 'blackbox':
	# 	args = ['bsetbg', '-full', image]
	# 	sp.Popen(args)
	#
	# elif desktop_env == 'lxde':
	# 	args = 'pcmanfm --set-wallpaper %s --wallpaper-mode=scaled' % image
	# 	sp.Popen(args, shell=True)
	#
	# elif desktop_env == 'lxqt':
	# 	args = 'pcmanfm-qt --set-wallpaper %s --wallpaper-mode=scaled' % image
	# 	sp.Popen(args, shell=True)
	#
	# elif desktop_env == 'windowmaker':
	# 	args = 'wmsetbg -s -u %s' % image
	# 	sp.Popen(args, shell=True)
	#
	# elif desktop_env == 'enlightenment':
	#    args = 'enlightenment_remote -desktop-bg-add 0 0 0 0 %s' % image
	#    sp.Popen(args, shell=True)
	#
	# elif desktop_env == 'awesome':
	# 	with sp.Popen("awesome-client", stdin=sp.PIPE) as awesome_client:
	# 		command = 'local gears = require("gears"); for s = 1, screen.count() do gears.wallpaper.maximized("%s", s, true); end;' % image
	# 		awesome_client.communicate(input=bytes(command, 'UTF-8'))

	elif desktop_env == 'windows':
			WINDOWS_SCRIPT = 'reg query "HKEY_CURRENT_USER\Control Panel\Desktop\Desktop"'

			return system.get_cmd_out(WINDOWS_SCRIPT)

	elif desktop_env == 'mac':
		try:
			from appscript import app
			app('Finder').desktop_picture.get()
		except ImportError:
			OSX_SCRIPT = 'tell app "finder" to get posix path of (get desktop picture as alias)'

			return system.get_cmd_out(['osascript', OSX_SCRIPT])
def set(image):

	'''Set the desktop wallpaper.

	Sets the desktop wallpaper to an image.

	Args:
		image (str): The path to the image to be set as wallpaper.
	'''

	desktop_env = system.get_name()

	if desktop_env in ['gnome', 'unity', 'cinnamon', 'pantheon', 'mate']:
		uri = 'file://%s' % image

		SCHEMA = 'org.gnome.desktop.background'
		KEY = 'picture-uri'

		if desktop_env == 'mate':
			uri = image

			SCHEMA = 'org.mate.background'
			KEY = 'picture-filename'

		try:
			from gi.repository import Gio

			gsettings = Gio.Settings.new(SCHEMA)
			gsettings.set_string(KEY, uri)
		except ImportError:
			try:
				gsettings_proc = p.Popen(['gsettings', 'set', SCHEMA, KEY, uri])
			except:  # MATE < 1.6
				sp.Popen(['mateconftool-2','-t','string','--set','/desktop/mate/background/picture_filename','%s' % image], stdout=sp.PIPE)
			finally:
				gsettings_proc.communicate()

				if gsettings_proc.returncode != 0:
					sp.Popen(['mateconftool-2','-t','string','--set','/desktop/mate/background/picture_filename','%s' % image])

	elif desktop_env == 'gnome2':
		args = ['gconftool-2','-t','string','--set','/desktop/gnome/background/picture_filename', '%s' % image]
		sp.Popen(args)

	elif desktop_env == 'kde':
		# This probably only works in Plasma 5+
		sp.Popen(['''qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
						var allDesktops = desktops();
						print (allDesktops);
						for (i=0;i<allDesktops.length;i++) {{
							d = allDesktops[i];
							d.wallpaperPlugin = "org.kde.image";
							d.currentConfigGroup = Array("Wallpaper",
														"org.kde.image",
														"General");
							d.writeConfig("Image", "file:///%s")
						}}
					''' % image], shell=True)

	elif desktop_env in ['kde3', 'trinity']:
		args = 'dcop kdesktop KBackgroundIface setWallpaper 0 "%s" 6' % image
		sp.Popen(args,shell=True)

	elif desktop_env == 'xfce4':
		# XFCE4's image property is not image-path but last-image (What?)

		list_of_properties = sp.check_output(['bash -c "xfconf-query -R -l -c xfce4-desktop -p /backdrop"'], shell=True)
		list_of_properties = list_of_properties.decode('utf-8')

		for i in list_of_properties.split('\n'):
			if i.endswith('last-image'):
				# The property given is a background property
				sp.Popen(
					['xfconf-query -c xfce4-desktop -p %s -s "%s"' % (i, image)],
					shell=True)

				sp.Popen(['xfdesktop --reload'], shell=True)

	elif desktop_env == 'razor-qt':
		desktop_conf = configparser.ConfigParser()
		# Development version

		desktop_conf_file = os.path.join(get_config_dir('razor')[0], 'desktop.conf')

		if os.path.isfile(desktop_conf_file):
			config_option = r'screens\1\desktops\1\wallpaper'

		else:
			desktop_conf_file = os.path.join(os.path.expanduser('~'),'.razor/desktop.conf')
			config_option = r'desktops\1\wallpaper'

		desktop_conf.read(os.path.join(desktop_conf_file))
		try:
			if desktop_conf.has_option('razor',config_option):  # only replacing a value
				desktop_conf.set('razor',config_option,image)
				with codecs.open(desktop_conf_file, 'w', encoding='utf-8', errors='replace') as f:
					desktop_conf.write(f)
		except:
			pass


	elif desktop_env in ['fluxbox','jwm','openbox','afterstep', 'i3']:
		try:
			args = ['feh','--bg-scale', image]
			sp.Popen(args)
		except:
			sys.stderr.write('Error: Failed to set wallpaper with feh!')
			sys.stderr.write('Please make sre that You have feh installed.')

	elif desktop_env == 'icewm':
		args = ['icewmbg', image]
		sp.Popen(args)

	elif desktop_env == 'blackbox':
		args = ['bsetbg', '-full', image]
		sp.Popen(args)

	elif desktop_env == 'lxde':
		args = 'pcmanfm --set-wallpaper %s --wallpaper-mode=scaled' % image
		sp.Popen(args, shell=True)

	elif desktop_env == 'lxqt':
		args = 'pcmanfm-qt --set-wallpaper %s --wallpaper-mode=scaled' % image
		sp.Popen(args, shell=True)

	elif desktop_env == 'windowmaker':
		args = 'wmsetbg -s -u %s' % image
		sp.Popen(args, shell=True)

	elif desktop_env == 'enlightenment':
	   args = 'enlightenment_remote -desktop-bg-add 0 0 0 0 %s' % image
	   sp.Popen(args, shell=True)

	elif desktop_env == 'awesome':
		with sp.Popen("awesome-client", stdin=sp.PIPE) as awesome_client:
			command = 'local gears = require("gears"); for s = 1, screen.count() do gears.wallpaper.maximized("%s", s, true); end;' % image
			awesome_client.communicate(input=bytes(command, 'UTF-8'))

	elif desktop_env == 'windows':
			WINDOWS_SCRIPT = '''reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d  %s /f

rundll32.exe user32.dll,UpdatePerUserSystemParameters
''' % image

			windows_script_file = os.path.join(tempfile.gettempdir(), 'wallscript.bat')

			with open(windows_script_file, 'w') as f:
				f.write(WINDOWS_SCRIPT)

			sp.Popen([windows_script_file], shell=True)

			# Sometimes the method above works
			# and sometimes the one below

			SPI_SETDESKWALLPAPER = 20
			ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image , 0)

	elif desktop_env == 'mac':
		try:
			from appscript import app, mactypes
			app('Finder').desktop_picture.set(mactypes.File(image))
		except ImportError:
			OSX_SCRIPT = '''tell application "System Events"
                                   set desktopCount to count of desktops
                                     repeat with desktopNumber from 1 to desktopCount
                                       tell desktop desktopNumber
                                         set picture to POSIX file "%s"
                                       end tell
                                     end repeat
                                 end tell''' % image

			sp.Popen(['osascript', OSX_SCRIPT])
	else:
		try:
			sp.Popen(['feh', '--bg-scale', image])
			# feh is nearly a catch-all for Linux WMs
		except:
			pass
