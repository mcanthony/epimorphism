from common.structs import App


class Test(App):
    def __init__(self, name="default"):
        App.__init__(self, "test", name)


class Interference(App):
    def __init__(self, name="default"):
        App.__init__(self, "interference", name)


class Epimorphism(App):
    def __init__(self, name="default"):
        App.__init__(self, "epimorphism", name)

    def get_substitutions(self):
        cull_enabled = self.state.get_par('_CULL_DEPTH') != 0
        subs = {'FRACT': self.fract, 'CULL_ENABLED': cull_enabled and "#define CULL_ENABLED" or ""}
        return subs
    
