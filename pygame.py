#!/usr/bin/env python
# covenvding=utf-8
# -*- coding: utf-8 -*-
import logging
import pygame
import sys
import math

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Konstanter
FPS = 60
SCREEN_SIZE = (800, 600)
CAPTION = "Pygame Example"

COLOR = {'ship': pygame.Color('#FF0000'),
         'ship_fill': pygame.Color('#660000'),
         'bg': pygame.Color('#333333'),
         'thruster': pygame.Color('#7799FF'),
}

# Game states
STATE_PREGAME = 1
STATE_RUNNING = 2
STATE_GAMEOVER = 3

class Controller():
    """Game controller."""

    def __init__(self):
        """Initialize game controller."""
        self.fps = FPS

        pygame.init()
        pygame.mixer.quit()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.crash_font = pygame.font.Font('freesansbold.ttf',20)



        self.player = Player(self)
        self.fuel = 800
        self.points = 0
        self.start_fuel = 800

        self.world = World(self)
        # Initialize game state
        self.game_state = STATE_PREGAME


    def run(self):
        """Main game loop."""
        while True:
            # Hantera event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ALT + F4 or icon in upper right corner.
                    self.quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Escape key pressed.
                    self.quit()

                if self.game_state == STATE_PREGAME:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_state = STATE_RUNNING

                if self.game_state == STATE_RUNNING:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        self.player.engine_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_w:
                        self.player.engine_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                        self.player.right_thruster_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_d:
                        self.player.right_thruster_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                        self.player.left_thruster_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_a:
                        self.player.left_thruster_off()


                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r: #restart
                        logging.info('Resatart')
                        self.game_state = STATE_RUNNING
                        self.player.x = SCREEN_SIZE[0] / 2
                        self.player.y = SCREEN_SIZE[1] / 2
                        self.player.speed = 0
                        self.player.rotation = -math.pi/2
                        self.player.ang_ve = 0
                        self.fuel = 800
                        self.points = 0
                        self.player.left_thruster_off()
                        self.player.right_thruster_off()
                        self.player.engine_off()
                if self.game_state == STATE_GAMEOVER:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  #Continue game
                        self.start_fuel = self.fuel
                        self.game_state = STATE_RUNNING
                        self.player.x = SCREEN_SIZE[0] / 2
                        self.player.y = SCREEN_SIZE[1] / 2
                        self.player.speed = 0
                        self.player.rotation = -math.pi/2
                        self.player.ang_ve = 0
                        self.player.left_thruster_off()
                        self.player.right_thruster_off()
                        self.player.engine_off()
                        if self.player.speed > 0.5 or self.fuel<0 or abs(grader>20):
                            self.fuel = 800
                            self.points = 0


#                    Hantera speltillstånd
            if self.game_state == STATE_PREGAME:
                pass

            if self.game_state == STATE_RUNNING:
                self.player.tick()
                self.world.tick()


                if self.player.y > 554 - 10:
                    if self.player.speed < 0.5 and abs(grader)<20:
                        logging.info('Success!! at {} m/s'.format(round(self.player.speed*5, 2)))
                        if 50<self.player.x<85: #poäng
                            self.points+=50
                        if 200<self.player.x<235:
                            self.points+=20
                        if 130<self.player.x<165:
                            self.points+=40
                        if 500<self.player.x<535:
                            self.points+=10
                        if 280<self.player.x<315:
                            self.points+=20
                        if 640<self.player.x<675:
                            self.points+=40
                        if 740<self.player.x<775:
                            self.points+=50
                        self.poäng =round((self.start_fuel-self.fuel)*0.03)
                        self.points += self.poäng

                        self.fuel+= self.poäng*10
                        self.game_state = STATE_GAMEOVER
                grader = (self.player.rotation +math.pi/2)*180/math.pi
                if self.fuel<=0 or self.player.y < 10:
                    self.game_state = STATE_GAMEOVER

                self.world.draw()
                self.player.draw()
                self.points_text = self.crash_font.render("points: {}".format(str(self.points)),True, (255, 255, 255))
                self.screen.blit(self.points_text,(20, 40))


            if self.game_state == STATE_GAMEOVER:
                logging.info('Points: {} m/s'.format(self.points))
                Success = "Success,"
                Right_speed = "You got the speed right;"
                You_crashed = "You Crashed! at {} m/s,".format(math.floor(self.player.speed*10))
                too_fast = "you must go {} m/s slower" .format(math.floor(self.player.speed*10-2))
                too_much_rotation = "But you had too much rotation ({}) degrees.".format(abs(math.floor(grader)))
                you_got_x_point = "You have {} points".format(self.points)
                forsätt = "press enter to continue"
                Restart = "Press enter to restart"
                To_little_fuel = "Your fueltank is empty"
                if self.fuel>0:
                    if self.player.speed < 0.5:
                        if abs(grader)<20:

                            self.crash_text = self.crash_font.render(Success,True, (255, 0, 0))
                            self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2)))
                            self.crash_text = self.crash_font.render(you_got_x_point,True, (255, 0, 0))
                            self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2+25)))
                            self.crash_text = self.crash_font.render(forsätt,True, (255, 0, 0))
                            self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2+50)))
                        else:
                            self.crash_text = self.crash_font.render(You_crashed,True, (255, 0, 0))
                            self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2-25)))
                            self.crash_text = self.crash_font.render(too_much_rotation,True, (255, 0, 0))
                            self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2)))
                            self.crash_text = self.crash_font.render(you_got_x_point,True, (255, 0, 0))
                            self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2+25)))
                            self.crash_text = self.crash_font.render(Restart,True, (255, 0, 0))
                            self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2+50)))

                    else:
                        self.crash_text = self.crash_font.render(You_crashed,True, (255, 0, 0))
                        self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2-25)))
                        self.crash_text = self.crash_font.render(too_fast,True, (255, 0, 0))
                        self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2)))
                        self.crash_text = self.crash_font.render(you_got_x_point,True, (255, 0, 0))
                        self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2+25)))
                        self.crash_text = self.crash_font.render(Restart,True, (255, 0, 0))
                        self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2+50)))

                else:
                    self.crash_text = self.crash_font.render(To_little_fuel,True, (255, 0, 0))
                    self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2-25)))
                    self.crash_text = self.crash_font.render(you_got_x_point,True, (255, 0, 0))
                    self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2+25)))
                    self.crash_text = self.crash_font.render(Restart,True, (255, 0, 0))
                    self.screen.blit(self.crash_text,((SCREEN_SIZE[0]/2-100), (SCREEN_SIZE[1]/2+50)))

            pygame.display.flip()



            self.clock.tick(self.fps)

    def quit(self):
        logging.info('Quitting... good bye!')
        pygame.quit()
        sys.exit()


