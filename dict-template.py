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

# Estructura para convertir el historia de partidas al formato PGN

# El diccionario de pieces designa la posición inciial de las fichas en una partida de ajedrez.

pieces = {
    'RL':'a1',
    'NL':'b1',
    'BL':'c1',
    'Q' :'d1',
    'K' :'e1',
    'BR':'f1',
    'NR':'g1',
    'RR':'h1',
    'P1':'a2',
    'P2':'b2',
    'P3':'c2',
    'P4':'d2',
    'P5':'e2',
    'P6':'f2',
    'P7':'g2',
    'P8':'h2',
    
    'rl':'a8',
    'nl':'b8',
    'bl':'c8',
    'q' :'d8',
    'k' :'e8',
    'br':'f8',
    'nr':'g8',
    'rr':'h8',
    'p1':'a7',
    'p2':'b7',
    'p3':'c7',
    'p4':'d7',
    'p5':'e7',
    'p6':'f7',
    'p7':'g7',
    'p8':'h7'
}
# El diccionario pos guarda la posición previa y acutal de cada pieza de ajedrez
pos = {
    'K' :['e1','e1'],
    'k' :['e8','e8'],
    'Q' :['d1','d1'],
    'q' :['d8','d8'],
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
