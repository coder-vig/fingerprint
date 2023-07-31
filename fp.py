# Install 'libfprint-2-dev' 
# sudo apt install libfrint-2-dev

import gi
gi.require_version('FPrint','2.0')
from gi.repository import FPrint, GLib

# Function to register finger print
def get_fingerprint_data(finger_location):
    ctx = GLib.main_context_default()
    c = FPrint.Context()
    c.enumerate()
    devices = c.get_devices()
    d = devices[0]
    f=FPrint.Print.new(d)
    fing = f.set_finger(FPrint.Finger(finger_location))
    d.open_sync()
    d.enroll_sync(f)
    d.close_sync()
    try:
        return f.serialize()
    except:
        return 'Error'


# Function to check finger print (1:1) match

def check_fingerprint_data(data):
    ctx =   GLib.main_context_default()
    c   =   FPrint.Context()
    c.enumerate()
    devices = c.get_devices()
    d       =   devices[0]
    f       =   FPrint.Print.new(d)
    g       =   f.deserialize(data)


    counter = 0

    d.open_sync()

    # try 5 attempts to test finger print
    while counter < 5:
        m          =    d.verify_sync(g)
        if m.match:
            d.close_sync()
            return m.match
        else:
            counter += 1
    d.close_sync()
    return False


# Function to check fingerprint (1:n)
# data is now a dictionary of prints of the format {'a':print,'b':print,...}
def check_finger_print_data_many(data):
    ctx     =   GLib.main_context_default()
    c       =   FPrint.Context()
    c.enumerate()
    devices= c.get_devices()
    d=devices[0]
    f = FPrint.Print.new(d)
   
    # reverse lookup

    dataset = { j : i for i,j in data.items() }
    
    d.open_sync()

    x = d.identify_sync([f.deserialize(i) for i in dataset.keys()])
    
    d.close_sync()
    
    if x.match:
        return dataset.get(x.match.serialize(),None)
    else:
        return False



