import pygame

import sys

from settings import Settings

from ship import Ship

from bullet import Bullet

from alien import Alien

from time import sleep

from game_stats import GameStats

from button import Button

from scoreboard import Scoreboard

class AlienInvasion:
    """
    管理游戏资源和行为的类
    """
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()

        self.settings = Settings()

        # 显示设置
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # 控制帧率
        self.clock = pygame.time.Clock()

        # 游戏标题
        pygame.display.set_caption('外星人入侵')

        # 创建记分牌与存储游戏信息的实例
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # 调用飞船
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # 调用外星人
        self.aliens = pygame.sprite.Group()
        self._create_fleet()        #调用外星人舰队

        # 游戏启动后应处于活跃状态
        self.game_active = False

        # 创建button按钮
        self.play_button = Button(self,"Play")

    def _check_keydown_events(self,event):
        """响应按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True

        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def _check_keyup_events(self,event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单机Play按钮时开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # 还原游戏设置
            self.settings.initialize_dynamic_settings()

            # 重置游戏统计信息
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            # 创建一个新的外星人舰队，并把飞船放到屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

    def fire_bullet(self):
        """创建一颗子弹，并且将其加入到编组bullets """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        # 更新子弹位置
        self.bullets.update()

        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 检查是否有子弹击中了外星人，如果有，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points *len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # 当一个舰队被消灭时，删除现有的子弹并创建一个新的外星舰队
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _create_alien(self,x_position,y_position):
        """创建一个外星人并放到当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_fleet(self):
        """创建一个外星人舰队"""
        # 创建一个外星人，再不断添加，知道没有空间添加外星人为止
        # 外星人的间距为外星人的宽度和高度
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size

        current_x,current_y = alien_width,alien_height

        while current_y <= (self.settings.screen_height - 5 * alien_width):
            while current_x <= (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width

            # 添加一个外星人后，重置x并递增y
            current_x = alien_width
            current_y += 2 * alien_height

    def _change_fleet_direction(self):
        """将整个外形舰队下移，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left >0:
            # 将ships_left减一
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            # 创建一个新的外星舰队，并将飞船放在屏幕正下方的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底部"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被碰撞到一样处理
                self.game_active = False
                break

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新整个舰队的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检查外星人是否到达屏幕底部
        self._check_aliens_bottom()

    def _update_screen(self):
        """每次循环时都重绘屏幕"""
        self.screen.fill(self.settings.bg_color)

        # 绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # 绘制飞船
        self.ship.blitme()

        # 绘制外星人
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活跃状态，就在屏幕上绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def run_game(self):
        """初始化游戏的主循环"""
        while True:
            # 调用按键函数
            self._check_events()
            if self.game_active:
                # 调用飞船刷新函数
                self.ship.update()

                # 调用子弹函数
                self._update_bullets()

                # 更新外星人位置
                self._update_aliens()

            # 调用屏幕刷新函数
            self._update_screen()

            # 帧率设置60
            self.clock.tick(165)

if __name__ == '__main__':
    # 创建游戏并测试运行
    ai = AlienInvasion()
    ai.run_game()