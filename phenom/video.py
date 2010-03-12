import time
import os.path

import math

from common.runner import *

import threading

from common.log import *
set_log("VIDEO")

class VideoRenderer(object):
    ''' The VideoRenderer object is responsible for sequentially capturing the
        frames output by the engine '''

    def __init__(self, cmdcenter, env):

        debug("Initializing video renderer")

        # initialize vars
        self.cmdcenter, self.env = cmdcenter, env
        self.frame_num = 0


    def capture(self):
        info("Capturing video frame %d at time %s" % (self.frame_num, self.cmdcenter.time()))

        # return if necessary
        if(not self.env.render_video):
            return False

        event = threading.Event()

        # define internal function for async execution
        def grab_frame():
            info("Grabbing frame")

            # save frame
            image = self.cmdcenter.grab_image()

            info("Finished grabbing")

            # pad frame_num
            digit_size = 5
            padded = "".join(["0" for i in xrange(digit_size - int(math.log10(self.frame_num + 1)) - 1)]) + str(self.frame_num + 1)

            # save
            image.save("video/%s/%s.png" % (self.video_name, padded))

            # inc frame num
            self.frame_num += 1

            # stop video if necessary
            if(self.env.max_video_frames and self.frame_num == int(self.env.max_video_frames)):
                self.stop_video(True)

            event.set()

            

        # grab frame
        async(grab_frame)

        # wait until we have frame
        #event.wait()

        info("Done waiting")


    def start_video(self, video_name=None):

        info("Starting video renderer")

        # turn on fps sync
        self.env.fps_sync = self.env.video_frame_rate

        # set vars
        self.frame_num = 0
        self.env.render_video = True

        # get video name if necessary
        if(not video_name):
            i = 0
            while(os.path.exists("video/%d/" % i)):
                i += 1
            video_name = str(i)

        # make directory
        os.mkdir("video/%s/" % video_name)

        # set video name
        self.video_name = video_name


    def stop_video(self, compress=False):

        info("Stopping video renderer")

        # return if necessary
        if(not self.env.render_video):
            return False

        # set vars
        self.env.render_video = False

        # run script to compress video
        if(compress):
            "mencoder mf://video/11/*.png -mf w=1536:h=1536:fps=30:type=png -ovc lavc -lavcopts vbitrate=11520000:mbd=2:keyint=132:v4mv:vqmin=3:lumi_mask=0.07:dark_mask=0.2:scplx_mask=0.1:tcplx_mask=0.1:naq:vhq -oac copy -o 11.avi"
            "mencoder 11.avi -oac copy -ovc copy -audiofile AUDIO.mp3 -o 11_audio.avi"

        # turn off fps sync
        self.env.fps_sync = False
