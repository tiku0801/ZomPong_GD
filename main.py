import pygame
import sys
from setting import Setting
from zombie import Zombie, STATUS
import random
from hammer import Hammer
#x = 96, 356, 671
#y = 170, 420, 670

class ZomPongGame:
    def __init__(self):
        pygame.init()
        self.setting = Setting()
        self.hammer = Hammer(int(self.setting.screen_width/2), int(self.setting.screen_height/2))
        self.zombies = [Zombie(90,172),Zombie(350,172),Zombie(615,172),
                        Zombie(90,424),Zombie(350,424),Zombie(615,424),
                        Zombie(90,676),Zombie(350,676),Zombie(615,676)]
        self.timer = 60
        self.score = 0
        self.miss = 0
        self.hammer_frame_count = 0
        self.game_over = False

        self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))
        pygame.display.set_caption('ZomPong')

        self.bg_img = pygame.image.load('image\\GAME_SCREEN.png')
        self.over_img = pygame.image.load('image\\GAME_OVER_SCREEN.png')

        self.zombieIdle = [pygame.image.load('zombie_sprite\\resize_2\\Idle1.png'),
                           pygame.image.load('zombie_sprite\\resize_2\\Idle2.png'),
                           pygame.image.load('zombie_sprite\\resize_2\\Idle3.png'),
                           pygame.image.load('zombie_sprite\\resize_2\\Idle4.png')]
        self.hammerAttack = [
            img for img in [pygame.image.load('hammer_sprite\\resize\\Hammer1.png'),
                            pygame.image.load('hammer_sprite\\resize\\Hammer2.png'),
                            pygame.image.load('hammer_sprite\\resize\\Hammer3.png')]
            for _ in range(2)
        ]
        self.zombieDead = [pygame.image.load('zombie_sprite\\resize_2\\Dead1.png'),
                           pygame.image.load('zombie_sprite\\resize_2\\Dead2.png'),
                           pygame.image.load('zombie_sprite\\resize_2\\Dead3.png'),
                           pygame.image.load('zombie_sprite\\resize_2\\Dead4.png'),
                           pygame.image.load('zombie_sprite\\resize_2\\Dead5.png'),
                           pygame.image.load('zombie_sprite\\resize_2\\Dead6.png'),
                           pygame.image.load('zombie_sprite\\resize_2\\Dead7.png'),
                           pygame.image.load('zombie_sprite\\resize_2\\Dead8.png')]

        pygame.mixer.music.load('music\\bg_music.mp3')
        pygame.mixer.music.play(-1)
        self.knock_out_sound = pygame.mixer.Sound('music\\knock_out.wav')
        self.knock_out_sound.set_volume(0.5)

    def run_game(self):
        clock = pygame.time.Clock()
        frame_count = 0
        while True:
            print(self.timer)
            if self.timer == 0:
                self.game_over = True
            else:
                frame_count += 1
                if frame_count % self.setting.fps == 0:
                    self.timer -= 1
                    if self.timer > 2:
                        self.update_exist_time()
                        self.create_zombie()

            self.check_events()
            self.update_screen(frame_count//4)
            clock.tick(self.setting.fps)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game_over: continue
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.hammer.update_hammer(pos[0], pos[1], True)
                self.hammer_frame_count = 0
                if self.check_collison(pos[0], pos[1]):
                    self.knock_out_sound.play()
                    self.score += 1

            self.hammer.update_hammer(pos[0], pos[1])

    def update_screen(self, frame_count):
        if self.game_over: 
            self.screen.fill(pygame.Color('black'))
            self.screen.blit(self.over_img, (120,10))
            self.draw_over_info()
            pygame.display.flip()
        else:
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(self.bg_img, (0, 0))
            self.draw_info()
            self.update_zombies(frame_count)
            self.update_hammer()
            pygame.display.flip()

    def create_zombie(self):        
        count = 0
        if random.randint(0,1) == 1:
            max_zombie_in_one_time = self.setting.max_zom
        else:
            max_zombie_in_one_time = 1
        for i in range(len(self.zombies)):
            hole = random.randint(0,len(self.zombies)-1)
            if random.randint(0,1) == 1:
                if self.zombies[hole].status == STATUS.WAITING and self.zombies[hole].height == 0:
                    count+=1 
                    self.zombies[hole].status = STATUS.APPEARING
                    if count == max_zombie_in_one_time:
                        break

    def update_exist_time(self):
        for zombie in self.zombies:
            zombie.exist_time += 1

    def update_hammer(self):
        if self.hammer.isClick:
            hammer_frame = self.hammerAttack[self.hammer_frame_count % len(self.hammerAttack)]
            self.hammer_frame_count += 1
            if self.hammer_frame_count >= len(self.hammerAttack):
                self.hammer.isClick = False
        else:
            hammer_frame = self.hammerAttack[0]
        self.screen.blit(hammer_frame, (self.hammer.x_pos, self.hammer.y_pos))   

    def check_collison(self, x_mouse, y_mouse):
        for zombie in self.zombies:
            if zombie.check_hit(x_mouse, y_mouse):
                zombie.status = STATUS.HIT
                zombie.dead_frame_count = 0
                return True
        return False

    def update_zombies(self, frame):
        missed_zombie = [zombie for zombie in self.zombies if zombie.status == STATUS.MISSED]
        self.miss += len(missed_zombie)
        for i,zombie in enumerate(self.zombies):
            if zombie.status == STATUS.DELETED or zombie.status == STATUS.MISSED:
                    zombie.status = STATUS.WAITING
            elif zombie.status == STATUS.HIT:
                if zombie.dead_frame_count < len(self.zombieDead):
                    dead_frame = self.zombieDead[zombie.dead_frame_count]
                    self.screen.blit(dead_frame, (zombie.x_pos, zombie.y_pos - zombie.height))
                    zombie.dead_frame_count += 1
                zombie.disappear()
                zombie.draw_zom()
            elif zombie.status == STATUS.APPEARING or zombie.status == STATUS.DISAPPEARING:
                zombie.move()
                zombie.disappear()
                zombie.draw_zom()
                sprite = self.zombieIdle[frame % len(self.zombieIdle)]
                cropped_image = sprite.subsurface((0, 0, sprite.get_rect().width, zombie.height))
                self.screen.blit(cropped_image, (zombie.x_pos, zombie.y_pos - zombie.height))
            
            if zombie.status == STATUS.WAITING:
                if self.timer <= self.setting.level_time[0] and self.timer > self.setting.level_time[1]: zombie.speed = self.setting.zom_speed[0]
                if self.timer <= self.setting.level_time[1]: zombie.speed = self.setting.zom_speed[1]

    def draw_info(self):
        time = self.setting.font.render(f'Time: {str(self.timer)}', True, pygame.Color('white'))
        time_rect = time.get_rect()
        time_rect.bottomright = (750, 50)
        self.screen.blit(time, time_rect)

        score = self.setting.font.render(f'Score: {str(self.score)}', True, pygame.Color('white'))
        score_rect = score.get_rect()
        score_rect.bottomright = (500, 50)
        self.screen.blit(score, score_rect)

        miss = self.setting.font.render(f'Miss: {str(self.miss)}', True, pygame.Color('white'))
        miss_rect = miss.get_rect()
        miss_rect.bottomright = (250, 50)
        self.screen.blit(miss, miss_rect)

    def draw_over_info(self):
        miss = self.setting.font.render(f'Miss: {str(self.miss)}', True, pygame.Color('white'))
        miss_rect = miss.get_rect()
        miss_rect.bottomleft = (350, 375)
        self.screen.blit(miss, miss_rect)

        score = self.setting.font.render(f'Score: {str(self.score)}', True, pygame.Color('white'))
        score_rect = score.get_rect()
        score_rect.bottomleft = (350, 325)
        self.screen.blit(score, score_rect)
            

if __name__ == '__main__':
    new_game = ZomPongGame()
    new_game.run_game()
