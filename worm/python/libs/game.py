import logging
class Game:
    mystr = ""
    times = 0
    def __init__(self):
        self.mystr = "Hello world "

    def run(self):
        self.test()

    def test(self):
        #logging.info(self)
        print(self.mystr + str(self.times))
        self.times += 1

