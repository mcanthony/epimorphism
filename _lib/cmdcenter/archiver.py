from common.globals import *

import random, os

from common.log import *
set_log("ARCHIVER")

class Archiver(object):
    
    def __init__(self):
        self.archive_idx = None
        
        self.current_archive_pos = None
        self.current_state_idx = None

        #Globals().load(self)


    def archive_size(self):
        return len(os.listdir('archive/state'))


    def arc(self, idx):
        ''' Loads a state from the archive '''
        debug("loading archive %d" % idx)

        idx = ("%5d" % int(idx)).replace(" ", "0")
        self.load("archive/fractal%s" % idx)

    def inc_archive(self, idx):
        ''' Increments the archive index and loads the state '''

        # randomly chose an index
        if(idx == 0):
            self.archive_idx = random.randint(0, self.archive_size)
        else:
            if(self.archive_idx != None):
                self.archive_idx += idx
            else:
                self.archive_idx = 0

        self.arc(self.archive_idx)


    def begin_archival(self):
        self.current_archive_pos = self.archive_size
        self.current_state_idx = None
        self.arch_next()
        

    def finish_archival(self):
        # remove images
        # remove states
        pass


    def arch_next(self):
        if(self.current_state_idx == None):
            self.current_state_idx = 0
        else:
            self.current_state_idx += 1
    
        if(not self.load_state(self.current_state_idx)):
            self.finish_archival()

        
    def arch_keep(self):
        self.archive_state(self.current_state_idx, self.current_archive_pos)
        # archive image

        self.arch_next()


    def arch_keep_image(self):
        # archive image
        self.arch_next()


    def arch_regen(self):
        # regen image
        # archive image
        # archive state
        self.arch_next()


    def archive_state(self, from_idx, to_idx):
        os.system("cp config/state/state_%d.est archive/state/%s%s.est" % (from_idx, self.app.name, ("%4d" % idx).replace(' ', '0')))

#    def archive_image(
