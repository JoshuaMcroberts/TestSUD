# -*- coding: cp1252 -*-
# This file define what exists in the world.
import glob, copy
from libraries import *
from engine import *

# CREATE A DICTIONARY READING FILES IN A FOLDER
# FilesToDict(*Path, ValidExt, If is room then put yes if not let blank)
def FilesToDict(Path, Ext, IsRoom='no'):
    ListOfFiles = glob.glob(Path + '*' + Ext)
    ListOfFilesB = copy.copy(ListOfFiles)

    if IsRoom.lower() == "yes":
        for n, i in enumerate(ListOfFilesB):
            a = i.replace(Path,'')
            b = a.replace(Ext,'')
            ListOfFilesB[n] = b

        for n, i in enumerate(ListOfFilesB):
            try:
                j = list(i)
                i = j[8]
                int(i)
                
            except ValueError:
                ListOfFiles.pop(n)

    Dict = {}

    for i in ListOfFiles:
        fileread = open(i,"r")
        thisfile = fileread.readlines()
        fileread.close()
    return Dict

# SHOW ROOM DESCRIPTION TO PLAYER IN FRIENDLY FORMAT
# ShowRoom(FilesToDict(RoomsPath, ValidExt, 'yes'),'1')
# Rooms = rooms dictionary
# Number = specific room number (ID)
def ShowRoom(Rooms, Number):
    return prcolor(6, Rooms[Number][1]) + '\n[ Exits: ' + prcolor(7,' '.join(list(Rooms[Number][0]))) + ' ]\n' + ' '.join(Rooms[Number][2:])

ClearScreen()

# Defines default paths and valid extension for files
RoomsPath = './rooms/'
ObjectsPath = './objects/'
# ItemsPath = './items/'
ValidExt = '.txt'

# Create subdirectories if don't exist
if os.path.isdir(RoomsPath) is False:
    os.mkdir(RoomsPath)
if os.path.isdir(ObjectsPath) is False:
    os.mkdir(ObjectsPath)
# if os.path.isdir(ItemsPath) is False:
#     os.mkdir(ItemsPath)

# # Items
# # Read folder "items" and create dictionary reading files in there
# # name: (look, touch, use)
# BaseItemsDic = FilesToDict(ItemsPath, ValidExt)
# # Void final dictionary of items
# ItemsDic = {}
# # Fulfill final dictionary of items (item name: atribute 1, attribute 2 etc)
# for i in BaseItemsDic:
# # name: Class(name, look, touch, use)
#     ItemsDic[i] = SudItem(i,BaseItemsDic[i][0],BaseItemsDic[i][1],BaseItemsDic[i][2])

# print (ItemsDic)

# OBJECTS
# Read folder "objects" and create dictionary reading files in there
# name: (look, touch, use)
BaseObjectsDic = FilesToDict(ObjectsPath, ValidExt)
# Void final dictionary of objects
ObjectsDic = {}
# Fulfill final dictionary of objects (object name: atribute 1, attribute 2 etc)
for i in BaseObjectsDic:
# name: Class(name, look, touch, use)
    ObjectsDic[i] = SudObject(i,BaseObjectsDic[i][0],BaseObjectsDic[i][1],BaseObjectsDic[i][2])

print (ObjectsDic)

# ROOMS
# Read folder "rooms" and create dictionary reading files in there
# IDs : (Exits, Room title, Room description)
BaseRoomsDic = FilesToDict(RoomsPath, ValidExt, 'yes')
# Void final dictionary of rooms
RoomsDic = {}
# Fulfill final dictionary of rooms
for i in BaseRoomsDic:
    desc = ShowRoom(BaseRoomsDic, i)
# 'ID' : Class(string: Room title, Exits, Room description)
# To call an area, use 'ID'
    RoomsDic[i] = SudArea(desc)

# Attaching interactive stuff to areas
#  - item_room > item_name > description_file_name
RoomsDic['1'].addObject('flower', ObjectsDic['rose']) # porto
RoomsDic['2'].addObject('carp', ObjectsDic['poo']) # praia
RoomsDic['3'].addObject('fruit', ObjectsDic['apple']) # alfandega
RoomsDic['4'].addObject('bird', ObjectsDic['sparrow']) # donzela
RoomsDic['6'].addObject('metal cylinder', ObjectsDic['lightsaber']) # Town square

# Link all areas with bidirectional references
#  - existing_room > direction to > new_room
RoomsDic['1'].addArea('north', RoomsDic['2']) # porto > n > praia
RoomsDic['1'].addArea('west', RoomsDic['3']) # porto > w > alfandega
RoomsDic['4'].addArea('north', RoomsDic['1']) # donzela > n > porto
RoomsDic['5'].addArea('east', RoomsDic['4']) # vila > e > donzela
RoomsDic['2'].addArea('east', RoomsDic['6']) # praia > e > Town Square

# Create a character
char = SudPlayer('PlayerName')

# Create a game with player and starting area
game = SudGame(char, RoomsDic['1'])

# Lets go!
#ClearScreen()
game.run()
