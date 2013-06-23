from common.complex import *

from OpenGL.GLUT import *

from interface.keyboardhandler import KeyboardHandler


class DefaultKeyboard(KeyboardHandler):
    def key_pressed(self, key, modifiers):
        # exit
        if(key == "\033"):
            self.cmdcenter.quit()#app.exit = True

        # toggle console
        elif(key == "`"):
            self.cmdcenter.cmd("toggle_console()")

        # toggle echo
        elif(key == GLUT_KEY_F10):
            self.cmdcenter.cmd("state.paths=[]")
            
        # toggle echo
        elif(key == GLUT_KEY_F11):
            self.cmdcenter.cmd("toggle_echo()")

        # toggle fps
        elif(key == GLUT_KEY_F12):
            self.cmdcenter.cmd("toggle_fps()")
     
        # save state
        elif(key == ' '): # space
            self.cmdcenter.cmd("save()")

        # toggle manual iteration
        elif(key == "\011"): # tab
            self.cmdcenter.cmd("toggle_manual()")

        # toggle next frame
        elif(key == "\015"): # enter
            self.cmdcenter.cmd("next()")

        # increment archive
        elif(key == '='):
            self.cmdcenter.cmd("inc_archive(1)")

        # decrement archive
        elif(key == ']'):
            self.cmdcenter.cmd("inc_archive(-1)")

        # randomize archive
        elif(key == '+'):
            self.cmdcenter.cmd("inc_archive(0)")   
     
        # reset fb
        elif(key == "\\"):
            self.cmdcenter.cmd("reset_fb()")

        # reset zn
        elif(key == GLUT_KEY_HOME):
            self.cmdcenter.cmd("reset_zn")
            
        # reset par
        elif(key == GLUT_KEY_END):
            self.cmdcenter.cmd("reset_par")

        # tap tempo
        elif(key == GLUT_KEY_F1):
            self.cmdcenter.cmd("tap_tempo()")


class DefaultInterferenceKeyboard(DefaultKeyboard):
    def key_pressed(self, key, modifiers):
        if(key == '1'):
            self.cmdcenter.cmd("state.par['_N'][0] += 1")
        elif(key == 'q'):
            self.cmdcenter.cmd("state.par['_N'][0] -= 1")
        elif(key == '2'):
            self.cmdcenter.cmd("state.par['_SLICES'][0] += 1")
        elif(key == 'w'):
            self.cmdcenter.cmd("state.par['_SLICES'][0] -= 1")
        elif(key == 'a'):
            self.cmdcenter.cmd("state.par['_VAL_TYPE'][0] += 1")
        elif(key == 'z'):
            self.cmdcenter.cmd("state.par['_VAL_TYPE'][0] -= 1")
        elif(key == 's'):
            self.cmdcenter.cmd("state.par['_HUE_TYPE'][0] += 1")
        elif(key == 'x'):
            self.cmdcenter.cmd("state.par['_HUE_TYPE'][0] -= 1")
        elif(key == 'd'):
            self.cmdcenter.cmd("state.par['_VAL_WRAP_TYPE'][0] += 1")
        elif(key == 'c'):
            self.cmdcenter.cmd("state.par['_VAL_WRAP_TYPE'][0] -= 1")
        elif(key == 'f'):
            self.cmdcenter.cmd("state.par['_HUE_WRAP_TYPE'][0] += 1")
        elif(key == 'v'):
            self.cmdcenter.cmd("state.par['_HUE_WRAP_TYPE'][0] -= 1")
        elif(key in ["7", "8", "9", "0"]):
            i = ["7", "8", "9", "0"].index(key)
            self.cmdcenter.cmd("inc_data('%s', 1)" % self.components[i])
        elif(key in ["u", "i", "o", "p"]):
            i = ["u", "i", "o", "p"].index(key)
            self.cmdcenter.cmd("inc_data('%s', -1)" % self.components[i])
        else:
            DefaultKeyboard.key_pressed(self, key, modifiers)



