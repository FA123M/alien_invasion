class Settings:
    """
    存储外星人入侵的所有设置选项
    """
    def __init__(self):
        """初始化游戏的静态设置"""
        # 显示设置
        self.screen_width = 1080
        self.screen_height = 720
        self.bg_color = (255, 255, 255)        #R G B三个参数分别控制红 绿 蓝三种颜色，通过组合得到需要的颜色

        # 外星人设置
        self.fleet_drop_speed = 10

        # 飞船设置
        self.ship_limit = 3

        # 以什么速度加快游戏的节奏
        self.speedup_scale = 1.1

        # 飞船升级属性提升幅度
        self.ship_up = 1.005

        # 外星人分数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 3
        self.bullet_speed = 5
        self.alien_speed = 1.0

        # 子弹设置
        self.bullet_width =  3       #宽和高都指的像素值
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 8

        # fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction = 1

        # 积分设置
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置的值和外星人的分数"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale

        self.bullet_width *= self.ship_up

        self.alien_points = int(self.alien_points * self.score_scale)