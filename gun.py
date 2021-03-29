from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
screen = tk.Canvas(root, bg='white')
screen.pack(fill=tk.BOTH, expand=True)

count = 0

class sharik:
    def __init__(self, x=100, y=400):
        'Конструктор класса sharik'
        'x - начальное положение мяча по горизонтали'
        'y - начальное положение мяча по вертикали'
        self.x = x
        self.y = y
        self.r = 20
        self.speed_x = 10
        self.speed_y = 10
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = screen.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 100

    def set_coords(self):
        'устанавливает координаты'
        screen.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        'Переместить мяч'
        global count
        if self.x + self.r >= 800 or self.x - self.r <= 0 and count == 0:
            self.speed_x = -1 * self.speed_x
            count += 1
        elif self.y - self.r <= 0 or self.y + self.r >= 600 and count == 0:
            self.speed_y = -1 * self.speed_y
            count += 1
        self.x += self.speed_x
        self.y += -1 * self.speed_y + 5
        self.speed_y -= 5

    def Hittest(self, object):
        'Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj'
        'object: Обьект, с которым проверяется столкновение'
        if ((self.x - object.x) ** 2 + (self.y - object.y) ** 2) ** 0.5 <= self.r + object.r:
            return True
        else:
            return False


class Gun():
    'класс, описывающий пушку и ее дуло'
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = screen.create_line(20, 450, 50, 420, width=10)

    def fire2_start(self, event):
        self.f2_on = 2

    def fire2_end(self, event):
        'Выстрел, начальные значения компонент скорости мяча speed_x и speed_y зависят от положения мыши'
        global balls, pylya
        pylya += 1
        new_ball = sharik()
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.speed_x = self.f2_power * math.cos(self.an)
        new_ball.speed_y = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        'Прицеливание и повороты. Зависит от положения мыши'
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            screen.itemconfig(self.id, fill='red')
        else:
            screen.itemconfig(self.id, fill='black')
        screen.coords(self.id, 20, 450, 20 + max(self.f2_power, 20) * math.cos(self.an), 450 + max(self.f2_power, 20) * math.sin(self.an))

    def power_up(self):
        'вытягивание дула'
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 2
            screen.itemconfig(self.id, fill='orange')
        else:
            screen.itemconfig(self.id, fill='black')


class Target:
    'цель, выстрелы и итоговая надпись'
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = screen.create_oval(0, 0, 0, 0)
        self.id_points = screen.create_text(30, 30, text=self.points, font='10')
        self.new_target()

    def new_target(self):
        'новая цель'
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(20, 50)
        color = self.color = 'red'
        screen.coords(self.id, x - r, y - r, x + r, y + r)
        screen.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        'шарик попадает в цель'
        screen.coords(self.id, -10, -10, -10, -10)
        self.points += points
        screen.itemconfig(self.id_points, text=self.points)


t1 = Target()
screen1 = screen.create_text(400, 300, text='', font='10')
g1 = Gun()
pylya = 0
balls = []


def new_game():
    global Gun, t1, screen1, balls, pylya
    t1.live = 1
    screen.itemconfig(screen1, text='')
    t1.new_target()
    pylya = 0
    balls = []
    screen.bind('<Button-1>', g1.fire2_start)
    screen.bind('<ButtonRelease-1>', g1.fire2_end)
    screen.bind('<Motion>', g1.targetting)
    while t1.live or balls:
        for b in balls:
            b.move()
            b.set_coords()
            if b.Hittest(t1) and t1.live:
                screen.delete(b.id)
                t1.live = 0
                t1.hit()
                screen.bind('<Button-1>', '')
                screen.bind('<ButtonRelease-1>', '')
                screen.itemconfig(screen1, text='Вы уничтожили цель за количество выстрелов, равное ' + str(pylya))
                screen.update()
                time.sleep(3)
                new_game()
        screen.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    screen.itemconfig(screen1, text='')
    screen.delete(Gun)
    root.after(750, new_game)


new_game()

root.mainloop()