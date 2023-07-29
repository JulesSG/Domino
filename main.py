import random
import pygame
import time

def crear_piezas():# crea las piezas
	piezas = []
	for i in range(7):
		for j in range(7):
			if [i,j] not in piezas and [j,i] not in piezas:
				piezas.append([i,j])
	print(piezas)
	return piezas

def repartir_piezas(): # reparte aleatoriamente las piezas
	piezas = crear_piezas()
	piezas_jugador = []
	posiPieza_jugador = []
	posiPieza_maquina = []
	piezas_maquina = []
	pozo =[]
	#piezas del jugador
	for i in range(7):
		pieza_seleccionada = random.randint(0,27)
		if pieza_seleccionada not in posiPieza_jugador:
			piezas_jugador.append(piezas[pieza_seleccionada])
			posiPieza_jugador.append(pieza_seleccionada)
		else:
			while pieza_seleccionada in posiPieza_jugador:
				pieza_seleccionada = random.randint(0,27)
			posiPieza_jugador.append(pieza_seleccionada)
			piezas_jugador.append(piezas[pieza_seleccionada])
	#piezas de la maquina
	for i in range(7):
		pieza_seleccionada = random.randint(0,27)
		if pieza_seleccionada not in posiPieza_maquina and pieza_seleccionada not in posiPieza_jugador :
			piezas_maquina.append(piezas[pieza_seleccionada])
			posiPieza_maquina.append(pieza_seleccionada)
		else:
			while pieza_seleccionada in posiPieza_jugador or pieza_seleccionada in posiPieza_maquina :
				pieza_seleccionada = random.randint(0,27)
			posiPieza_maquina.append(pieza_seleccionada)
			piezas_maquina.append(piezas[pieza_seleccionada])
	for i in range(28):
		if i not in posiPieza_jugador and i not in posiPieza_maquina:
			pozo.append(piezas[i])


	return [piezas_jugador, piezas_maquina, pozo]


def inicio(): # decide quien inicia la partida y con cual pieza
	distro=repartir_piezas()
	jugador = distro[0]
	maquina = distro[1]
	pozo = distro[2]
	doble_jugador = 0
	doble_maquina = 0
	for i in range(7):
		if [i,i] in jugador and i > doble_jugador:
			doble_jugador = i
		if [i, i] in maquina and i > doble_maquina:
			doble_maquina = i
	if doble_jugador > doble_maquina:
		primero = "J"
	else:
		primero = "M"
		doble_jugador = doble_maquina
	print(f"Piezas jugador: {jugador}")
	print(f"Piezas maquina: {maquina}")
	print(f"Piezas pozo: {pozo}")
	print(f"primero juega: {primero}")
	return [jugador, maquina, pozo, primero, doble_jugador]





