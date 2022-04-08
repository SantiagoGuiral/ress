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
import moves2PGN_parser as pgn

def save_pgn(txt):
	"""Guarda el historial de movimientos en un archivo de texto par luego ser convertidos a PGN.
	"""
	with open ('chess-pgn.txt', 'w') as f:
		f.write(txt)
	pgn.to_pgn()


def rect_size(w, h):
	""" Obtiene el ancho y largo de las casillas del tablero de ajedrez. Recibe como argumentos el ancho y el largo del
	tablero completo.
	"""
	wc = w / 8 # Ancho casilla
	hc = h / 8 # Largo casilla
	return wc, hc


def get_square(wc, hc, coordinates):
	"""Obtiene la identificación de las casillas en el tablero de ajedrez. Ex. (a1). Recibe las coordenadas de los contornos
	y los asocia con la casilla correspondiente dentro del tablero.
	"""
	ids = []
	
	# Obtiene la identicación para cada contorno
	for coordinate in coordinates:
		square_id = get_square_id(wc, hc, coordinate) # Obtiene la identifiación
		ids.append(square_id) # Almacena la identificación en una lista.
	
	return ids


def get_square_id(wc, hc, coordinate):
	""" Genera la identificación de la casilla donde se encuentra la coordenada del contorno que representa la posición inicial
	y final. Retorna la identificación como cadena de caracteres.
	"""
	x = coordinate[0] # Punto en el eje x
	y = coordinate[1] # Punto en el eje y
	hc = y / hc # Ubicación de el punto respecto al largo del tablero
	wc = x / wc # Ubicación de el punto respecto al ancho del tablero

	hc = math.ceil(hc) # Valor entero
	numbers = {1:'h', 2:'g', 3:'f', 4:'e', 5:'d', 6:'c', 7:'b', 8:'a'} # Obtiene la casilla de forma horizontal
	height = numbers.get(hc, 'Not found')

	wc = math.ceil(wc) # Valor entero
	letters = {1:'8', 2:'7', 3:'6', 4:'5', 5:'4', 6:'3', 7:'2', 8:'1'} # Obtiene la casilla de forma vertical
	width = letters.get(wc, 'Not Found')

	coordinate = height + width # Forma la identificación de la casilla dentro del tablero
	return coordinate


def initial_position():
	""" Estructura que representa cada ficha con la posición previa y la posición actual.
	"""
	pos = {
            'K':['e1','e1'],
            'k':['e8','e8'],
            'Q':['d1','d1'],
            'q':['d8','d8'],
            'RL':['a1','a1'],
            'RR':['h1','h1'],
            'rl':['a8','a8'],
            'rr':['h8','h8'],
            'NL':['b1','b1'],
            'NR':['g1','g1'],
            'nl':['b8','b8'],
            'nr':['g8','g8'],
            'BL':['c1','c1'],
            'BR':['f1','f1'],
            'bl':['c8','c8'],
            'br':['f8','f8'],
            'P1':['a2','a2'],
            'P2':['b2','b2'],
            'P3':['c2','c2'],
            'P4':['d2','d2'],
            'P5':['e2','e2'],
            'P6':['f2','f2'],
            'P7':['g2','g2'],
            'P8':['h2','h2'],
            'p1':['a7','a7'],
            'p2':['b7','b7'],
            'p3':['c7','c7'],
            'p4':['d7','d7'],
            'p5':['e7','e7'],
            'p6':['f7','f7'],
            'p7':['g7','g7'],
            'p8':['h7','h7']
        }
	return pos


