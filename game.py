import pygame
from pygame.locals import *
import storage


class Game:
	columnvalues = [61,114,167,220,273,326,379,432] # x-coords for the board's columns
	rowvalues = [432,379,326,273,220,167,114,61] # y-coords for the board's rows
	whitescore = 0
	blackscore = 0

	def __init__(self, configdata):
		self.GameOn = True
		self.config = configdata
		self.screensize = self.width, self.height = 500, 500
		pygame.init()
		self.screen = pygame.display.set_mode(self.screensize)
		pygame.display.set_caption('PyChess')
		
		self.background = pygame.image.load("assets/chessboard.jpg")
		self.background = pygame.transform.scale(self.background, self.screensize)

		while self.GameOn:
			self.screen.blit(self.background,(0,0))
			self.loadpieceimg()
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN and event.button == 1:
					pos = x,y = pygame.mouse.get_pos()
					for piece in self.whitepieces:
						if self.whitepieces.get(piece)["obj_rect"].collidepoint(pos):
							self.wshowmoves(piece)
							break
					for piece in self.blackpieces:
						if self.blackpieces.get(piece)["obj_rect"].collidepoint(pos):
							self.bshowmoves(piece)
							break
					
			pygame.display.flip()
	
	def getposxy(self, col, row): #returns tuple
		x = self.columnvalues[int(col)]
		y = self.rowvalues[int(row)]
		return x,y

	def wshowmoves(self, piece):
		avalspace = pygame.image.load("assets/avalspace.png").convert_alpha()
		avalspace = avalspace.set_alpha(125)
		killspace = pygame.image.load("assets/killspace.png").convert_alpha()
		killspace = killspace.set_alpha(125)
		actions = self.wavaliableactions(piece) #actions = [{pos:(x,y),kill:True/False}]
		for act in actions:
			if act["kill"]:
				act["obj"] = killspace
				act["obj_rect"] = killspace.get_rect()
			else:
				act["obj"] = avalspace
				act["obj_rect"] = avalspace.get_rect()
				actcenterpos = act["obj_rect"].centerx , act["obj_rect"].centery = act["pos"][0], act["pos"][1]
			self.screen.blit(act["obj"], (act["obj_rect"].x,act["obj_rect"].y) )

	def loadpieceimg(self):

			#Starting with White Pieces that are alive
			for piece in self.whitepieces:
				if self.whiteisalive(piece):
					sqcord = self.whitepieces.get(piece)["pos"]
					coords = self.getposxy(sqcord[0], sqcord[1])
					self.whitepieces.get(piece)["obj"] = pygame.image.load(self.whitepieces.get(piece)["img"]).convert_alpha()
					self.whitepieces.get(piece)["obj_rect"] = self.whitepieces.get(piece)["obj"].get_rect()
					#imgsize = imgwidth, imgheight = self.whitepieces.get(piece)["obj_rect"].width, self.whitepieces.get(piece)["obj_rect"].height
					self.whitepieces.get(piece)["obj_rect"].centerx = coords[0]
					self.whitepieces.get(piece)["obj_rect"].centery = coords[1]
					rectcoords = rectx, recty = self.whitepieces.get(piece)["obj_rect"].x, self.whitepieces.get(piece)["obj_rect"].y
					self.screen.blit(self.whitepieces.get(piece)["obj"], (rectx, recty) )


			#Starting with Black Pieces that are alive
			for piece in self.blackpieces:
				if self.blackisalive(piece):
					sqcord = self.blackpieces.get(piece)["pos"]
					coords = self.getposxy(sqcord[0], sqcord[1])
					self.blackpieces.get(piece)["obj"] = pygame.image.load(self.blackpieces.get(piece)["img"]).convert_alpha()
					self.blackpieces.get(piece)["obj_rect"] = self.blackpieces.get(piece)["obj"].get_rect()
					#imgsize = imgwidth, imgheight = self.blackpieces.get(piece)["obj_rect"].width, self.blackpieces.get(piece)["obj_rect"].height
					self.blackpieces.get(piece)["obj_rect"].centerx = coords[0]
					self.blackpieces.get(piece)["obj_rect"].centery = coords[1]
					rectcoords = rectx, recty = self.blackpieces.get(piece)["obj_rect"].x, self.blackpieces.get(piece)["obj_rect"].y
					self.screen.blit(self.blackpieces.get(piece)["obj"], (rectx, recty) )
			

	whitepieces = {
		"p1":{"pos":[0,1], "img":"assets/wpawn.png"},
		"p2":{"pos":[1,1], "img":"assets/wpawn.png"},
		"p3":{"pos":[2,1], "img":"assets/wpawn.png"},
		"p4":{"pos":[3,1], "img":"assets/wpawn.png"},
		"p5":{"pos":[4,1], "img":"assets/wpawn.png"},
		"p6":{"pos":[5,1], "img":"assets/wpawn.png"},
		"p7":{"pos":[6,1], "img":"assets/wpawn.png"},
		"p8":{"pos":[7,1], "img":"assets/wpawn.png"},
		"b1":{"pos":[2,0], "img":"assets/wbishop.png"},
		"b2":{"pos":[5,0], "img":"assets/wbishop.png"},
		"k1":{"pos":[1,0], "img":"assets/wknight.png"},
		"k2":{"pos":[6,0], "img":"assets/wknight.png"},
		"r1":{"pos":[0,0], "img":"assets/wrook.png"},
		"r2":{"pos":[7,0], "img":"assets/wrook.png"},
		"K":{"pos":[4,0], "img":"assets/wking.png"},
		"Q":{"pos":[3,0], "img":"assets/wqueen.png"}
	}

	blackpieces = {
		"p1":{"pos":[0,6], "img":"assets/bpawn.png"},
		"p2":{"pos":[1,6], "img":"assets/bpawn.png"},
		"p3":{"pos":[2,6], "img":"assets/bpawn.png"},
		"p4":{"pos":[3,6], "img":"assets/bpawn.png"},
		"p5":{"pos":[4,6], "img":"assets/bpawn.png"},
		"p6":{"pos":[5,6], "img":"assets/bpawn.png"},
		"p7":{"pos":[6,6], "img":"assets/bpawn.png"},
		"p8":{"pos":[7,6], "img":"assets/bpawn.png"},
		"b1":{"pos":[2,7], "img":"assets/bbishop.png"},
		"b2":{"pos":[5,7], "img":"assets/bbishop.png"},
		"k1":{"pos":[1,7], "img":"assets/bknight.png"},
		"k2":{"pos":[6,7], "img":"assets/bknight.png"},
		"r1":{"pos":[0,7], "img":"assets/brook.png"},
		"r2":{"pos":[7,7], "img":"assets/brook.png"},
		"K":{"pos":[4,7], "img":"assets/bking.png"},
		"Q":{"pos":[3,7], "img":"assets/bqueen.png"}
	}

	def whiteisalive(self, piece):
		if self.whitepieces[piece] == None:
			return False
		else:
			return True

	def blackisalive(self, piece):
		if self.blackpieces[piece] == None:
			return False
		else:
			return True

