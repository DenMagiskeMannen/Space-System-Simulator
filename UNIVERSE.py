"""
Created on Sun Aug 11 19:42:05 2024

@author: teodo
"""
import pygame
import time
import random
import math

def MeterToPixel(Meters, zoom):
    DirectPixels = Meters / (1274200 / zoom)
    DirectPixels = math.floor(DirectPixels + 0.5)
    return DirectPixels

def PixelToMeter(Pixels, zoom):
    Meters = Pixels * (1274200 / zoom)
    return Meters

pygame.init()
screenie = (1280, 720)
screen = pygame.display.set_mode(screenie)
clock = pygame.time.Clock()
running = True

class Celestial():
    Bodies = []
    
    def __init__(self, Point=None, Mass=None, Size=None, Velocity=None, Colour=None):
        if Point is not None:
            self.point = Point
        else:
            self.point = [random.randint(0, screenie[0]), random.randint(0, screenie[1])]
        
        self.size = Size if Size is not None else 6371000  # Default radius in meters
        self.mass = Mass if Mass is not None else 5.972 * (10 ** 24)  # Default mass in kg
        self.velocity = Velocity if Velocity is not None else [random.randint(-5, 5), random.randint(-5, 5)]
        self.colour= Colour if Colour is not None else [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        
        self.PixelRadius = MeterToPixel(self.size, zoom)
        self.Information = []
        self.Bodies.append(self)
    
    def Force(self):
        self.Information = []
        G = 6.674 * 10 ** (-11)  # NM**2/kg**2
        M1 = self.mass
        for each in self.Bodies:
            if each != self:
                M2 = each.mass
                Vector = (each.point[0] - self.point[0], each.point[1] - self.point[1])
                VLength = math.sqrt(Vector[0]**2 + Vector[1]**2)
                r = PixelToMeter(VLength, zoom)
                if r <= self.size+each.size:
                    #print("Metric system mf'er!")
                    if self.mass >= each.mass:
                        each.SELF_DESTRUCT()
                        self.mass+=each.mass
                        self.size+=each.size*0.1 #Needs scaling
                """
                elif VLength <= self.PixelRadius+each.PixelRadius:
                    #print("pixel supremecy")
                    each.SELF_DESTRUCT()
                    self.mass+=each.mass
                    self.size+=each.size*0.1 #Needs Scaling
                """
                Direction = (Vector[0] / VLength, Vector[1] / VLength)
                F = (G * M1 * M2) / (r**2)
                dic = {}
                dic["ID"] = each
                dic["Direction"] = Direction
                dic["Force"] = F
                self.Information.append(dic)
    
    def Act(self, dt):
        for each in self.Information:
            Force = [each["Direction"][0] * each["Force"], each["Direction"][1] * each["Force"]]
            Acceleration = [Force[0] / self.mass, Force[1] / self.mass]
            self.velocity[0] +=Acceleration[0]*dt
            self.velocity[1]+= Acceleration[1] *dt
            self.point[0]+=self.velocity[0] *dt
            self.point[1]+=self.velocity[1]*dt
            self.PixelRadius = MeterToPixel(self.size, zoom)
            
        if self.point[0] < 0:
            self.point[0]+=5
            self.velocity[0]=self.velocity[0]*(-0.95)
        elif self.point[0] > screenie[0]:
            self.point[0]-=5
            self.velocity[0]=self.velocity[0]*(-0.95)
            
        if self.point[1] < 0:
            self.point[1]+=5
            self.velocity[1]=self.velocity[1]*(-0.95)
        elif self.point[1] > screenie[1]:
            self.point[1]-=5
            self.velocity[1]=self.velocity[1]*(-0.95)
            
    def SELF_DESTRUCT(self):
        self.Bodies.remove(self)
        

# Initial zoom level
zoom = 1.0
#Celestial(Velocity=[0, 0],Mass=5.972 * (10 ** 27),Size=6371000)
for i in range(50):
    Celestial(Velocity=[0, 0])
#SUN = Celestial(Point=[screenie[0] // 2, screenie[1] // 2], Size=63710000 * 3, Mass=5.972 * (10 ** 27), Velocity=[0, 0])

#for i in range(100):
    #Celestial(Velocity=[0, 0])
dt = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Button 4 (usually back button on some mice)
                zoom = zoom*1.1
            elif event.button == 5:  # Button 5 (usually forward button on some mice)
                zoom = zoom/1.1
    
    while len(Celestial.Bodies)<30:
        Celestial(Velocity=[0, 0])
    for bod in Celestial.Bodies:
        bod.Force()
        bod.Act(dt)
    print(len(Celestial.Bodies))
    screen.fill("white")
    for bod in Celestial.Bodies:
        pygame.draw.circle(screen, "black", (int(bod.point[0]), int(bod.point[1])), int(bod.PixelRadius))
   
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
