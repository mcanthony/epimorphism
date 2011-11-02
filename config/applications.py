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
    
