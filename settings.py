class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230, 230, 230)  # 背景颜色
        # self.ship_speed_factor = 1  # 飞船速度
        self.ship_limit = 3  # 三艘飞船，
        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # 外星人设置，
        self.fleet_drop_speed = 10
        # 运动方向1表示向右-1表示向左，
        # self.fleet_direction = 1
        # 游戏加速设置，
        self.speedup_scale = 1.1
        # 外星人点数的提高速度，
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # 运动方向1表示向右-1表示向左，
        self.fleet_direction = 1
        # 计分
        self.alien_point = 5

    def increase_speed(self):
        """提高速度设置，"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_point = int(self.alien_point * self.score_scale)
        # print(self.alien_point)

