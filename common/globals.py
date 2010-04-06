import sys

class Globals(object):
    def __call__(self):
        return self


    def init(self, app, cmdcenter, interface, engine):
        self.app, self.cmdcenter, self.interface, self.engine = app, cmdcenter, interface, engine


    def load(self, obj):
        setattr(obj, "app", self.app)
        setattr(obj, "context", self.app._context)
        setattr(obj, "profile", self.app._profile)
        setattr(obj, "state", self.app._state)
        setattr(obj, "cmdcenter", self.cmdcenter)
        setattr(obj, "interface", self.interface)
        setattr(obj, "engine", self.engine)


Globals = Globals()   

