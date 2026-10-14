from classes.bus import Bus
import dbus_fast
from dbus_fast import DBusError, Variant
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

    def answer(self):
        if self.is_incoming_call():
            try:
                interface = self._dbus_obj.get_interface('org.pipewire.Telephony.Call1')
                interface.call_answer_sync()
            except DBusError as e:
                raise ValueError("Could not hangup call.")
        else:
            raise ValueError("This is not an incoming call.")

    def hangup(self):
        try:
            interface = self._dbus_obj.get_interface('org.pipewire.Telephony.Call1')
            interface.call_hangup_sync()
        except DBusError as e:
            raise ValueError("Could not hangup call.")
        return

    def is_incoming_call(self):
        try:
            result = self.get_state()
        except ValueError as e:
            raise e
        if result != "incoming":
            return False
        return True

    def get_state(self):
        try:
            # use getAll instead of get because it crashes wireplumber if the number is empty
            interface = self._dbus_obj.get_interface('org.freedesktop.DBus.Properties')
            properties: dict = interface.call_get_all_sync("org.pipewire.Telephony.Call1")
        except DBusError as e:
            raise ValueError("Could not get call state.")
        result = ""
        for key, value in properties.items():
            if isinstance(value, Variant) and key == "State":
                result = value.value
                break
        return result

    def get_number(self):
        try:
            # use getAll instead of get because it crashes wireplumber if the number is empty
            interface = self._dbus_obj.get_interface('org.freedesktop.DBus.Properties')
            properties: dict = interface.call_get_all_sync("org.pipewire.Telephony.Call1")
        except DBusError as e:
            raise ValueError("Could not get phone number for call.")
        result = ""
        for key, value in properties.items():
            if isinstance(value, Variant) and key == "LineIdentification":
                result = value.value
                break
        if result == "":
            result = "Unknown"
        return result