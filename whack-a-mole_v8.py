import pygame
import random
import pdb
import numpy
import math
import os, sys
import datetime, time
import json
import platform


from twisted.internet import reactor
from twisted.internet.task import LoopingCall

try:
    #from pyfixation import VelocityFP
    #print("Pyfixation success.")
    from pyviewx.client import iViewXClient, Dispatcher
    print("Pyview client success")
    from pyviewx.pygame import Calibrator
    print("Pyview pygame support success.")
    from pyviewx.pygame import Validator
    print("Pyview validator support success.")
    import numpy as np
    print("numpy success")
    eyetrackerSupport = True
except ImportError:
    print("Warning: Eyetracker not supported on this machine.")
    eyetrackerSupport = False 

#Logger class, as provided by Mike Schoelles
class Logger():
    def __init__(self,header,dl = '\t', nl = '\n', fl = 'NA', logtype="main", ts_shift = 1.0):
	self.header = header
	self.delim = dl
	self.newline = nl
	self.filler = fl
	self.file = None
	self.logtype = logtype
	self.init_time = time.time()
	self.ts_shift = 0
	self.fn = None
	self.dir = None
	return
    
    #date-time formatting function; great for logging information
    def getDateTimeStamp(self):
	d = datetime.datetime.now().timetuple()
	return "%d-%02.d-%02.d_%02.d-%02.d-%02.d" % (d[0], d[1], d[2], d[3], d[4], d[5])
    
    def get_ts( self ):
	
	#take current time, subtract from initial time (set at __init__)
	return (time.time() - self.init_time) * (10.0 ** self.ts_shift)
    
    def set_filename(self, dir = None, session_dir = True, id = '', datestamp = True, ext = ".txt"):
	
	#unique subject and session id: [subjectID]_[datetimestamp]
	basename = id + ('_' if id else '') + self.getDateTimeStamp()
	
	#set preferred directory OR default to new directory named after THIS FILE
	basedir = dir if dir else os.path.splitext(os.path.basename(__file__))[0] + "_data"
	
	#if you want a directory for each subject/session...
	if session_dir:
	    basedir = basedir + '/' + basename
	
	#construct final filepath
	self.fn = basedir + '/' + self.logtype + '_' + basename + ext
	self.dir = basedir
	return
    
    def open_log(self):
	
	#if filename or directory are undefined, set them to the default
	if not self.fn or not self.dir:
	    self.set_filename()
	
	#if desired directory doesn't exist, make one
	if not os.path.exists(self.dir):
	    os.makedirs(self.dir)
	
	#open the file to be written
	self.file = open(self.fn,'w')
	
	#write the header and newline character
	self.file.write(self.delim.join(self.header))
	self.file.write(self.newline)
	return
    
    def log(self,  **kwargs):
	
	#create a full-length line of filler values
	line = [self.filler] * len(self.header)
	
	#for each pair of keywords and values passed to function...
	for k, v in kwargs.iteritems(): 
	
	    #if the key is part of the header
	    if k in self.header:
	    
		#add a value in that position of this line.
		line[self.header.index(k)] = str(v)
	
	#write line to file and newline character
	self.file.write(self.delim.join(line)) #convert list to delimited string
	self.file.write(self.newline)
	return
    
    def close_log(self):
	
	#close the file
	self.file.close()
	return

