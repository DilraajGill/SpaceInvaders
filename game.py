try:
    import simplegui

except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from vector import Vector
import random
import time

#-----------------------------------------------------------------------------------
class Spritesheet:
    
    def __init__(self, sprite_url, columns, rows, dest_centre, velocity, spriteType):
        self.img = simplegui.load_image(sprite_url)
        self.dest_centre = dest_centre # position 

        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.columns = columns
        self.rows = rows
        self.frame_index = [0, 0] # to access different frame change the frame_index 
        self.vel = velocity
        self.pos = Vector(dest_centre[0], dest_centre[1])
        self.type = spriteType

        self.frame_width = self.width/columns
        self.frame_height = self.height/rows

        self.frame_centre_x = self.frame_width/2
        self.frame_centre_y = self.frame_height/2

    def draw(self, canvas):
        frame_pos_x = self.frame_width * self.frame_index[0] + self.frame_centre_x
        frame_pos_y = self.frame_height * self.frame_index[1] + self.frame_centre_y

        source_centre = (frame_pos_x, frame_pos_y)
        source_dim = (self.frame_width, self.frame_height)
        dest_size = (50, 50)

        canvas.draw_image(self.img, source_centre,
                          source_dim, [self.pos.x, self.pos.y], dest_size)
    def update(self):
        self.pos.add(self.vel)
#----------------------------------------------------------------------------------
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.space = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        
        elif key == simplegui.KEY_MAP['left']:
            self.left = True

        elif key == simplegui.KEY_MAP['space']:
            self.space = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False

        elif key == simplegui.KEY_MAP['left']:
            self.left = False
            
        elif key == simplegui.KEY_MAP['space']:
            self.space = False

 #-------------------------------------------------------------------------------   
class Interaction:
    def __init__(self, game, keyboard, mouse):
        self.game = game
        self.keyboard = keyboard
        self.mouse = mouse

    def updateWelcome(self):

        if not isinstance(self.mouse.click_pos(), type(None)):
            if self.mouse.click_pos().x in range(280, 370) and self.mouse.click_pos().y in range(180,220):
                self.game.screen = "gameplayEasy"   
              
            if self.mouse.click_pos().x in range(424, 564) and self.mouse.click_pos().y in range(180, 220):
                self.game.screen = "gameplayMedium"
                
            if self.mouse.click_pos().x in range(616, 706) and self.mouse.click_pos().y in range(180, 220):
                self.game.screen = "gameplayHard"

            if self.mouse.click_pos().x in range(30, 180) and self.mouse.click_pos().y in range(10,40):
                self.game.screen = "instructions"
          
    def updateInstructions(self):
        if not isinstance(self.mouse.click_pos(), type(None)):
            if self.mouse.click_pos().x in range(850, 990) and self.mouse.click_pos().y in range(10, 40):
                self.game.screen = "welcome"

    def updateGameplay(self):
        if self.keyboard.right:
            self.game.player.vel.add(Vector(self.game.playerSpeed, 0))

        elif self.keyboard.left:
            self.game.player.vel.subtract(Vector(self.game.playerSpeed, 0))

        
        if self.keyboard.space and len(self.game.playerBullets) < 10:
            playerX, playerY = self.game.player.pos.get_p()
            newBullet = None
            if self.game.bulletpoweractive:
                newBullet = Bullet(Vector(), self.game, "cyan", Vector(0, 10))

            else:
                newBullet = Bullet(Vector(), self.game, "green")

            newBullet.pos.x = playerX - (newBullet.lineWidth / 2)
            newBullet.pos.y = playerY - (self.game.player.height / 2) - newBullet.lineHeight
            
            if len(self.game.playerBullets) > 0:
                if newBullet.pos.y >= self.game.playerBullets[-1].pos.y + newBullet.lineHeight + 30:
                    self.game.playerBullets.append(newBullet)

            else:
                self.game.playerBullets.append(newBullet)

    def updateGameover(self):
        pass


    def update(self):
        if self.game.screen == "welcome":
            self.updateWelcome()

        elif self.game.screen == "gameplayEasy":
            self.updateGameplay()

        elif self.game.screen == "gameplayMedium":
            self.updateGameplay()

        elif self.game.screen == "gameplayHard":
            self.updateGameplay()
        
        elif self.game.screen == "gameover":
            self.updateGameover()

        elif self.game.screen == "instructions":
            self.updateInstructions()
