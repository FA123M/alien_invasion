class GameStats:
    """跟踪游戏统计信息"""
    def __init__(self, ai_game):
        """初始化游戏信息"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 在任何情况下都不应该重置最高分
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能出现变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1