#Logger class, as provided by Mike Schoelles
class Logger():
    def __init__(self,header,dl = '\t', nl = '\n', fl = 'NA', logtype="main", ts_shift = 1.0):
        self.header = header
        self.delim = dl
        self.newline = nl
        self.filler = fl
        self.file = None
        self.logtype = logtype
        self.init_time = time.time()
        self.ts_shift = 0
        self.fn = None
        self.dir = None
        return
    
    #date-time formatting function; great for logging information
    def getDateTimeStamp(self):
        d = datetime.datetime.now().timetuple()
        return "%d-%02.d-%02.d_%02.d-%02.d-%02.d" % (d[0], d[1], d[2], d[3], d[4], d[5])
    
    def get_ts( self ):
        
        #take current time, subtract from initial time (set at __init__)
        return (time.time() - self.init_time) * (10.0 ** self.ts_shift)
    
    def set_filename(self, dir = None, session_dir = True, id = '', datestamp = True, ext = ".txt"):
        
        #unique subject and session id: [subjectID]_[datetimestamp]
        basename = id + ('_' if id else '') + self.getDateTimeStamp()
        
        #set preferred directory OR default to new directory named after THIS FILE
        basedir = dir if dir else os.path.splitext(os.path.basename(__file__))[0] + "_data"
        
        #if you want a directory for each subject/session...
        if session_dir:
            basedir = basedir + '/' + basename
        
        #construct final filepath
        self.fn = basedir + '/' + self.logtype + '_' + basename + ext
        self.dir = basedir
        return
    
    def open_log(self):
        
        #if filename or directory are undefined, set them to the default
        if not self.fn or not self.dir:
            self.set_filename()
        
        #if desired directory doesn't exist, make one
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        
        #open the file to be written
        self.file = open(self.fn,'w')
        
        #write the header and newline character
        self.file.write(self.delim.join(self.header))
        self.file.write(self.newline)
        return
    
    def log(self,  **kwargs):
        
        #create a full-length line of filler values
        line = [self.filler] * len(self.header)
        
        #for each pair of keywords and values passed to function...
        for k, v in kwargs.iteritems(): 
        
            #if the key is part of the header
            if k in self.header:
            
                #add a value in that position of this line.
                line[self.header.index(k)] = str(v)
        
        #write line to file and newline character
        self.file.write(self.delim.join(line)) #convert list to delimited string
        self.file.write(self.newline)
        return
    
    def close_log(self):
        
        #close the file
        self.file.close()
	return

#Game world class
class World():

        if eyetrackerSupport:
            gaze_buffer = []
            d = Dispatcher()

        stop = False
