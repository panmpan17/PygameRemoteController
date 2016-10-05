import pygame
from bottle import route, run
from multiprocessing import Process, Queue

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STEP = 10

class Web(object):
    def __init__(self, queue):
        self.q = queue
        with open("controller.html", "r") as file:
            self.html = file.read()

    def index(self):
        return self.html
    index.route = "/"

    def up(self):
        self.q.put("up")
        return "Y"
    up.route = "/up"

    def down(self):
        self.q.put("down")
        return "Y"
    down.route = "/down"

    def right(self):
        self.q.put("right")
        return "Y"
    right.route = "/right"

    def left(self):
        self.q.put("left")
        return "Y"
    left.route = "/left"

    # Server Start
    def start(self, hst="0.0.0.0", prt="9090"):
        run(host=hst, port=prt)

    # Route
    @classmethod
    def routeapp(cls, web):
        for kw in dir(web):
            attr = getattr(web, kw)
            if hasattr(attr, 'route'):
                route(attr.route)(attr)

class Game(object):
    def __init__(self, queue, tick=30, x=200, y=200):
        self.x = x
        self.y = y
        self.tick = tick
        self.q = queue

    def start(self):
        pygame.init()
        window = pygame.display.set_mode((400, 400))
        pygame.display.set_caption(" Pygame Remote Controll ")

        clock = pygame.time.Clock()
        while True:
            window.fill(WHITE)
            pygame.draw.circle(window, BLACK, (self.x, self.y), 10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("QUIT")
                    pygame.quit()
                    p.terminate()
                    break
            if not self.q.empty():
                event = self.q.get()
                if event == "up":
                    self.y -= STEP
                elif event == "down":
                    self.y += STEP
                elif event == "right":
                    self.x += STEP
                elif event == "left":
                    self.x -= STEP
            pygame.display.flip()
            clock.tick(self.tick)

if __name__ == "__main__":
    q = Queue()

    webApp = Web(q)
    Web.routeapp(webApp)
    p = Process(target=webApp.start, args=())
    p.start()

    gameApp = Game(q)
    gameApp.start()