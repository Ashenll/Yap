from random import randrange as rnd,choice
from tkinter import*
import math
import time
import random
root=Tk()
fr=Frame(root)
root.geometry('800x600')
canv=Canvas(root,bg='white')
canv.pack(fill=BOTH,expand=1)
class ball():
 def __init__(self,x=40,y=450):
  self.x=x
  self.y=y
  self.r=10
  self.vx=0
  self.vy=0
  self.color=choice(['blue','green','brown'])
  self.id=canv.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill=self.color)
  self.live=30
 def set_coords(self):
  canv.coords(self.id,self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r)

 def move(self):
 
  if self.y <= 550:
   self.vy -= 1.2
   self.y -= self.vy
   self.x += self.vx
   self.vx *= 0.99
   self.set_coords()
  else:

   if self.vx ** 2 + self.vy ** 2 > 10:
    self.vy = -self.vy / 2
    self.vx = self.vx / 2
    self.y = 549  
   if self.live < 0:
    balls.pop(balls.index(self))
    canv.delete(self.id)
   else:
    self.live -= 1
 
  if self.x > 780 or self.x < 20:  
   self.vx = -self.vx / 2
   self.x = min(max(self.x, 21), 779)  

 def hittest(self,ob):
  if abs(ob.x-self.x)<=(self.r+ob.r)and abs(ob.y-self.y)<=(self.r+ob.r):
   return True
  else:
   return False

class gun():
 def __init__(self):
  self.f2_power=10
  self.f2_on=0
  self.an=1
  self.id=canv.create_line(20,450,50,420,width=7)
 def fire2_start(self,event):
  self.f2_on=1
 def fire2_end(self,event):
  global balls,bullet
  bullet+=1
  new_ball=ball()
  new_ball.r+=5
  self.an=math.atan((event.y-new_ball.y)/(event.x-new_ball.x))
  new_ball.vx=self.f2_power*math.cos(self.an)
  new_ball.vy=-self.f2_power*math.sin(self.an)
  balls+=[new_ball]
  self.f2_on=0
  self.f2_power=10
 def targetting(self,event=0):
  if event:
   self.an=math.atan((event.y-450)/(event.x-20))
  if self.f2_on:
   canv.itemconfig(self.id,fill='orange')
  else:
   canv.itemconfig(self.id,fill='black')
  canv.coords(self.id,20,450,20+max(self.f2_power,20)*math.cos(self.an),450+max(self.f2_power,20)*math.sin(self.an))
 def power_up(self):
  if self.f2_on:
   if self.f2_power<100:
    self.f2_power+=1
   canv.itemconfig(self.id,fill='orange')
  else:
   canv.itemconfig(self.id,fill='black')

class target():
 def __init__(self):
  self.points = 0 
  self.hits = 0 
  self.id = canv.create_oval(0, 0, 0, 0)
  self.id_points = canv.create_text(30, 30, text=self.points, font='28')
  self.new_target()
  self.live = 1
  self.vx = rnd(-3, 3)  
  self.vy = rnd(-3, 3)  

 def new_target(self):

  x = self.x = rnd(600, 780)
  y = self.y = rnd(300, 550)
  r = self.r = rnd(2, 50)
  color = self.color = 'red'
  canv.coords(self.id, x - r, y - r, x + r, y + r)
  canv.itemconfig(self.id, fill=color)

 def move(self):
  
  self.x += self.vx
  self.y += self.vy

  
  if self.x - self.r <= 0 or self.x + self.r >= 800:
   self.vx = -self.vx  
  if self.y - self.r <= 0 or self.y + self.r >= 600:
   self.vy = -self.vy 


  canv.move(self.id, self.vx, self.vy)

  def set_random_velocity(self):

   self.vx = random.uniform(-3, 3)
   self.vy = random.uniform(-3, 3)

  for other_target in t1:
   if other_target != self:
    dist_x = self.x - other_target.x
    dist_y = self.y - other_target.y
    distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

    
    if distance < self.r + other_target.r:
     self.vx += dist_x * 0.01  
     self.vy += dist_y * 0.01
     other_target.vx -= dist_x * 0.01
     other_target.vy -= dist_y * 0.01
 def hit(self, points=1):
  canv.coords(self.id, -10, -10, -10, -10)
  self.points += points
  canv.itemconfig(self.id_points, text=self.points)


t1 = [target() for _ in range(2)]
screen1=canv.create_text(400,300,text='',font='28')
g1=gun()
bullet=0
balls=[]


def check_targets():
 for target in t1:
  if target.live:
   return False 
 return True  


def new_game(event=''):
 global gun, t1, screen1, balls, bullet

 for target in t1:
  target.new_target()
  target.live = 1
 bullet = 0
 balls = []

 canv.bind('<Button-1>', g1.fire2_start)
 canv.bind('<ButtonRelease-1>', g1.fire2_end)
 canv.bind('<Motion>', g1.targetting)

 while not check_targets():
  for b in balls:
   b.move()

  for target in t1:
   target.move()

  for b in balls:
   for target in t1:
    if b.hittest(target) and target.live:
     target.live = 0
     target.hit()
     balls.remove(b)  
     canv.delete(b.id)  

  canv.update()
  time.sleep(0.03)
  g1.targetting()
  g1.power_up()

 canv.itemconfig(screen1, text='Вы уничтожили все цели за ' + str(bullet) + ' выстрелов')

 canv.bind('<Button-1>')
 canv.bind('<ButtonRelease-1>')
 canv.bind('<Motion>')

 time.sleep(0.01)
 g1.targetting()
 g1.power_up()
 canv.delete(gun)
 canv.itemconfig(screen1, text='')
 root.after(750, new_game)


new_game()
mainloop()