## World constants
#set of colors
        colors = {
                'turquoise': (26, 188, 156),
                'green sea': (22, 160, 133),
                'emerald': (46, 204, 113),
                'nephritis': (39, 174, 96),
                'peter river': (52, 152, 219),
                'belize hole': (41, 128, 185),
                'amethyst': (155, 89, 182),
                'wisteria': (142, 68, 173),
                'wet asphalt': (52, 73, 94),
                'midnight blue': (44, 62, 80),
                'sun flower': (241, 196, 15),
                'orange': (243, 156, 18),
                'carrot': (230, 126, 34),
                'pumpkin': (211, 84, 0),
                'alizarin': (231, 76, 60),
                'pomegranate': (192, 57, 43),
                'clouds': (236, 240, 241),
                'silver': (189, 195, 199),
                'concrete': (149, 165, 166),
                'asbestos': (127, 140, 141),
                'brown':(165, 110, 110),
                'hot pink':(255, 105, 180),
	        'white':(255,255,255)
                }

        class Hole():
                def __init__(self, left, top, width, height):
                        self.left= left
                        self.top= top
                        self.width= width
                        self.height= height
                        self.rect= pygame.Rect(left, top, width, height)

        class Mole():
                def __init__(self, name, x, y, timer, counter=0, color='brown' , size= 60, is_there= False, hit= False):
                        self.name= name
                        self.x= x
                        self.y= y
                        self.timer= timer
                        self.counter= counter
                        self.min_x= x-59
                        self.max_x= x+59
                        self.min_y= y-59
                        self.max_y= y+59
                        self.color= color
                        self.size= size
                        self.is_there= False
                        self.hit= False

                def get_name(self):
                        return self.name
                def get_xy(self):
                        return [self.x, self.y]
		def get_x(self):
		    return self.x
		def get_y(self):
		    return self.y
                def within_mole(self, x, y):
                        if x > self.min_x and x < self.max_x:
                                if y > self.min_y and y < self.max_y:
                                        return True
                        return False
                def get_size(self):
                        return self.size
                def get_eye1(self):
                        return self.x-9, self.y-3
                def get_eye2(self):
                        return self.x+9, self.y-3
                def get_mouth(self):
                        return pygame.Rect(self.x-10, self.y+15, 20, 6)
                def isit_there(self):
                        return self.is_there
                def set_is_there(self, val):
                        self.is_there= val
                def set_color(self, color):
                        self.color= color
                def get_color(self):
                        return self.color
                def incr_counter(self):
                        self.counter+=1
                def set_counter(self, val):
                        self.counter= val
                def get_timer(self):
                        return self.timer
                def get_counter(self):
                        return self.counter
                def is_hit(self):
                        return self.hit
                def set_hit(self, val):
                        self.hit= val
                def draw_me(self, screen):
                        pygame.draw.circle(screen, World.colors[self.get_color()], self.get_xy(), self.size, 0)
                        pygame.draw.circle(screen, World.colors["clouds"], self.get_eye1(), 9, 0)
                        pygame.draw.circle(screen, World.colors["clouds"], self.get_eye2(), 9, 0)
                        pygame.draw.circle(screen, World.colors["wet asphalt"], self.get_eye1(), 5, 0)
                        pygame.draw.circle(screen, World.colors["wet asphalt"], self.get_eye2(), 5, 0)
                        pygame.draw.rect(screen, World.colors["pomegranate"], self.get_mouth(), 0)
                def step_up(self):
                        self.y-=1
                def step_down(self):
                        self.y+=1


        #Initializes the world object
        def __init__(self, path = None):

                self.calibrating= False
                self.gaze_window= 30

                #self.resolution = [800,600]
                self.margin = 0
                pygame.font.init()
                self.font = pygame.font.SysFont("comic sans", 60, True, False)

                #self.screen = pygame.display.set_mode(self.resolution) # returns a Surface
                self.screen = pygame.display.set_mode( ( 0, 0 ), pygame.FULLSCREEN )
                self.screen_res= self.screen.get_rect()
		self.screenw= self.screen_res[2]
		self.screenh= self.screen_res[3]
		self.center= [self.screenw//2, self.screenh//2]
		self.bottomleft= [self.screenw//4, 7*self.screenh//8]

                self.clock = pygame.time.Clock()

                self.timer = 0
                self.score = 0

                self.hole_field= []
                self.hole_covers= []
		
		self.draw_laser= False
		self.lasercoord= (0,0)

                self.hole_field.append(self.Hole(self.screenw//4,self.screenh//3,165,90))
                self.hole_field.append(self.Hole(self.screenw//2-self.screenw//18,self.screenh//3,165,90))
                self.hole_field.append(self.Hole(3*self.screenw//4-self.screenw//10,self.screenh//3,165,90))
                self.hole_field.append(self.Hole(self.screenw//4,2*self.screenh//3,165,90))
                self.hole_field.append(self.Hole(self.screenw//2-self.screenw//18,2*self.screenh//3,165,90))
                self.hole_field.append(self.Hole(3*self.screenw//4-self.screenw//10,2*self.screenh//3,165,90))

                self.hole_covers.append(self.Hole(self.screenw//4,self.screenh//3+25,165,40))
                self.hole_covers.append(self.Hole(self.screenw//2-self.screenw//18,self.screenh//3+25,165,40))
                self.hole_covers.append(self.Hole(3*self.screenw//4-self.screenw//10,self.screenh//3+25,165,40))
                self.hole_covers.append(self.Hole(self.screenw//4,2*self.screenh//3+25,165,40))
                self.hole_covers.append(self.Hole(self.screenw//2-self.screenw//18,2*self.screenh//3+25,165,40))
                self.hole_covers.append(self.Hole(3*self.screenw//4-self.screenw//10,2*self.screenh//3+25,165,40)) 
                self.moles= []
                self.mole1= self.Mole("X",0,0,0,0)
                self.mole2= self.Mole("Y",0,0,0,0)


                self.moles.append(self.Mole("A",self.screenw//4+80,self.screenh//3, 45))
                self.moles.append(self.Mole("B",self.screenw//2-self.screenw//18+80,self.screenh//3, 60))
                self.moles.append(self.Mole("C",(3*self.screenw//4)-self.screenw//10+80,self.screenh//3, 75))
                self.moles.append(self.Mole("D",self.screenw//4+80,2*self.screenh//3, 45))
                self.moles.append(self.Mole("E",self.screenw//2-self.screenw//18+80,2*self.screenh//3, 60))
                self.moles.append(self.Mole("F",(3*self.screenw)//4-self.screenw//10+80,2*self.screenh//3, 75))

                self.fix = None
                self.samp = None
                if eyetrackerSupport:
                    #self.client = iViewXClient( "128.113.89.143" , 4444 )
		    self.client = iViewXClient( "128.113.89.141" , 4444 )
                    self.client.addDispatcher( self.d )
                    self.calibrator = Calibrator( self.client, self.screen, reactor = reactor ) #escape = True?

                self.eye_x = None
                self.eye_y = None
                
                self.calibration_points= 5
                self.calibration_auto= True


        def input(self):
                for event in pygame.event.get():
                        #key was pressed
                        if event.type == pygame.KEYDOWN:
                                k = event.key
                                if k == pygame.K_ESCAPE:
                                        #self.stop = True
					event_logger.log(ts = event_logger.get_ts(), event = 'Escape Pressed')
                                        self.lc.stop()
                                elif k == pygame.K_SPACE:
				    event_logger.log(ts = event_logger.get_ts(), event = 'Space Pressed')
                                    if self.eye_x and self.eye_y:
                                        (ex,ey)= (self.eye_x, self.eye_y)
					self.draw_laser= True
					self.lasercoord= (ex,ey)					
                                        for m in self.moles:
                                                if m.within_mole(ex, ey):
                                                        if m.isit_there() and not m.is_hit():
							        event_logger.log(ts = event_logger.get_ts(), event = 'MOLE HIT')
                                                                self.score += 1
                                                                m.set_color('white')
                                                                m.set_hit(True)
                                                                # pygame.mixer.init()
                                                                # pygame.mixer.music.load('doh.mp3')
                                                                # pygame.mixer.music.play()
			if event.type == pygame.MOUSEBUTTONDOWN:
			    event_logger.log(ts = event_logger.get_ts(), event = 'Mouse Pressed')
			    (mx,my)= pygame.mouse.get_pos()
			    self.draw_laser= True
			    self.lasercoord= (mx,my)		    
			    for m in self.moles:
				if m.within_mole(mx, my):
				    if m.isit_there() and not m.is_hit():
					event_logger.log(ts = event_logger.get_ts(), event = 'MOLE HIT')
					self.score += 1
					m.set_color('white')
					m.set_hit(True)    
					#pygame.mixer.init()
					#pygame.mixer.music.load('doh.mp3')
					#pygame.mixer.music.play()										


                if eyetrackerSupport and len( World.gaze_buffer ) > 1:
                    xs = 0
                    ys = 0
                    for i in World.gaze_buffer:
                        xs += i[0]
                        ys += i[1]

                    #self.prev_x_avg = self.i_x_avg
                    #self.prev_y_avg = self.i_y_avg
                    self.eye_x = int( xs / self.gaze_window )
                    self.eye_y = int( ys / self.gaze_window )





        def logic(self):
                (self.mole1).incr_counter()
                (self.mole2).incr_counter()

                if (self.mole1).get_counter() == (self.mole1).get_timer():
                        (self.mole1).set_is_there(False)
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+self.mole1.get_name()+" is down")
                        (self.mole1).set_counter(0)
                if (self.mole2).get_counter() == (self.mole2).get_timer():
                        (self.mole2).set_is_there(False)
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+self.mole2.get_name()+" is down")
                        (self.mole2).set_counter(0)

                if self.mole1== self.Mole(0,0,0,0) or (self.mole1).isit_there() == False:
                        mole= random.choice(self.moles)
                        while mole == self.mole2 or mole == self.mole1:
                                mole= random.choice(self.moles)
                        mole.set_color('brown')
                        mole.set_hit(False)
                        self.mole1= mole
                        (self.mole1).set_is_there(True)
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+mole.get_name()+" is up")

                if self.mole2== self.Mole(0,0,0,0) or (self.mole2).isit_there() == False:
                        mole= random.choice(self.moles)
                        while mole == self.mole1 or mole == self.mole2:
                                mole= random.choice(self.moles)
                        mole.set_color('brown')
                        mole.set_hit(False)
                        self.mole2 = mole
                        (self.mole2).set_is_there(True)
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+mole.get_name()+" is up")

                if self.mole1.get_counter() < 20:
                        self.mole1.step_up()
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+self.mole1.get_name()+" going up")
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+self.mole1.get_name()+" postition= "+str(self.mole1.get_x()) + " , "+str(self.mole1.get_y()))
                if self.mole2.get_counter() < 20:
                        self.mole2.step_up()
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+self.mole2.get_name()+" going up")
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+self.mole2.get_name()+" postition= "+str(self.mole2.get_x()) + " , "+str(self.mole2.get_y()))

                if (self.mole1.get_timer()-self.mole1.get_counter()) < 21:
                        self.mole1.step_down()
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+self.mole1.get_name()+" going down")
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+self.mole1.get_name()+" postition= "+str(self.mole1.get_x()) + " , "+str(self.mole1.get_y()))
                if (self.mole2.get_timer()-self.mole2.get_counter()) < 21:
                        self.mole2.step_down()
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+self.mole2.get_name()+" going down")
			frame_logger.log(ts = frame_logger.get_ts(), event = "Mole "+self.mole2.get_name()+" postition= "+str(self.mole2.get_x()) + " , "+str(self.mole2.get_y()))


        #text-drawing helper function; simplifies text
        def draw_text( self, text, color, loc, surf, justify = "center" ):
                t = self.font.render( str(text), True, color )
                tr = t.get_rect()
                setattr( tr, justify, loc )
                surf.blit( t, tr )
                return tr

        def draw(self):

                        ###Layer 0: Screen Background
                        self.screen.fill(World.colors['emerald'])

                        textcolor = World.colors["clouds"]
                        self.draw_text("WHACK-A-MOLE", textcolor,self.center, self.screen)
                        score_str= str(self.score)
                        self.draw_text("Score: "+score_str, textcolor,self.bottomleft, self.screen)

                        for i in self.hole_field:
			    pygame.draw.ellipse(self.screen, World.colors["wet asphalt"], i, 0)

                        self.mole1.draw_me(self.screen)

                        self.mole2.draw_me(self.screen)

                        for i in self.hole_covers:
			    pygame.draw.ellipse(self.screen, World.colors["wet asphalt"], i, 0)		

                        if self.eye_x and self.eye_y:
			    pygame.draw.circle(self.screen, World.colors["sun flower"], (self.eye_x, self.eye_y), 10, 2)
			    
			if self.draw_laser:
			    pygame.draw.line(self.screen, World.colors["pomegranate"], (self.screenw//2,self.screenh), self.lasercoord, 8)
			    self.draw_laser= False				
			    
                        pygame.display.update()



        #Begin the reactor
        def run( self ):
            #coop.coiterate(self.process_pygame_events()).addErrback(error_handler)
            if eyetrackerSupport:
                self.calibrating = True
                reactor.listenUDP( 5555, self.client )
                self.calibrator.start( self.start , points = self.calibration_points, auto = int(self.calibration_auto))
            else:
                self.start( None )
            reactor.run()
        ###


        def start(self, lc, results=None):
                self.calibrating= False
                self.lc = LoopingCall( self.refresh )
                cleanupD = self.lc.start( 1.0/60 )
                cleanupD.addCallbacks( self.quit )


        def quit( self, lc ):
                reactor.stop()

        def refresh(self):
                if not self.calibrating:
                    self.input()
                    self.logic()
                    self.draw()

        if eyetrackerSupport:
            @d.listen( 'ET_SPL' )
            def iViewXEvent( self, inResponse ):
                self.inResponse = inResponse
                global x, y
                if self.calibrating:
                    return
                
                try:
                    x = float( inResponse[2] )
                    y = float( inResponse[4] )

                    #if good sample, add
                    if x != 0 and y != 0:
                        World.gaze_buffer.insert( 0, ( x, y ) )
                        if len( World.gaze_buffer ) > self.gaze_window:
                            World.gaze_buffer.pop()
                        #print(World.gaze_buffer[0])
                
                except(IndexError):
                    print("IndexError caught-- AOI error on eyetracking machine?")

if __name__ == "__main__":
    event_logger = Logger(["ts","event"])
    event_logger.set_filename(id = 'events', ext = '.tsv')
    event_logger.open_log()  
    frame_logger = Logger(["ts","event"])
    frame_logger.set_filename(id = 'frames', ext = '.tsv')
    frame_logger.open_log()        
    if len(sys.argv) > 1:
	    W = World(path = sys.argv[1].upper())
    else:
	    W = World()

    W.run()
    event_logger.close_log()
    frame_logger.close_log()
    
