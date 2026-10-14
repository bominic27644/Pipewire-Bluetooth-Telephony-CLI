# Pipewire-Bluetooth-Telephony-CLI

A simple CLI app for managing calls on a Bluetooth connected phone. This allows users to dial numbers, view active calls, answer incoming calls, and hangup existing calls. This utilizes the [Pipewire Bluetooth telephony DBus API](https://gitlab.freedesktop.org/pipewire/pipewire/-/blob/master/spa/plugins/bluez5/README-Telephony.md?ref_type=heads). As a result, this only works on Linux or other systems that may use DBus for interprocess communication and pipewire for audio. 

## Running

To run this program, ensure python and uv are installed. In addition, the following build dependencies are needed:

```shell
gcc gobject-introspection-devel cairo-gobject-devel pkg-config python3-devel gtk4
```

For fedora-based systems, use the following command:

```shell
sudo dnf install gcc gobject-introspection-devel cairo-gobject-devel pkg-config python3-devel gtk4
```

For install instructions for other distributions, please refer to the documentation for [PyGObject](https://pygobject.gnome.org/getting_started.html).

Once that is done, the python dependencies can be installed using the following command:

```shell
uv sync
```

Finally, the program can be run using the command below:

```shell
uv run main.py
```