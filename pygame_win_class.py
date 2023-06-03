import pygame
import threading
import numpy as np

class pygameWin():
## paramaters
    def __init__(self,points,zoom_factor,faces, is_axis_on, axis_faces):
        ###setting up the variables i will use
        ###setting up the initialiser of pygame
        pygame.init()
        pygame.mixer.init()
        print("running")
        self.points = points ##linked list
        self.faces = faces
        self.zoom_factor = zoom_factor
        self.changes = False
        self.is_axis_on = is_axis_on
        self.axis_faces = axis_faces
        self.x_axis, self.y_axis, self.z_axis = [(-150,0,0),(150,0,0)], [(0,-150,0),(0,150,0)],[(0,0,-150),(0,0,150)]

    
    def draw_text(self,surf, text, size, x_refPoint, y_refPoint):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.white)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x_refPoint, y_refPoint)
        surf.blit(text_surface, text_rect)
            
    def draw_line(self,x_refPoint,y_refPoint, xT, yT):
        pygame.draw.line(self.window, self.white, (x_refPoint,y_refPoint), (xT,yT), width=1)

    def draw_x(self,x_refPoint,y_refPoint):  ##scale from a point
        pygame.draw.line(self.window, self.white, (x_refPoint-1,y_refPoint-1), (x_refPoint+1,y_refPoint+1), width=1)
        pygame.draw.line(self.window, self.white, (x_refPoint+1,y_refPoint-1), (x_refPoint-1,y_refPoint+1), width=1)
        
    def find(self,x_refPoint,y_refPoint,xt,yt,zt):                                                                                                                                                          ##to be used locally for finding points near the mouse - is just a linear search bevcause the data is unordered checks a 5 pixel range
        for i in range(len(self.points)):                                                                                                                                                                           ##need to convert mouse click or points ##also needs to check which graph it is in ##needs to check z_refPoint coods as well
            if self.points[i][0] >= (x_refPoint-xt)/self.zoom_factor - 5 and self.points[i][0] <= (x_refPoint-xt)/self.zoom_factor + 5:                                                                     ##easy just make another if statement next to the y_refPoint section
                if y_refPoint <= 300 and self.points[i][1] >= (yt - y_refPoint)/self.zoom_factor - 5/self.zoom_factor and self.points[i][1] <= (yt-y_refPoint)/self.zoom_factor + 5/self.zoom_factor:                       ##check if the xurser is in the z_refPoint graph or y_refPoint graph and change the inputs
                    print("found")                                                                                                                                                                          ###would prefer to check the visual points against visual points and find an actual point relative to them
                    return i
                elif y_refPoint > 320 and self.points[i][2] >= (zt-y_refPoint)/self.zoom_factor - 5/self.zoom_factor and self.points[i][2] <= (zt-y_refPoint)/self.zoom_factor + 3/self.zoom_factor:
                    print("found")
                    return i
        else:
            return None
        
    def TD_plot(self,x_refPoint,y_refPoint,z_refPoint):   ##could also do 3d by applying the x_refPoint rotational matrix transformation
        ThreeD_main_pointx = x_refPoint*np.cos(self.rotation_around_x) + y_refPoint*np.sin(self.rotation_around_x)*np.sin(self.rotation_around_y) + z_refPoint*np.sin(self.rotation_around_x)*np.cos(self.rotation_around_y)
        ThreeD_main_pointy = y_refPoint*np.cos(self.rotation_around_y) - z_refPoint*np.sin(self.rotation_around_y)
        ThreeD_main_pointz = -x_refPoint*np.sin(self.rotation_around_x) + y_refPoint*np.cos(self.rotation_around_x)*np.sin(self.rotation_around_y) + z_refPoint*np.cos(self.rotation_around_y)*np.cos(self.rotation_around_x)
        return ThreeD_main_pointx,ThreeD_main_pointy,ThreeD_main_pointz ##should just unpack the varibales
    
    ###does not work correctly - maybe the indexing difference
    def prims(self):   ##best O(1) average O(n^2) worst error o(n^3) ##assume all faces are apparent and add any new vertices
        route = []
        for i in range(len(self.points)): ##consider the start i the next node x_refPoint and the final node found after the in runction
            for j in self.points[i][3]:
                for k in self.points[j][3]:
                    if j in self.points[k][3]:
                        route.append([i+1,j+1,k+1]) ##adds more than it needs to ##does this work? the index points are -1 for interpreting in mys ocde

        return route
        
    
                
    ##route is constantly appended to in reverse
    #is made face true
    ##if it has a line going to a point and from a point indicating 2 faces then i can delete the path im considering
    def runalgo(self):
        self.fps = 100
        clock = pygame.time.Clock()
        self.window_width, self.window_height =  800,600
        self.parse = (self.window_width, self.window_height)
        centre_x, centre_y = 600,300
        self.set = []

        ####test
        press_x = False
        ####

        ## colours
        self.red = (255,0,0)
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.font_name = pygame.font.match_font('arial')


        self.window = pygame.display.set_mode(self.parse)
        pygame.display.set_caption("")
        point = None
        game_over = True
        running = True
        ##defining the x_refPoint y_refPoint and z_refPoint referance points
        x_refPoint = 100
        y_refPoint = 300
        z_refPoint = 520
        self.rotation_around_y = 0
        self.rotation_around_x = 0
