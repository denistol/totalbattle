import time
import pyautogui

class Bot:
    def __init__(self) -> None:
        self.march_count = 0
        self.speedups_per_march = 4
        self.init()

    def get_location(self,screenshot_name):
        try:
            loc = pyautogui.locateOnScreen("images/" + screenshot_name)
            return dict(left=loc.left, top=loc.top)
        except:
            print("Location ", screenshot_name, " not found!")
            return None
        
    def click_to(self, loc, offset=3):
        if loc is not None:
            time.sleep(0.5)

            x = loc["left"]+offset
            y = loc["top"] + offset

            pyautogui.moveTo(x,y, 0.5)
            pyautogui.click(x,y )
            time.sleep(1)

    def get_center(self):
        top_right = self.get_location('screen_top_right.png')
        top_left = self.get_location('screen_top_left.png')
        bot_right = self.get_location('screen_bot_right.png')

        if top_left is None or top_left is None or bot_right is None:
            print('Window not found!')
            return None
        center_x = (top_left["left"] + top_right["left"]) / 2
        center_y = (top_right["top"] + bot_right["top"]) / 2

        return dict(left=center_x, top=center_y)
    
    def click_center(self):
        c = self.get_center()
        
        if c is not None:
            self.click_to(c)

    def click_watchover(self):
        loc = self.get_location('watchover.png')
        self.click_to(loc)

    def click_go_btn(self):
        loc = self.get_location('go_btn.png')
        self.click_to(loc)

    def click_monsters(self):
        loc_1 = self.get_location('monsters.png')
        loc_2 = self.get_location('monsters2.png')
        self.click_to(loc_1 or loc_2)

    def click_attack_btn(self):
        loc = self.get_location('attack_btn.png')
        self.click_to(loc)
            
    def click_select_all_btn(self):
        loc = self.get_location('select_all_btn.png')
        self.click_to(loc)

    def click_start_march_btn(self):
        loc = self.get_location('start_march_btn.png')
        self.click_to(loc)

    def has_march(self):
        has_troops = self.get_location('troops.png')
        if has_troops is not None:
            return True
        
        loc_1 = self.get_location('speedup.png')
        time.sleep(4)
        loc_2 = self.get_location('speedup.png')
        loc = loc_1 or loc_2
        if loc is not None:
            self.click_to(loc, 20)
        has_troops_march = self.get_location('troops.png')
        if has_troops_march is not None:
            return True
        return False
    
    def use_speedup(self):
        loc = self.get_location('speedup.png')
        self.click_to(loc)
        loc_use = self.get_location('use.png')

        for _ in range(self.speedups_per_march):
            self.click_to(loc_use, 15)

    def run_march(self):
        print("Run march: ", 1 + self.march_count )
        pyautogui.press('esc')
        pyautogui.press('esc')
        self.click_watchover()
        self.click_monsters()
        self.click_go_btn()
        pyautogui.press('esc')
        self.click_center()
        self.click_attack_btn()
        self.click_select_all_btn()
        self.click_start_march_btn()
        time.sleep(1)
        if(self.has_march()):
            self.use_speedup()
            self.march_count = self.march_count + 1

    def init(self):
        while True:
            if self.has_march() or self.get_center() is None:
                time.sleep(2)
            else:
                self.run_march()

Bot()