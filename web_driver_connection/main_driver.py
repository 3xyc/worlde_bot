import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import os
import time


class WordleConnection:

    def __init__(self, headless=False):
        self.driver = self.connect()
        self.board, self.tiles = self.load_board_and_tiles()
        self.current_index = 0
        self.keyboard = self.load_keyboard()

    def connect(headless=False):
        options = Options()
        options.headless = headless
        url = "https://www.nytimes.com/games/wordle/index.html"
        if os.name =="nt":
            chrome_service = Service("C:\Program Files\Chromedriver\chromedriver.exe")
        else:
            chrome_service = Service("/Users/a1/Downloads/Code/chromedriver")
        driver = webdriver.Chrome(service=chrome_service, options=options)
        driver.get(url)
        return driver

    def disconnect(self):
        self.driver.quit()

    def load_board_and_tiles(self):
        board = self.driver.find_element(By.CLASS_NAME, "Board-module_board__lbzlf")
        tiles = self.driver.find_elements(By.CLASS_NAME, "Tile-module_tile__3ayIZ")[:30:]
        return board, tiles

    def read_last_row(self):
        if self.current_index == 0:
            return [tile.text for tile in self.tiles[self.current_index:self.current_index+5:]]
        return [tile.text for tile in self.tiles[self.current_index-5:self.current_index:]]

    def load_keyboard(self):
        buttons = self.driver.find_elements(By.CLASS_NAME,"Key-module_key__Rv-Vp")
        keyboard = {b.get_attribute("data-key"): b for b in buttons}


        keyboard["del"] = keyboard['←']
        keyboard["enter"] = keyboard['↵']
        keyboard.pop('←')
        keyboard.pop('↵')
        return keyboard

    def get_coloring(self):
        time.sleep(2)
        result = ""
        if self.current_index < 25:
            greens = []
            for i, tile in enumerate(self.tiles[self.current_index:self.current_index+5:]):
                state = tile.get_attribute("data-state")
                print(state)
                if state == 'absent':
                    result+=tile.text.lower()
                elif state == "correct":
                    result+=tile.text.upper()
                    greens.append(i)
                elif state == "present":
                    result+=tile.text.upper()
                else:
                    print("HEREEE")
                    for i in range(5):
                        self.keyboard["del"].click()
                    return False, False
            self.current_index +=5
        print(result)
        print(greens)
        return result, greens



        self.current_index += 5

    def write(self, guess="guess"):
        print("Try to write: ",guess)
        for b in guess:
            self.keyboard[b].click()
        self.keyboard["enter"].click()
        return self.get_coloring()





if __name__ == "__main__":
    wordle_connection = WordleConnection()

    while True:
        try:
            c = input("r to read, w to write, q to quit: ")
            if c == "q":
                break
            if c == "r":
                print(wordle_connection.read_last_row())
            if c == "w":
                guess = input("enter guess: ")
                wordle_connection.write(guess=guess)
        except:
            print(traceback())
    wordle_connection.disconnect()

