from context import libdesktop
import sys
import os

def test_volume_get_volume():

	print('The current volume is:', libdesktop.volume.get_volume())

def test_volume_set_volume():

	print('Setting volume to 100%')
	libdesktop.volume.set_volume(100)

	print('It is now:', libdesktop.volume.get_volume())

	assert libdesktop.volume.get_volume() == 100

	print('Setting volume to 53%')
	libdesktop.volume.set_volume(53)

	print('It is now:', libdesktop.volume.get_volume())

	assert libdesktop.volume.get_volume() == 53

	print('Setting volume back to 100%')
	libdesktop.volume.set_volume(100)

def test_volume_increase_volume():

	print('Current volume:', libdesktop.volume.get_volume())

	print('Setting volume to 50%')
	libdesktop.volume.set_volume(50)

	print('Increasing volume by 25%')
	libdesktop.volume.increase_volume(25)

	print('It is now:', libdesktop.volume.get_volume())

	assert libdesktop.volume.get_volume() == 75

def test_volume_decrease_volume():

	print('Current volume:', libdesktop.volume.get_volume())

	print('Setting volume to 50%')
	libdesktop.volume.set_volume(50)

	print('Decreasing volume by 25%')
	libdesktop.volume.decrease_volume(25)

	print('It is now:', libdesktop.volume.get_volume())

	assert libdesktop.volume.get_volume() == 25

def test_volume_unix_is_pulseaudio_server():

	print('The PulseAudio sound server %s' % 'is running' if libdesktop.volume.unix_is_pulseaudio_server() else 'is not running.')

def test_volume_mute():

	print('Muting volume.')

	libdesktop.volume.mute()

	assert libdesktop.volume.is_muted() is True

def test_volume_is_muted():

	print('The volume %s' % 'is muted' if libdesktop.volume.is_muted() else 'is not muted.')

def test_volume_unmute():

	print('Muting volume.')

	libdesktop.volume.mute()

	print('Unmuting volume.')

	libdesktop.volume.unmute()

	assert libdesktop.volume.is_muted() is False

	print('-' * 50)


