from sprite_sheet import SpriteSheet


class player:
    """
    Controls all aspects of player including Sprite, Health, Matches, Treasures, Location, Speed
    """
    def __init__(self, mapp):
        self.x = 350                            #Initial starting x coordinate
        self.y = 200                            #Initial starting y coordinate
        self.ani_speed_init = 6                 #Initial frames in walking animation
        self.ani_speed = self.ani_speed_init    #Resets the walking speed
        self.get_frames()                       #Retrieves walking frames from sprite sheet
        self.ani_up = self.walking_frames_up    #Loads frames into list
        self.ani_left = self.walking_frames_left
        self.ani_down = self.walking_frames_down
        self.ani_right = self.walking_frames_right
        self.ani_pos=0                          #Sets initial walking speed to 0, which is no movement
        self.ani_max=len(self.ani_up)-1         #Looped walking frames
        self.img = self.ani_up[0]               #sets current sprite image to facing north, no movement
        self.update(0,'n')                      #updates image with 0 speed and facing north
        self.light = False                      #Match currently not turned on
        self.matches = 6                        #Sets initial match count
        self.hp = 100                           #Sets initial health
        self.hp_max = 100                       #Sets max health
        self.alive = True                       #sets user to alive
        self.mapp = mapp                        #Initializes ASCII map
        self.row = (len(mapp) - 2)              #Sets row location
        self.col = 1                            #Sets column location
        self.pos = (self.row, self.col)         #Gets current Position
        self.rect = self.img.get_rect()         #Gets image size
        self.frame_speed = 1                    #Sets pace that the algorithm moves through animations
        self.treas_num = 0                      #initial treasure count



    def get_hp(self):
        """

        :return: current hp
        """
        return self.hp()


    def update(self, pos, dir):
        """
        Moves the sprite through the correct animation based on which direction is given
        :param pos: either 0 or 1. 0 is standing still, 1 is moving
        :param dir: either 'n' 'e' 'w' or 's' for north east west or south facing
        :return: Sprite turned the correct direction and movement if requested
        """
        screen_x = 0                                    #Movement of screen x, y
        screen_y = 0
        if dir == 'n' and pos != 0:                     #if parameter dir = north, and movement is needed
            self.ani_speed-=1                           #begin iterating through list of sprites
            if self.ani_speed == 0:                     #if ani speed is 0, move to next image in list and reset ani speed
                self.img = self.ani_up[self.ani_pos]    #this prevents the images from iterating too quickly, now they change once every 10 frames, or 6 times a second
                self.ani_speed = self.ani_speed_init
                if self.ani_pos >= self.ani_max:        #if ani pos is larger than the max number of frames, skip the standing still frame and loop back through again
                    self.ani_pos = 1
                else:
                    self.ani_pos += 1                   #otherwise, add one to the pos
            screen_y -= self.frame_speed                #move the screen down at the rate of movement
        elif dir == 'n' and pos == 0:                   #if movement not needed, change sprite to standing still, facing requested direction
            self.img = self.ani_up[0]

        if dir == 'w' and pos != 0:
            self.ani_speed-=1
            if self.ani_speed == 0:
                self.img = self.ani_left[self.ani_pos]
                self.ani_speed = self.ani_speed_init
                if self.ani_pos >= self.ani_max:
                    self.ani_pos = 1
                else:
                    self.ani_pos += 1
            screen_x -= self.frame_speed
        elif dir == 'w' and pos == 0:
            self.img = self.ani_left[0]

        if dir == 's' and pos != 0:
            self.ani_speed-=1
            if self.ani_speed == 0:
                self.img = self.ani_down[self.ani_pos]
                self.ani_speed = self.ani_speed_init
                if self.ani_pos >= self.ani_max:
                    self.ani_pos = 1
                else:
                    self.ani_pos += 1
            screen_y += self.frame_speed
        elif dir == 's' and pos == 0:
            self.img = self.ani_down[0]

        if dir == 'e' and pos != 0:
            self.ani_speed-=1
            if self.ani_speed == 0:
                self.img = self.ani_right[self.ani_pos]
                self.ani_speed = self.ani_speed_init
                if self.ani_pos >= self.ani_max:
                    self.ani_pos = 1
                else:
                    self.ani_pos += 1
            screen_x += self.frame_speed
        elif dir == 'e' and pos == 0:
            self.img = self.ani_right[0]
        return self.img, self.x, self.y, screen_x, screen_y

    def check_collision(self):
        """
        Currently not used, was created for testing
        :return: Nothing
        """
        self.get_surroundings()

    def get_surroundings(self):
        """
        This method checks the area and sets the surroundings to variables.
        The 'if' statement will check for Treasure in these locations. If found, it calls the self.get_treasure method
        :return: The variables self.n, self.e, self.w, self.s are filled with the corresponding items.
        Not currently implemented
        """
        self.n = self.mapp[self.row - 1][self.col]  # Returns the value 'north' of the Explorer
        self.e = self.mapp[self.row][self.col + 1]  # Returns the value 'east' of the Explorer
        self.w = self.mapp[self.row][self.col - 1]  # Returns the value 'west' of the Explorer
        self.s = self.mapp[self.row + 1][self.col]  # Returns the value 'south' of the Explorer

    def lightswitch(self,start_ticks):
        """
        turns the light on or off
        :param start_ticks: timer
        :return: state change for light
        """
        if self.matches > 0:
            if self.light == True:
                self.light = False
            elif self.light == False:
                self.light = True
                self.matches -= 1

    def get_frames(self):
        self.get_up_frames()
        self.get_left_frames()
        self.get_down_frames()
        self.get_right_frames()

    def get_up_frames(self):
        """
        loads a sprite sheet and pulls corresponding sprites using x and y coordinate location
        :return:
        list containing wlaking frames facing up
        """
        self.walking_frames_up = []                         #Initial empty list
        sprite_sheet = SpriteSheet("player.png")            #loads sprite sheet using SpriteSheet Class
        # Load all the forward facing images into a list
        image = sprite_sheet.get_image(-5, 520, 64, 55)     #(x coordinate, y coordinate, height, width)
        self.walking_frames_up.append(image)                #add to list
        image = sprite_sheet.get_image(60, 520, 64, 55)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(124, 520, 64, 55)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(188, 520, 64, 55)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(252, 520, 64, 55)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(316, 520, 64, 55)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(380, 520, 64, 55)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(444, 520, 64, 55)
        self.walking_frames_up.append(image)
        image = sprite_sheet.get_image(508, 520, 64, 55)
        self.walking_frames_up.append(image)

    def get_left_frames(self):
        """
                loads a sprite sheet and pulls corresponding sprites using x and y coordinate location
                :return:
                list containing walking frames facing left
                """
        self.walking_frames_left = []
        sprite_sheet = SpriteSheet("player.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(-5, 588, 64, 55)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(60, 588, 64, 55)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(124, 588, 64, 55)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(188, 588, 64, 55)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(252, 588, 64, 55)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(316, 588, 64, 55)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(380, 588, 64, 55)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(444, 588, 64, 55)
        self.walking_frames_left.append(image)
        image = sprite_sheet.get_image(508, 588, 64, 55)
        self.walking_frames_left.append(image)

    def get_down_frames(self):
        """
                loads a sprite sheet and pulls corresponding sprites using x and y coordinate location
                :return:
                list containing walking frames facing down
                """
        self.walking_frames_down = []
        sprite_sheet = SpriteSheet("player.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(-5, 653, 64, 55)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(60, 653, 64, 55)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(124, 653, 64, 55)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(188, 653, 64, 55)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(252, 653, 64, 55)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(316, 653, 64, 55)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(380, 653, 64, 55)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(444, 653, 64, 55)
        self.walking_frames_down.append(image)
        image = sprite_sheet.get_image(508, 653, 64, 55)
        self.walking_frames_down.append(image)

    def get_right_frames(self):
        """
                loads a sprite sheet and pulls corresponding sprites using x and y coordinate location
                :return:
                list containing walking frames facing right
                """
        self.walking_frames_right = []
        sprite_sheet = SpriteSheet("player.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(-5, 718, 64, 55)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(60, 718, 64, 55)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(124, 718, 64, 55)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(188, 718, 64, 55)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(252, 718, 64, 55)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(316, 718, 64, 55)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(380, 718, 64, 55)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(444, 718, 64, 55)
        self.walking_frames_right.append(image)
        image = sprite_sheet.get_image(508, 718, 64, 55)
        self.walking_frames_right.append(image)
