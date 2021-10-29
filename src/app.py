"""App test camera and object recognition"""
import os
import logging
import time
import requests

from rtsparty import Stream
from objectdaddy import Daddy

import cv2
from utils import is_raspberrypi


class HalloweenMannequinHead:
    def __init__(self):
        logging.info("Starting application")
        self.on_pi = is_raspberrypi()

        self._setup_stream()
        self._setup_object_recognition()
        self.server_mode = bool(os.environ.get("SERVER_MODE", False))
        #        if not self.server_mode:
        #            self._setup_servo()
        self._setup_servo()

    def _setup_servo(self):
        """Sets up the servo; requires raspberry pi to run"""
        from servo_controller import ServoController

        self.servo_controller = ServoController()
        self.servo_controller.set_servo_fraction(.5)

    def _setup_stream(self):
        """Set up the stream to the camera"""
        logging.info("Starting stream")
        stream_uri = os.environ.get("STREAM_URI", None)
        if stream_uri or self.on_pi:
            self.stream = Stream(stream_uri)
        else:
            logging.info(
                f"""can't access local webcam, not running on Raspberry Pi.
                Set env STREAM_URI to access a webcam over network. on_pi={self.on_pi}"""
            )

    def _setup_object_recognition(self):
        """Set up object recognition and load models"""
        logging.info("Loading ML models")
        self.daddy = Daddy()

    def get_location_x_fraction(self, detection):
        """Returns the object's horizontal location in the frame as a fraction of the full frame"""
        frame_height, frame_width = detection.frame.shape[:2]
        fraction = round(detection.x / float(frame_width), 2)
        return fraction

    def object_detected(self, detection):
        """Call back for some recognized objct being detected"""
        x_fraction = self.get_location_x_fraction(detection)
        if self.server_mode:
            host = os.environ.get("RASPBERRY_PI_HOST", "localhost")
            url = "http://{}:8000/servo/?f={}".format(host, x_fraction)
            requests.get(url)
        else:
            self.servo_controller.set_servo_fraction(x_fraction)

    def process_frames_from_stream(self, accept_list):
        """Processes the frames from the stream"""
        accept_set = set(accept_list)
        while True:
            frame = self.stream.get_frame()
            if self.stream.is_frame_empty(frame):
                continue
            self.latest_frame = frame
            results, frame = self.daddy.process_frame(frame, draw_bounding_boxes=True)
            cv2.imshow("Live Playback", frame)
            cv2.waitKey(1)

            for detection in results:
                if (detection.label in accept_set) or detection.is_person():
                    logging.info(f"{detection.label} detected")
                    self.object_detected(detection)
                else:
                    logging.info(f".. {detection.label} ignored.")
            
            time.sleep(0.1)     # don't busy loop

    def run(self, accept_list):
        """Run the application"""
        try:
            self.process_frames_from_stream(accept_list)
        except KeyboardInterrupt:
            if self.servo_controller:
                self.servo_controller.set_servo_fraction(.5)    # try to neutral on exit, may fail.
                del self.servo_controller
            logging.info("Exiting application")


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    hmh = HalloweenMannequinHead()
    hmh.run(["person", "cat", "dog"])
