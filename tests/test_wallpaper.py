from context import libdesktop
import os

def test_wallpaper_get_wallpaper():

	print('The desktop wallpaper is:', libdesktop.wallpaper.get_wallpaper())

def test_wallpaper_set_wallpaper():

	original_wallpaper = libdesktop.wallpaper.get_wallpaper()

	print('The wallpaper is:', libdesktop.wallpaper.get_wallpaper())

	print('Setting it to: test_desktop_bg.png')

	libdesktop.wallpaper.set_wallpaper(os.path.abspath('test_desktop_bg.jpg'))

	print('Image credit: Felipe Santana (Unsplash)')

	print('It is now:', libdesktop.wallpaper.get_wallpaper())

	assert libdesktop.wallpaper.get_wallpaper() == os.path.abspath('test_desktop_bg.jpg')

	print('Restoring wallpaper to original.')

	libdesktop.wallpaper.set_wallpaper(original_wallpaper)


