"""
----------SANTIAGO RIOS GUIRAL--------------------------------------------------
----------santiago.riosg@udea.edu.co--------------------------------------------
--------------------------------------------------------------------------------
----------EMMANUEL GOMEZ OSPINA-------------------------------------------------
----------emmanuel.gomezo@udea.edu.co-------------------------------------------
--------------------------------------------------------------------------------
----------Curso Básico de Procesamiento de Imágenes y Visión Artificial---------
--------------------------------------------------------------------------------
"""

import math

def save_pgn(txt):
	with open ('chess-png.txt', 'w') as f:
		f.write(txt)


def rect_size(w, h):
	wc = w / 8
	hc = h / 8
	return wc, hc


def get_square(wc, hc, x, y):
	hc = y / hc
	wc = x / wc

	hc = math.ceil(hc)
	numbers = {1:'h', 2:'g', 3:'f', 4:'e', 5:'d', 6:'c', 7:'b', 8:'a'}
	height = numbers.get(hc, 'Not found')

	wc = math.ceil(wc)
	letters = {1:'8', 2:'7', 3:'6', 4:'5', 5:'4', 6:'3', 7:'2', 8:'1'}
	width = letters(wc, 'Not Found')

	coordinate = width + height
	return coordinate


def initial_position():
	pos = {'K':['e1','e1'],'k':['e8','e8'],'Q':['d1','d1'],'q':['d8','d8'],'RL':['a1','a1'],'RR':['h1','h1'],'rl':['a8','a8'],'rr':['h8','h8'],'NL':['b1','b1'],'NR':['g1','g1'],'nl':['b8','b8'],'nr':['g8','g8'],'BL':['c1','c1'],'BR':['f1','f1'],'bl':['c8','c8'],'br':['f8','f8'],'P1':['a2','a2'],'P2':['b2','b2'],'P3':['c2','c2'],'P4':['d2','d2'],'P5':['e2','e2'],'P6':['f2','f2'],'P7':['g2','g2'],'P8':['h2','h2'],'p1':['a7','a7'],'p2':['b7','b7'],'p3':['c7','c7'],'p4':['d7','d7'],'p5':['e7','e7'], 'p6':['f7','f7'],'p7':['g7','g7'],'p8':['h7','h7']}
	return pos


def get_piece_move(pos, coord1, coord2):
    piece = ''
    following = ''
    actual = ''
    for key, value in pos.items():
        if coord1 == value[1]:
            piece = key
            actual = coord1
            following = coord2
            break
        if coord2 == value[1]:
            piece = key
            actual = coord2
            following = coord1
            break
    
    move = actual + piece + following
    pos[piece] = [actual, following]
    return pos, piece, move
   

def convert_to_pgn(move):
	pass

