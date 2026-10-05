from classes.bus import Bus
import dbus_fast
from dbus_fast import DBusError
from dbus_fast.glib import ProxyObject, MessageBus

class Call:
    bus: MessageBus = Bus().session_bus
    dbus_object_path = ''
    _introspection: dbus_fast.introspection.Node
    _dbus_obj: ProxyObject
    def __init__(self, call_path):
        self.dbus_object_path = call_path
        if len(self.dbus_object_path) == 0:
            raise ValueError("The DBus Object Path cannot be empty")
        try:
            self._introspection = self.bus.introspect_sync('org.pipewire.Telephony', self.dbus_object_path)
            self._dbus_obj = self.bus.get_proxy_object('org.pipewire.Telephony', self.dbus_object_path, self._introspection)
        except DBusError as e:
            raise ValueError("Could not set up the DBus object.")