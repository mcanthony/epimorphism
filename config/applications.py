from common.structs import App


class Test(App):
    def __init__(self, name="default"):
        App.__init__(self, "test", name)


class Interference(App):
    def __init__(self, name="default"):
        App.__init__(self, "interference", name)


class Julia(App):
    def __init__(self, name="default"):
        App.__init__(self, "julia", name)


class Epimorphism(App):
    def __init__(self, name="default"):
        App.__init__(self, "epimorphism", name)

    def get_substitutions(self):
        cull_enabled = self.state.par['_CULL_DEPTH'] != 0
        subs = App.get_substitutions(self)
        subs.update({'FRACT': self.fract, 'CULL_ENABLED': cull_enabled and "1" or ""})
        return subs


class Lissajousglitch(App):
    def __init__(self, name='default'):
        App.__init__(self, 'lissajousglitch', name)
