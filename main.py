import sys, logging, open_color, arcade, os, random

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = ""

STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
NUM_ENEMIES = 3
ENEMY_HP = 100
HIT_SCORE = 20
KILL_SCORE = 100
PLAYER_HEALTH = 500



class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        '''
        super().__init__("assets/laserRed.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class EnemyBullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the enemy bullet
        '''
        super().__init__("assets/laserGreen.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the enemy bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    #Spawns player in the middle of the screen with PLAYER_HEALTH health
    def __init__(self):
        super().__init__("assets/playerShip.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION
        self.hp = PLAYER_HEALTH
    
    def update(self, horiz, vert):
        '''
        Moves the player, which can now be vertical and horizontal
        '''
        self.center_x += horiz
        self.center_y += vert
    
    

class Meteor(arcade.Sprite):
    def __init__(self):
        #I wanted variety, so sprites and their spawns are random within limits
        #I think it is okay if multiple spawn on top of each other. The player will
        #take damage from all, making it more punishing to be hit by them

        #Determening sprite
        self.sprite = random.randint(0, 5)
        if(self.sprite == 0):
            super().__init__("assets/meteorBrown_big1.png", 0.5)
        elif(self.sprite == 1): 
            super().__init__("assets/meteorBrown_big1.png", 0.5)
        elif(self.sprite == 2): 
            super().__init__("assets/meteorGrey_small1.png", 0.5)
        elif(self.sprite == 3): 
            super().__init__("assets/meteorGrey_big2.png", 0.5)
        elif(self.sprite == 4):
            super().__init__("assets/meteorBrown_med3.png", 0.5)
        else:
            super().__init__("assets/meteorBrown_med1.png", 0.5)

        #Determining spawn location
        self.sprite = random.randint(0, 5)
        if(self.sprite == 0):
            (self.center_x, self.center_y) = (0, 200)
        elif(self.sprite == 1): 
            (self.center_x, self.center_y) = (800, 100)
        elif(self.sprite == 2): 
            (self.center_x, self.center_y) = (20, 300)
        elif(self.sprite == 3): 
            (self.center_x, self.center_y) = (800, 50)
        elif(self.sprite == 4):
            (self.center_x, self.center_y) = (20, 700)
        else:
            (self.center_x, self.center_y) = (800, 400)

        #Velocities are onnly horizontal and are based on spawn location
        if(self.sprite == 0):
            self.speed = 5
        elif(self.sprite == 1): 
            self.speed = -5
        elif(self.sprite == 2): 
            self.speed = 5
        elif(self.sprite == 3): 
            self.speed = -5
        elif(self.sprite == 4):
            self.speed = 5
        else:
            self.speed = -5

    def update(self):
        self.center_x += self.speed
        
    

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes an enemy UFO
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/ufoGreen.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
        self.updateNumber = 2

    def update(self):
        '''
        Moves the ship, which will sway from side to side
        '''
        self.center_x += self.updateNumber

class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        #A lot of variables, hopefully names should be clear
        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.meteor_list = arcade.SpriteList()
        self.player = Player()
        self.playerDY = 0
        self.playerDX = 0
        self.score = 0
        self.hover = 3
        self.timer = 0
        self.damage_timer = 0
        self.bullet_timer = 0
        self.spawnTimer = 0
        self.bulletTime = 60
        self.enemyHitScore = 10
        self.enemyHP = 100
        self.meteorTimer = 0
        self.meteors = 3
        self.level = 1

    #Spawns first set of UFOs
    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES):
            x = 120 * (i*2) + 170
            y = 550
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)


    #Moves all bullets, ships, meteors, and UFOs
    def update(self, delta_time):
        self.bullet_list.update()
        self.player.update(self.playerDX, self.playerDY)
        self.enemy_list.update()
        self.enemy_bullet_list.update()
        self.meteor_list.update()

        #Spawning meteors. They spawn every 150 ticks.
        self.meteorTimer += 1
        if(self.meteorTimer == 150):
            self.meteorTimer = 0
            for i in range(self.meteors):
                met = Meteor()
                self.meteor_list.append(met)

        
        #Making enemies sway side to side, which is every 20 ticks
        #Increments spawn timers. They can only respawn on an interval
        self.timer += 1
        self.spawnTimer += 1
        if(self.timer == 20):
            for e in self.enemy_list:
                e.updateNumber *= -1
            self.timer = 0

        #Collision with meteors
        #They are allowed to spawn on top of each other, but randomly
        #When they do that, the player loses points and health for both
        for c in arcade.check_for_collision_with_list(self.player, self.meteor_list):
            self.score -= 50
            self.damage_indicator = str(50)
            self.damage_timer = 0
            #This ticks a lot when colliding, so damage is not that much per tick
            #but adds up to a lot during play
            self.player.hp -= 15


        #Respawning enemies, making levels more difficult, larger rewards
        #Enemies only respawn when player is alive
        if (len(self.enemy_list) == 0 and self.spawnTimer % 50 == 0 and self.player.hp > 0):
            for i in range(NUM_ENEMIES):
                x = 120 * (i*2) + 170
                y = 550
                self.enemyHP *= 1.5
                self.enemyHitScore *= 2
                self.level += 1
                self.meteors += 1
                if(self.bulletTime >= 30):
                    self.bulletTime -= 10
                enemy = Enemy((x,y))
                enemy.hp = self.enemyHP
                self.enemy_list.append(enemy)

        #Checking for bullet collisions
        #Score is based on level
        for e in self.enemy_list:
             #check_for_collision_with_list registers hits many times from one bullet. This system only registers a hit once.
            for b in self.bullet_list:
                if ((b.center_y == e.center_y + 5 or b.center_y == e.center_y) and ((b.center_x >= e.center_x - 45) and (b.center_x <= e.center_x + 45))):
                    self.score += HIT_SCORE * self.level
                    e.hp -= BULLET_DAMAGE
                    if (e.hp <= 0):
                        e.kill()
                        self.score += KILL_SCORE * self.level
        
        #Coding enemy bullets. They get faster with every respawn
        self.bullet_timer += 1
        if(self.bullet_timer > self.bulletTime):
            for e in self.enemy_list:
                x = e.center_x
                y = e.center_y - 15
                enemyBullet = EnemyBullet((x,y),(0,-10),BULLET_DAMAGE)
                self.enemy_bullet_list.append(enemyBullet)
            self.bullet_timer = 0

        #Coding the player damage
        for b in self.enemy_bullet_list:
                if ((b.center_y == self.player.center_y + 5 or b.center_y == self.player.center_y) and ((b.center_x >= self.player.center_x - 45) and (b.center_x <= self.player.center_x + 45))):
                    self.score -= self.enemyHitScore * 3
                    self.damage_indicator = str(-20)
                    self.damage_timer = 0
                    self.player.hp -= 20
                    
        #Making damage text disappear after a while
        self.damage_timer += 1
        if(self.damage_timer > 70):
            self.damage_indicator = " "

        #I still can't get player.kill() to work, so this is how I simulate it.
        #I despawn all meteors and UFOs, stop drawing the player, and disable the firing of bullets
        #Then the text with the final score shows on the screen.
        if(self.player.hp < 0):
            for m in self.meteor_list:
                m.kill()
            for e in self.enemy_list:
                e.kill()
            self.timer = 500
            self.meteorTimer = 500
            self.damage_indicator = " "


    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        #This part simulates a Game Over screen
        if(self.player.hp > 0):
            self.player.draw()
            self.bullet_list.draw()
            arcade.draw_text("Score: " +str(self.score), 20, SCREEN_HEIGHT - 40, open_color.green_3, 16)
            arcade.draw_text("Health: " + str(self.player.hp), 710, SCREEN_HEIGHT - 40, open_color.red_7, 14)
            arcade.draw_text("Level " + str(self.level), 710, 40, open_color.blue_4, 14)
        else:
            arcade.draw_text("Your final score was " + str(self.score) + " points.",
            SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT /2, open_color.red_7, 32)
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()
        self.meteor_list.draw()
        arcade.draw_text(self.damage_indicator, self.player.center_x, self.player.center_y + 10, (255, 0, 0), 16)




    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.playerDX = -5
        elif key == arcade.key.RIGHT:
            self.playerDX = 5
        elif key == arcade.key.UP:
            self.playerDY = 5
        elif key == arcade.key.DOWN:
            self.playerDY = -5
        elif key == arcade.key.SPACE and self.player.hp > 0:
            #Fires bullets if player is alive
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT:
            self.playerDX += 5
        elif key == arcade.key.RIGHT:
            self.playerDX -= 5
        elif key == arcade.key.UP:
            self.playerDY -= 5
        elif key == arcade.key.DOWN:
            self.playerDY += 5


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()