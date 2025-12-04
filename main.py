from machine import Pin
from neopixel import NeoPixel

class state:
    NONE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2

class color:
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    RED   = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE  = [0, 0, 255]

class game:
    def __init__(self, led_board_pin, button_pins, light_pins, player_1_button_pin, player_1_led_pin, player_2_button_pin, player_2_led_pin):
        self.rows = 4
        self.columns = 7

        self.neo = NeoPixel(Pin(led_board_pin, Pin.OUT), self.rows * self.columns)

        self.buttons = [Pin(button_pin, Pin.IN, Pin.PULL_UP) for button_pin in button_pins]
        self.lights = [Pin(light_pin, Pin.OUT) for light_pin in light_pins]

        self.player_1_button = Pin(player_1_button_pin, Pin.IN, Pin.PULL_UP)
        self.player_1_led = Pin(player_1_led_pin, Pin.OUT)
        self.player_2_button = Pin(player_2_button_pin, Pin.IN, Pin.PULL_UP)
        self.player_2_led = Pin(player_2_led_pin, Pin.OUT)


        self.board = [[state.NONE for _ in range(self.rows)] for _ in range(self.columns)]

    def coord_to_led(self, x, y):
        if x % 2 == 0:
            return x * self.rows + self.rows - 1 - y
        else:
            return x * self.rows + y
    
    def render(self):
        for x in range(self.rows):
            for y in range(self.columns):
                led = self.coord_to_led(x,y)
                match (self.board[x][y]):
                    case (state.NONE):
                        self.neo[led] = color.BLACK
                    case (state.PLAYER_1):
                        self.neo[led] = color.RED
                    case (state.PLAYER_2):
                        self.neo[led] = color.BLUE
        self.neo.write()

led_board_pin = 13
button_pins = [5, 6, 7, 15, 16, 17, 18]
light_pins = [1, 2, 42, 41, 40, 39, 38]
player_1_button_pin = 10
player_1_led_pin = 4
player_2_button_pin = 21
player_2_led_pin = 20

connect_4 = game(led_board_pin, button_pins, light_pins, player_1_button_pin, player_1_led_pin, player_2_button_pin, player_2_led_pin)

connect_4.board[0][0] = state.PLAYER_1
connect_4.render()