##        dd = 1
        press = 0
        is_ctrl = 0
##        main running loop
        while running:
##            set up parameters
            clock.tick(300)##fps
            self.window.fill(self.black)
##            basic event calls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    ##if any changes are detected then run the prims algo
                    if self.changes == True:
                        self.faces = self.prims()#self.points)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.changes = True ##new
                    pos_x, pos_y = pygame.mouse.get_pos()               

                    if event.button == 1:
                        press = pygame.time.get_ticks()                
                        print("c")
                    if event.button == 3:
##                        print("right click")
                        move_pos = self.find(pos_x,pos_y,x_refPoint,y_refPoint,z_refPoint)
                        

                    if event.button == 4 and pos_x <= 300:##zoom in                                                           #and dxl <= 0 and dy <= 0 and dyd >= 0: ##only need to use one for the and function               
                        self.zoom_factor += 0.5
                        if self.zoom_factor == 0:  ##cannot divide by 0
                            self.zoom_factor += 0.5 
                    elif event.button == 5 and pos_x <= 300: ##zoom out
                        self.zoom_factor -= 0.5
                        if self.zoom_factor == 0: ##cannot divide by 0
                            self.zoom_factor -= 0.5
                    elif event.button == 4 and pos_x > 300 and is_ctrl == False:
                        self.rotation_around_y += 0.5 ##+ rotation clockwise around the x_refPoint axis

                    elif event.button == 4 and pos_x > 300 and is_ctrl == True:
                        self.rotation_around_x += 0.5  ##+ rotation clockwise in the y_refPoint axis

                    
                    elif event.button == 5 and pos_x > 300 and is_ctrl == False:
                        self.rotation_around_y -= 0.5 ##- rotation clockwise in the x_refPoint axis

                                        
                    elif event.button == 5 and pos_x > 300 and is_ctrl == True:
                        self.rotation_around_x -= 0.5 ## rotation clockwise in the y_refPoint axis

                            
                if event.type == pygame.KEYDOWN:
                    self.changes = True ##new
                    if event.key == pygame.K_RIGHT:
                        x_refPoint -= 10
                    if event.key == pygame.K_LEFT:
                        x_refPoint += 10
                    if event.key == pygame.K_UP:
                        y_refPoint += 10
                        z_refPoint += 10
                    if event.key == pygame.K_DOWN:
                        y_refPoint -= 10
                        z_refPoint -= 10
                    if event.key == pygame.K_SPACE:
                        self.rotation_around_y += 1
                        
                    if event.key == pygame.K_LCTRL:
                        is_ctrl = True
                    if event.key == pygame.K_f and is_ctrl == True and self.axis_faces == False:
                        self.axis_faces = True
                        print("true")
                    elif event.key == pygame.K_f and is_ctrl == True and self.axis_faces == True:
                        self.axis_faces = False
                        print("false")

                    if event.key == pygame.K_x:
                        press_x = True
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LCTRL:
                        is_ctrl = False

                        
                    if event.key == pygame.K_x:
                        press_x = False

                if pygame.mouse.get_pressed()[0]:
                    self.changes = True ##new
                    click_x, click_y = pygame.mouse.get_pos()
                    self.draw_text(self.window, f"{(click_x - x_refPoint)/self.zoom_factor},{(y_refPoint - click_y)/self.zoom_factor}", 15, click_x + 20, click_y + 20)
                                                                                                                                            ##y_refPoint- for the same logic later
                    
                if event.type == pygame.MOUSEBUTTONUP:                                                                                                          ##make an arg func or store as a list directly
                    self.changes = True ##new
                    click_x, click_y = pygame.mouse.get_pos()
                    if event.button == 1 and (pygame.time.get_ticks() - press <= 200):                                                                      ##could call this a def so if find returns None its called again
                        print(click_x,click_y)
                        point = [click_x, click_y]
                    elif event.button == 1 and (pygame.time.get_ticks() - press > 200):                                                                     ##could i just use the elif statement and say if either is None then make point at that pos
                        first_point = self.find(pos_x,pos_y,x_refPoint,y_refPoint,z_refPoint)                                                                                  ##its random that i chose 200 maybe use a lower number
                        second_point = self.find(click_x,click_y,x_refPoint,y_refPoint,z_refPoint)
                        if first_point != None and second_point != None:
                            self.points[first_point][3].append(second_point)
                            print("it works",first_point,second_point)                                                                                      ###3d linear transformations but only consider the x_refPoint coord
                        print("d")
                        
                    elif event.button == 3 and move_pos != None:
                        if pos_y <= 300 and click_y <= 300:
                            self.points[move_pos][0] = (click_x - x_refPoint)/self.zoom_factor                                                                ##need to consider which graph i am in
                            self.points[move_pos][1] = (y_refPoint - click_y)/self.zoom_factor
                            print("right click y_refPoint")
                        elif pos_y > 300 and click_y > 300:
                            self.points[move_pos][0] = (click_x- x_refPoint)/self.zoom_factor 
                            self.points[move_pos][2] = (z_refPoint - click_y)/self.zoom_factor
                            print("right click z_refPoint")
                        
                            ##pretty general because i dont need to worry about clicking outside of the graph or clicking nothing
                        ##runs the dot connect things  ##uses the find algorithm to find the first and second point and appends the second point to the connecters part of the first
                            
            ##graph one - maybe make a function        
            pygame.draw.line(self.window, self.white, (100,300), (100,100), width=1) ##root colour start pos end pos width
            pygame.draw.line(self.window,self.white, (100,300), (300,300), width=1)
            self.draw_text(self.window, f"x {(310 - x_refPoint)//self.zoom_factor}", 20, 310, 300) ##root - text - size - x_refPoint - y_refPoint
            self.draw_text(self.window, f"y {(y_refPoint - 90)//self.zoom_factor}", 20, 90, 90)

            ##graph two
            pygame.draw.line(self.window, self.white, (100,520), (100,320), width=1)
            pygame.draw.line(self.window, self.white, (100,520), (300,520), width=1)
            self.draw_text(self.window, f"x {(310 - x_refPoint)//self.zoom_factor}", 20, 310, 520) ##root - text - size - x_refPoint - y_refPoint ##apply self.zoom_factor
            self.draw_text(self.window, f"z {(z_refPoint - 90)//self.zoom_factor}", 20, 90, 310)

            ##write the key binds
            self.draw_text(self.window, "x-rotate graph",15, 100, 550)
            self.draw_text(self.window, "ctrl+f - enable/disable faces",15, 100, 570)

            ##3d graph ##could use the dd function to calculate how big the line would be
            if self.is_axis_on == True:##function for drawing the 3D graph axis
                x_axis_one = self.TD_plot(self.x_axis[0][0],self.x_axis[0][1],self.x_axis[0][2]) ##cant i just use self.axis[0]
                x_axis_two = self.TD_plot(self.x_axis[1][0],self.x_axis[1][1],self.x_axis[1][2])
                y_axis_one = self.TD_plot(self.y_axis[0][0],self.y_axis[0][1],self.y_axis[0][2])
                y_axis_two = self.TD_plot(self.y_axis[1][0],self.y_axis[1][1],self.y_axis[1][2])
                z_axis_one = self.TD_plot(self.z_axis[0][0],self.z_axis[0][1],self.z_axis[0][2])
                z_axis_two = self.TD_plot(self.z_axis[1][0],self.z_axis[1][1],self.z_axis[1][2])
                pygame.draw.line(self.window, (0,0,255), (x_axis_one[0] + centre_x,centre_y - x_axis_one[1]), (x_axis_two[0] + centre_x,centre_y - x_axis_two[1]), width=1)
                pygame.draw.line(self.window, (0,0,255), (y_axis_one[0] + centre_x,centre_y - y_axis_one[1]), (y_axis_two[0] + centre_x,centre_y - y_axis_two[1]), width=1)
                pygame.draw.line(self.window, (0,0,255), ( z_axis_one[0] + centre_x,centre_y - z_axis_one[1]), (z_axis_two[0] + centre_x,centre_y - z_axis_two[1]), width=1)               
                
            #point = on_click()
            if point is not None:
                if (point[0] >= 100 and point[0] <= 300) and (point[1] >= 100 and point[1] <= 300):
                    self.points.append([(point[0] - x_refPoint)/self.zoom_factor,(y_refPoint - point[1])/self.zoom_factor,0,[]]) ##x_refPoint y_refPoint
                elif (point[0] >= 100 and point[0] <= 300) and (point[1] >= 320 and point[1] <= 520):
                    self.points.append([(point[0] - x_refPoint)/self.zoom_factor,0,(z_refPoint - point[1])/self.zoom_factor,[]]) ##make x_refPoint z_refPoint and add a conversion metric
    ##                points.append(point)
                point = None
            for i in range(len(self.points)):
                if not i in self.set:
                    transform_x = self.points[i][0]*self.zoom_factor
                    transform_y = self.points[i][1]*self.zoom_factor
                    transform_z = self.points[i][2]*self.zoom_factor                                                                                                        ###the transformed poitns to be drawn 

                    if (transform_x + x_refPoint >= 100 and transform_x + x_refPoint <= 300) and (y_refPoint - transform_y >= 100 and y_refPoint - transform_y <= 300):          
                        self.draw_x(transform_x + x_refPoint,y_refPoint - transform_y)
                        ##, current_scale)
                        ###plotting the 3d part ##T(x_refPoint,y_refPoint)=(ax+by,cx+dy)=[acbd][xy], make a vector command from centre_x centre_y
                        ##this dd will be a scale of its position relative to the centre,x_refPoint
                        #self.draw_line(centre_x + self.rotation_around_y - 5,centre_y + 10,centre_x + self.rotation_around_y + 5,centre_y + 10)     
                        if self.points[i][3] is not None:                                                                                                                                                       ###should have used a function unless i make the whole 3d part a function
                            for place in self.points[i][3]:
                                ThreeD_pointx, ThreeD_pointy, ThreeD_pointz = self.TD_plot(self.points[place][0]*self.zoom_factor,self.points[place][1]*self.zoom_factor,self.points[place][2]*self.zoom_factor)
                                self.draw_line(transform_x + x_refPoint,y_refPoint - transform_y,self.points[place][0]*self.zoom_factor + x_refPoint,y_refPoint - self.points[place][1]*self.zoom_factor)
                                self.draw_line(transform_x + x_refPoint,z_refPoint - transform_z,self.points[place][0]*self.zoom_factor + x_refPoint,z_refPoint - self.points[place][2]*self.zoom_factor)
                    if (transform_x + x_refPoint >= 100 and transform_x + x_refPoint <= 300) and (z_refPoint - transform_z >= 320 and z_refPoint - transform_z <= 520):
                        self.draw_x(transform_x + x_refPoint,z_refPoint - transform_z)
                                                                                                                                                                ##it doesnt make sense for the z_refPoint lines to be drawn here too but its more efficient
                    if self.axis_faces == False:
                        ThreeD_main_pointx, ThreeD_main_pointy, ThreeD_main_pointz = self.TD_plot(transform_x, transform_y, transform_z)                                                                     #transform_x*np.cos(self.rotation_around_y) + transform_z*np.sin(self.rotation_around_y),transform_y,-transform_x*np.sin(self.rotation_around_y)+transform_z*np.cos(self.rotation_around_y)#x_refPoint,transform_z*np.cos(self.rotation_around_y)-transform_z*np.sin(self.rotation_around_y),transform_y*np.sin(self.rotation_around_y)+transform_z*np.cos(self.rotation_around_y)#transform_x*self.rotation_around_y, transform_y, transform_z*self.rotation_around_y
                        self.draw_x(ThreeD_main_pointx + centre_x,centre_y - ThreeD_main_pointy)
                        if self.points[i][3] is not None:                                                                                                       ###should have used a function unless i make the whole 3d part a function
                            for place in self.points[i][3]:
                                ThreeD_pointx, ThreeD_pointy, ThreeD_pointz = self.TD_plot(self.points[place][0]*self.zoom_factor,self.points[place][1]*self.zoom_factor,self.points[place][2]*self.zoom_factor)
                                self.draw_line(ThreeD_main_pointx + centre_x, centre_y - ThreeD_main_pointy, ThreeD_pointx + centre_x,centre_y - ThreeD_pointy)
            if self.axis_faces == True:
