# Halloween Mannequin Head
A mannequin head that turns to follow any person that walks in front of it.

## Installation
To install, clone this repository to your Raspberry Pi and run the following command.
```bash
make install
```

A few environment variables are required:

```bash
# Only run the servo component that accepts request on a flask server;
# this lets you do the camera processing elsewhere
# If you're just using a raspberry pi, don't set this env var
SERVER_MODE=True

# Stream URL - set this if you're using an external camera like the Wyze V2
STREAM_URI=rtsp://username:password@host/live/
```

## Change notes
* app tests for being invoked on non-RPI yet linux dev machine, doesn't try to initialize servos if not.
Supports development under WSL on windows.
Also install JMPEG streamer app from windows store to remote laptop camera.
* added range checks to servo server inputs
* note: debugging under