class Player():
    def __init__(self, controller):
        self.controller = controller
        self.screen = controller.screen
        self.x = SCREEN_SIZE[0] / 2
        self.y = SCREEN_SIZE[1] / 2
        self.engine = False
        self.left_thruster = False
        self.right_thruster = False
        self.gravity = 0.01
        self.speed = 0
        self.direction = 0
        self.engine_power = 0.03
        self.rotation = -math.pi / 2
        self.ang_ve = 0

    def draw(self):
        surface = pygame.Surface((21, 21), flags=pygame.SRCALPHA)


        pygame.draw.rect(self.screen, (0,255,0), (0, 0, self.controller.fuel, 10))



        pygame.draw.polygon(surface, COLOR['ship_fill'], ((10, 0), (15, 15), (5, 15)), 0)
        pygame.draw.polygon(surface, COLOR['ship'], ((10, 0), (15, 15), (5, 15)), 1)

        if self.engine:
            pygame.draw.polygon(surface, COLOR['thruster'], ((13, 16), (10, 19), (7, 16)), 0)

        if self.left_thruster:
            pygame.draw.polygon(surface, COLOR['thruster'], ((6, 12), (5, 14), (2, 13), (6, 12), 0))

        if self.right_thruster:
            pygame.draw.polygon(surface, COLOR['thruster'], ((14, 12), (15, 14), (18, 13), (14, 12), 0))

        bild = pygame.transform.rotate(surface, -self.rotation * 180 / math.pi - 90)

        self.screen.blit(bild, (self.x - bild.get_width() / 2, self.y - bild.get_height() / 2))





    def tick(self):
        self.speed *= 0.99

        # Apply gravity
        x = self.speed * math.cos(self.direction)
        y = self.speed * math.sin(self.direction) + self.gravity

        self.speed = math.sqrt(x**2 + y**2)
        self.direction = math.atan2(y, x)

        # Update speed and direction of travel if engine is powered on
        if self.engine:
            x = x + self.engine_power * math.cos(self.rotation)
            y = y + self.engine_power * math.sin(self.rotation)

            self.speed = math.sqrt(x**2 + y**2)
            self.direction = math.atan2(y, x)
            self.controller.fuel -=1

        # Update position
        self.x = self.x + self.speed * math.cos(self.direction)
        self.y = self.y + self.speed * math.sin(self.direction)



        if self.left_thruster:

            self.ang_ve += 0.03
            self.controller.fuel-=0.4


        if self.right_thruster:

            self.ang_ve -= 0.03
            self.controller.fuel-=0.4

        self.ang_ve *=0.99#Slowing down

        self.rotation = self.rotation - self.ang_ve*math.pi/180




        logging.debug('Speed: {}'.format(self.speed))
        logging.debug('Degree: {}'.format(self.rotation))


    def engine_on(self):
        self.engine = True

    def engine_off(self):
        self.engine = False

    def left_thruster_on(self):
        self.left_thruster = True

    def left_thruster_off(self):
        self.left_thruster = False

    def right_thruster_on(self):
        self.right_thruster = True

    def right_thruster_off(self):
        self.right_thruster = False


class World():
    def __init__(self, controller):
        self.controller = controller
        self.screen = controller.screen

    def draw(self):

        self.font = pygame.font.SysFont(None, 32)

        self.hud = pygame.Surface((SCREEN_SIZE[0], 60), flags=pygame.SRCALPHA)

        self.hud.blit(self.font.render("50",True, (255, 255, 255)),(50,5))#points on screen
        self.hud.blit(self.font.render("20",True, (255, 255, 255)),(200,5))
        self.hud.blit(self.font.render("40",True, (255, 255, 255)),(130,5))
        self.hud.blit(self.font.render("10",True, (255, 255, 255)),(500,5))
        self.hud.blit(self.font.render("20",True, (255, 255, 255)),(280,5))
        self.hud.blit(self.font.render("40",True, (255, 255, 255)),(640,5))
        self.hud.blit(self.font.render("50",True, (255, 255, 255)),(740,5))


        self.screen.fill(COLOR['bg'])
        pygame.draw.rect(self.screen, (255,255,255), (0, 550, 800, 3))

        self.screen.blit(self.hud, (0, 515))


    def tick(self):
        pass


if __name__ == "__main__":
    logger.info('Starting...')
    c = Controller()
    c.run()
