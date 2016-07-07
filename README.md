# libdesktop

A cross-platform library for miscellaneous OS functions and conveniences.

License: MIT

*NOTE:* This library is not related *in any way* to `libdesktop-agnostic`.

# Usage

Install:

```bash
$ pip install libdesktop
```

You may need to use `sudo -H`.

Simply:

```python
import libdesktop
```
and call functions. See [documentation](#documentation)

# Documentation

- [`start_terminal_emulator()`](#start_terminal_emulator)
- [`start_gui_text_editor()`](#start_gui_text_editor)
- [`get_desktop_environment()`](#get_desktop_environment)
- [`set_desktop_wallpaper()`](#set_desktop_wallpaper)
- [`linux_exec_desktop_file()`](#linux_exec_desktop_file)
- [`is_running()`](#is_running)
- [`get_config_dir()`](#get_config_dir)

## `start_terminal_emulator()`

```python
start_terminal_emulator(background=False, exec_cmd='', shell_after_cmd_exec=False)
```

Starts a suitable Terminal based on user's OS and desktop environment.

- If `background` is `True`, then the Terminal process starts in the background.
- If `exec_cmd` is specified, the Terminal is started and the `exec_cmd` string is run as a script.
- If `shell_after_cmd_exec` is `True`, user's default shell is started after running `exec_cmd`

Returns: nothing

## `start_gui_text_editor()`

```python
start_gui_text_editor(file='')
```

Start the user's default plain-text editor.
Optionally launch to edit `file`(s), which should be a `str` of a full path to text file(s).

Returns: nothing

## `get_desktop_environment()`

```python
get_desktop_environment()
```

Get the user's desktop environment (Linux/Unix) or OS (Windows/Mac).

Returns: `str`

## `set_desktop_wallpaper()`

```python
set_desktop_wallpaper(image)
```
Sets the user's wallpaper to `image` (should be `str` of a full path to image).

Returns: `bool` (`True`/`False` depends on success)

## `linux_exec_desktop_file()`

```python
linux_exec_desktop_file(desktop_file, *uris)
```

Execute the `desktop_file` (should be `str` of full path to `.desktop` file).
Any arguments after `desktop_file` is interpreted as a URI, opening `.desktop` file with the URI(s).

For example,

```python
linux_exec_desktop_file('/usr/share/applications/org.gnome.gedit.desktop', 'file1', 'file2')
```

will open Gedit (GNOME editor) with `file1` and `file2` open (these are specifed as URIs). Note that these must be full paths.

*NOTE:* As implied by the name, this works *only* on Linux, since the concept of `.desktop` files to specify apps is only on Linux desktop environments.

## `is_running()`

```python
is_running(process)
```
Check if `process` is running.

Returns: `bool`

## `get_config_dir()`

```python
get_config_dir(app_name='')
```

Get the user's configuration directory. If `app_name` is specified, get `app_name`'s configuration directory instead.
Assuming said app follows standards.

Returns: `str`
