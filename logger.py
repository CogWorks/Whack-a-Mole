import os, json
import time, datetime  



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
    
    


if __name__ == '__main__':
    logger = Logger(["ts","event","item"])
    logger.set_filename(id = 'test', ext = '.tsv')
    logger.open_log()
    
    logger.log(ts = logger.get_ts(), event = 'test1', item = 'a butt')
    time.sleep(.1)
    
    logger.log(ts = logger.get_ts(), item = 'two butts', not_in_header = "bananas")
    time.sleep(.3)
    
    logger.log(ts = logger.get_ts(), event = 'test3')
    time.sleep(.1)
    
    logger.log(item = 'no more butts plz I beg', event = 'test4', ts = logger.get_ts())
    
    logger.close_log()
