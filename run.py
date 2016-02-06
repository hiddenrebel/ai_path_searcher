#!/usr/bin/python
import sys
import ast

class SkiingInSingapore:

	mapWidth_size = 0
	mapHeight_size = 0
	mapSki_render = {} #collect all area
	footpath = []
	highest_loc = []
	pathDic = dict()
	indexPath = 0
	start_path=[0,0,0]
	longest_path = []


	def __init__(self, mapSki):
		self.mapSki = mapSki
		self.searchArea_horizon()

	def searchArea_horizon(self):
		dp_mapSki = ();
		for i, line in enumerate(self.mapSki):
			if i == 0:
				size = line.rstrip().split(' ')
				self.mapWidth_size = int(size[0]) - 1
				self.mapHeight_size = int(size[1]) - 1
			else:
				dp_mapSki = dp_mapSki + (line.rstrip(),)

		# find the highest number
		for i, line in enumerate(dp_mapSki):
			self.mapSki_render[i] = line.rstrip().split(' ')
			self.searchHighest(line,i)

		# collect all the highest number exist
		for i, line in enumerate(dp_mapSki):
			self.mapSki_render[i] = line.rstrip().split(' ')
			self.collectHighest(line,i)

		# searching path from the list of highest number and append it into self.longest_path
		for locate in self.highest_loc:
			self.searchPath(locate)
			longestPath = self.getLongest_path()
			self.longest_path.append(longestPath)
			self.pathDic = dict()
			self.footpath = []

		#searching for the longest path exist
		terpanjang = 0
		terpanjang_path = []
		for longestNya in self.longest_path:
			if longestNya['longest'] > terpanjang:
				terpanjang = longestNya['longest']
				terpanjang_path = longestNya['path']

		for longestNya in self.longest_path:
			if longestNya['longest'] == terpanjang:
				print terpanjang,terpanjang_path
		return

	def getLongest_path(self):
		longest = 0
		terpanjang = []
		for way in self.pathDic:
			if len(ast.literal_eval(self.pathDic[way]))>longest:
				longest = len(ast.literal_eval(self.pathDic[way]))
				terpanjang = self.pathDic[way]
		return {'longest':longest,'path':terpanjang}

	def collectHighest(self,dp_mapSki,loop):
		for idx, elevation in enumerate(self.mapSki_render[loop]):
			current = elevation;
			if int(current) == self.start_path[2]:
				self.highest_loc.append([loop,idx,int(current)])
		

	def searchHighest(self,line,loop):
		current = 0
		# print self.mapSki_render[loop]
		for idx, elevation in enumerate(self.mapSki_render[loop]):
			current = elevation;
			if int(current)>=int(self.start_path[2]):
				self.start_path[0] = loop
				self.start_path[1] = idx
				self.start_path[2] = int(current)

	def recordPathDic(self,removePath=[]):
		if len(self.footpath)>0:
			self.pathDic[self.indexPath]=','.join(str(e) for e in self.footpath)

			self.itung = self.itung + 1
			self.indexPath = self.indexPath + 1
			if removePath != self.start_path:
				self.footpath.remove(removePath)
			
				
	def searchPath(self,path=[]):				
		manyWind_direction = 0

		self.footpath.append(path)
		mapData = self.calibrate(path)
		for checkWay in mapData:
			if type(checkWay[0]) == int:
				self.searchPath(checkWay)
			manyWind_direction = manyWind_direction + 1
			if manyWind_direction == 4:
				self.recordPathDic(path)


	def calibrate(self,mapPath):
		wind_direction = []
		wind_data = [0,0,0]

		# mapPath[0] => untuk line
		# mapPath[1] => untuk index
		# mapPath[2] => untuk value

		#set Value untuk North
		north = mapPath[0] - 1
		
		if north < 0:
			wind_data = [None,None,None]
		else:
			if int(self.mapSki_render[north][mapPath[1]]) < mapPath[2]:
				wind_data[0]= north
				wind_data[1]= mapPath[1]
				wind_data[2]= int(self.mapSki_render[north][mapPath[1]])
			else:
				wind_data = [None,None,None]
				
		wind_direction.append(wind_data)
		wind_data = [0,0,0]
		
		#Set Value untuk East
		if mapPath[1] != self.mapWidth_size:
			east = mapPath[1] + 1
			if int(self.mapSki_render[mapPath[0]][east]) < mapPath[2]:
				wind_data[2]= int(self.mapSki_render[mapPath[0]][east])
				wind_data[0]= mapPath[0]
				wind_data[1]= east
			else:
				wind_data = [None,None,None]
		else:
			wind_data = [None,None,None]
		wind_direction.append(wind_data)
		wind_data = [0,0,0]
		

		#set Value untuk South
		if mapPath[0] != self.mapHeight_size:
			south = mapPath[0] + 1
			if int(self.mapSki_render[south][mapPath[1]]) < mapPath[2]:
				wind_data[2] = int(self.mapSki_render[south][mapPath[1]])
				wind_data[0] = south
				wind_data[1] = mapPath[1]
			else:
				wind_data = [None,None,None]
		else:
			wind_data = [None,None,None]
		wind_direction.append(wind_data)
		wind_data = [0,0,0]

		#set Value untuk West
		west = mapPath[1] - 1
		if west < 0:
			wind_data = [None,None,None]
		else:
			if int(self.mapSki_render[mapPath[0]][west]) < mapPath[2]:
				wind_data[2] = int(self.mapSki_render[mapPath[0]][west])
				wind_data[0] = mapPath[0]
				wind_data[1] = west
			else:
				wind_data = [None,None,None]
		wind_direction.append(wind_data)

		return wind_direction
		
with open('map.txt', 'r') as myfile:
	ski = SkiingInSingapore(myfile)
	

