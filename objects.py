import pygame

class Bird(pygame.sprite.Sprite):

    #變數
    y = 500 #垂直位置
    dy = 0 #垂直速度
    ay = 0.25 #垂直加速度
    sp_num = 0
    sprites = []

    #初始化
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        #載入動畫包
        for i in range(1, 4):
            pic = pygame.image.load(f"圖片/Bird_{i}.png")
            self.sprites.append(pygame.transform.scale(pic, (68, 48)).convert_alpha())

        self.image = self.sprites[self.sp_num//5]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (80, 500)
    
    def update(self):

        #計算新座標
        self.dy += self.ay
        self.y += self.dy
        self.rect.top = self.y

        #更新動畫
        self.sp_num = (self.sp_num + 1) % 15
        self.image = self.sprites[self.sp_num//5]
        self.mask = pygame.mask.from_surface(self.image)

        #邊界偵測
        if(self.rect.top <= 0):
            self.dy = 1

        if(self.rect.bottom >= 1020):
            return True
    
    def jump(self):
        self.dy = -7
    
    def reset(self):

        self.rect.topleft = (80, 500)
        self.dy = 0
        self.y = 500


class Tube(pygame.sprite.Sprite):

    #變數
    y = 0 #高度
    x = 640 #水平位置
    dx = -3 #水平速度

    #初始化
    def __init__(self, position):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(f"圖片/{position}_tube.png")
        self.image = pygame.transform.scale(self.image, (100, 600)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.x = 640
        self.y = self.y
        self.rect = self.image.get_rect()
        if position == "Top":
            self.rect.topleft = (640, -200)
        else:
            self.rect.topleft = (640, 600)
    
    def update(self, hight):

        #計算新座標
        self.y = hight
        self.x += self.dx
        self.rect.left = self.x
        self.rect.top = self.y

        self.mask = pygame.mask.from_surface(self.image)

        if(self.rect.right <= 0):
            self.x = 640
            return True

    def reset(self):

        self.x = 640
        
class Button(pygame.sprite.Sprite):

    #變數
    x = 0
    y = 0
    sprites = []
    width = 0
    hight = 0

    def __init__(self, name, x, y, width, hight, sp_num, scalex):

        pygame.sprite.Sprite.__init__(self)

        self.sprites = []
        for i in range(1, sp_num+1):
            pic = pygame.image.load(f"圖片/{name}_{i}.png")
            self.sprites.append(pygame.transform.scale(pic, (width*scalex, hight*scalex)).convert_alpha())

        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left = x
        self.rect.top = y
        self.width = width*scalex
        self.hight = hight*scalex

    def detect(self, pos):

        if(pos[0]>=self.x and pos[0]<=self.x+self.width) and (pos[1]>=self.y and pos[1]<=self.y+self.hight):
            self.image = self.sprites[1]
            return True
        else:
            self.image = self.sprites[0]
            return False