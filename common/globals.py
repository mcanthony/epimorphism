import sys

class Globals(object):
    def __call__(self):
        return self

    def init(self, app, env, context, profile, state, cmdcenter, interface, engine):
        self.app, self.env, self.context, self.profile, self.state, self.cmdcenter, self.interface, self.engine = app, env, context, profile, state, cmdcenter, interface, engine

    def load(self, obj):
        setattr(obj, "app", self.app)
        setattr(obj, "env", self.env)
        setattr(obj, "context", self.context)
        setattr(obj, "profile", self.profile)
        setattr(obj, "state", self.state)
        setattr(obj, "cmdcenter", self.cmdcenter)
        setattr(obj, "interface", self.interface)
        setattr(obj, "engine", self.engine)

#    def load(self):
#        sys._getframe(1).f_locals['app'] = self.app
#        sys._getframe(1).f_locals['env'] = self.env
#        sys._getframe(1).f_locals['context'] = self.context
#        sys._getframe(1).f_locals['profile'] = self.profile
#        sys._getframe(1).f_locals['state'] = self.state
#        sys._getframe(1).f_locals['cmdcenter'] = self.cmdcenter
#        sys._getframe(1).f_locals['interface'] = self.interface
#        sys._getframe(1).f_locals['engine'] = self.engine


Globals = Globals()   

