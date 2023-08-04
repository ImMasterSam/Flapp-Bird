import pygame
import objects
from time import sleep
from random import randint

pygame.init()

#背景
screen = pygame.display.set_mode((640,1000))
pygame.display.set_caption("Flappy 跳跳鳥")
bg_pic = pygame.image.load("圖片\\background.png")
bg_pic = pygame.transform.scale2x(bg_pic)
bg_pic = bg_pic.convert()

#圖片物件
logo = pygame.image.load("圖片\\Logo.png")
logo = pygame.transform.scale(logo, (534, 144)).convert_alpha()
go_title = pygame.image.load("圖片\\GameOver.png")
go_title = pygame.transform.scale(go_title, (480, 105)).convert_alpha()
my_name = pygame.image.load("圖片\\My_Name.png")
my_name = pygame.transform.scale(my_name, (200, 40)).convert_alpha()

#角色物件
bird = objects.Bird()
top_tube = objects.Tube("Top")
bottom_tube = objects.Tube("Bottom")
start_button = objects.Button("Start_button", 216, 500, 52, 29, 2, 4)
menu_button = objects.Button("Menu_button", 220, 500, 40, 14, 2, 5)

#角色群組
game = pygame.sprite.Group()
tubes = pygame.sprite.Group()
game.add(bird)
tubes.add(top_tube)
tubes.add(bottom_tube)
game.add(top_tube)
game.add(bottom_tube)

menu = pygame.sprite.Group()
menu.add(start_button)

game_over = pygame.sprite.Group()
game_over.add(menu_button)


#字體
font1 = pygame.font.Font("Minecraft.ttf", 100)

#主程式
clock = pygame.time.Clock()
mid_hight = 500
score = 0
running = True
game_status = 0
while running:

    #FPS
    clock.tick(59)

    screen.blit(bg_pic, (0, 0))
    pos = pygame.mouse.get_pos()

    if game_status == 1:

        #更新柱體
        bottom_tube.update(mid_hight+100)
        if top_tube.update(mid_hight-700):
            mid_hight = randint(300, 700)

        if bottom_tube.rect.left == 79 or bottom_tube.rect.left == 80:
            score += 1

        #更新鳥
        if bird.update():
            bird.reset()
            top_tube.reset()
            bottom_tube.reset()
            sleep(1)
            score = 0
            game_status = 2
        
        #碰撞偵測
        hit_tube = pygame.sprite.spritecollide(bird, tubes, False, pygame.sprite.collide_mask)
        if len(hit_tube) > 0:
            bird.reset()
            top_tube.reset()
            bottom_tube.reset()
            sleep(1)
            score = 0
            game_status = 2

        #按鍵反應
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()

        #更新畫面
        score_text = font1.render(str(score), True, (220, 220, 220))
        screen.blit(score_text, (300, 200))
        game.draw(screen)
        pygame.display.update()
    
    elif game_status == 0:
        screen.blit(logo, (53, 150))
        screen.blit(my_name, (220, 900))
        menu.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if start_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                game_status = 1

        pygame.display.update()
    
    elif game_status == 2:
        screen.blit(go_title, (80, 150))
        game_over.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if menu_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                game_status = 0

        pygame.display.update()

pygame.quit()