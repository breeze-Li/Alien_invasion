import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_setting, screen, ):
        """初始化外星人并设置其起始位置，"""
        super(Alien, self, ).__init__()
        self.screen = screen
        self.ai_setting = ai_setting
        # 加载外星人图像并设置其位置属性，
        self.image = pygame.image.load(r'images\alien.bmp')
        self.rect = self.image.get_rect()
        # 每个外星人最初都在屏幕左上角附近，
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def update(self):
        """左右移动外星人"""
        self.x += self.ai_setting.alien_speed_factor * self.ai_setting.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制外星人，"""
        self.screen.blit(self.image, self.rect, )

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