#-------------------------------------------------------------------------------
class Player:
    def __init__(self, pos, game):
        self.pos = pos
        self.vel = Vector()
        self.image = simplegui.load_image('https://cs.rhul.ac.uk/home/zkac421/sprites/space%20ship.png')
        self.img_centre = (9, 10)
        self.img_dims = (18, 20)
        self.width = 90
        self.height = 100
        self.game = game
        
    def draw(self, canvas):
        canvas.draw_image(self.image, self.img_centre, self.img_dims, self.pos.get_p(), (self.width, self.height))
        if self.pos.x + self.width / 2 < 0: # whole circle off left of screen
            self.pos.x += self.game.frameWidth
        elif self.pos.x - self.width / 2 > self.game.frameWidth: # whole circle off right of screen
            self.pos.x -= self.game.frameWidth
        elif self.pos.x - self.width / 2 < 0: # partial circle off left of screen
            canvas.draw_image(self.image, self.img_centre, self.img_dims, (self.game.frameWidth + self.pos.x, self.pos.y), (self.width, self.height))
        elif self.pos.x + self.width / 2 > self.game.frameWidth: # partical circle off right of screen
            canvas.draw_image(self.image, self.img_centre, self.img_dims, (self.pos.x - self.game.frameWidth, self.pos.y), (self.width, self.height))
    
    def update(self):
        self.pos.add(self.vel)
        self.vel.x *= 0.85
#----------------------------------------------------------------------------------
class Enemy:
    def __init__(self, game, url, score, velocity, pos, width, height, frames):
        self.img = simplegui.load_image(url)
        self.game = game
        self.width = width
        self.height = height
        self.columns = frames 
        self.score = score
        self.health = True
        self.frame_index = [0]
        self.frame_width = self.width / self.columns
        self.frame_height = self.height
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height / 2
        self.v = velocity
        self.pos = pos
        self.frame_clock = 0
        
    def draw(self, canvas):
        source_size = (self.frame_width, self.frame_height)
        dest_size = (50, 50)
        source_centre = (self.frame_width * self.frame_index[0] + self.frame_centre_x,
                        self.frame_centre_y)
        canvas.draw_image(self.img, source_centre, source_size, (self.pos.x, self.pos.y), dest_size)

    def update(self):
        if self.frame_clock % 30 == 0:
            self.drawFrame()
        self.pos.add(self.v)
        self.frame_clock += 1
    
    def drawFrame(self):
        self.frame_index = [self.frame_index[0] + 1]
        if self.frame_index == [self.columns - 1]:
            self.frame_index = [0]

#----------------------------------------------------------------------------------
class Bullet:
    def __init__(self, pos, game, color, vel=Vector(0, 5)):
        self.pos = pos # y position is the top of the line
        self.vel = vel
        self.lineWidth = 5
        self.lineHeight = 10
        self.color = color
        self.game = game 

    def draw(self, canvas):
        x, y = self.pos.get_p()
        canvas.draw_line((x, y), (x,y + self.lineHeight), self.lineWidth, self.color)

    def update(self):
        self.pos.subtract(self.vel)

    def checkLeftScreen(self):
        return self.pos.y + self.lineHeight <= 0

    def hit(self, target):

        distance = target.pos.copy().subtract(self.pos).length()
        return distance <= self.lineHeight + 25
        # 25 is the size of the frame from the centre
