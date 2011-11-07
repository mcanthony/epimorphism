from common.globals import *

import os.path
import os

import math

from common.runner import *

import threading

from common.log import *
set_log("VIDEO")

class VideoRenderer(object):
    ''' The VideoRenderer object is responsible for sequentially capturing the
        frames output by the engine '''


    def __init__(self):
        debug("Initializing video renderer")
        Globals().load(self)

        self.frame_num = 0
        self.capturing_event = threading.Event()


    def capture(self):
        info("Capturing video frame %d at time %s" % (self.frame_num, self.cmdcenter.time()))

        # return if necessary
        if(not self.app.render_video):
            return False

        # encapsulated for asynchronous execution
        def grab_image():
            image = self.cmdcenter.grab_image()

            # pad frame_num
            digit_size = 5
            padded = "".join(["0" for i in xrange(digit_size - int(math.log10(self.frame_num + 1)) - 1)]) + str(self.frame_num + 1)

            # save
            image.save("media/video/%s/%s.png" % (self.video_name, padded))

            # stop video if necessary
            if(self.app.max_video_frames and self.frame_num == int(self.app.max_video_frames)):
                self.stop_video(True)

                if(self.app.video_script):
                    info("Video rendering complete.  Exiting program")
                    self.app.exit = True

            self.capturing_event.set()


        if(self.frame_num != 0):
            self.capturing_event.wait()
        self.capturing_event.clear()

        # inc frame num
        self.frame_num += 1

        # async grab frame
        self.cmdcenter.engine.do_get_fb = True
        async(grab_image)


    def start_video(self, video_name=None):

        info("Starting video renderer")

        # turn on fps sync
        self.app.fps_sync = self.app.video_frame_rate

        # set vars
        self.frame_num = 0
        self.app.render_video = True

        # get video name if necessary
        if(not video_name):
            i = 0
            while(os.path.exists("media/video/%d/" % i)):
                i += 1
            video_name = str(i)

        # make directory
        os.mkdir("media/video/%s/" % video_name)

        # set video name
        self.video_name = video_name


    def stop_video(self, compress=False):
        info("Stopping video renderer")

        # return if necessary
        if(not self.app.render_video):
            return False

        self.app.render_video = False

        def compress():
            # example for cropping & adding audio track
            # ffmpeg -i 06\ Miss\ Rose.mp3 -ab 192k -ar 44100 -f image2 -r 30 -i video/3/%05d.png -vcodec libx264 -vpre fast  -bf 0 -crf 20 -threads 7 -croptop 484 -cropbottom 484 -cropleft 64 -cropright 64 -t 00:03:18 3_2c.mp4

            cmd = "ffmpeg -f image2 -i video/%s/%%05d.png  -vcodec libx264 -vpre fast -r 30 -crf 22 -threads 7 %s.mp4" % (self.video_name)*2

            info("Compressing with command - " + cmd)
            os.system(cmd)


            print "to add audio - mencoder %s.avi -oac copy -ovc copy -audiofile AUDIO.mp3 -o %s_audio.avi" % (self.video_name, self.video_name)

        async(compress)                           

        # turn off fps sync
        self.app.fps_sync = False
