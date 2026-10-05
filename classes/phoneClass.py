import dbus_fast
from dbus_fast import DBusError
from dbus_fast.glib import ProxyObject, MessageBus
from classes.callClass import Call

from classes.bus import Bus

class Phone:
    bus: MessageBus = Bus().session_bus
    dbus_object_path = ''
    _introspection: dbus_fast.introspection.Node
    _dbus_obj: ProxyObject
    def __init__(self, dbus_object_path):
        self.dbus_object_path = dbus_object_path
        if len(self.dbus_object_path) == 0:
            raise ValueError("The DBus Object Path cannot be empty")
        try:
            self._introspection = self.bus.introspect_sync('org.pipewire.Telephony', self.dbus_object_path)
            self._dbus_obj = self.bus.get_proxy_object('org.pipewire.Telephony', self.dbus_object_path, self._introspection)
        except DBusError as e:
            raise ValueError("Could not set up the DBus object.")

    def get_address(self):
        interface = self._dbus_obj.get_interface('org.pipewire.Telephony.AudioGateway1')
        value = interface.get_address_sync()
        return value

    def get_name(self):
        #TODO: get phone name
        return "PhoneName"

    def dial(self, number: str):
        try:
            interface = self._dbus_obj.get_interface('org.pipewire.Telephony.AudioGateway1')
            result = interface.call_dial_sync(number)
        except DBusError as e:
            raise ValueError("Could not dial number.")
        return Call(result)

    def get_calls(self):
        try:
            interface = self._dbus_obj.get_interface('org.freedesktop.DBus.ObjectManager')
            result = interface.call_get_managed_objects_sync()
        except DBusError as e:
            raise ValueError("Could not get a list of calls.")
        calls: list[Call] = []
        for callID in result:
            calls.append(Call(callID))
        if len(calls) == 0:
            raise ValueError("There are currently no calls.")
        return calls