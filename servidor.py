import socket
import sys
import time
from procesosAparte import RegresaIP
def Servidor(main):

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	puerto=10000
	#address= str(socket.gethostbyname(socket.gethostname()))
	


	address=RegresaIP()



	server_address = (address, puerto)
	print('starting up on {} port {}'.format(*server_address))
	sock.bind(server_address)

	# Listen for incoming connections
	sock.listen(3)
	main.iptexto.SetLabel("IP: "+address)
	main.puertotexto.SetLabel("Puerto: "+str(puerto))
	while True:
		# Wait for a connection
		#print('waiting for a connection')
		connection, client_address = sock.accept()
		try:
			data = connection.recv(1024)
			datastr=data.decode('utf-8')
			#print(datastr)
			if datastr =="":
				pass
				#print('sending data back to the client')
				connection.send(data)


			elif "Add: " in datastr:
				respuesta=""
				#Add: lol.exe 3 2 1 
				cadena =datastr.split(" ")
				lol = [x[0] for x in main.tareaslist]

				if cadena[1] in lol:
					respuesta="Ya se encuentra en lista este programa"
				else:
					main.tareas.InsertItem(len(main.tareaslist),cadena[1])
					main.tareas.SetItem(len(main.tareaslist), 1, cadena[2])
					main.tareas.SetItem(len(main.tareaslist), 2, cadena[3])
					main.tareas.SetItem(len(main.tareaslist), 3, cadena[4])

					main.tareas.SetItemData(len(main.tareaslist), len(main.tareaslist))
					main.tareaslist.append([cadena[1],int(cadena[2]),int(cadena[3]),int(cadena[4])])
					respuesta="Se a agregado a lista este programa"

				connection.send(respuesta.encode())


			elif "TList--" == datastr:
				enviar=""
				if len(main.tareaslist)==0:
					enviar="***:"
					
				else:
					for i in main.tareaslist:
						enviar=enviar+str(i[0])+"-"+str(i[1])+"-"+str(i[2])+"-"+str(i[3])+":"	
				datos=enviar
				connection.send(datos.encode())
			

			elif "ListEjec--"== datastr:
				enviar=""
				listate=[]
				for i in main.primerlista:
					listate.append(str(i[1])+" ID- "+str(i[0])+":")
					
				listateI=sorted(listate)
				for i in listateI:
					enviar=enviar+i
				datos=enviar
				connection.send(datos.encode())


			elif "CerrarServer--"== datastr:
				connection.close()
				break

			
			elif "Delete--" in datastr:
				item = int(datastr.split(" ")[1])
				main.tareaslist.pop(item)
				main.tareas.DeleteItem(item)
				datos="Borrado con exito"
				connection.send(datos.encode())
			else:
				datos="Hola: "+str(client_address[0])
				connection.send(datos.encode())
				print(type(client_address))
				print('no data from', client_address)
				
			

		finally:
			# Clean up the connection
			connection.close()


