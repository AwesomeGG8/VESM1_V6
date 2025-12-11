from machine import Pin, PWM
from neopixel import NeoPixel
from time import sleep_ms
from random import randint

class state:
    NONE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    TIE = 3
    POWER_ON = 4

class winner:
    NONE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    TIE = 3

class color:
    BLACK  = [0, 0, 0]
    WHITE  = [255, 255, 255]
    RED    = [255, 0, 0]
    GREEN  = [0, 255, 0]
    BLUE   = [0, 0, 255]
    PURPLE = [50, 0, 255]

class game:
    def __init__(self, led_board_pin, button_pins, light_pins, player_1_button_pin, player_1_led_pin, player_2_button_pin, player_2_led_pin, speaker_pin):
        self.rows = 4
        self.columns = 7

        self.neo = NeoPixel(Pin(led_board_pin, Pin.OUT), self.rows * self.columns)

        self.buttons = [Pin(button_pin, Pin.IN, Pin.PULL_UP) for button_pin in button_pins]
        self.lights = [Pin(light_pin, Pin.OUT) for light_pin in light_pins]

        self.player_1_button = Pin(player_1_button_pin, Pin.IN, Pin.PULL_UP)
        self.player_1_led = Pin(player_1_led_pin, Pin.OUT)
        self.player_2_button = Pin(player_2_button_pin, Pin.IN, Pin.PULL_UP)
        self.player_2_led = Pin(player_2_led_pin, Pin.OUT)

        self.speaker = PWM(Pin(speaker_pin), 20000)

        self.board = [[state.NONE for _ in range(self.rows)] for _ in range(self.columns)]
        self.clear()
        self.power_on()

    def coord_to_led(self, x, y):
        x = self.columns - x - 1
        y = self.rows - y - 1
        if x % 2 == 0:
            return x * self.rows + self.rows - 1 - y
        else:
            return x * self.rows + y
    
    def render(self):
        for x in range(self.columns):
            for y in range(self.rows):
                led = self.coord_to_led(x,y)
                if self.board[x][y] == state.NONE:
                    self.neo[led] = color.BLACK
                elif self.board[x][y] == state.PLAYER_1:
                    self.neo[led] = color.RED
                elif self.board[x][y] == state.PLAYER_2:
                    self.neo[led] = color.BLUE
                elif self.board[x][y] == state.TIE:
                    self.neo[led] = color.PURPLE
                elif self.board[x][y] == state.POWER_ON:
                    self.neo[led] = color.GREEN
        self.neo.write()

    def fill_board(self, wanted_state):
        for x in range(self.columns):
            for y in range(self.rows):
                self.board[x][y] = wanted_state
        self.render()

    def start_game(self):
        sleep_ms(randint(1000, 3000))

        prev_player_1_state = self.player_1_button.value()
        prev_player_2_state = self.player_2_button.value()

        self.fill_board(state.POWER_ON)
        
        while True:
            player_1_state = self.player_1_button.value()
            player_2_state = self.player_2_button.value()

            if player_1_state == 0 and prev_player_1_state == 1:
                return state.PLAYER_1
            if player_2_state == 0 and prev_player_2_state == 1:
                return state.PLAYER_2


    def place_in_column(self, column, player):
        self.beep(220, 512, 100)
        if self.board[column][0] == state.NONE:
            self.board[column][0] = player
            self.render()
            sleep_ms(100)
            for row in range(1, self.rows):
                if self.board[column][row] != state.NONE:
                    break
                self.board[column][row] = self.board[column][row - 1]
                self.board[column][row - 1] = state.NONE

                self.render()
                sleep_ms(100)
        else:
            self.board[column][self.rows - 1] = state.NONE
            for row in range(self.rows - 1, 0, -1):
                self.board[column][row] = self.board[column][row - 1]
            self.board[column][0] = player
            self.render()
            sleep_ms(100)

    def check_buttons(self):
        values = []
        for i in range(len(self.buttons)):
            button = self.buttons[i]
            values.append(button.value())
        return values

    def check_winner(self):
        player_1_win = [state.PLAYER_1 for _ in range(4)]
        player_2_win = [state.PLAYER_2 for _ in range(4)]
        player_1_won = False
        player_2_won = False

        for x in range(self.columns):
            column = [self.board[x][y] for y in range(self.rows)]
            if column == player_1_win:
                player_1_won = True
            if column == player_2_win:
                player_2_won = True

        for x in range(self.columns - 3):
            for y in range(self.rows):
                row = [self.board[x + i][y] for i in range(4)]
                if row == player_1_win:
                    player_1_won = True
                if row == player_2_win:
                    player_2_won = True

        for x in range(self.columns - 3):
            diagonal = []
            for y in range(self.rows):
                diagonal.append(self.board[x + y][y])
                if diagonal == player_1_win:
                    player_1_won = True
                if diagonal == player_2_win:
                    player_2_won = True
            
        for x in range(self.columns - 1, 2, -1):
            diagonal = []
            for y in range(self.rows):
                diagonal.append(self.board[x - y][y])
                if diagonal == player_1_win:
                    player_1_won = True
                if diagonal == player_2_win:
                    player_2_won = True

        if player_1_won and player_2_won:
            return winner.TIE
        elif player_1_won:
            return winner.PLAYER_1
        elif player_2_won:
            return winner.PLAYER_2

        return winner.NONE

    def winner_animation(self, player):
        for x in range(self.columns):
            for y in range(self.rows):
                self.board[x][y] = player
            self.render()
            sleep_ms(100)

        for y in range(self.rows):
            for x in range(self.columns):
                self.board[x][y] = state.NONE
            self.render()
            sleep_ms(100)

    def tie_animation(self):
        for x in range(self.columns - 4):
            for y in range(self.rows):
                self.board[x][y] = state.PLAYER_1
                self.board[self.columns - x - 1][y] = state.PLAYER_2
            self.render()
            sleep_ms(100)

        for y in range(self.rows):
            self.board[3][y] = state.TIE
        self.render()
        sleep_ms(100)

        for x in range(4, self.columns):
            for y in range(self.rows):
                self.board[x][y] = state.TIE
                self.board[self.columns - x - 1][y] = state.TIE
            self.render()
            sleep_ms(100)

        for y in range(self.rows):
            for x in range(self.columns):
                self.board[x][y] = state.NONE
            self.render()
            sleep_ms(100)

    def power_on(self):
        for x in range(self.columns - 4):
            for y in range(self.rows):
                self.board[x][y] = state.POWER_ON
                self.board[self.columns - x - 1][y] = state.POWER_ON
            self.render()
            sleep_ms(100)

        for y in range(self.rows):
            self.board[3][y] = state.POWER_ON
        self.render()

        for y in range(self.rows):
            for x in range(self.columns):
                self.board[x][y] = state.NONE
            self.render()
            sleep_ms(100)
        
        self.place_in_column(2, state.PLAYER_1)
        self.place_in_column(3, state.PLAYER_2)
        
        self.place_in_column(4, state.PLAYER_1)
        self.place_in_column(2, state.PLAYER_2)
        
        self.place_in_column(3, state.PLAYER_1)
        self.place_in_column(4, state.PLAYER_2)
        
        self.place_in_column(5, state.PLAYER_1)
        self.place_in_column(5, state.PLAYER_2)
        
        self.place_in_column(2, state.PLAYER_1)
        self.place_in_column(3, state.PLAYER_2)
        
        self.place_in_column(3, state.PLAYER_1)
        self.place_in_column(3, state.PLAYER_2)
        
        sleep_ms(250)

        self.tie_animation()

    def clear_board(self):
        for x in range(self.columns):
            for y in range(self.rows):
                self.board[x][y] = state.NONE

        self.render()

    def clear_button_lights(self):
        for light in self.lights:
            light.value(0)

    def clear(self):
        self.clear_board()
        self.clear_button_lights()
        self.player_1_led.value(0)
        self.player_2_led.value(0)

    def beep(self, f, d, s):
        self.speaker.freq(f)
        self.speaker.duty(d)
        sleep_ms(s)
        self.speaker.duty(0)

    def play_game(self):
        player = self.start_game()
        self.winner_animation(player)
        self.clear()

        while self.check_winner() == winner.NONE:

            if player == state.PLAYER_1:
                self.player_1_led.value(1)
                self.player_2_led.value(0)
            else:
                self.player_1_led.value(0)
                self.player_2_led.value(1)

            button_values = self.check_buttons()

            column = -1
            for i in range(len(button_values)):
                if button_values[i] == 0:
                    column = i
                    break

            if column == -1:
                continue
        
            self.lights[column].value(1)
            self.place_in_column(column, player)
            self.lights[column].value(0)

            if player == state.PLAYER_1:
                player = state.PLAYER_2              
            else:
                player = state.PLAYER_1

            sleep_ms(100)
        
        win = self.check_winner()
        
        if win != winner.TIE:
            self.winner_animation(win)
        else:
            self.tie_animation()

        self.clear()

led_board_pin = 13
button_pins = [5, 6, 7, 15, 16, 18, 17]
light_pins = [1, 2, 42, 41, 40, 39, 38]
player_1_button_pin = 10
player_1_led_pin = 4
player_2_button_pin = 21
player_2_led_pin = 14
speaker_pin = 37

connect_4 = game(led_board_pin, button_pins, light_pins, player_1_button_pin, player_1_led_pin, player_2_button_pin, player_2_led_pin, speaker_pin)
while True:
    try:
        connect_4.play_game()
    except Exception as e:
        connect_4.clear()