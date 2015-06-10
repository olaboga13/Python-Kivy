__author__ = 'Ania'
"""
Nalezy napisac gre Pong na urzadzenie mobilne
"""
#:kivy 1.9.0
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, Clock, \
        ObjectProperty
from kivy.vector import Vector

"""
klasa reprezentujaca pilke (jej ruch)
"""
class PongBall(Widget):

    # predkosc pilki na osiach x i y
    velocity_x = NumericProperty(10000)
    velocity_y = NumericProperty(10000)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
"""
klasa reprezentujaca paletke tenisowa
"""
class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx,vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
"""
klasa przedstawiajaca gre
"""
class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel = (4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # ruch paletek
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # ruch pilki gora-dol
        if(self.ball.y< self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # zdobycie punktu
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
    #poruszanie paletkami przez uzytkownika
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width /3:
            self.player2.center_y = touch.y

"""
aplikacja
"""
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
"""
uruchomienie gry
"""
if __name__ == '__main__':
    PongApp().run()