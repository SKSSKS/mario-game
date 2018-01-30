import pygame
import sys
import time

#game engine initialization
pygame.init()

#fps
clock = pygame.time.Clock()
fps = 120

#Main screen of the game
size = [1200,600]
screen = pygame.display.set_mode(size)
screen.fill([255,255,255])

#background image
background_img = pygame.image.load( 'background_01.png').convert()
background_img = pygame.transform.scale( background_img, size )

#set caotion++++++++++++++++++++++++++++++++++++++++++++++++++++
pygame.display.set_caption("MARYO")



class Images(pygame.sprite.Sprite):
        
        def __init__(self,img):
            #initialize super class
            super(Images,self).__init__()
            
            self.image = pygame.image.load(img)
            self.rect = self.image.get_rect()
            self.image.set_colorkey(    [   0,  0,  0]  )

# To fire bullete
class fire(pygame.sprite.Sprite):
    def __init__(self):
        super(fire, self).__init__()
        
        self.image = pygame.image.load("fireball.png")
        self.image = pygame.transform.scale(self.image,[30,20])
        self.rect  = self.image.get_rect()
    
    def update(self):
        self.rect.x -= 10

#Creatin sprite group
all_sprite = pygame.sprite.Group()
fire_list = pygame.sprite.Group()

#===============================================================================
class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        
        file = open("score_card.txt", 'r')
        file = file.readline()
        self.i = file
        
        self.score = 1
        self.game_level = 1
        
        self.image = pygame.font.SysFont(None, 25, True, False)
        self.image = self.image.render(str(self.score), True, [255,255,255])
        self.rect = self.image.get_rect()
        self.rect.center = [300,60]
    
    def update(self):
        
        self.score += 0.1
        
        file = open("score_card.txt", 'r')
        file = file.readline()
        self.i = file
        self.image = pygame.font.SysFont(None, 25, True, False)
        self.image = self.image.render("Score: "+str(int(self.score))+"| Top score: "+self.i+" Level:"+str(self.game_level), True, [255,255,255])
        if int( self.score ) % 100 == 0:
            self.game_level += 1
            level() 
            
hit = Score() # object of score
upper_img = Images("cactus_bricks.png")
lower_img = Images("fire_bricks.png")
player     = Images("maryo.png")
enemy = Images("dragon.png")

# to set position of bullete
def shoot():
    bullet = fire()
    # Set the bullet so it is where the player is
    bullet.rect.x = enemy.rect.x
    bullet.rect.y = enemy.rect.y + 30
    # Add the bullet to the lists
    all_sprite.add(bullet)
    fire_list.add(bullet)

#to update position of upper and lower images for level

def level():
    
    hit.score = 1
    lower_img.rect.y -= 25
    upper_img.rect.y += 25
    hit.rect.y = upper_img.rect.bottom + 10
    if player.rect.top < upper_img.rect.bottom:
        player.rect.top = upper_img.rect.bottom + 1
    elif player.rect.bottom > lower_img.rect.top:
        player.rect.bottom = lower_img.rect.top - 1


    
#===============================================================================

#===============================================================================


#===============================================================================
def gameTopScore():
    try:
        file = open("score_card.txt","r")
        file = file.readlines()
        i = file[0]
        i = int(i)
        if(hit.score > i):
            file = open("score_card.txt","w")
            file.write(str(int(hit.score)))
            file.close()
    except:
        file = open("score_card.txt","w")
        file.write(str(int(hit.score))) 
        file.close()
#===============================================================================
def gameOver():
    gameTopScore()
    
    pygame.mixer.music.load("mario_dies.wav")
    pygame.mixer.music.play(1,0)
    
    end = Images("end.png")
    end.rect.center = [int(size[0]/2), int(size[1]/2)]
    all_sprite.add(end)
    all_sprite.draw(screen)
    time.sleep(3)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                done = True
                all_sprite.remove(end)
        all_sprite.draw(screen)
        pygame.display.flip()
    if done:
        all_sprite.empty()
        main()

#===============================================================================
def game_start():
    start = Images("start.png")
    start.rect.center = [int(size[0]/2), int(size[1]/2)]
    all_sprite.add(start)
    done = False
    while not done:
        screen.fill([0,0,0])
        all_sprite.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                all_sprite.remove(start)
                done = True
        all_sprite.draw(screen)
        pygame.display.flip()
        clock.tick(10)
    if done:
        main()


#===============================================================================
#for score




#===============================================================================
def main():
    
    

    y_speed = 0        
    hit.score = 1
    #load upper image++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    upper_img.rect.x = 0
    upper_img.rect.y = -150
    
    #load lower image
    
    lower_img.rect.x = 0
    lower_img.rect.y = 550
    
    #load player
    
    p_speed = 0
    player.rect.y = 200
    player.rect.x = 50
    
    #load enemy
    enemy.rect.x = 1100
    enemy.rect.y = upper_img.rect.bottom
    e_speed = 5
    
    
    
    # add sprite into list
    all_sprite.add(lower_img) #add lower image
    all_sprite.add(upper_img) #add upper image
    all_sprite.add(player)    #add player
    all_sprite.add(enemy)     #add enemy
    
    #Creating user event to fire bullet continuously
    fireing_bullet = pygame.USEREVENT
    pygame.time.set_timer(fireing_bullet,700)
    
    
    
    #music
    pygame.mixer.music.load("mario_theme.wav")
    pygame.mixer.music.play(-1, 0.0)
    
    all_sprite.add(hit)
    
    while True:
        screen.blit( background_img,[0,0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                file = open("score_card.txt","r")
                for i in file:
                    if int(i) < hit.score:
                        gameTopScore()
                pygame.quit()
                sys.exit()
     
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p_speed = -5
                
                        
            elif event.type == fireing_bullet:
                shoot()    
            else:
                p_speed = 3
        if enemy.rect.bottom > lower_img.rect.top + 10:
            e_speed = -10
        elif enemy.rect.y < upper_img.rect.bottom :
            e_speed = 10
        
        enemy.rect.y += e_speed
        
        player.rect.y += p_speed
        
        
        if player.rect.top < upper_img.rect.bottom:
            p_speed = 0
            gameOver()
        elif player.rect.bottom > lower_img.rect.top :
            gameOver()
            p_speed = 0
        
        
        
        
            
        all_sprite.update()
        
        
    
        
        
        for bullet in fire_list:
            
            player_hit = pygame.sprite.spritecollide(player, fire_list,True)
            
            for i in player_hit:
                gameOver()
                
    
            
            if bullet.rect.x < -10:
                fire_list.remove(bullet)
                all_sprite.remove(bullet)
                   
        all_sprite.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    game_start()
