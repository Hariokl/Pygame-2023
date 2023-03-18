import settings as st


class Level:
    def __init__(self):
        self.level = 1
        self.time = 0
        self.monsters_standard_hp = 10
        self.monsters_hp = self.monsters_standard_hp
        self.amplifier = 1.01
        self.monsters_spawn_time = 10  # 10 * 0.99**x

    def update(self):
        self.time += st.get_time("level")
        self.monster_hp = (self.monsters_standard_hp * self.level) * self.amplifier ** self.time
