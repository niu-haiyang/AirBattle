# 绘制血槽
pygame.draw.line(screen, BLACK,
                 (each.rect.left, each.rect.top - 5),
                 (each.rect.right, each.rect.top - 5),
                 2)
# 当生命大于20%显示绿色，否则显示红色
energy_remain = each.energy / enemy.MidEnemy.energy
if energy_remain > 0.2:
    energy_color = GREEN
else:
    energy_color = RED
pygame.draw.line(screen, energy_color,
                 (each.rect.left, each.rect.top - 5),
                 (each.rect.left + each.rect.width * energy_remain,
                  each.rect.top - 5), 2)
else:
# 毁灭
if not (delay % 3):
    if e2_destroy_index == 0:
        enemy2_down_sound.play()
    screen.blit(each.destroy_images[e2_destroy_index], each.rect)
    e2_destroy_index = (e2_destroy_index + 1) % 4
    if e2_destroy_index == 0:
        each.reset()