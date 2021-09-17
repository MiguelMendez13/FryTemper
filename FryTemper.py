import wx
import wx.adv
import threading
import multiprocessing
import time
import os
import sys
from os import system
import requests
import win32ui
import win32gui
import win32con
import win32api
from wx.core import FNTP_DEFAULT_STYLE
from procesosAparte import scale_bitmap,imagenIco,VerificarProcesos,TaskBarIcon
import servidor
path=os.path.split(__file__)[0]+"/"
import socket



	
def actualizarLista(lista_mostrar,primerlista):
	primerlista.clear()
	listn=VerificarProcesos()
	for x in listn:
		primerlista.append(x)
	lista_mostrar.DeleteAllItems()
	for fila in primerlista:
		#	print(fila)
		lista_mostrar.InsertItem(fila[0], str(fila[0]))
		lista_mostrar.SetItem(fila[0], 1, str(fila[1]))
		lista_mostrar.SetItem(fila[0], 2, str(fila[3]))
		lista_mostrar.SetItem(fila[0], 3, str(fila[-1]))

		lista_mostrar.SetItemData(fila[0], fila[0])




def actualizarHora(listaWxTareas,tareaslist,primerlista,lista_mostrar):
	#system("taskkill /F /PID "+xi[0])

	while  True:
		contador=0
		
		for x in tareaslist:
			if(x[1]==0 and x[2]==0 and x[3]==0):
				tareaslist.pop(contador)
				listaWxTareas.DeleteItem(contador)
				if(x[0]=="AutoCerrar"):
					os._exit(0)
				else:
					system("taskkill /F /PID "+x[0])
				actualizarLista(lista_mostrar,primerlista)
			contador+=1
		
			
		for x in tareaslist:
			if (x[3]==0 and x[2]==0 and x[1]==0):
				print("acabo: "+x[0])
				

			elif (x[2]!=0 and x[3]==0):
				x[2]-=1
				x[3]=59
		
			elif(x[1]!=0 and x[2]==0):
				x[1]-=1
				x[2]=60
			else:
				x[3]-=1

		for x in range(0,len(tareaslist)):

			listaWxTareas.SetItem(x, 1, str(tareaslist[x][1]))
			listaWxTareas.SetItem(x, 2, str(tareaslist[x][2]))
			listaWxTareas.SetItem(x, 3, str(tareaslist[x][3]))
		time.sleep(1)
		#print("\n\n")

class ingTiempo(wx.Dialog):
	def __init__(self,main,lista):
		self.lista = lista
		self.main=main
		wx.Dialog.__init__(self,main, title="Tiempo", size=(230,200))
		self.sec=0
		panel = wx.Panel(self, -1)

		self.nombre=wx.StaticText(panel, label="Id: "+str(lista[0])+" Nombre: "+lista[1],pos=wx.Point(0,20),size=wx.Size(230,30),style = wx.ALIGN_CENTER)
		font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL) 
		self.nombre.SetFont(font)

		boton=wx.Button(panel, label="Agregar",pos=wx.Point(75,130), size=wx.Size(60,30))
		
		self.lssegundos= [str(x2) for x2 in [x for x in range(0,60)]]
		self.lsminutos= [str(x2) for x2 in [x for x in range(0,60)]]
		self.lshoras= [str(x2) for x2 in [x for x in range(0,24)]]

		txt1=wx.StaticText(panel, label="Horas",pos=wx.Point(0,70),size=wx.Size(70,30),style = wx.ALIGN_CENTER)		
		txt2=wx.StaticText(panel, label="Minutos",pos=wx.Point(70,70),size=wx.Size(70,30),style = wx.ALIGN_CENTER)
		txt3=wx.StaticText(panel, label="Segundos",pos=wx.Point(140,70),size=wx.Size(70,30),style = wx.ALIGN_CENTER)
		txt1.SetFont(font)
		txt2.SetFont(font)
		txt3.SetFont(font)

		self.hrs = wx.Choice(panel, wx.ID_ANY, choices=self.lshoras,pos=wx.Point(10,100),size=wx.Size(50,30))
		self.min = wx.Choice(panel, wx.ID_ANY, choices=self.lsminutos,pos=wx.Point(80,100),size=wx.Size(50,30))
		self.seg = wx.Choice(panel, wx.ID_ANY, choices=self.lssegundos,pos=wx.Point(150,100),size=wx.Size(50,30))


		self.hrs.SetSelection(0)
		self.min.SetSelection(0)
		self.seg.SetSelection(0)


		self.Bind(wx.EVT_CLOSE, self.cerrar)
		boton.Bind(wx.EVT_BUTTON, self.agregar)
		
	def cerrar(self,event):		
		self.Destroy()

	def regresar(self):
		return(self.sec)

	def agregar(self,event):
		hors=str(self.lshoras[self.hrs.GetSelection()])
		mns=str(self.lsminutos[self.min.GetSelection()])
		segg=str(self.lssegundos[self.seg.GetSelection()])
		

		verifi = [x[0] for x in  self.main.tareaslist]
		
		#print("Nombre: "+self.lista[1]+" Horas: "+hors+" Minutos: "+mns+" Segundos: "+segg)
		self.main.tareas.InsertItem(len(self.main.tareaslist),self.lista[1])
		self.main.tareas.SetItem(len(self.main.tareaslist), 1, hors)
		self.main.tareas.SetItem(len(self.main.tareaslist), 2, mns)
		self.main.tareas.SetItem(len(self.main.tareaslist), 3, segg)

		self.main.tareas.SetItemData(len(self.main.tareaslist), len(self.main.tareaslist))
		self.main.tareaslist.append([self.lista[1],int(hors),int(mns),int(segg)])
		

		self.Destroy()
		self.sec = 1



