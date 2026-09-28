from dbus_fast.aio import MessageBus
from dbus_fast import unpack_variants, DBusError
from dbus_fast import Variant
import asyncio

g_bus: MessageBus
g_phonePath = ""

async def main():
    global g_bus
    global g_phonePath
    try:
        g_bus = await MessageBus().connect()
    except DBusError:
        print("Could not connect to session DBus. Exiting...")
        return -1
    introspection = await g_bus.introspect('org.pipewire.Telephony', '/org/pipewire/Telephony')
    obj = g_bus.get_proxy_object('org.pipewire.Telephony', '/org/pipewire/Telephony', introspection)
    try:
        modem = obj.get_interface('org.freedesktop.DBus.ObjectManager')
        modems: dict = await modem.call_get_managed_objects()
    except DBusError:
        print("Could not get a list of Bluetooth phones to connect to! Exiting...")
        return -1
    if len(modems) == 0:
        print("No Bluetooth phones found found! Exiting...")
        print("Make sure your phone is connected and supports calling over Bluetooth and that the necessary codecs are enabled in your WirePlumber config!")
        return -1
    print("Select an phone to manage calls for:")
    num_phones = 0
    for key, value in modems.items():
        for key, value in value.items():
            for key, value in value.items():
                if isinstance(value, Variant) and key == "Address":
                    num_phones += 1

                    #TODO: Resolve Bluetooth address to device name
                    print(num_phones, ". ", value.value, sep='')
    phone_num = input("> ")
    while True:
        if not phone_num.isdigit() or int(phone_num) <= 0 or int(phone_num) > num_phones:
            phone_num = input("> ")
        else:
            break
    g_phonePath = list(modems)[int(phone_num)-1]
    print("Welcome to !")
    while True:
        if menu() == -1:
            break
    return 0

def menu():
    print("Select an option:")
    print("q: Quit")
    option = input("> ")
    if option == "q":
        return -1
    return 0

asyncio.run(main())