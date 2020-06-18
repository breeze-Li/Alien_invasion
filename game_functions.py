import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def cheek_events(ai_setting, screen, stats, play_button,
                 ship, aliens, bullets, sb, ):
    # 监视键盘和鼠标，
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 监视键盘的按起键
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y, sb,)
        elif event.type == pygame.KEYDOWN:
            cheek_keydown_events(event, ai_setting, screen, ship, bullets, stats, aliens, sb)
        elif event.type == pygame.KEYUP:
            cheek_keyup_events(event, ship)


def check_play_button(ai_setting, screen, stats, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y, sb, ):
    # 点击事件
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y, )
    if button_click and not stats.game_active:
        # 重置游戏统计信息，
        stats.reset_stats()
        stats.game_active = True
        # 重置计分牌图像，
        sb.prep_level()
        sb.prep_highest_score()
        sb.prep_score()
        sb.prep_ships()
        # 清空外星人和子弹，
        bullets.empty()
        aliens.empty()
        # 创建一群新的外星人，并让飞船居中，
        create_fleet(ai_setting, screen, aliens, ship, )
        ship.center_ship()
        # 隐藏鼠标，
        pygame.mouse.set_visible(False)
        # 重置游戏设置，
        ai_setting.initialize_dynamic_settings()


def check_key_p(ai_setting, screen, stats, ship, aliens, bullets, sb,):
    """按P键以开始游戏，"""
    if not stats.game_active:
        # 重置游戏统计信息，
        stats.reset_stats()
        stats.game_active = True
        # 重置计分牌图像，
        sb.prep_level()
        sb.prep_highest_score()
        sb.prep_score()
        sb.prep_ships()
        # 清空外星人和子弹，
        bullets.empty()
        aliens.empty()
        # 创建一群新的外星人，并让飞船居中，
        create_fleet(ai_setting, screen, aliens, ship, )
        ship.center_ship()
        # 隐藏鼠标，
        pygame.mouse.set_visible(False)
        # 重置游戏设置，
        ai_setting.initialize_dynamic_settings()


def cheek_keydown_events(event, ai_setting, screen, ship, bullets, stats, aliens,sb):
    """按键响应"""
    if event.key == pygame.K_RIGHT:
        # 飞船向右移动，
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        # 飞船向左移动，
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_setting, screen, ship, )
    if event.key == pygame.K_q:
        sys.exit()
    if event.key == pygame.K_p:
        check_key_p(ai_setting, screen, stats, ship, aliens, bullets, sb, )


def cheek_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        # 飞船停止向右移动，
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        # 飞船停止向左移动，
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False


def update_screen(ai_setting, screen, ship, aliens, bullets, stats, play_button, sb, ):
    """ 更新屏幕上的图像并切换到新屏幕， """
    # 每次循环都重绘屏幕，
    screen.fill(ai_setting.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.drow_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分，
    sb.show_score()
    # 如果游戏处于非活动状态，就绘制play按钮，
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见，
    pygame.display.flip()


def update_bullets(ai_setting, screen, ship, aliens, bullets, sb, stats):
    """更新子弹的位置，并删除已经消失的子弹，"""
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))  # 验证子弹是否删除
    check_bullet_alien_collisions(ai_setting, screen, ship, aliens, bullets, sb, stats)


def check_bullet_alien_collisions(ai_setting, screen, ship, aliens, bullets, sb, stats):
    """ 检查是否有子弹击中了外星人，如果是,就删除相应的子弹和外星人，"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True, )
    # 删除所有的子弹，并新建一群外星人，加快游戏节奏
    if collisions:
        for alien in collisions.values():
            stats.score += ai_setting.alien_point * len(alien)
            sb.prep_score()
        check_highest_score(stats, sb, )
    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()
        # 等级加1
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_setting, screen, aliens, ship, )


def fire_bullet(butlles, ai_setting, screen, ship, ):
    # 创建一个子弹，并将其加入到编组中，
    if len(butlles) < ai_setting.bullets_allowed:
        new_bullet = Bullet(ai_setting, screen, ship, )
        butlles.add(new_bullet)


def get_number_aliens_x(ai_setting, alien_width, ):
    # 计算一行可容纳多少个外星人
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    # print('number_aliens_x:{}'.format(number_aliens_x))
    return number_aliens_x


def get_number_aliens_y(ai_setting, ship_height, alien_height, ):
    available_space_y = (ai_setting.screen_height - (3 * alien_height) - ship_height)
    number_aliens_y = int(available_space_y / (2 * alien_height))
    # print('number_aliens_y:{}'.format(number_aliens_y))
    return number_aliens_y


def create_alien(ai_setting, screen, aliens, alien_number, number_aliens_y, ):
    # 创建一个外星人
    alien = Alien(ai_setting, screen, )
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * number_aliens_y
    aliens.add(alien)


def create_fleet(ai_setting, screen, aliens, ship):
    """创建一群外星人"""
    # 创建一个外星人，并计算一行可容纳多少个外星人，
    alien = Alien(ai_setting, screen)
    number_aliens_x = get_number_aliens_x(ai_setting, alien.rect.width, )
    number_aliens_y = get_number_aliens_y(ai_setting, ship.rect.height, alien.rect.height, )

    # 创建外星人群
    for alien_number in range(number_aliens_x):
        for y_number in range(number_aliens_y):
            create_alien(ai_setting, screen, aliens, alien_number, y_number, )


def update_aliens(ai_setting, stats, screen, ship, aliens, bullets, sb, ):
    """检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置，"""
    check_fleet_edges(ai_setting, aliens)
    aliens.update()
    # 检测外星人和飞船之间的碰撞，
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, stats, screen, ship, aliens, bullets, sb)

    check_aliens_bottom(ai_setting, stats, screen, ship, aliens, bullets, sb)


def ship_hit(ai_setting, stats, screen, ship, aliens, bullets, sb):
    """响应被外星人碰撞的飞船，"""
    """这里可能会有一个问题，如果这个 -1 放在 if 里面，它将会执行4次，放在外面执行3次，"""
    stats.ships_left -= 1
    # 更新记分牌和飞船剩余数量，
    sb.prep_ships()
    if stats.ships_left > 0:
        aliens.empty()
        bullets.empty()
        create_fleet(ai_setting, screen, aliens, ship, )
        ship.center_ship()
        # print(stats.ships_left)
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_setting, stats, screen, ship, aliens, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, screen, ship, aliens, bullets, sb)
            break


def check_fleet_edges(ai_setting, aliens, ):
    """检测是否有外星人打到边缘，"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens, )
            break


def change_fleet_direction(ai_setting, aliens, ):
    """将整个外星人群下移并改变他们的方向，"""
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1


def check_highest_score(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.highest_score:
        stats.highest_score = stats.score
        sb.prep_highest_score()
