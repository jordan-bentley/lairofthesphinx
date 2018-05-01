import pygame, sys #Allows use of Pypgame library and sys allows for the game window to close when necessary
from pygame import *    #Allows use of sprite library
import wall_graphics    #Class that reads in the sprite_sheet containing the wall graphics
import player           #Class controlling the player sprite and attributes
import ui               #Class that controls the User Interface, health and match number
import sub_map          #Class that reads in an ASCII text file and converts it to a nested list
import sprites          #Class that assigns sprite attributes to graphics when they are loaded in
import questions        #Class that controls the questions and answers, retrieved from SQL database


h=400                   #sets height of screen
w=800                   #sets width of screen

screen = pygame.display.set_mode((w,h))     #initializes pygame window with predetermined width and height
fade_screen = Surface((w,h))                #initializes death screen
fade_screen.fill((255,255,255))             #gives death screen the correct color scheme

clock = pygame.time.Clock()                 #initializes the clock to allow the game to progress at a set pace
tiles = wall_graphics.tile("maze/maze2.txt") #initializes the tiles object to read and control the wall graphics
player1 = player.player(tiles.mapp)         #initializes the player object to read and control player sprite/attributes
qs = questions.Question()                   #initializes the qs object to read and control questions/answers from db
pos = 0                                     #Sets initial speed of player in main()

global question                             #creates global variable question to control when a question will be displayed
question = False                            #sets questions to False meaning it will not display


if True:                                    #This is meant to change the starting location of player if map changes
    init_x = 225                            #needs to be updated, currently only setup for maze2.txt
    init_y = -436

layout = tiles.get_sprites()                #creates the layout of the map using the get_sprites method from wall_graphics
tiles.x = init_x                            #sets beginning x location of the first wall sprite
tiles.y = init_y                            #sets beginning y location of the first wall sprite
filter = pygame.surface.Surface((800, 400)) #creates a filter that can overlay over the game if needed - vision()
ui = ui.UI()                                #initializes the ui object to read and control User Interface attributes
fade_screen.set_alpha(ui.alph)              #Sets the brightness of the death screen
submap = sub_map.SubMap(tiles.mapp)         #reads in ascii textfile and generates a nested list containing the map


def vision():
    """
    allows player to 'see' a set area around the player sprite
    :return: correct vision size based on light state in player class
    """
    light=pygame.image.load('circle.png')                   #loads a circle of set size for lighting
    filter.fill(pygame.color.Color(225, 225, 225, 0))       #overlays a black image on entire screen with circle.png being transparent
    if player1.light == True:                               #if the light is on
        light = pygame.transform.scale(light, (1200,1200))      #make the transparent circle large to show more space
        filter.blit(light, (-200,-400))                         #adds the circle image to the filter at set coordinates
    elif player1.light == False:                            #if the light is off
        light=pygame.transform.scale(light, (600,600))          #make the transparent circle smaller to show less space
        filter.blit(light, (95,-70))                            #adds the circle image to the filter at set coordinates
    screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)    #Adds the filter to the main screen with correct color scheme
                                                                        #at set coordinates of (0,0)

def set_sprites():
    """
    only ran from main, once before the gameloop begins
    creates sprite groups to allow them to be manipulated easier
    sets sprite initial locations
    :return: walls, player, floors, doors, treasures
            sprite groups containing the coordinates, images, and sizes of each sprite in regards
            to their location on the screen
    """
    doors = pygame.sprite.Group()                   #creates sprite group for doors
    floors = pygame.sprite.Group()                  #creates sprite group for floors
    walls = pygame.sprite.Group()                   #creates sprite group for walls
    treasures = pygame.sprite.Group()               #creates sprite group for treasures
    exit = pygame.sprite.Group()
    player = sprites.Player(player1.img)            #creates sprite group for player
    count = 0                                       #keeps count to iterate through a list
    for image in tiles.wall_sprites:
        sprite = sprites.Wall(image, tiles.sprite_coor[count])  #creates a wall sprite object using the Wall class in sprites.py
        walls.add(sprite)                                       #adds the wall sprite to the walls sprite group
        count += 1                                              #increases count by 1 to move to the next element
    for sprite in walls:
        sprite.rect.x += init_x                     #moves the starting location of each sprite relative to player location
        sprite.rect.y += init_y
    count = 0                                       #resets count for next loop
    for image in tiles.floor_sprites:
        sprite = sprites.Floor(image, tiles.floor_coor[count])
        floors.add(sprite)
        count += 1
    for sprite in floors:
        sprite.rect.x += init_x
        sprite.rect.y += init_y
    count = 0
    for image in tiles.door_sprites:
        sprite = sprites.Door(image, tiles.door_coor[count])
        doors.add(sprite)
        count += 1
    for sprite in doors:
        sprite.rect.x += init_x
        sprite.rect.y += init_y
    count = 0
    for image in tiles.tres_sprites:
        sprite = sprites.Floor(image, tiles.tres_coor[count])
        treasures.add(sprite)
        count += 1
    for sprite in treasures:
        sprite.rect.x += init_x
        sprite.rect.y += init_y
    for image in tiles.exit_sprites:
        sprite = sprites.Floor(image, tiles.exit_coor[0])
        exit.add(sprite)
    for sprite in exit:
        sprite.rect.x += init_x
        sprite.rect.y += init_y
    return walls, player, floors, doors, treasures, exit #returns sprite groups

