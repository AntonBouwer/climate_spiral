import pygame as pg
import sys
import csv

window_size = (width, height) = (800, 800)
game_title = "Climate Spiral"
radius_i = 100
radius_m = 200
radius_o = 300
radius_gap = radius_m - radius_i
screen_center = pg.math.Vector2(width // 2, height // 2)
white = pg.Color(255, 255, 255)
blue = pg.Color(0, 0, 255)
red = pg.Color(255, 0, 0)
orange = pg.Color(255, 165, 0)

# Read the data from the csv file
with open("temp_deviations.csv") as csv_file:
    data = list(csv.reader(csv_file))

# Preprocess the data
# Remove the 1st two rows
data = data[2:]
# Remove the 1st column
data = [row[1:] for row in data]
# Remove the last 6 columns
data = [row[:-6] for row in data]
# Remove the last row
data = data[:-1]
# Convert the data to floats
data = [[float(i) for i in row] for row in data]
# Flatten the list
data = [item for sublist in data for item in sublist]


# Function that chooses the color of the line based on the temperature deviation
def set_color(temp):
    if temp < -1:
        return blue  # Blue
    elif temp < 0:  # Lerp from blue to white
        return white.lerp(blue, abs(temp))
    elif temp < 1:  # Lerp from white to red
        return white.lerp(red, temp)
    else:
        return (255, 0, 0)  # Red


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(window_size)
        self.clock = pg.time.Clock()
        self.done = False
        self.data_index = 1
        self.year = 1880
        pg.display.set_caption(game_title)

    def run(self):
        while not self.done:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def update(self):
        if self.data_index < len(data):
            self.data_index += 1
            if self.data_index % 12 == 1:
                self.year += 1
                pg.display.set_caption(f"{game_title} - {self.year}")

    def draw_lines(self):
        for i in range(0, self.data_index - 1):
            start_pos = pg.math.Vector2.from_polar(
                (radius_m + radius_gap * data[i], -60 + i * 30)
            )
            end_pos = pg.math.Vector2.from_polar(
                (radius_m + radius_gap * data[i + 1], -60 + (i + 1) * 30)
            )
            pg.draw.line(
                self.screen,
                set_color(data[i]),
                screen_center + start_pos,
                screen_center + end_pos,
                1,
            )

    def draw(self):
        # Fill the screen with a dark blue color
        self.screen.fill((0, 0, 50))
        # Load the background image and blit it to the screen
        self.draw_lines()
        background_image = pg.image.load("spiral.png")
        self.screen.blit(
            background_image, screen_center - background_image.get_rect().center
        )
        # Draw the lines
        # self.draw_lines()
        self.year_text = pg.font.SysFont("Arial", 36).render(
            str(self.year), True, orange
        )
        self.screen.blit(
            self.year_text, screen_center - self.year_text.get_rect().center
        )
        pg.display.update()


if __name__ == "__main__":
    Game().run()
    pg.quit()
    sys.exit()
