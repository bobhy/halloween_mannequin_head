'''
    Random tools to enable running a mockup on a dev laptop.
'''
import io

def is_raspberrypi():
    """Detect if we're actually running on a Raspberry Pi

    Returns:
        bool: True if running on Raspberry PI, false else (and no exceptions)

    Credit:
            https://raspberrypi.stackexchange.com/a/118473/139770
    """
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower():
                return True
    except Exception:
        pass
    return False
