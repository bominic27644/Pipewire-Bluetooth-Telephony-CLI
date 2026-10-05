from dbus_fast import DBusError
from dbus_fast.glib import MessageBus

class Bus:
    session_bus: MessageBus

    def __init__(self):
        try:
            self.session_bus = MessageBus().connect_sync()
        except DBusError:
            raise ConnectionError("Could not connect to session DBus.")
        pass