def update_walls(walls, x, y):
    """
    moves the wall sprites relative to the movement of the player
    :param walls: wall group created in set_sprites()
    :param x: amount to shift the sprites on the x axis
    :param y: amount to shift the sprites on the y axis
    :return: sprites will have moved relative to the player
    """
    for sprite in walls:
        sprite.rect.x -= x
        sprite.rect.y -= y

def update_exit(exit, x, y):
    """
    moves the exit sprites relative to the movement of the player
    :param exit: exit group created in set_sprites()
    :param x: amount to shift the sprites on the x axis
    :param y: amount to shift the sprites on the y axis
    :return: sprites will have moved relative to the player
    """
    for sprite in exit:
        sprite.rect.x -= x
        sprite.rect.y -= y

def update_treasures(treasures, x, y):
    """
    moves the treasure sprites relative to the movement of the player
    :param treasures: wall group created in set_sprites()
    :param x: amount to shift the sprites on the x axis
    :param y: amount to shift the sprites on the y axis
    :return: sprites will have moved relative to the player
    """
    for sprite in treasures:
        sprite.rect.x -= x
        sprite.rect.y -= y

def update_floors(floors, x, y):
    """
    moves the treasure sprites relative to the movement of the player
    :param floors: floor group created in set_sprites()
    :param x: amount to shift the sprites on the x axis
    :param y: amount to shift the sprites on the y axis
    :return: sprites will have moved relative to the player
    """
    for sprite in floors:
        sprite.rect.x -= x
        sprite.rect.y -= y

def update_doors(doors, x, y):
    """
    moves the door sprites relative to the movement of the player
    :param doors: door group created in set_sprites()
    :param x: amount to shift the sprites on the x axis
    :param y: amount to shift the sprites on the y axis
    :return: sprites will have moved relative to the player
    """
    for sprite in doors:
        sprite.rect.x -= x
        sprite.rect.y -= y


def end_game():
    while True:
        clock.tick(60)
        for event in pygame.event.get():                        #User input handling
            if event.type == pygame.QUIT:                       #if the user clicks 'X' on window
                sys.exit()                                          #game exit
                                                                #set player speed to 1

        ui.alph += 1  # increments fade to white by manner of one per clock tick
        fade_screen.set_alpha(ui.alph)  # screen fades at specified rate
        screen.blit(fade_screen, (0, 0))  # shows fade on screen
        ui.tres_count(player1.treas_num)
        if ui.alph >= 100:                     # handling for when to show death message
            screen.blit(ui.survive_indicator, (int(w / 8), int(h / 4)))
        pygame.display.update()