def ventana(): # se crea la ventana de la partida

	data = inicio() # se llama a la funcion inicio
	# turno 0 es jugador, turno 1 es maquina
	turno = 0
	# Inicializamos pygame
	pygame.init()
	# Muestro una ventana de 1600x600
	size = 1600, 600
	screen = pygame.display.set_mode(size)
	# Cambio el título de la ventana
	pygame.display.set_caption('Domino')

	#diccionarios para el manejo de las fichas en pantalla
	dadosP_pantalla = {}
	dadosP_rec = {}
	dados_juego = {}
	dadosJ_rec = {}
	#mostrar fichas iniciales
	for i in crear_piezas():
		dadosP_pantalla[str(i)] = pygame.image.load(str('DOMINÒ/' + str(i) + '.png'))
		dadosP_rec[str(i)]=dadosP_pantalla[str(i)].get_rect()
	for i in crear_piezas():
		dados_juego[str(i)] = pygame.image.load(str('DOMINÒ/' + str(i) + '.png'))
		dadosJ_rec[str(i)] = dados_juego[str(i)].get_rect()
	for i in range(7):
		dadosP_rec[str(data[0][i])].move_ip(200+35*i, 450)


	# Comenzamos el bucle del juego
	fuente = pygame.font.Font(None, 30) # tipo de letra
	rows = 0 # pasadas
	run = True
	cola = 0
	cabeza = 0
	torso = []
	cont = 0
	x1=730
	x2 = 840
	while run:

		# Capturamos los eventos que se han producido
		for event in pygame.event.get():
			# Si el evento es salir de la ventana, terminamos
			if event.type == pygame.QUIT:
				run = False
		screen.fill((51,255,255))
		#solo la primera pasada
		if rows == 0:
			# Crea un objeto imagen y obtengo su rectángulo
			for i in range(7):
				screen.blit(dadosP_pantalla[str(data[0][i])], dadosP_rec[str(data[0][i])])




			mensaje = fuente.render('Buscando el doble mayor :3', 1, (0, 0, 0))
			screen.blit(mensaje, (250, 250))
			pygame.display.flip()
			barraProgreso = "...."
			for i in range(5):
				mensaje = fuente.render(barraProgreso, 1, (0, 0, 0))
				screen.blit(mensaje, (310, 280))
				pygame.display.flip()
				barraProgreso+="...."
				time.sleep(0.5) # tiempo de espera
			screen.fill((51, 255, 255))
			if data[3] == "J":
				turno = 1
				mensaje = fuente.render(f'Empieza el jugador con un doble {data[4]}', 1, (0, 0, 0))
				screen.blit(mensaje, (250, 250))
				pygame.display.flip()
				time.sleep(0.5)
				for i in range(7):
					screen.blit(dadosP_pantalla[str(data[0][i])], dadosP_rec[str(data[0][i])])
					pygame.display.flip()
					time.sleep(0.5)

				posicion = data[0].index([data[4],data[4]])
				moverFicha= data[0].pop(posicion)
				# [ficha,izquiera-1 o derecha1 o central 0]
				torso.append([moverFicha,0])
				print(torso)
				dadosJ_rec[str(moverFicha)].move_ip(800, 250)

				screen.blit(dados_juego[str(moverFicha)], dadosJ_rec[str(moverFicha)])
				cola = moverFicha[0]
				cabeza = moverFicha[0]
				pygame.display.flip()

			else:
				mensaje = fuente.render(f'Empieza la maquina con un doble {data[4]}', 1, (0, 0, 0))
				screen.blit(mensaje, (250, 250))
				pygame.display.flip()
				time.sleep(0.5)
				posicion = data[1].index([data[4], data[4]])
				moverFicha = data[1].pop(posicion)
				torso.append([moverFicha,  0])
				screen.blit(dados_juego[str(moverFicha)], dadosJ_rec[str(moverFicha)])
				dadosJ_rec[str(moverFicha)].move_ip(800, 250)
				pygame.display.flip()
				turno = 0
				cola = moverFicha[0]
				cabeza = moverFicha[0]

			rows+=1
		else:

			# juego:


			if turno  == 0:
				#juega jugador
				# comprobacion de si tiene una ficha funcional:


				temp = []
				for i in data[0]:
					if cola in i:
						temp.append(i)
					elif cabeza in i:
						temp.append(i)
				# si no hay ficha funcional, toma del pozo fichas ramdon
				if temp == []:
					while temp == []:
						mensaje = fuente.render(f'Tomando del pozo', 1, (0, 0, 0))
						screen.blit(mensaje, (250, 20))
						p = random.randint(0, len(data[2])-1)
						if cola in data[2][p]:
							temp.append(data[2][p])
							data[0].append(data[2][p])
							data[2].pop(data[2].index(data[2][p]))
						elif cabeza in data[2][p]:
							temp.append(data[2][p])
							data[0].append(data[2][p])
							data[2].pop(data[2].index(data[2][p]))
					dadosP_rec.clear()
					# se pintan los cuadros de nuevo con las fichas del pozo si tomo
					for i in range(len(data[0]) ):
						print(f"reacomodando cuadros {data[0][i]}")

						dadosP_rec[str(data[0][i])] = dadosP_pantalla[str(data[0][i])].get_rect()
						dadosP_rec[str(data[0][i])].move_ip(200 + 35 * i, 450)
					for i in range(len(data[0])):
						screen.blit(dadosP_pantalla[str(data[0][i])], dadosP_rec[str(data[0][i])])
					pygame.display.flip()
				piezasTemp = len(temp) -1
				#se analizan las entradas del teclado
				keys = pygame.key.get_pressed()
				if keys[pygame.K_RIGHT]:
					print(f"temp: {temp}, cont{cont}")
					if cont > len(temp):
						cont = len(temp)
					time.sleep(0.5)
					#navegar entre las fichas que son funcionales
					if len(temp) != 1:
						if cont != 0:
							dadosP_rec[str(temp[cont - 1])] = dadosP_rec[str(temp[cont - 1])].move(0, 50)
						if piezasTemp < cont:
							cont = 0
						dadosP_rec[str(temp[cont])] = dadosP_rec[str(temp[cont])].move(0, -50)
						cont += 1
					else:
						dadosP_rec[str(temp[0])] = dadosP_rec[str(temp[0])].move(0, 50)
						cont = 0
				# Selecciona una ficha para poner en el tablero
				if keys[pygame.K_SPACE ]:
					time.sleep(0.5)
					print(f"contador {cont}, temp: {temp}")
					print(f"temp[cont - 1]: {temp[cont - 1]} ")
					data[0].pop(data[0].index(temp[cont-1]))
					# se analiza como se debe poner la ficha ya sea en la cola o en la cabeza del tablero
					if cola == temp[cont - 1][0]:
						dados_juego[str(temp[cont - 1])] = pygame.transform.rotate(dados_juego[str(temp[cont - 1])], -90)
						torso.append([temp[cont - 1], -1])
						dadosJ_rec[str(temp[cont - 1])].move_ip(x1, 260)
						cola = temp[cont-1][1]
						x1 -= 64
					elif cola == temp[cont - 1][1]:
						dados_juego[str(temp[cont - 1])] = pygame.transform.rotate(dados_juego[str(temp[cont - 1])], 90)
						torso.append([temp[cont - 1], -1])
						dadosJ_rec[str(temp[cont - 1])].move_ip(x1, 260)
						x1 -= 64
						cola = temp[cont - 1][0]
					elif cabeza == temp[cont - 1][0]:
						dados_juego[str(temp[cont - 1])] = pygame.transform.rotate(dados_juego[str(temp[cont - 1])], 90)
						torso.append([temp[cont - 1], 1])
						dadosJ_rec[str(temp[cont - 1])].move_ip(x2, 260)
						x2+=64
						cabeza = temp[cont - 1][1]
					elif cabeza == temp[cont - 1][1]:
						dados_juego[str(temp[cont - 1])] = pygame.transform.rotate(dados_juego[str(temp[cont - 1])], -90)
						dadosJ_rec[str(temp[cont - 1])].move_ip(x2, 260)
						torso.append([temp[cont - 1], 1])
						x2+=64
						cabeza = temp[cont - 1][0]
					turno = 1

				# se valida si el jugador es ganador y se termina el juego
				if data[0] == []:
					mensaje = fuente.render(f'Gano el jugador', 1, (0, 0, 0))
					screen.blit(mensaje, (250, 0))
					pygame.display.flip()
					time.sleep(5)
					pygame.quit()
					break
			else: #turno de la maquina

				time.sleep(2)
				temp = []

				for i in data[1]:
					if cola in i:
						temp.append(i)
					elif cabeza in i:
						temp.append(i)
				print(f"Eligido por la maquina: {temp}")
				if temp == []:
					while temp == []:
						p = random.randint(0, len(data[2])-1)
						if cola in data[2][p]:
							temp.append(data[2][p])
							data[1].append(data[2][p])
							data[2].pop(data[2].index(data[2][p]))
						elif cabeza in data[2][p]:
							temp.append(data[2][p])
							data[1].append(data[2][p])
							data[2].pop(data[2].index(data[2][p]))

				data[1].pop(data[1].index(temp[0])) # elimina la ficha que se puso en tablero
				#posicionar la ficha:
				if cabeza== temp[0][0]:
					dados_juego[str(temp[0])] = pygame.transform.rotate(dados_juego[str(temp[0])], 90)
					torso.append([temp[0], -1])
					dadosJ_rec[str(temp[0])].move_ip(x2, 260)
					x2 += 64

					cabeza = temp[0][1]
				elif cabeza == temp[0][1]:
					dados_juego[str(temp[0])] = pygame.transform.rotate(dados_juego[str(temp[0])], -90)
					torso.append([temp[0], -1])
					dadosJ_rec[str(temp[0])].move_ip(x2, 260)
					x2 += 64
					cabeza = temp[0][0]
				elif cola == temp[0][0]:
					dados_juego[str(temp[0])] = pygame.transform.rotate(dados_juego[str(temp[0])], -90)
					torso.append([temp[0], 1])
					dadosJ_rec[str(temp[0])].move_ip(x1, 260)
					x1 -= 64
					cola = temp[0][1]
				elif cola ==temp[0][1]:
					dados_juego[str(temp[0])] = pygame.transform.rotate(dados_juego[str(temp[0])],90)
					dadosJ_rec[str(temp[0])].move_ip(x1, 260)
					torso.append([temp[0], 1])
					x1 -= 64

					cola = temp[0][0]
				turno = 0
				if data[1] == []:
					mensaje = fuente.render(f'Gano la maquina', 1, (0, 0, 0))
					screen.blit(mensaje, (250, 0))
					pygame.display.flip()
					time.sleep(5)
					pygame.quit()
			#actualizacion de los frames en pantalla

			for i in range(len(data[0])):

				screen.blit(dadosP_pantalla[str(data[0][i])], dadosP_rec[str(data[0][i])])

			screen.blit(dados_juego[str(torso[0][0])],dadosJ_rec[str(torso[0][0])])
			for i in torso:
				print(i[0])
				screen.blit(dados_juego[str(i[0])],dadosJ_rec[str(i[0])])
			if turno == 0:
				mensaje = fuente.render(f'Turno del jugador/ fichas pozo {len(data[2])} / fichas de jugador {len(data[0])} \n Fichas maquina {len(data[1])}', 1, (0, 0, 0))
				screen.blit(mensaje, (100, 10))
			else:
				mensaje = fuente.render(f'Turno de la maquina/ fichas {len(data[1])}', 1, (0, 0, 0))
				screen.blit(mensaje, (250, 10))
		pygame.display.flip()
	# Salgo de pygame
	pygame.quit()

ventana()