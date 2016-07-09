# libdesktop

A cross-platform library for miscellaneous OS functions and conveniences.
Things, quirks and workarounds I've figured out, so you don't have to.

License: MIT

*NOTE:* This library is not related *in any way* to `libdesktop-agnostic`.

# Usage

Install:

```bash
$ pip3 install libdesktop
```

You may need to use `sudo -H` with this.

Windows and macOS users: replace `pip3` with `pip` or whatever the Python 3 `pip` is.

Simply:

```python
import libdesktop
```
and call functions. See [documentation](#documentation)

# Documentation

- [`add_to_system_startup()`](#add_to_system_startup)
- [`start_terminal_emulator()`](#start_terminal_emulator)
- [`start_gui_text_editor()`](#start_gui_text_editor)
- [`open_file_with_default_program()`](#open_file_with_default_program)
- [`get_desktop_environment()`](#get_desktop_environment)
- [`set_desktop_wallpaper()`](#set_desktop_wallpaper)
- [`linux_exec_desktop_file()`](#linux_exec_desktop_file)
- [`linux_create_desktop_file()`](#linux_create_desktop_file)
- [`restart_program()`](#restart_program)
- [`is_in_path`](#is_in_path)
- [`is_running()`](#is_running)
- [`get_config_dir()`](#get_config_dir)

## `add_to_system_startup()`

```python
libdesktop.add_to_system_startup(command, name, all_users=False, run_in_terminal=False)
```

Adds program to system startup/boot.

- If `all_users` is `True`, adds for all users (requires root access on OS X and Linux).
- If `run_in_terminal` is `True`, runs in Terminal on startup.

## `start_terminal_emulator()`

```python
libdesktop.start_terminal_emulator(background=False, exec_cmd='', shell_after_cmd_exec=False, return_cmd=False)
```

Starts a suitable Terminal based on user's OS and desktop environment.

- If `background` is `True`, then the Terminal process starts in the background.
- If `exec_cmd` is specified, the Terminal is started and the `exec_cmd` string is run as a script.
- If `shell_after_cmd_exec` is `True`, user's default shell is started after running `exec_cmd`
- If `return_cmd` is `True`, Terminal is not started, but command to start is returned, for further use or modification.

*NOTE:* some terminal emulators exit immediately after running command (`exec_cmd`). You might want to use `read` (\*nix) or `pause` (DOS) to keep it open.

Returns: `str` if `return_cmd`, otherwise nothing

## `start_gui_text_editor()`

```python
libdesktop.start_gui_text_editor(file='')
```

Start the user's default plain-text editor.
Optionally launch to edit `file`(s), which should be a `str` of a full path to text file(s).

Returns: nothing

## `open_file_with_default_program()`

```python
libdesktop.open_file_with_default_program(file)
```

Opens `file` (should be a `str` of full path to file) with the default program for it.

Returns: nothing

## `get_desktop_environment()`

```python
libdesktop.get_desktop_environment()
```

Get the user's desktop environment (Linux/Unix) or OS (Windows/Mac).

Returns: `str`

## `set_desktop_wallpaper()`

```python
libdesktop.set_desktop_wallpaper(image)
```
Sets the user's wallpaper to `image` (should be `str` of a full path to image).

Returns: `bool` (`True`/`False` depends on success)

## `linux_exec_desktop_file()`

```python
libdesktop.linux_exec_desktop_file(desktop_file, *uris)
```

Execute the `desktop_file` (should be `str` of full path to `.desktop` file).
Any arguments after `desktop_file` is interpreted as a URI, opening `.desktop` file with the URI(s).

For example,

```python
libdesktop.linux_exec_desktop_file('/usr/share/applications/org.gnome.gedit.desktop', 'file1', 'file2')
```

will open Gedit (GNOME editor) with `file1` and `file2` open (these are specified as URIs). Note that these must be full paths.

Returns: nothing

*NOTE:* As implied by the name, this works *only* on Linux, since the concept of `.desktop` files to specify apps is only on Linux desktop environments.

## `linux_create_desktop_file()`

```python
libdesktop.linux_create_desktop_file(name, execute, terminal=False, additional_opts=None, filename='', return_str=False)
```

Creates a new `.desktop` file from parameters.

The new `.desktop` file's

- `Name` parameter will be `name`
- `Exec` parameter will be `execute`
- `Terminal` parameter will be based on if `terminal` is `True` or `False`.

Additional options can be specified as lists in the form:

```python
additional_opts = ['GenericName=Something', 'Version=3.0']
```

etc.

By default it will write the resulting `.desktop` into specified `filename`, but if `return_str` is `True`, will return resulting `.desktop` as a `str`.

Returns: `str` if `return_str` is `True`, otherwise nothing.

*NOTE:* As implied by the name, the result works *only* on Linux, since the concept of `.desktop` files to specify apps is only on Linux desktop environments.

## `restart_program()`

```python
libdesktop.restart_program(additional_args=None, remove_args=None)
```
Restart current process/script and

- If `additional_args` list is specified, restart, with additional arguments. `additional_args` must be such: `additional_args=['--option', 'option2']` etc.

- If `remove_args` list is specified, restart, with removed arguments. `remove_args` must be such: `remove_args=['--option', 'option2']` etc.

Returns: nothing

## `is_in_path()`

```python
libdesktop.is_in_path(program)
```

If `program` is in the system's `PATH`, returns `True`, else `False`.

Returns: `bool`

## `is_running()`

```python
libdesktop.is_running(process)
```
Check if `process` is running.

Returns: `bool`

## `get_config_dir()`

```python
libdesktop.get_config_dir(app_name='')
```

Get the user's configuration directory. If `app_name` is specified, get `app_name`'s configuration directory instead.
Assuming said app follows standards.

Returns: `str`
