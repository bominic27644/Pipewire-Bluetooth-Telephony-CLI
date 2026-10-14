from dbus_fast.glib import MessageBus
from dbus_fast import DBusError
from classes.phoneClass import Phone
from classes.callClass import Call
from classes.bus import Bus

g_phone: Phone

def main():
    global g_phone
    if set_phone() == -1:
        return -1
    print("Welcome to !")
    while True:
        if menu() == -1:
            break
    return 0

def menu():
    print("Current phone: ", g_phone.get_name())
    print("Select an option:")
    print("1. Manage calls")
    print("2. Hangup all calls")
    print("3. Change phone")
    print("q: Quit")
    option = input("> ")
    match option:
        case '1':
            list_calls()
        case '2':
            try:
                g_phone.hangup_all()
            except ValueError as e:
                print(e)
        case '3':
            if set_phone() == -1:
                return -1
        case 'q':
            return -1
        case _:
            return 0
    return 0

def list_calls():
    global g_phone
    calls: list[Call]
    num_calls = 0
    try:
        calls = g_phone.get_calls()
    except ValueError as e:
        print(e)
        return -1
    print("Select a call:")
    for call in calls:
        try:
            num_calls += 1
            print(num_calls, ". ", call.get_number(), " (", call.get_state(), ")", sep="")
        except ValueError as e:
            print(e)
            return -1
    print("b: go back to the main menu")
    call_num = input("> ")
    while True:
        if not call_num.isdigit() and call_num.lower() == "b":
            break
        elif not call_num.isdigit() or int(call_num) <= 0 or int(call_num) > num_calls:
            call_num = input("> ")
        else:
            break
    if call_num == 'b':
        return 0
    else:
        return manage_call(calls[int(call_num)-1])

def set_phone():
    global g_phone
    try:
        bus: MessageBus = Bus().session_bus
    except ConnectionError as e:
        print("Could not connect to session DBus. Exiting...")
        return -1
    introspection = bus.introspect_sync('org.pipewire.Telephony', '/org/pipewire/Telephony')
    obj = bus.get_proxy_object('org.pipewire.Telephony', '/org/pipewire/Telephony', introspection)
    try:
        modem = obj.get_interface('org.freedesktop.DBus.ObjectManager')
        modems: dict = modem.call_get_managed_objects_sync()
    except DBusError:
        print("Could not get a list of Bluetooth phones to connect to! Exiting...")
        return -1
    if len(modems) == 0:
        print("No Bluetooth phones found found! Exiting...")
        print("Make sure your phone is connected and supports calling over Bluetooth and that the necessary codecs are enabled in your WirePlumber config!")
        return -1
    print("Select an phone to manage calls for:")
    num_phones = 0
    phones: list[Phone] = []
    for key, value in modems.items():
        try:
            phones.append(Phone(key))
        except ValueError as e:
            print(e)
        num_phones = len(phones)
        print(num_phones, ". ", phones[num_phones-1].get_name(), " (", phones[num_phones-1].get_address(), ")",  sep='')
    phone_num = input("> ")
    while True:
        if not phone_num.isdigit() or int(phone_num) <= 0 or int(phone_num) > num_phones:
            phone_num = input("> ")
        else:
            break
    try:
        g_phone = phones[int(phone_num)-1]
    except ValueError as e:
        print(e)
        print("Exiting...")
        return -1

def manage_call(call: Call):
    print("Current call: ", call.get_number(), " (", call.get_state(), ")", sep="")
    print("Select an option:")
    print("1. Hangup call")
    if call.is_incoming_call():
        print("2. Answer")
    print("b: go back to the main menu")
    option = input("> ")
    try:
        match option:
            case '1':
                call.hangup()
            case '2':
                call.answer()
            case 'b':
                return -1
            case _:
                return 0
    except ValueError as e:
        print(e)
    return 0

if __name__ == "__main__":
    main()