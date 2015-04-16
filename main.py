#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Timothy
#
# Created:     17/11/2014
# Copyright:   (c) Timothy 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def distanceBetween(pos1,pos2):
    return (((pos1[0] - pos2[0])**2) + ((pos1[1] - pos2[1])**2))**0.5
class stationaryCharge:
    xPos = 0.0
    yPos = 0.0
    charge = 0.0
    def __init__(self,xPos,yPos,charge):
        self.xPos = xPos
        self.yPos = yPos
        self.charge = charge
class TestCharge:
    xPos = 0.0
    yPos= 0.0
    charge = 0.0
    velocity = 0.0
    direction = 0.0
    mass = 1
    def __init__(self,xPos,yPos,charge,vel=0):
        self.xPos = xPos
        self.yPos = yPos
        self.lastXPos = xPos
        self.lastYPos = yPos
        self.charge = charge
        self.velocity = vel
        self.direction = 0.0
        self.timeToLive = 900
        self.distanceTravelled = 0
    def updatePosition(self):
        import math
        self.lastXPos = self.xPos
        self.lastYPos = self.yPos
        self.xPos = self.xPos + (self.velocity * math.cos(math.radians(self.direction)))
        self.yPos = self.yPos + (self.velocity * math.sin(math.radians(self.direction)))
        self.distanceTravelled = self.distanceTravelled + distanceBetween((self.xPos,self.yPos),(self.lastXPos,self.lastYPos))
        if self.distanceTravelled > 20:
            self.timeToLive = 0
        self.timeToLive = self.timeToLive - 1
    def reactToStationary(self,other):
        #calculate field strength
        import math
        distance = distanceBetween((self.xPos,self.yPos),(other.xPos,other.yPos))/1000
        fieldStrength = other.charge/(distance**2)#(4*3.141592653589793*(8.85*(10**-11))*(distance**2))
        forcedirection = math.degrees(math.atan2((self.yPos - other.yPos),(self.xPos - other.xPos)))
        #calculate components and resolve
        forceforce = fieldStrength * self.charge
        xVelChange = (forceforce * math.cos(math.radians(forcedirection)))/self.mass
        yVelChange = (forceforce * math.sin(math.radians(forcedirection)))/self.mass
        resultX = xVelChange + (self.velocity * math.cos(math.radians(self.direction)))
        resultY = yVelChange + (self.velocity * math.sin(math.radians(self.direction)))
        self.direction = math.degrees(math.atan2(resultY,resultX))
        self.velocity = ((resultX**2) + (resultY**2))**0.5
def main():
    import pygame, sys, os, random
    clock = pygame.time.Clock()
    pygame.init()
    FPS = 60
    DEVPINK = (255,0,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (0,255,255)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    gridspacing = 5
    mainSurface = pygame.display.set_mode((1366,768))
    stationaryArray = []
    stationaryChargeAmount = 1
    #stationaryArray = [stationaryCharge(205,150,10),stationaryCharge(605,150,-1)]
##    for apple in range(0,100):
##        stationaryArray.append(stationaryCharge(301 + (apple*5),300,10))
##        stationaryArray.append(stationaryCharge(301 + (apple*5),600,-10))
    testChargeArray = []
    stationaryRadius = 10
    chargeToPlace = 0.01
    linemode = False
    vel0mode = False
    trails = True
##    for i in range(0,65):
##        for j in range(0,38):
##            testChargeArray.append(TestCharge(i*10,j*10,chargeToPlace))
    while True:
        if trails == False:
            mainSurface.fill(BLACK)
        for charge in testChargeArray:
            for other in stationaryArray:
                charge.reactToStationary(other)
            charge.updatePosition()
            if vel0mode == True:
                charge.velocity = 0
##            if charge.timeToLive <= 0:
##                testChargeArray.remove(charge)
            for other in stationaryArray:
                if distanceBetween((charge.xPos,charge.yPos),(other.xPos,other.yPos)) < stationaryRadius:
                    if charge in testChargeArray:
                        testChargeArray.remove(charge)
                        break
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    testChargeArray.append(TestCharge((pygame.mouse.get_pos()[0]),pygame.mouse.get_pos()[1],chargeToPlace))
                if event.button == 3:
                    testChargeArray.append(TestCharge((pygame.mouse.get_pos()[0]),pygame.mouse.get_pos()[1],chargeToPlace,10))
##                if event.button == 3:
##                    stationaryArray.append(stationaryCharge(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],10))
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    mainSurface.fill(BLACK)
                    testChargeArray = []
                    for i in range(0,round(1366/gridspacing)):
                        for j in range(0,round(768/gridspacing)):
                            testChargeArray.append(TestCharge(i*gridspacing,j*gridspacing,chargeToPlace))
                    if linemode == True:
                        for charge in testChargeArray:
                            for other in stationaryArray:
                                charge.reactToStationary(other)
                            charge.updatePosition()
                        for charge in testChargeArray:
                            if charge.distanceTravelled < 300:
                                pygame.draw.line(mainSurface,RED,(charge.xPos,charge.yPos),(charge.lastXPos,charge.lastYPos))
                        testChargeArray = []
                elif event.key == K_UP:
                    stationaryArray.append(stationaryCharge(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],stationaryChargeAmount))
                elif event.key == K_DOWN:
                    stationaryArray.append(stationaryCharge(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],-1*stationaryChargeAmount))
                elif event.key == K_LEFT:
                    stationaryArray = []
        for testCharge in testChargeArray:
            pygame.draw.circle(mainSurface,DEVPINK,(round(testCharge.xPos),round(testCharge.yPos)),1,0)
        for testCharge in stationaryArray:
            pygame.draw.circle(mainSurface,GREEN,(round(testCharge.xPos),round(testCharge.yPos)),stationaryRadius,0)
        pygame.display.update()
        clock.tick(FPS)
if __name__ == '__main__':
    from pygame.locals import *
    main()
