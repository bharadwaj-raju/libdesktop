# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import os
import sys
import subprocess as sp
import tempfile
import shutil
import configparser
import traceback
import ctypes
from .get_desktop_environment import get_desktop_environment
from .get_config_dir import get_config_dir

def set_desktop_wallpaper(image):

	desktop_env = get_desktop_environment()

	try:

		if desktop_env in ['gnome', 'unity', 'cinnamon', 'pantheon']:

			uri = 'file://%s' % image

			try:

				from gi.repository import Gio

				SCHEMA = 'org.gnome.desktop.background'
				KEY = 'picture-uri'
				gsettings = Gio.Settings.new(SCHEMA)

				gsettings.set_string(KEY, uri)

			except:

				args = ['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', uri]
				sp.Popen(args)

		elif desktop_env == 'mate':

			try: # MATE >= 1.6

				args = ['gsettings', 'set', 'org.mate.background', 'picture-filename', '%s' % image]
				sp.Popen(args)

			except: # MATE < 1.6

				args = ['mateconftool-2','-t','string','--set','/desktop/mate/background/picture_filename','%s' % image]
				sp.Popen(args)

		elif desktop_env == 'gnome2':

			args = ['gconftool-2','-t','string','--set','/desktop/gnome/background/picture_filename', '%s' % image]
			sp.Popen(args)

		elif desktop_env == 'kde':

			# The KDE 4+ method of changing *anything* in the CLI is either
			# non-existent or deprecated or horribly convoluted.
			# There have been long-open bugs (5 yrs and counting) but no fix.

			old_working_dir = os.getcwd()

			if not os.path.isdir(os.path.join(os.path.expanduser('~'), '.wall_slide_kde')):

				os.mkdir(os.path.join(os.path.expanduser('~'), '.wall_slide_kde'))

			os.chdir(os.path.join(os.path.expanduser('~'), '.wall_slide_kde'))

			for dirpath, dirnames, files in os.walk('.'):

				if files:

					for file in os.listdir('.'):

						os.remove(file)

			kde_random_image = tempfile.NamedTemporaryFile(delete=False)

			shutil.copyfile(image, kde_random_image.name)

			os.chdir(old_working_dir)

		elif desktop_env in ['kde3', 'trinity']:

			args = 'dcop kdesktop KBackgroundIface setWallpaper 0 "%s" 6' % image
			sp.Popen(args,shell=True)

		elif desktop_env=='xfce4':

			# XFCE4's image property is not image-path but last-image (What?)

			list_of_properties_cmd = sp.Popen(['bash -c "xfconf-query -R -l -c xfce4-desktop -p /backdrop"'], shell=True, stdout=sp.PIPE)

			list_of_properties, list_of_properties_err = list_of_properties_cmd.communicate()

			list_of_properties = list_of_properties.decode('utf-8')

			for i in list_of_properties.split('\n'):

				if i.endswith('last-image'):

					# The property given is a background property
					sp.Popen(
						['xfconf-query -c xfce4-desktop -p %s -s "%s"' % (i, image)],
						shell=True)

					sp.Popen(['xfdesktop --reload'], shell=True)

		elif desktop_env=='razor-qt':

			desktop_conf = configparser.ConfigParser()
			# Development version

			desktop_conf_file = os.path.join(get_config_dir('razor'),'desktop.conf')

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

			except: pass


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
				awesome_client.communicate(input=bytes(command, 'UTF-8'));

		elif desktop_env == 'windows':

				WIN_SCRIPT = '''reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d  %s /f

rundll32.exe user32.dll,UpdatePerUserSystemParameters
''' % image

				win_script_file = os.path.join(tempfile.gettempdir(), 'wallscript.bat')

				with open(win_script_file, 'w') as f:

					f.write(WIN_SCRIPT)

				sp.Popen([win_script_file], shell=True)

				# Sometimes the method above works
				# and sometimes the one below

				SPI_SETDESKWALLPAPER = 20
				ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image , 0)

		elif desktop_env == 'mac':

			try:

				from appscript import app, mactypes

				app('Finder').desktop_picture.set(mactypes.File(image))

			except ImportError:

				OSX_SCRIPT = '''tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
				''' % image

				osx_script_file = os.path.join(tempfile.gettempdir(), 'wallscript.AppleScript')

				with open(osx_script_file, 'w') as f:

					f.write(OSX_SCRIPT)

				sp.Popen(['/usr/bin/osascript', osx_script_file])
		else:

			sys.stderr.write('Error: Failed to set wallpaper. (Desktop not supported)')

			return False

		return True

	except:

		print(traceback.format_exc())

		return False