#----------------------------------------------------------------------------------
class Mouse: 
    def __init__(self):
        self.mouse_pos = None
        
    def click_handler(self, position):
        self.mouse_pos = Vector(position[0], position[1])
               
    def click_pos(self):
        
        last_click = self.mouse_pos
        return last_click
#----------------------------------------------------------------------------------
class Game:
    def __init__(self):
        self.screen = "welcome" # the different screens will be: "welcome", "gameplay" and "gameover"
        self.frameWidth = 1000
        self.frameHeight = 600
        self.level = 1
        self.count = 0
        self.bonus = True
    
        self.frame = simplegui.create_frame("Alien Jam", self.frameWidth, self.frameHeight)
        self.initWelcome()
        self.initGameplay()
        self.interObj = Interaction(self, Keyboard(), Mouse())

        self.frame.set_mouseclick_handler(self.interObj.mouse.click_handler)
        self.frame.set_draw_handler(self.draw)
        self.frame.set_keydown_handler(self.interObj.keyboard.keyDown)
        self.frame.set_keyup_handler(self.interObj.keyboard.keyUp)

        self.frame.start()


    def initWelcome(self):
        # creates variables needed for welcome screen
        self.welcomeText = "ALIEN JAM"
        self.scoreTable = "SCORE TABLE"
        self.sprite1_url = "https://www.cs.rhul.ac.uk/home/zkac282/cs1822/sprite_animated_1.png"
        self.sprite2_url = "https://www.cs.rhul.ac.uk/home/zkac282/cs1822/sprite_animated_3.png"
        self.sprite3_url = "https://www.cs.rhul.ac.uk/home/zkac282/cs1822/sprite_animated_2.png"
        self.bonusSprite = "https://cs.rhul.ac.uk/home/zjac013/cs1822/babyYoda.png"

        self.welcomeIcons = []

        self.sprite1 = " = 10 POINTS"
        self.sprite2 = " = 20 POINTS"
        self.sprite3 = " = 30 POINTS"
        self.sprite4 = " = 50 POINTS"
        self.spriteTexts = [self.sprite1, self.sprite2, self.sprite3, self.sprite4]

        self.easy = "EASY"
        self.medium = "MEDIUM"
        self.hard = "HARD"
        self.type = "SELECT GAME DIFFICULTY:"
        self.lvlDifficulty = [self.easy, self.medium, self.hard]

        self.instructions = "INSTRUCTIONS"

        self.spriteLineSpacing = 60

        self.livesText = "LIVES"
        self.scoreText = "SCORE: "
        self.lives = []
        self.lifeSprite = "https://www.cs.rhul.ac.uk/home/zjac013/cs1822/planet22.png"
        self.bulletpowerSprite = "https://www.cs.rhul.ac.uk/home/zkac421/sprites/arrowpowerup.png"
        self.playerspeedpowerSprite = "https://www.cs.rhul.ac.uk/home/zkac291/sprites/jerrycan.png"
        self.bulletpoweractive = False
        self.oldSpeed = 0
        
        # add lives to a list 
        self.lives.append(Spritesheet(self.lifeSprite,  1, 1, (140, 25), Vector(0, 0), ""))
        self.lives.append(Spritesheet(self.lifeSprite,  1, 1, (200, 25), Vector(0, 0), ""))
        self.lives.append(Spritesheet(self.lifeSprite,  1, 1, (260, 25), Vector(0, 0), ""))

        # get the width of the text
        self.welcome_width = (self.frameWidth - self.frame.get_canvas_textwidth(self.welcomeText, 60, "monospace")) / 2
        self.scoreTableWidth = (self.frameWidth - self.frame.get_canvas_textwidth(self.scoreTable, 50, "monospace")) / 2
        self.sprite_width = (self.frameWidth - self.frame.get_canvas_textwidth(self.sprite1, 30, "monospace")) / 2
        self.scoreWidth = (self.frameWidth - self.frame.get_canvas_textwidth(self.scoreText, 30, "monospace")) / 2
        self.typeWidth = (self.frameWidth - self.frame.get_canvas_textwidth(self.type, 30, "monospace")) / 2

        self.lvlMedium = (self.frame.get_canvas_textwidth(self.medium, 40, "monospace")) + 280
        self.lvlHard = (self.frame.get_canvas_textwidth(self.hard, 40, "monospace")) + 260*2

        self.lvlWidth = [280, self.lvlMedium, self.lvlHard]

        # icons
        self.welcomeIcons.append(Enemy(self, self.sprite1_url, 10, Vector(0, 0), Vector(self.sprite_width-15, 380+(0*self.spriteLineSpacing)), 468, 152, 3))
        self.welcomeIcons.append(Enemy(self, self.sprite2_url, 10, Vector(0, 0), Vector(self.sprite_width-15, 380+(1*self.spriteLineSpacing)), 633, 150, 3))
        self.welcomeIcons.append(Enemy(self, self.sprite3_url, 10, Vector(0, 0), Vector(self.sprite_width-15, 380+(2*self.spriteLineSpacing)), 627, 152, 3))
        self.welcomeIcons.append(Spritesheet(self.bonusSprite,  2, 1, (self.sprite_width-15, 380+(3*self.spriteLineSpacing)), Vector(0, 0), ""))
        self.powerUp = []
        self.lifePowerUps = 0
        self.lastTime = 0


    def initGameplay(self):
        self.bgURL = "https://www.cs.rhul.ac.uk/home/zjac013/cs1822/b.png"
        self.bgImage = simplegui.load_image(self.bgURL)
        self.bgDims = (self.bgImage.get_width(), self.bgImage.get_height())
        self.bgCentre = (self.bgImage.get_width()/2, self.bgImage.get_height()/2)

        self.enemyList = []
        self.bonusList = []

        self.player = Player(Vector(0, 0), self)
        self.player.pos =  Vector(self.frameWidth // 2, self.frameHeight - self.player.height)
        self.playerBullets = []
        self.enemyBullets = []
        self.score = 0
        self.playerSpeed = 1
       
    def createEnemies(self, rows):
        numEnemiesPerRow = (self.frameWidth // 50)
        if numEnemiesPerRow - 4 > 0:
            numEnemiesPerRow -= 4

        enemyType = 0
        for row in range(rows):
            for col in range(numEnemiesPerRow):
                posX = 50 * col
                posY = 80 + (50 * row) + (15*row) # 80 so it doesn't overlap with lives etc.

                if enemyType == 0:
                    self.enemyList.append(Enemy(self, self.sprite1_url, 10, Vector(self.speed, 0), Vector(posX, posY), 468, 152, 3))

                elif enemyType == 1:
                    self.enemyList.append(Enemy(self, self.sprite2_url, 20, Vector(self.speed, 0), Vector(posX, posY), 633, 150, 3))
                
                else:
                    self.enemyList.append(Enemy(self, self.sprite3_url, 30, Vector(self.speed, 0), Vector(posX, posY), 627, 152, 3))

                enemyType += 1
                enemyType %= 3


    def drawWelcome(self, canvas):
        # Draw icons next to text
        for i in range(len(self.welcomeIcons)):
            icon = self.welcomeIcons[i]
            if i < 3:
                icon.update()

            icon.draw(canvas)
        
        # Draw text on canvas
        for i in range(len(self.spriteTexts)):
            canvas.draw_text(self.spriteTexts[i], [self.sprite_width, 390 + (i*self.spriteLineSpacing)], 30, "white", "monospace")

        for n in range(len(self.lvlDifficulty)):
            canvas.draw_text(self.lvlDifficulty[n], [self.lvlWidth[n], 220], 40, "white", "monospace")
        canvas.draw_text(self.type, [self.typeWidth, 180], 30, "white", "monospace")

        canvas.draw_text(self.instructions, [30, 40], 20, "white", "sans-serif")
            
        canvas.draw_text(self.welcomeText, [self.welcome_width, 90], 60, "white", "monospace")
        canvas.draw_text(self.scoreTable, [self.scoreTableWidth, 320], 50, "white", "monospace")
    
    def drawRound(self, canvas):
        text = "NEXT ROUND"
        if self.level == 1:
            text = "FIRST ROUND"
        nextRoundWidth = (self.frameWidth - self.frame.get_canvas_textwidth(text, 100, "monospace")) / 2
        self.bonus = False

        canvas.draw_text(text, [nextRoundWidth, self.frameHeight / 2], 100, "white", "monospace")

    def moveEnemiesDown(self):  
        
        lastEnemy = self.enemyList[-1]
        lastEnemyCondition = (lastEnemy.v.x > 0 and lastEnemy.pos.x >= self.frameWidth) or (lastEnemy.v.x < 0 and lastEnemy.pos.x <= 0)
        firstEnemy = self.enemyList[0]
        firstEnemyCondition = (firstEnemy.v.x > 0 and firstEnemy.pos.x >= self.frameWidth) or (firstEnemy.v.x < 0 and firstEnemy.pos.x <= 0)

        if firstEnemyCondition or lastEnemyCondition:
            for enemy in self.enemyList:
                enemy.v.x *= -1
                enemy.pos.add(Vector(0, 50))

    def drawBullets(self, enemy):
         
        bullet = Bullet(Vector(), self, "red")
        bullet.pos.x = enemy.pos.x
        bullet.pos.y = enemy.pos.y + 15
        
        if len(self.enemyBullets) > 0:
            if bullet.pos.y >= self.enemyBullets[-1].pos.y:
                self.enemyBullets.append(bullet)
        else:
            self.enemyBullets.append(bullet)


    def drawGameplay(self, canvas, numBullets):
        self.setSpeed(numBullets)
        self.count += 1

        # draw background on the canvas
        canvas.draw_image(self.bgImage, self.bgCentre, self.bgDims, (self.frameWidth / 2, self.frameHeight / 2), (self.frameWidth, self.frameHeight))
       
        # draw player on the canvas
        self.player.update()
        self.player.draw(canvas)

        # draw bullets on the canvas
        removeBullet = []
        removeList = []
        removeEnemy = []

        # send a life when count is in range 1300, 1700
        if self.count % self.randTime() == 0 and self.lifePowerUps == 0:
            self.powerUp.append(Spritesheet(self.lifeSprite,  1, 1, self.randPos(), Vector(0, 1), "extraLife"))
            self.lifePowerUps += 1


        # send a bullet powerup every 2000 counts after level 2
        if (self.level > 2) and (self.count % 2000 == 0):
            self.powerUp.append(Spritesheet(self.bulletpowerSprite,  1, 1, self.randPos(), Vector(0, 1), "bulletSpeed"))


        # send a player speed powerup every other 1000 counts after level 2
        if (self.level > 2) and (self.count % 1000 == 0) and (self.count % 2000 != 0):
            self.powerUp.append(Spritesheet(self.playerspeedpowerSprite,  1, 1, self.randPos(), Vector(0, 1), "playerSpeed"))
        

        self.drawPowerUp(canvas)
        #draw player bullets
        for bullet in self.playerBullets:
            bullet.update()
            bullet.draw(canvas)
            if bullet.checkLeftScreen():
                removeList.append(bullet)

        # next round
        if len(self.enemyList) == 0:
            self.drawRound(canvas)
            if self.count % 100 == 0:
                self.level += 1 
                self.createEnemies(self.level)
        count = 0                  
            
        # draw enemies on the canvas
        for enemy in self.enemyList:
            enemy.update()
            self.moveEnemiesDown()
            enemy.draw(canvas)

            if enemy.frame_index == [enemy.columns - 1]:
                removeEnemy.append(enemy)

            # check if enemy was hit and update the frame        
            for b in self.playerBullets:
                if b.hit(enemy) and enemy.frame_index != [enemy.columns - 1]: # if bullet hits enemy and enemy isn't already hit
                    enemy.frame_index = [enemy.columns - 1]
                    self.score += enemy.score
                    removeList.append(b)

            # remove enemy and a life if y position of enemy is greater than player y position
            if enemy.pos.y > self.player.pos.y and len(self.lives) > 0:
                self.lives.remove(self.lives[len(self.lives)-1])
                removeEnemy.append(enemy)
                if len(self.lives) < 1:
                    self.screen = "gameover"

        # draw bonus sprite
        if not(self.bonus) and random.randint(1,100) == 50:
            self.bonusList.append(Enemy(self, self.bonusSprite, 50, Vector(self.speed, 0), Vector(0, 20), 600, 300, 2))
            self.bonus = True
        if len(self.bonusList) != 0:
            bonusSprite = self.bonusList[0]
            if self.bonusList[0].pos.x > self.frameWidth:
                self.bonusList.clear()
            else:
                self.bonusList[0].update()
                self.bonusList[0].draw(canvas)
                for b in self.playerBullets:
                    if b.hit(bonusSprite) and bonusSprite.frame_index != [bonusSprite.columns - 1]: # if bullet hits enemy and enemy isn't already hit       
                        self.bonusList[0].frame_index = [self.bonusList[0].columns - 1]
                        self.score += self.bonusList[0].score
                        removeList.append(b)
                        self.bonusList.clear()

        for enemy in removeEnemy:
            self.enemyList.remove(enemy)

        # remove player bullets
        for bullet in removeList:
            if bullet in self.playerBullets:
                self.playerBullets.remove(bullet)
        
        # draw lives on the canvas
        self.scoreText = "Score: " + str(self.score).zfill(4)
        canvas.draw_text(self.livesText, [20, 30], 30, "white", "monospace")
        canvas.draw_text(self.scoreText, [self.frameWidth - 200, 30], 30, "white", "monospace")

        for n in self.lives:
            n.draw(canvas)
     
        # draw enemy bullets on canvas
        for n in range(numBullets):
            if len(self.enemyList) > 0 and len(self.enemyBullets) <= numBullets:      
                self.drawBullets(random.choice(self.enemyList))
       
        for b in self.enemyBullets:
            b.draw(canvas)
            b.pos.add(b.vel)
        
            if b.pos.y > self.frameHeight:
                 removeBullet.append(b)
       
            if b.hit(self.player) and len(self.lives) > 0:
                removeBullet.append(b)
                self.lives.remove(self.lives[len(self.lives)-1])
        
        # remove enemy bullet once it disappears from screen        
        for r in removeBullet:
            self.enemyBullets.remove(r)
        if len(self.lives) < 1:
            self.screen = "gameover"   
        

    def setSpeed(self, numBullets):
        if self.level == 1:
            if self.screen == "gameplayEasy":
                self.speed = 1.5
            elif self.screen == "gameplayMedium":
                self.speed = 2
            elif self.screen == "gameplayHard":
                self.speed = 2.5
        if self.level > 5:
            self.speed += 0.25

    def drawGameover(self, canvas):
        # draw background image
        canvas.draw_image(self.bgImage, self.bgCentre, self.bgDims, (self.frameWidth / 2, self.frameHeight / 2), (self.frameWidth, self.frameHeight))
        
        gameOverX = (self.frameWidth - self.frame.get_canvas_textwidth("GAME OVER", 60, "monospace")) / 2
        canvas.draw_text('GAME OVER', (gameOverX, self.frameHeight / 2), 60, 'White', "monospace")

        pointsTextX = (self.frameWidth - self.frame.get_canvas_textwidth("Points: " + str(self.score), 40, "monospace")) / 2
        canvas.draw_text('Points: ' + str(self.score), (pointsTextX, (self.frameHeight / 2) + 60), 40, 'White', "monospace")

    def drawInstructions(self, canvas):
        self.title = "WELCOME"
        self.p1 = "After centuries of peace our galaxy has been attacked"
        self.p2 = "by the most feared enemies of the galaxy."
        self.p3 = "You have been assigned to protect three of our planets."
        self.p4 = "The enemy must be destroyed otherwise the planets will be."
        self.nl = ""

        self.p5 = "Use space bar to fire bullets, left or right arrow keys to move."
        self.p6 = "After you have killed all enemies you are then ready to"
        self.p7 = "fight the mightiest."
        self.p8 = "As you advance the number of enemies will increase."
        self.p9 = "But do not lose hope, we are by your side."
       

        self.p10 = "We will send you power-ups to make the fight easier."
        self.p11 = "Make sure you shoot them before they hit the ground,"
        self.p12 = "otherwise they will be lost."
        self.p13 = "If you feel ready you can choose to go in a more advanced mission."
        self.p14 = "Beware they are more dangerous."
        self.main = "Main Menu"
    
        self.instructionsTxt = [self.p1, self.p2, self.p3, self.p4, self.nl, self.p5, self.p6, 
                        self.p7, self.p8, self.p9, self.nl, self.p10, self.p11, self.p12, self.p13, self.p14]
        
        for n in range(len(self.instructionsTxt)):
            canvas.draw_text(self.instructionsTxt[n], [50, (n+4)*28] , 23,  "green", "monospace")
            
        canvas.draw_text(self.title, [50, 40] , 35,  "green", "monospace")
        canvas.draw_text(self.main, [850, 40] , 25,  "green", "monospace")

    def drawPowerUp(self, canvas):
        removePowerUp = []
        if self.bulletpoweractive and (time.time() - self.lastTime > 5):
            self.bulletpoweractive = False

        elif self.playerSpeed != self.oldSpeed and self.oldSpeed != 0 and (time.time() - self.lastTime > 5):
            self.speed -= 1
            self.oldSpeed = 0
            

        for n in self.powerUp:
            n.update()
            n.draw(canvas)

            for b in self.playerBullets:
                if b.hit(n):
                    if n.type == "extraLife" and len(self.lives) > 0:
                        extraLifePos = (self.lives[len(self.lives)-1].pos.x+60, 25)
                        extraLife = Spritesheet(self.lifeSprite,  1, 1, extraLifePos, Vector(0, 0), "")
                        self.lives.append(extraLife)
                        removePowerUp.append(n)
                        self.lifePowerUps -= 1

                    elif n.type == "bulletSpeed":
                        self.bulletpoweractive = True
                        removePowerUp.append(n)
                        self.lastTime = time.time()


                    elif n.type == "playerSpeed":
                        self.oldSpeed = self.playerSpeed
                        self.playerSpeed += 1
                        removePowerUp.append(n)
                        self.lastTime = time.time()

        if (len(removePowerUp) > 0) and (n in self.powerUp):
            for n in removePowerUp:
                self.powerUp.remove(n)     

    def randPos(self):
        x = random.randrange(10, self.frameWidth)
        return (x, 150)

    def randTime(self):
        return random.randrange(1300, 1700)

    def draw(self, canvas):
        
        self.interObj.update()
        if self.screen == "welcome":
            self.drawWelcome(canvas)

        elif self.screen == "gameplayEasy":
            self.drawGameplay(canvas, 2)
        
        elif self.screen == "gameplayMedium":
            for n in self.enemyBullets:
                n.pos.add(Vector(0,0.5))
            self.drawGameplay(canvas, 4)    
          
        elif self.screen == "gameplayHard":
            for n in self.enemyBullets:
                n.pos.add(Vector(0,1))
            self.drawGameplay(canvas, 6)

        elif self.screen == "gameover":
            self.drawGameover(canvas)

        elif self.screen == "instructions":
            self.drawInstructions(canvas)

game = Game()