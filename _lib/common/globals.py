class Globals(object):
    ''' Quite hacky way to have the main config & application objects available in any object without having to pass them around. '''

    def __call__(self):
        return self


    def init(self, app, state, cmdcenter, interface, engine):
        self.app, self.state, self.cmdcenter, self.interface, self.engine = app, state, cmdcenter, interface, engine


    def load(self, obj, access=["app", "state", "cmdcenter", "interface", "engine"]):
        if("app" in access):
            setattr(obj, "app", self.app)
        if("state" in access):
            setattr(obj, "state", self.state)
        if("cmdcenter" in access):
            setattr(obj, "cmdcenter", self.cmdcenter)
        if("interface" in access):
            setattr(obj, "interface", self.interface)
        if("engine" in access):
            setattr(obj, "engine", self.engine)


Globals = Globals()   