class entrada(wx.Frame):
	def __init__(self,primerlista,path):
		self.tareaslist=[]
		self.primerlista = primerlista
		self.path=path
		self.servidor=[]

		wx.Frame.__init__(self,None,-1,title="FryTemper V1.0",style=wx.MINIMIZE_BOX 
			| wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,pos=wx.Point(80,10),size=wx.Size(600,500))
		self.cab = 0

		self.scroll = wx.Panel(self, -1)
		#self.scroll.SetScrollbars(1, 1, 500, 400)

		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		fileMenu2 = wx.Menu()
		fileMenu3 = wx.Menu()


		self.nombre=wx.StaticText(self.scroll, label="Nombre",pos=wx.Point(50,20),size=wx.Size(500,30),style = wx.ALIGN_CENTER)
		font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL) 
		self.nombre.SetFont(font)

		self.icono=wx.StaticBitmap(self.scroll, -1, pos=wx.Point(250,50),size=wx.Size(80,80))
		bit=wx.Bitmap(path+"error.bmp",wx.BITMAP_TYPE_BMP)
		bits=scale_bitmap(bit,80,80)

		self.icono.SetBitmap(bits)

		self.lista_mostrar = wx.ListCtrl(self.scroll, pos=wx.Point(10,200),size=wx.Size(565,250)
		,style=wx.LC_REPORT|wx.BORDER_SUNKEN|wx.LC_HRULES|wx.LC_VRULES )
		self.lista_mostrar.InsertColumn(0, "ID", width=30)
		self.lista_mostrar.InsertColumn(1, "Nombre de Aplicacion/Servicio", width=250)
		self.lista_mostrar.InsertColumn(2, "Nombre de sesión", width=149)
		self.lista_mostrar.InsertColumn(3, "Uso de memoria", width=115)
	
		self.tareas = wx.ListCtrl(self.scroll, pos=wx.Point(360,50),size=wx.Size(200,100)
		,style=wx.LC_REPORT|wx.BORDER_SUNKEN|wx.LC_HRULES|wx.LC_VRULES )
		self.tareas.InsertColumn(0, "Nombre", width=100)
		self.tareas.InsertColumn(1, "Hrs", width=33)
		self.tareas.InsertColumn(2, "Mts", width=34)
		self.tareas.InsertColumn(3, "Seg", width=33)

		boton2=wx.Button(self.scroll, label="Actualizar lista",pos=wx.Point(50,60), size=wx.Size(100,30))
		boton=wx.Button(self.scroll, label="AutoClose",pos=wx.Point(60,100), size=wx.Size(80,30))
		self.Bind(wx.EVT_ICONIZE, self.Minimizar)

		self.servidorcheck=wx.CheckBox(self.scroll, label="Servidor",pos=wx.Point(40,140),size=wx.Size(90,30))
		self.iptexto=wx.StaticText(self.scroll, label="IP: ***.***.***.***",pos=wx.Point(130,145),size=wx.Size(100,20),style = wx.ALIGN_CENTER)
		self.puertotexto=wx.StaticText(self.scroll, label="Puerto: 000000",pos=wx.Point(130,165),size=wx.Size(100,20),style = wx.ALIGN_CENTER)
		
		font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		self.puertotexto.SetFont(font)
		self.iptexto.SetFont(font)
		
		for fila in primerlista:
			#	print(fila)
			self.lista_mostrar.InsertItem(fila[0], str(fila[0]))
			self.lista_mostrar.SetItem(fila[0], 1, str(fila[1]))
			self.lista_mostrar.SetItem(fila[0], 2, str(fila[2]))
			self.lista_mostrar.SetItem(fila[0], 3, str(fila[3]))

			self.lista_mostrar.SetItemData(fila[0], fila[0])


		self.lista_mostrar.Bind(wx.EVT_LIST_COL_CLICK, self.press3)
		self.lista_mostrar.Bind(wx.EVT_LIST_ITEM_SELECTED, self.press)
		self.lista_mostrar.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.press2)
		self.tareas.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.borrar)
		

		self.servidorcheck.Bind(wx.EVT_CHECKBOX,self.activarSer)


		boton.Bind(wx.EVT_BUTTON, self.autoClose)
		boton2.Bind(wx.EVT_BUTTON, self.actualizar)
		self.Bind(wx.EVT_CLOSE, self.closee)



		
		self.actualizando = threading.Thread(target=actualizarHora, args=(self.tareas,self.tareaslist,self.primerlista,self.lista_mostrar,))
		self.actualizando.start()
		self.Show(True)

	def activarSer(self,event):
		if self.servidorcheck.GetValue()==True:
			self.servidor.append(threading.Thread(target=servidor.Servidor, args=(self,)))
			self.servidor[len(self.servidor)-1].start()
		else:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_address = ('192.168.0.3', 10000)
			sock.connect(server_address)
			message = b'CerrarServer--'
			sock.send(message)
			sock.close()
			self.servidor[len(self.servidor)-1].join()
			self.servidor.pop(len(self.servidor)-1)
			self.iptexto.SetLabel("IP: ***.***.***.***")
			self.puertotexto.SetLabel("Puerto: 000000")
			print("cerrado servidor")
		
	def borrar(self,event):
		#print(event.GetIndex())
		resp=wx.MessageDialog(self,"Estas seguro de borar",caption="Borar",style=wx.YES_NO | wx.CANCEL).ShowModal()
		if resp==wx.ID_YES:
			self.tareaslist.pop(event.GetIndex())
			self.tareas.DeleteItem(event.GetIndex())


	def press3(self,event):

		if(event.GetColumn()==1):
			listaa ={x[1].lower():x[0] for x in self.primerlista}
			listaa2=sorted(listaa)
			self.lista_mostrar.DeleteAllItems()
			contador=0
			for fil in listaa2:
				fila=primerlista[listaa[fil]]
				#print(fila)
				self.lista_mostrar.InsertItem(contador, str(fila[0]))
				self.lista_mostrar.SetItem(contador, 1, str(fila[1]))
				self.lista_mostrar.SetItem(contador, 2, str(fila[3]))
				self.lista_mostrar.SetItem(contador, 3, str(fila[-1]))
				self.lista_mostrar.SetItemData(contador, contador)
				contador+=1
		if(event.GetColumn()==0):
			self.lista_mostrar.DeleteAllItems()
			for fila in primerlista:
			#	print(fila)
				self.lista_mostrar.InsertItem(fila[0], str(fila[0]))
				self.lista_mostrar.SetItem(fila[0], 1, str(fila[1]))
				self.lista_mostrar.SetItem(fila[0], 2, str(fila[3]))
				self.lista_mostrar.SetItem(fila[0], 3, str(fila[-1]))

				self.lista_mostrar.SetItemData(fila[0], fila[0])

	def press(self, event):
		#print(event.GetText())
		self.nombre.SetLabel(str("Id: "+ str(self.primerlista[int(event.GetText())][0])+"  "+self.primerlista[int(event.GetText())][1]))
		
		icono = imagenIco(self.primerlista[int(event.GetText())][1],path)
		#print(dir(self.lista_mostrar))
		#print("press "+event.GetText())
		bit=wx.Bitmap(path+icono,wx.BITMAP_TYPE_BMP)
		bits=scale_bitmap(bit,80,80)
		self.icono.SetBitmap(bits)

	def press2(self, event):
		verifi = [x[0] for x in  self.tareaslist]
		lista=self.primerlista[int(event.GetText())]
		if lista[1] in verifi:
			print("Ya existe")
		else:
			preguntiempo = ingTiempo(self,lista)
			nuev = preguntiempo.ShowModal()
			
		#print(preguntiempo.regresar())



	def closee(self,event):
		os._exit(0)
		#system("taskkill /F /PID python.exe")
	def autoClose(self,event):
		verifi = [x[0] for x in  self.tareaslist]
		lista=[1001001, 'AutoCerrar', '916', 'Services', '0', '1', '10101 KB']
		if lista[1] in verifi:
			print("Ya existe")
		else:
			preguntiempo = ingTiempo(self,lista)
			nuev = preguntiempo.ShowModal()
		

	def Minimizar(self, event):
		
		self.TaskBarIcon = TaskBarIcon(self,path)
		self.Hide()

	def actualizar(self,event):
		self.lista_mostrar
		self.primerlista
		lol=actualizarLista(self.lista_mostrar,self.primerlista)

		


if __name__ == '__main__':
	primerlista=VerificarProcesos()
	app = wx.App()
	entra = entrada(primerlista,path)
	app.MainLoop()