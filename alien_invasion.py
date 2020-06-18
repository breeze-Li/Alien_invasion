import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
from game_state import GameStats
import game_functions as gf
from button import Button
from scoreboard import ScoreBoard


def run_game():
    # 初始化游戏并创建一个屏幕对象，
    pygame.init()
    ai_setting = Settings()  # 实例化


    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption('Alien Invasion')
    # 创建一艘飞船
    ship = Ship(ai_setting, screen)  # 实例化
    # 创建一个用于储存子弹的编组
    bullets = Group()
    # 创建一个外星人编组，
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_setting, screen, aliens, ship, )
    pygame.display.set_caption("外星人入侵")
    # 创建play按钮，
    play_button = Button(ai_setting, screen, "PLAY")
    # 实例化计分牌，
    stats = GameStats(ai_setting)
    sb = ScoreBoard(ai_setting, screen, stats)
    # 开始游戏的主循环
    while True:
        gf.cheek_events(ai_setting, screen, stats, play_button,
                      ship, aliens, bullets, sb, )
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_setting, screen, ship, aliens, bullets, sb, stats)
            gf.update_aliens(ai_setting, stats, screen, ship, aliens, bullets, sb, )
        gf.update_screen(ai_setting, screen, ship, aliens, bullets, stats, play_button, sb)


run_game()
