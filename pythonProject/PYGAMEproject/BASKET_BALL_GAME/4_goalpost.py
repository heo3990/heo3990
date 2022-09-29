import pygame
import os
import math,random

class Bar(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.speed = 8
        self.to_left = 0
        self.to_right = 0

    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x += (self.to_left + self.to_right)

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > (screen_width//2) - self.rect.width:
            self.rect.x = (screen_width//2) - self.rect.width

class Ball(pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def first_move(self, bar_posx, bar_width):
        self.rect.x += bar_posx

        if self.rect.x < ((bar_width//2) - (self.rect.width//2)):
            self.rect.x = ((bar_width//2) - (self.rect.width//2))
        elif self.rect.x > (screen_width//2) - ((bar_width//2) + (self.rect.width//2)):
            self.rect.x = (screen_width//2) - ((bar_width//2) + (self.rect.width//2))

    def move(self,angle,speed):
        global g, ball_wall_collision
        if not ball_wall_collision:
            rad_angle = math.radians(angle)
        else:
            rad_angle = math.radians(180 - angle)

        to_x = (speed/4) * math.cos(rad_angle)
        to_y = ((speed/4) * math.sin(rad_angle) * -1) + g
        
        self.rect.x += to_x
        self.rect.y += to_y

        g += 0.3

        if self.rect.x > screen_width - self.rect.width:
            ball_wall_collision = True
        
        if self.rect.y > screen_height:
            return 1

    def ball_goalpost_collision(self,sprite):
        if pygame.sprite.collide_rect(self, sprite):
                return sprite


class Aim_line(pygame.sprite.Sprite):
    def __init__(self,image,position,angle):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(bottomleft=position)
        self.original_image = image
        self.angle = angle
        self.to_angle_up = 0
        self.to_angle_down = 0
        self.angle_speed = 2

    def draw(self,screen):
        screen.blit(self.image, self.rect)
        
    def move(self, bar_posx, bar_width):
        self.rect.x += bar_posx

        if self.rect.x < ((bar_width//2) + 20):
            self.rect.x = ((bar_width//2) + 20)
        elif self.rect.x > ((screen_width//2) - (bar_width//2)) + 20:
            self.rect.x = ((screen_width//2) - (bar_width//2)) + 20

    def rotate(self, angle,aim_position):
        self.angle += angle

        if self.angle > 80:
            self.angle = 80
        elif self.angle < 10:
            self.angle = 10
        
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(bottomleft=aim_position)

class Goalpost(pygame.sprite.Sprite):
    def __init__(self,image,position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)

    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def move(self):
        global goalpost_to_down
        if goalpost_to_down:
            self.rect.y += 4
        else:
            self.rect.y -= 4

        if self.rect.y >= 600:
            goalpost_to_down = False
        elif self.rect.y <= 100:
            goalpost_to_down = True


def write_text(font,text,color,x,y,screen):
    text_obj = font.render(text,True, color)
    text_rect = text_obj.get_rect(center=(x,y))
    screen.blit(text_obj,text_rect)

def game_restart():
    global start, ball_wall_collision, ball_speed, ball_speed_num, g, goalpost_y, goalpost,\
        goalpost_to_down
    g = 0.5
    start = False
    ball_wall_collision = False
    ball_speed = 0
    ball_speed_num = 0
    ball.rect.centerx = bar.rect.centerx
    ball.rect.centery = bar.rect.y - 10
    aim.angle = 45
    del goalpost
    goalpost_y = random.randint(100,screen_height-300)
    goalpost = Goalpost(goalpost_image,(screen_width-30,goalpost_y))
    goalpost_to_down = True
    

pygame.init()
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("BASKET GAME")
clock = pygame.time.Clock()

# 이미지 불러오는 폴더 경로 설정
current_folder = os.path.dirname(__file__)

# 배경화면 불러오기
background = pygame.image.load(os.path.join(current_folder, 'background.png'))

# Bar 이미지 불러오기
bar_image = pygame.image.load(os.path.join(current_folder,'bar.png'))
bar = Bar(bar_image, (screen_width//4, screen_height - 200))

# Ball 이미지 불러오기
ball_image = pygame.image.load(os.path.join(current_folder,'ball.png'))
ball = Ball(ball_image, (bar.rect.centerx, bar.rect.y - 10))

# aim 이미지 불러오기
aim_image = pygame.image.load(os.path.join(current_folder, 'aim.png'))
aim = Aim_line(aim_image, ((bar.rect.centerx + 20), bar.rect.y + 5),45)

# 골대 이미지 불러오기
goalpost_image = pygame.image.load(os.path.join(current_folder,'goalpost.png'))
goalpost_y = random.randint(100,screen_height-300)
goalpost = Goalpost(goalpost_image,(screen_width-30,goalpost_y))
goalpost_to_down = True

# 색깔
RED = (255,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)

# 시작여부
start = False

# 공 스피드
ball_speed = 0
ball_speed_num = 0

# 중력, 벽과 충돌 체크
g = 0.5
ball_wall_collision = False

# 게임 재개
is_game_end = False

# 폰트
game_font = pygame.font.Font(None,80)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                bar.to_left -= bar.speed
            elif event.key == pygame.K_RIGHT:
                bar.to_right += bar.speed
            elif event.key == pygame.K_UP:
                aim.to_angle_up += aim.angle_speed
            elif event.key == pygame.K_DOWN:
                aim.to_angle_down -= aim.angle_speed
            elif event.key == pygame.K_SPACE:
                if ball_speed == 100:
                    break
                ball_speed_num = 1
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                bar.to_left = 0
            elif event.key == pygame.K_RIGHT:
                bar.to_right = 0
            elif event.key == pygame.K_UP:
                aim.to_angle_up = 0
            elif event.key == pygame.K_DOWN:
                aim.to_angle_down = 0
            elif event.key == pygame.K_SPACE:
                ball_speed_num = 0
                start = True

    screen.blit(background,(0,0))

    if ball_speed != 100:
        ball_speed += ball_speed_num

    bar.draw(screen)
    bar.move()
    ball.draw(screen)
    if not start:
        ball.first_move((bar.to_left + bar.to_right), bar.rect.width)
        aim.move((bar.to_left + bar.to_right), bar.rect.width)
        aim.rotate(aim.to_angle_up+aim.to_angle_down,((bar.rect.centerx + 20), bar.rect.y + 5))
        aim.draw(screen)
    else:
        ball.move(aim.angle, ball_speed - 10)
        if ball.move(aim.angle, ball_speed) == 1:
            print("失敗")
            game_restart()

    goalpost.draw(screen)
    goalpost.move()
    if ball.ball_goalpost_collision(goalpost):
        print("成功")
        game_restart()


    write_text(game_font,f"PW : {ball_speed}",RED,150,700,screen)
    write_text(game_font,f"angle : {aim.angle}",BLUE,150,750,screen)

    pygame.display.update()

pygame.quit()