def check_col(walls, floors, doors, treasures, exit, player, dir, touched):
    """
    checks for collision between the player and various other sprites
    :param walls: wall sprite group
    :param floors: floor sprite group
    :param doors: door sprite group
    :param treasures: treasure sprite group
    :param player: player sprite group
    :param exit: exit sprite group
    :param dir: direction the player is traveling, str of 'n', 's', 'e' or 'w'
    :param touched: Bool value of whether the player is being asked a question
    :return: touched = True if its False when passed in and the player has touched a door, otherwise
            it remains False
    """
    global question                                     #allows use of global variable question
    col = pygame.sprite.spritecollideany(player, walls) #checks for collision between the player and any wall
    door_col = pygame.sprite.spritecollideany(player, doors) #checks for collision between the player and any door
    treas_col = pygame.sprite.spritecollideany(player, treasures)
    exit_col = pygame.sprite.spritecollideany(player, exit)

    if exit_col != None:
        end_game()

    if door_col != None:                               #if there is collision between the player and a door
        if question == False and touched == False:      #if a question is not being asked and the door isn't already being touched
            update_walls(walls, 0, 1)                     #prevent the map from continuing to move
            update_floors(floors, 0, 1)                    #move prevention
            update_doors(doors, 0, 1)                       #move prevenetion
            update_exit(exit, 0, 1)
            question = True                             #make question = True to begin a different state in the gameloop

        elif question == False and touched == True:                         #if no question but the door is being touched meaning the question was answered correctly
            used_doors = pygame.sprite.spritecollide(player, doors, True)   #remove door from the doors group
            update_walls(walls, 0, 1)                                       #move prevention
            update_floors(floors, 0, 1)                                     #move prevention
            update_doors(doors, 0, 1)                                       #move prevention
            update_exit(exit, 0, 1)
            floors.add(used_doors)                                          #make the door sprite act like a wall sprite for collision purposes

        elif question == True and touched == True:          #if question and door is being touched, prevent movement
            update_walls(walls, 0, 1)                           #this ensures that the player wont walk around with a question on screen
            update_floors(floors, 0, 1)
            update_doors(doors, 0, 1)
            update_exit(exit, 0, 1)

    elif door_col == None:                                   #resets door being touched for use again when another door is touched
        touched = False

    if treas_col != None:
        #screen.blit(ui.treasure_get, (int(w/3), (int(h/2))))
        player1.treas_num += 1                                                  #Increase treasure number
        used_treasure = pygame.sprite.spritecollide(player, treasures, True)    #removes treasure from active treasure list
        floors.add(used_treasure)                                               #treasure room becomes floor for collision purposes

    if col != None and dir == 'n':                      #if collision with a wall and the direction the player was moving is north
        update_walls(walls, 0, 1)                       #prevent movement | moves the screen backwards 1 pixel and sets
        update_floors(floors, 0, 1)                         #player speed = 0
        update_doors(doors, 0, 1)
        update_exit(exit, 0, 1)
        update_treasures(treasures, 0, 1)
    elif col != None and dir == 's':                    #if collision with a wall and the direction the player wsa moving is south
        update_walls(walls, 0, -1)                      #prevent movement
        update_floors(floors, 0, -1)
        update_exit(exit, 0, -1)
        update_doors(doors, 0, -1)
        update_treasures(treasures, 0, -1)
    elif col != None and dir == 'e':                    #if collision with wall and direction = east
        update_walls(walls, -1, 0)                      #prevent movement
        update_floors(floors, -1, 0)
        update_exit(exit, -1, 0)
        update_doors(doors, -1, 0)
        update_treasures(treasures, -1, 0)
    elif col != None and dir == 'w':                    #if collision with wall and direction = west
        update_walls(walls, 1, 0)                       #prevent movement
        update_floors(floors, 1, 0)
        update_doors(doors, 1, 0)
        update_exit(exit, 1, 0)
        update_treasures(treasures, 1, 0)

    return touched                                      #returns to value of touched - Boolean

def update_ui():
    """
    keeps Health and Matches on top of other graphics
    :return: Updated health and match numbers
    """
    ui.update_match(player1.matches)                                    #calls update match method in UI using player match count
    ui.update_treasure(player1.treas_num)
    player1.hp -= .01                                                  #decreases health at steady rate
    ui.update_health((254, 0, 0), 10, 350, player1.hp, player1.hp_max)  #Updates health bar (size, locationx, locationy, current hp, max hp
    #ui.arrows()           #testing
    death()                                                             #ends game if dead

def death():
    """
    checks player health and makes a death message appear
    :return: if player is dead, the screen will turn white and message will display
            player should be able to play again, but still working on implementing
            TODO: Play Again
    """
    if player1.hp <= 0:                                             #Checks health, if less than or equal to 0
        player1.alive = False                                        #sets player alive to false
        ui.alph += 1                                                 #increments fade to white by manner of one per clock tick
        fade_screen.set_alpha(ui.alph)                               #screen fades at specified rate
        screen.blit(fade_screen, (0,0))                              #shows fade on screen
        if ui.alph >= 100 and ui.alph <= 249:                        #handling for when to show death message
            screen.blit(ui.death_indicator, (int(w/3),int(h/4)))
        elif ui.alph >= 250:
            screen.blit(ui.death_indicator, (int(w/3),int(h/4)))
            screen.blit(ui.try_again, (int(w/8), int((h/4)+50)))

