"""
Wintery flappy bird game

Author: Lotta Rantala
"""

import random as r
import pygame
from pygame.constants import KEYDOWN
from bird import Bird

#setup for the different game variables
game = {
    "width" : 800,
    "height" : 500,
    "run" : True,
    "fps" : 120,
    "gravity" : 1.3,
    "points" : 0,
    "falling" : False,
    "obstacles" : [],
}

#for storing the images
images = {
    "bird": None,
    "background" : None,
    "ice" : None
}

#setup for the pygame stuff
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([game["width"], game["height"]])
pygame.display.set_caption("Ice Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("sans", 25)

#how often to spawn an obstacle
SPAWN_OBSTACLE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_OBSTACLE, 2000)

#the bird
flappy =  Bird()

def load_images():
    #loads all the images used in the game
    bird_image = pygame.image.load("images/bird_pic.png")
    images["bird"] = pygame.transform.scale(bird_image, (40, 40))
    images["background"] = pygame.image.load("images/background_pic.png")
    ice_image = pygame.image.load("images/ice_pic.png")
    images["ice"] =pygame.transform.scale(ice_image, (50, 400))

def draw_screen():
    #draws the images on the screen
    screen.blit(images["background"], (0, 0))
    screen.blit(images["bird"], (flappy.x, flappy.y))
    for obs in game["obstacles"]:
        screen.blit(images["ice"], obs)
    points = font.render("Points: "+(str(int(game["points"]))),1, (0, 0, 0))
    screen.blit(points, (10, 460))

def spawn_obstacle(x=850):
    #chooses obstacle's top start point from this list, leaves a space and rest is bottom obstacle
    start_points = [100, 150, 200, 250, 300, 350]
    space = 150
    height = r.choice(start_points)
    top_obs = images["ice"].get_rect(midbottom = (x, height))
    bottom_obs = images["ice"].get_rect(midtop = (x, height + space))
    return top_obs, bottom_obs

def move_obstacle(list):
    for obs in list: 
        obs.centerx -= 2
    return list

def died():
    print("\n\nYou died :(\n\nYou got {} points\n\n".format(int(game["points"])))
    flappy.x = 100
    flappy.y = 200
    game["points"] = 0
    game["obstacles"] = []
    game["falling"] = False
    game["run"] = False

def check_collision():
    bird_rect = images["bird"].get_rect(topleft=(flappy.x, flappy.y))
    for obs in game["obstacles"]:
        if bird_rect.colliderect(obs):
            died()
        #birds x-cord is even but obstacles is uneven
        if bird_rect.left - obs.right == 1:
            #one obstacle is divided in upper and lower part, so 0,5p + 0,5p = 1p
            game["points"] += 0.5

def main():
    #loads the images first, then starts the game
    load_images()
    #let's add one obstacle in the starting screen
    game["obstacles"].extend(spawn_obstacle(x=700))
    draw_screen()
    while game["run"]:
        clock.tick(game["fps"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game["run"] = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game["falling"] = True
                    flappy.jump()
            elif event.type == SPAWN_OBSTACLE and game["falling"]:
                game["obstacles"].extend(spawn_obstacle())
        if game["falling"]:
            flappy.y += game["gravity"]
            move_obstacle(game["obstacles"])
        if flappy.y > game["height"] - flappy.height/2:
            flappy.y = game["height"] - flappy.height
            died()
        check_collision()
        draw_screen()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()