class DefaultJuliaKeyboard(DefaultKeyboard):
    def key_pressed(self, key, modifiers):
        if(key == '1'):
            self.cmdcenter.cmd("inc_data('%s', 1)" % self.components[0])
        elif(key == 'q'):
            self.cmdcenter.cmd("inc_data('%s', -1)" % self.components[0])

        # increment zn_r
        elif(key in ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"]):
            i = ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"].index(key)
            z0 = r_to_p(self.state.zn[i])
            z1 = [z0[0], z0[1]]
            z1[0] += self.app.par_scale * 0.05
            self.cmdcenter.radial_2d('zn', i, self.app.kbd_switch_spd, z0, z1)

        # decrement zn_r
        elif(key in ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]):
            i = ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"].index(key)
            z0 = r_to_p(self.state.zn[i])
            z1 = [z0[0], z0[1]]
            z1[0] -= self.app.par_scale * 0.05
            if(z1[0] < 0.0):
                z1[0] = 0
            self.cmdcenter.radial_2d('zn', i, self.app.kbd_switch_spd, z0, z1)

        # increment zn_th
        elif(key in ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"]):
            i = ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"].index(key)
            z0 = r_to_p(self.state.zn[i])
            z1 = [z0[0], z0[1]]
            z1[1] += self.app.par_scale * 2.0 * pi / 32.0
            self.cmdcenter.radial_2d('zn', i, self.app.kbd_switch_spd, z0, z1)

        # decrement zn_th
        elif(key in ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"]):
            i = ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"].index(key)
            z0 = r_to_p(self.state.zn[i])
            z1 = [z0[0], z0[1]]
            z1[1] -= self.app.par_scale * 2.0 * pi / 32.0
            self.cmdcenter.radial_2d('zn', i, self.app.kbd_switch_spd, z0,  z1)

        # magnify par_scale
        elif(key == GLUT_KEY_PAGE_UP):
            self.app.par_scale *= 2.0

        # minify par_scale
        elif(key == GLUT_KEY_PAGE_DOWN):
            self.app.par_scale /= 2.0

        else:
            DefaultKeyboard.key_pressed(self, key, modifiers)


class DefaultEpimorphismKeyboard(DefaultKeyboard):
    def key_pressed(self, key, modifiers):
        # set pars if CTRL
        if((modifiers & GLUT_ACTIVE_CTRL) == GLUT_ACTIVE_CTRL):

            # increment par[i] - BORKEN
            if(ord(key) in [49, 0, 27, 28, 28, 30, 31, 127, 57, 48, 1, 19, 4, 6, 7, 8, 10, 11, 12, 59]): # row 1 & 3
                i = [49, 0, 27, 28, 28, 30, 31, 127, 57, 48, 1, 19, 4, 6, 7, 8, 10, 11, 12, 59].index(ord(key))
                if(modifiers & GLUT_ACTIVE_SHIFT == GLUT_ACTIVE_SHIFT) : i += 20
                x0 = self.state.par[i]
                x1 = self.state.par[i] + 0.05
                self.cmdcenter.linear_1d('par', i, self.app.kbd_switch_spd, x0, x1)

            # decrement par[i] - BORKEN
            elif(ord(key) in [17, 23, 5, 18, 20, 25, 21, 9, 15, 16, 26, 24, 3, 22, 2, 14, 13, 44, 46, 31]): # row 2 & 4
                i = [17, 23, 5, 18, 20, 25, 21, 9, 15, 16, 26, 24, 3, 22, 2, 14, 13, 44, 46, 31].index(ord(key))
                if(modifiers & GLUT_ACTIVE_SHIFT == GLUT_ACTIVE_SHIFT) : i += 20
                x0 = self.state.par[i]
                x1 = self.state.par[i] - 0.05
                self.cmdcenter.linear_1d('par', i, self.app.kbd_switch_spd, x0, x1)

        else:

            # increment component
            if(key in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]):
                i = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"].index(key)
                self.cmdcenter.cmd("inc_data('%s', 1)" % self.components[i])


            # decrement component
            elif(key in ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]):
                i = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"].index(key)
                self.cmdcenter.cmd("inc_data('%s', -1)" % self.components[i])

            # random component
            elif(key in ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"]):
                i = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"].index(key)
                self.cmdcenter.cmd("inc_data('%s', 0)" % self.components[i])

            # increment zn_r
            elif(key in ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"]):
                i = ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"].index(key)
                z0 = r_to_p(self.state.zn[i])
                z1 = [z0[0], z0[1]]
                z1[0] += self.app.par_scale * 0.05
                self.cmdcenter.radial_2d('zn', i, self.app.kbd_switch_spd, z0, z1)

            # decrement zn_r
            elif(key in ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]):
                i = ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"].index(key)
                z0 = r_to_p(self.state.zn[i])
                z1 = [z0[0], z0[1]]
                z1[0] -= self.app.par_scale * 0.05
                if(z1[0] < 0.0):
                    z1[0] = 0
                self.cmdcenter.radial_2d('zn', i, self.app.kbd_switch_spd, z0, z1)

            # increment zn_th
            elif(key in ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"]):
                i = ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"].index(key)
                z0 = r_to_p(self.state.zn[i])
                z1 = [z0[0], z0[1]]
                z1[1] += self.app.par_scale * 2.0 * pi / 32.0
                self.cmdcenter.radial_2d('zn', i, self.app.kbd_switch_spd, z0, z1)

            # decrement zn_th
            elif(key in ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"]):
                i = ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"].index(key)
                z0 = r_to_p(self.state.zn[i])
                z1 = [z0[0], z0[1]]
                z1[1] -= self.app.par_scale * 2.0 * pi / 32.0
                self.cmdcenter.radial_2d('zn', i, self.app.kbd_switch_spd, z0,  z1)

            # magnify par_scale
            elif(key == GLUT_KEY_PAGE_UP):
                self.app.par_scale *= 2.0

            # minify par_scale
            elif(key == GLUT_KEY_PAGE_DOWN):
                self.app.par_scale /= 2.0

            # inc current_state_idx
            elif(key == GLUT_KEY_PAGE_UP):
                self.cmdcenter.update_current_state_idx()

            # switch midi speed
            elif(key == GLUT_KEY_F7):
                if(self.app.midi_speed >= 0.5):
                    self.cmdcenter.interface.renderer.flash_message("Changing midi_speed to 0.01")
                    self.app.midi_speed = 0.01
                else:
                    self.cmdcenter.interface.renderer.flash_message("Changing midi_speed to 0.5")
                    self.app.midi_speed = 0.5

            # record events
            elif(key == GLUT_KEY_F8):
                self.cmdcenter.toggle_record()

            # default
            else:
                DefaultKeyboard.key_pressed(self, key, modifiers)