def gameloop(walls, player, floors, doors, treasures, exit):
    """
    main logic for game
    :param walls: wall sprite group
    :param player: player sprite group
    :param floors: floor sprite group
    :param doors: door sprite group
    :param treasures: treasure sprite group
    :return: allows game to run
    """
    global question                         #allows use of global question variable
    pos = 0                                 #sets initial speed of player
    dir = 'n'                               #sets initial direction of player
    #rp_check = False   #testing
    touched = False                         #resets touched when the game starts
    while True:                         #MAIN GAME LOOP BEGINS
        screen.fill((0, 0, 0))          #Creates black canvas for a background
        clock.tick(60)                  #Clock will 'tick' 60 times per second which updates the while loop 60 times per sec


        for event in pygame.event.get():                        #User input handling
            if event.type == pygame.QUIT:                       #if the user clicks 'X' on window
                sys.exit()                                          #game exit
            elif event.type == KEYDOWN and event.key == K_UP:   #if a key is pressed down and that key is the up arrow
                pos = 1                                             #set player speed to 1
                dir = 'n'                                           #set player direction to north
            elif event.type == KEYUP and event.key == K_UP:     #if a key is released and that key is the up arrow
                pos = 0                                             #set player speed to 0
                dir = 'n'                                           #set player direction to north
            elif event.type == KEYDOWN and event.key == K_LEFT:
                pos = 1
                dir = 'w'
            elif event.type == KEYUP and event.key == K_LEFT:
                pos = 0
                dir = 'w'
            elif event.type == KEYDOWN and event.key == K_DOWN:
                pos = 1
                dir = 's'
            elif event.type == KEYUP and event.key == K_DOWN:
                pos = 0
                dir = 's'
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                pos = 1
                dir = 'e'
            elif event.type == KEYUP and event.key == K_RIGHT:
                pos = 0
                dir = 'e'
            elif event.type == KEYUP and event.key == K_m:      #if key released is 'm', use a match start a timer
                start_ticks = pygame.time.get_ticks()
                player1.lightswitch(start_ticks)
            elif event.type == KEYDOWN and event.key == K_p:    #testing purposes
                for sprite in floors:
                    print touched
                    print question
                print '\n'
            elif event.type == KEYUP and player1.alive == False and event.key == K_y: #death handling
                main()

        # bg(layout, world)
        touched = check_col(walls, floors, doors, treasures, exit, player, dir, touched)          #checks collision using check_col()
        player_img, player_x, player_y, screen_x, screen_y = player1.update(pos, dir)       #updates the player sprite, returns current image, players location, the change in the screen respectively
        update_walls(walls, screen_x, screen_y)                         #updates the walls using the screen variables recieved from player1.update
        update_floors(floors, screen_x, screen_y)                       #updates the floors with screen variables
        update_doors(doors, screen_x, screen_y)                         #updates the doors with screen variables
        update_exit(exit, screen_x, screen_y)
        update_treasures(treasures, screen_x, screen_y)                 #updates the treasures with screen variables
        pygame.sprite.Group.draw(floors, screen)                        #Draws the floor sprite group
        pygame.sprite.Group.draw(walls, screen)                         #Draws the walls sprite group
        pygame.sprite.Group.draw(doors, screen)                         #Draws the doors sprite group
        pygame.sprite.Group.draw(treasures, screen)                     #Draws the treasures sprite group
        pygame.sprite.Group.draw(exit, screen)
        screen.blit(player_img, (player_x, player_y))                   #draws the player with current image and location

        while question == True:                 #QUESTION GAMELOOP
            clock.tick(60)                      #keep the clock ticking
            qs.get_question()                   #calls question class to retrieve data from external database
            ongoing = qs.draw_question()       #shows the question and waits for input
            if ongoing == False:               #if the answer was correct
                qs.reset()                      #reset class attributes for next question
                question = False                #question no longer being asked, breaks question game loop, returns to main game loop
                touched = True                  #door is still being touched
            update_ui()                 #Draws ui above everything else
            pygame.display.update()     #Makes the above changes to the screen that is shown to the player
        #wall_sprites(walls)    #testing
        vision()                        #Draws the vision area above player
        update_ui()                     #Draws ui above everything else
        pygame.display.update()         #Makes the changes to the screen that is shown to the player

def main():
    """
    main function for game
    :return: game plays
    """
    walls, player, floors, doors, treasures, exit = set_sprites() # retrieves sprite groups using set_sprites function
    player1.alive = True                                    # Returns player to alive state to begin game
    screen.fill((0,0,0))                                    # Remakes black background

    gameloop(walls, player, floors, doors, treasures, exit)       #Runs main game loop



main()  #main call