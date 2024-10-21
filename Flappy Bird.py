import pygame
import objects
from time import sleep
from random import randint

pygame.init()

#背景
screen = pygame.display.set_mode((640,1000))
pygame.display.set_caption("Flappy 跳跳鳥")
icon = pygame.image.load("圖片/icon.png")
pygame.display.set_icon(icon)
bg_pic = pygame.image.load("圖片/background.png")
bg_pic = pygame.transform.scale2x(bg_pic)
bg_pic = bg_pic.convert()

#圖片物件
logo = pygame.image.load("圖片/Logo.png")
logo = pygame.transform.scale(logo, (534, 144)).convert_alpha()
go_title = pygame.image.load("圖片/GameOver.png")
go_title = pygame.transform.scale(go_title, (480, 105)).convert_alpha()
my_name = pygame.image.load("圖片/My_Name.png")
my_name = pygame.transform.scale(my_name, (200, 40)).convert_alpha()
guide = pygame.image.load("圖片/Guide.png")
guide = pygame.transform.scale(guide, (462, 330)).convert_alpha()


#角色物件
bird = objects.Bird()
top_tube = objects.Tube("Top")
bottom_tube = objects.Tube("Bottom")
start_button = objects.Button("Start_button", 216, 500, 52, 29, 2, 4)
menu_button = objects.Button("Menu_button", 220, 500, 40, 14, 2, 5)
x_button = objects.Button("X_button", 35, 35, 13, 14, 2, 3)
updatelog_button = objects.Button("Updatelog_button", 520, 850, 50, 70, 2, 2)
ok_button = objects.Button("OK_button", 220, 600, 40, 14, 2, 5)

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
menu.add(x_button)
menu.add(updatelog_button)

game_over = pygame.sprite.Group()
game_over.add(menu_button)

up_log = pygame.sprite.Group()
up_log.add(ok_button)



#字體
font1 = pygame.font.Font("Minecraft.ttf", 100)
font2 = pygame.font.Font("Minecraft.ttf", 60)
font3 = pygame.font.Font("Minecraft.ttf", 20)
font4 = pygame.font.Font("Minecraft.ttf", 40)

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


    #清單畫面
    if game_status == 0:
        screen.blit(logo, (53, 150))
        screen.blit(my_name, (220, 950))
        menu.draw(screen)
        
        vers = font3.render("v1.1", True, (255, 255, 255))
        screen.blit(vers, (555, 960))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if start_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                game_status = 1

            if x_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                running = False

            if updatelog_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                game_status = 4
                

        pygame.display.update()
    

    #遊戲準備
    elif game_status == 1:
        screen.blit(guide, (89, 300))

        score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_status = 2

        pygame.display.update()


    #遊戲中
    elif game_status == 2:

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
            game_status = 3
        
        #碰撞偵測
        hit_tube = pygame.sprite.spritecollide(bird, tubes, False, pygame.sprite.collide_mask)
        if len(hit_tube) > 0:
            bird.reset()
            top_tube.reset()
            bottom_tube.reset()
            sleep(1)
            game_status = 3

        #按鍵反應
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        #更新畫面
        score_text = font1.render(str(score), True, (220, 220, 220))
        screen.blit(score_text, (300, 200))
        game.draw(screen)
        pygame.display.update()
    

    #結束畫面
    elif game_status == 3:
        screen.blit(go_title, (80, 150))
        game_over.draw(screen)

        end_score = font2.render(f"SCORE : {score}", True , (255, 255, 255))
        screen.blit(end_score, (165, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if menu_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                game_status = 0

        pygame.display.update()
    

    #更新日誌
    elif game_status == 4:

        log = open("更新日誌.txt", 'r')
        i = 0
        for line in log.readlines():
            i += 1
            text = font4.render(line[:-1], True, (255, 255, 255))
            screen.blit(text, (70, 150+45*i))
        
        up_log.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if ok_button.detect(pos) and event.type == pygame.MOUSEBUTTONDOWN:
                game_status = 0

        pygame.display.update()
        

pygame.quit()