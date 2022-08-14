from ..keyboard_controller import KeyboardController


def steering_cb(val):
    print(f"Steering: {val}")


def throttle_cb(val):
    print(f"Throttle: {val}")


def brake_cb(val):
    print(f"Brake: {val}")


def test_init():
    key = KeyboardController("test")


def test_initialize():
    key = KeyboardController("test")
    key.initialize(steering_cb=steering_cb, throttle_cb=throttle_cb, brake_cb=brake_cb)
