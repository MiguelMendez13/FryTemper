import wx
import wx.adv
import threading
import time
import os
import sys
from os import system
import requests
import win32ui
import win32gui
import win32con
import win32api


path=os.path.split(__file__)[0]+"/"
print(path)
def scale_bitmap(bitmap, width, height):
	image = wx.Bitmap.ConvertToImage(bitmap)
	image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
	result = wx.Bitmap(image)
	return result


def imagenIco(imagen,pathc):
	imagen=imagen.replace(".exe","")
	cadena="powershell (Get-Process "+imagen+").path"
	imgg=""
	#print(cadena)
	ruta=os.popen(cadena).read().split("\n")[0]

	if(ruta=="\n" or ruta==""):
		imgg="error.bmp"
		#print("salto")
	else:
		try:
			ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
			

			large, small = win32gui.ExtractIconEx(ruta,0)
			win32gui.DestroyIcon(small[0])

			hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
			hbmp = win32ui.CreateBitmap()
			hbmp.CreateCompatibleBitmap( hdc, ico_x, ico_x )
			hdc = hdc.CreateCompatibleDC()

			hdc.SelectObject( hbmp )
			hdc.DrawIcon( (0,0), large[0] )

			hbmp.SaveBitmapFile( hdc, path+'icon.bmp')
			imgg="icon.bmp"
		except Exception as e:
			imgg="error.bmp"
	#print(ruta)
	return(imgg)

def VerificarProcesos():
	salida4 = os.popen("tasklist /FO CSV").read().split("\n")
	lista=[]
	listanombres=[]
	lol=0
	id=0
	ultimo=salida4[-1]
	#print(len(salida4))
	for x in salida4:
		if(lol==0 or lol==1 or lol==2 or lol==3):
			pass
		else:
			if("svchost.exe" in x):
				pass
			else:
				if(x==ultimo):
					pass
				elif("python.exe" in x):
					pass
				else:
					listatemp=str(x).replace('"', "").split(",")

					if(listatemp[0] in listanombres):
						pass
					else:
						listanombres.append(listatemp[0])
						lista.append([id,listatemp[0],listatemp[1],listatemp[2],listatemp[3],listatemp[4],listatemp[-1]])
						id+=1
			
				pass
		lol=lol+1
#	print(lista)
	return(lista)

def terminar(tareaslist,contar,listaWxTareas):
	pass
	#tareaslist.pop(contar)
	#listaWxTareas.DeleteItem(contar)
	

def hora(xi,listaWxTareas,tareaslist,primerlista,contar):
	hora=int(xi[1])+1
	minu=int(xi[2])+1
	segu=int(xi[3])

	for x in range(hora,0,-1):
		listaWxTareas.SetItem(contar, 1, str(x-1))
		for x2 in range(minu,0,-1):
			listaWxTareas.SetItem(contar, 2, str(x2-1))
			for x3 in range(segu,0,-1):
				listaWxTareas.SetItem(contar, 3, str(x3))
				time.sleep(1)
			
			segu=60
		if(hora==1):
			pass
		else:
			minu=60

	#print("Finish")
	listaWxTareas.SetItem(contar, 3, str(0))
	#	print("exit")
	system("taskkill /F /PID "+xi[0])
	#terminar(tareaslist,contar,listaWxTareas)


def actualizarHora(listaWxTareas,tareaslist,hiloTareas,primerlista):
	contar=len(tareaslist)


	while  True:
		if(len(tareaslist) > contar):
			
			hiloTareas.append(threading.Thread(target=hora, args=(tareaslist[-1],listaWxTareas,tareaslist,primerlista,contar,)))
			hiloTareas[contar].start()
		#hiloTareas[contar].join()
		#hiloTareas.pop(contar)
		#print("Detenido")

		"""print(len(tareaslist))
			print(contador)
			contar=0
			hiloTareas.clear()
			print("Tarealist:")
			print(tareaslist)
			
			for xi in tareaslist:
				print("xi:")
				print(xi)
				hiloTareas.append(threading.Thread(target=hora, args=(xi,listaWxTareas,tareaslist,primerlista,contar,)))
				hiloTareas[contar].start()
				contar+=1
			print(hiloTareas)
			"""
		contar=len(tareaslist)
		time.sleep(.01)
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
		self.main.tareaslist.append([self.lista[1],hors,mns,segg])
		

		self.Destroy()
		self.sec = 1



class entrada(wx.Frame):
	def __init__(self,primerlista,path):
		self.tareaslist=[]
		self.hiloTareas=[]
		self.primerlista = primerlista
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

		boton=wx.Button(self.scroll, label="AutoClose",pos=wx.Point(75,130), size=wx.Size(80,30))

		for fila in primerlista:
			#	print(fila)
			self.lista_mostrar.InsertItem(fila[0], str(fila[0]))
			self.lista_mostrar.SetItem(fila[0], 1, str(fila[1]))
			self.lista_mostrar.SetItem(fila[0], 2, str(fila[3]))
			self.lista_mostrar.SetItem(fila[0], 3, str(fila[-1]))

			self.lista_mostrar.SetItemData(fila[0], fila[0])

		self.actualizando = threading.Thread(target=actualizarHora, args=(self.tareas,self.tareaslist,self.hiloTareas,self.primerlista,))
		self.actualizando.start()


		self.lista_mostrar.Bind(wx.EVT_LIST_COL_CLICK, self.press3)
		self.lista_mostrar.Bind(wx.EVT_LIST_ITEM_SELECTED, self.press)
		self.lista_mostrar.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.press2)
		boton.Bind(wx.EVT_BUTTON, self.autoClose)

		self.Show(True)

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
	def autoClose(self,event):
		lista=[1001001, 'python.exe', '916', 'Services', '0', '1', '10101 KB']
		preguntiempo = ingTiempo(self,lista)
		nuev = preguntiempo.ShowModal()
if __name__ == '__main__':
	primerlista=VerificarProcesos()
	app = wx.App()
	entra = entrada(primerlista,path)
	app.MainLoop()