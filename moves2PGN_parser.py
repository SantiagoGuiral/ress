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

import time

def start_read(source_file):
	"""Obtiene el historial de movimientos de la partida de ajedrez y lo guarda en una cadena de caracteres.
	"""
	with open(source_file,"r") as f:
		record = f.read()
		return record

def move(m):
	"""Pasa cada movimiento de una ficha al formato PGN.
	"""
	M = ""  #Guarda la jugada en formato PGN
	capture = 0
	# Caracteriza el movimiento, sí se mueve una ficha o dos en el caso del movimiento Castle
	if(m.lower() == "ooo" or m.lower() == "oo"):
		M = '-'.join(m.upper()) #https://stackoverflow.com/a/3258612/8235105
		return M
	else:
		# Organiza la jugada en formato PGN
		if(m[0].lower() != "x"): # Jugadas cuando solo se movio una ficha
			past = m[0:2]
			present = m[-2:len(m)]
			piece = m[2:-2]
		else:	# Jugadas cuando se presenta la captura de una ficha
			past = m[1:3]
			present = m[-2:len(m)]
			piece = m[3:-2]
			capture = 1
		#rendering the move:
		pt = piece[0] #piece type
		if(pt.lower() == "p"):
			M = f"{past[0]}x{present}" if(capture) else f"{present}"
		else:
			M = f"{pt.upper()}{past}x{present}" if(capture) else f"{pt.upper()}{past}{present}" #remove upper() if needed
		return M


def decode_stringhistory(record):
	""" Cambia el formato del historial de jugadas y lo pasa a PGN. para esto recibe una cadena de caracteres con los movimientos 
	de las fichas y para cada una formatea la jugada de acuerdo al estandar PGN.
	"""
	record_listed = record.split(" - ") # Separa las jugadas 
	record_listed[-1] = record_listed[-1][:-1] # Elimina el espacio al inicio y final de la cadena de caracteres
	if(record_listed[-1] == ""):
		record_listed.pop()
	record_ordered = "" # Cadena de caracteres que guarda las jugadas PGN
	# Itera sobre cada jugada para pasarla a PGN
	for i,m in enumerate(record_listed):
		iteration = i//2+1
		Blackstate = i%2
		if(not Blackstate):
			record_ordered += f"{iteration}. "
		processed_move = move(m) # Organiza la jugada en formato PGN
		record_ordered += f"{processed_move} " # Agrega la jugada a la cadena de caracteres
	return record_ordered


def to_pgn():
	"""Convierte el historial de jugadas en la partida de ajedrez en formato PGN.
	"""
	#moves source file
	source = "chess-pgn.txt" # Archivo con el historial de jugadas
	#record
	record = start_read(source) # Cadena de caracteres con el historial de jugadas

	# Formato de inicio del archivo PGN de salida
	PGNrecord = """[Event "PDI Final project"]
	[Site "Universidad de Antioquia"]
	[Date "2022.04.06"]
	[EventDate "2022.04.06"]
	[Round "1"]
	[Result "1-0"]
	[White "Garry Kasparov"]
	[Black "Veselin Topalov"]
	[ECO "B01"]
	[WhiteElo "3000"]
	[BlackElo "3000"]
	[PlyCount "18"]

	"""

	result = decode_stringhistory(record) # Decodifica el historial de jugadas a formato PGN 
	PGNrecord += result # Genera una cadena de caracteres con el historial en PGN
	timestr = time.strftime("%H:%M:%S-%d+%m+%y")
	fname = f"PGN{timestr}.txt" 
	# Crea el archivo con la partida de ajedrez en formato PGN
	with open(fname, "w+") as f:
		f.write(PGNrecord)
	return 0