def get_piece_move(pos, coordinates, cnt_moves):
	""" Identificación y detección de la pieza de ajedrez. Recibe la estructura donde se almacenan las posiciónes de las piezas,
	una lista con las coordenadas de los contornos de la diferencia de imágenes y el contador de movimientos de las piezas.
	Retorna la estructura con el historial de movimientos, la pieza que se movio y el movimiento efectuado.
	"""
	piece = '' # Pieza que se movio
	following = '' # Posición a la que llego la pieza
	actual = '' # Posición de donde salio la pieza
	capture = 0 # Indica si hubo captura de alguna pieza
	move = '' # movimiento efectuado
	paso = '' # Captura al paso

	if len(coordinates) == 2: # Movimiento donde solo se mueve una ficha
		coord1 = coordinates[0] # Coordenada en x
		coord2 = coordinates[1] # Coordenada en y
		
		# Indica si se capturó una pieza del jugador rival
		for key, value in pos.items():
			if coord1 == value[1] or coord2 == value[1]:
				capture += 1

		# Establece el movimiento de la ficha luego de la captura
		if capture == 1:
			# Itera sobre el diccionario donde se establece las posiciones de las piezas para comparar las coordenadas obtenidas de la diferencia con los movimientos guardados
			for key, value in pos.items():
				if coord1 == value[1]:
					piece = key # Ficha que se movio
					actual = coord1 # Nueva posición
					following = coord2 # Antigua posición
					break
				if coord2 == value[1]: 
					piece = key # Ficha que se movio
					actual = coord2 # Nueva posición
					following = coord1 # Antigua posición
					break
			move = actual + piece + following # Movimiento. Lugar de partida - Pieza - Lugar de llegada
			pos[piece] = [actual, following] # Actualiza la posición de la pieza en el diccionario
		else:
			# Itera sobre el diccionario cuando hay captura de ficha para comparar las coordenadas obtenidas de la diferencia con los movimientos guardados
			for key, value in pos.items():
				if cnt_moves % 2 != 0 and key.isupper(): # Captura por parte de una ficha blanca
					if coord1 == value[1]:
						piece = key # Ficha que se movio
						actual = coord1
						following = coord2
						break
					if coord2 == value[1]:
						piece = key # Ficha que se movio
						actual = coord2
						following = coord1
						break
				elif cnt_moves % 2 == 0 and key.islower(): # Captura por parte de una ficha negra
					if coord1 == value[1]:
						piece = key # Ficha que se movio
						actual = coord1
						following = coord2
						break
					if coord2 == value[1]:
						piece = key # Ficha que se movio
						actual = coord2
						following = coord1
						break
			# Al capturar una pieza se para la actualización de la posición de esta ficha
			for key, value in pos.items():
				if following == value[1]:
					pos[key] = [value[1], '.'] # Actualiza el diccionario con la ficha capturada
					break

			move = 'X' +  actual + piece + following # Movimiento con captura de una ficha (X)
			pos[piece] = [actual, following] # Actualiza el diccionario con el movimiento

	elif len(coordinates) == 4: # Movimiento castle
		# Actualiza la posición del rey (k)y la torre (r) cuando se efectuá un castle
		for coord in coordinates:
			if coord == 'g1': # Castle corto blanco
				move = 'OO' 
				pos['K'] = ['e1', 'g1']
				pos['RR'] = ['h1', 'f1']
				break
			elif coord == 'c1': # Castle largo blanco
				move = 'OOO'
				pos['K'] = ['e1', 'c1']
				pos['RL'] = ['a1', 'd1']
				break
			elif coord == 'g8': # Castle corto negro
				move = 'oo'
				pos['k'] = ['e8', 'g8']
				pos['rr'] = ['h8', 'f8']
				break
			elif coord == 'c8': # Castle largo negro
				move = 'ooo'
				pos['k'] = ['e8', 'c8']
				pos['rl'] = ['a8', 'd8']
				break
		piece = 'Castle'

	elif len(coordinates) == 3: # Movimiento de captura al paso
		for coord in coordinates:
			if coord[1] == '6': # Capturá de una ficha negra
				following = coord
				break
			elif coord[1] == '3': # Captura de una ficha blanca
				following = coord
				break
		# Actualizá la posición de la pieza que hace la captura
		for coord in coordinates:
			if coord[0] != following[0]:
				actual = coord
			elif coord[0] == following [0] and coord[1] != following[1]:
				paso = coord
		for key, value in pos.items():
			if actual == value[1]:
				piece = key
				break
		for key,value in pos.items():
			if paso == value[1]:
				pos[key] = [value[1], '.']

		pos[piece] = [actual, following] # Actualiza el diccionario con el movimiento
		move = 'X' + actual + piece + following # Movimiento con captura de una ficha

	return pos, piece, move


def update_pgn(pgn, move):
	""" Actualiza la cadena de caracteres con el historial de movimientos. Se actualiza por cada movimiento.
	"""
	new_pgn = pgn + move + " - "
	return new_pgn

