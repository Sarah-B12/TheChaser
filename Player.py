"""
Sarah Brongniart 337903892
Sarah
"""


class Player:
    player_step = 3
    wallet = 0
    joker = False

    def get_step(self):
        return self.player_step

    def get_wallet(self):
        return self.wallet

    def get_joker(self):
        return self.joker

    def set_joker(self):
        self.joker = True

    def clr_joker(self):
        self.joker = False

    def step_plus_one(self):
        self.player_step += 1

    def add_wallet(self):
        self.wallet += 5000

    def change_wallet_step(self, num):
        num = int(num)
        if num == 2:
            self.wallet *= 2
            self.player_step -= 1
        elif num == 3:
            self.wallet /= 2
            self.player_step += 1
        else:
            return