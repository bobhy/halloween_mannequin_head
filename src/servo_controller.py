import RPi.GPIO as gpio
import time
import logging


class ServoController:
    def __init__(self):
        """Set up the servos"""
        logging.info("Setting up servo")
        self.servo_pin = 17
        self._setup_gpio(self.servo_pin)
        self._set_servo_range()

    def _set_servo_range(self):
        """Sets the range of the servo"""
        self.servo_bounds_degrees = 20
        self.servo_max = 180 - self.servo_bounds_degrees
        self.servo_min = self.servo_bounds_degrees
        self.servo_range = self.servo_max - self.servo_min

    def __del__(self):
        """Clean up"""
        self.pwm.stop()
        gpio.cleanup()

    def _setup_gpio(self, on_gpio_pin):
        """Set up the gpio on (GPIO) pin"""
        gpio.setmode(gpio.BCM)
        self.servo_pin = on_gpio_pin
        gpio.setup(self.servo_pin, gpio.OUT)
        self.pwm = gpio.PWM(self.servo_pin, 50)
        self.pwm.start(0)

    def set_servo_angle(self, angle: int):
        """Set the angle of the servo"""
        logging.info("Setting angle to {}".format(angle))
        gpio.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(angle / 18 + 2)
        time.sleep(1)
        gpio.output(self.servo_pin, False)
        self.pwm.ChangeDutyCycle(0)

    def set_servo_fraction(self, fraction: float):
        """ "Converts a fraction of full travel into servo angle

        Args:
            fraction (float): a real [0,1.0] represents desired servo travel.
                             Not a "percentage", fraction value of 0.5 requests neutral,
                             0.0 is one extreme, 1.0 is the other.
        """
        angle = int((1 - fraction) * self.servo_range) + self.servo_min
        self.set_servo_angle(angle)