##                try:
                if self.faces is not None:                                                                                                                      ##if the user wants the faces to be shown this loops through the faces list - converts the polygon face vertexes to position coordinates and draws them
                    for face_point in range(len(self.faces)):
                        poly_points = []
                        for point_in_face in self.faces[face_point]:
                            trans_x_poly = self.points[point_in_face][0]*self.zoom_factor
                            trans_y_poly = self.points[point_in_face][1]*self.zoom_factor
                            trans_z_poly = self.points[point_in_face][2]*self.zoom_factor
                            input_poly_x, input_poly_y, input_poly_z = self.TD_plot(trans_x_poly, trans_y_poly, trans_z_poly)
                            poly_points.append([input_poly_x + centre_x,centre_y - input_poly_y]) ##in (x_refPoint,y_refPoint)
                        pygame.draw.polygon(self.window,((1+face_point)%255,(255-face_point)%255,face_point%255),poly_points)
##                except:
##                    print("error with faces")
                ##has to draw n-1 lines - this tries to draw n
            if press_x == True:
                self.rotation_around_y += 0.01
                self.rotation_around_x += 0.01
            pygame.display.flip()  #####and is not none data type
        pygame.quit()
##order the list of points and do a binary search for when yu right click near a point ##run in multithread
##pygameWin_zero = pygameWin()



##for the depth perception thing add a depth variable thats affected by sin and cos of the axis angle rotation
