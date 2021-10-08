import os
import sys
from os import system
import requests
import win32ui
import win32gui
import win32con
import win32api
import wx

import wx.adv

Titulopoput = 'FryShopScraper'
TRAY_ICON = 'icon_31.gif'

def RegresaIP():
	salida4 = os.popen("ipconfig").read().split("Adaptador")
	ipsalir=salida4[1].split("IPv4.")[1].split("\n")[0].split(": ")[1]
	return(ipsalir)



def scale_bitmap(bitmap, width, height):
	image = wx.Bitmap.ConvertToImage(bitmap)
	image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
	result = wx.Bitmap(image)
	return result


def imagenIco(imagen,path):
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
	listaDefi=[]
	for i in lista:
		listaDefi.append([i[0],i[1],i[3],i[-1]])

#	print(lista)
	return(listaDefi)



def create_menu_item(menu, label, func):
	item = wx.MenuItem(menu, -1, label)
	menu.Bind(wx.EVT_MENU, func, id=item.GetId())
	menu.Append(item)
	return item

class TaskBarIcon(wx.adv.TaskBarIcon):
	def __init__(self, frame,path):
		self.frame = frame
		super(TaskBarIcon, self).__init__()
		self.set_icon(TRAY_ICON)
		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.click_derecho)

	def CreatePopupMenu(self):
		menu = wx.Menu()
		create_menu_item(menu, 'Abrir', self.abrir)
		menu.AppendSeparator()
		create_menu_item(menu, 'Salir', self.salirr)
		return menu

	def set_icon(self, path):
		icon = wx.Icon(wx.Bitmap(path))
		self.SetIcon(icon, Titulopoput)

	def click_derecho(self, event):
		self.frame.Show(True)
		self.Destroy()

	def abrir(self, event):
		self.frame.Show(True)
		self.Destroy()
	
	def salirr(self, event):
		wx.CallAfter(self.Destroy)
		self.frame.Close()
		os._exit(1)