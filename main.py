
import xbmcplugin
import xbmcgui
import sys
import requests
import json
import resolveurl as urlresolver
import tmdb

#Obtiene el handle del plugin (ID nico para el addon)
HANDLE = int(sys.argv[1])
api_key = tmdb.api_key
ide_serie = 918
fanArt = "https://upload.wikimedia.org/wikipedia/en/b/b9/M%2AA%2AS%2AH_TV_title_screen.jpg"
poster = "https://image.tmdb.org/t/p/original/mpxGTA1DWVn4Lx8entsDePv9ICU.jpg"
icon = "https://cdn.icon-icons.com/icons2/4134/PNG/96/audio_video_media_control_resume_plain_icon_260667.png"


def get_params():
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
				params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
				splitparams={}
				splitparams=pairsofparams[i].split('=')
				if (len(splitparams))==2:
					param[splitparams[0]]=splitparams[1]
		return param

def play_video(path):
	hmf = urlresolver.HostedMediaFile(url=path)
	stream_url = hmf.resolve()
	play_item = xbmcgui.ListItem(offscreen=True)
	play_item.setPath(stream_url)
	xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)

#Funcion para mostrar el menu principalsys.argv[2]
def crear_menu_pelis():
			r = requests.get("http://146.190.143.193:5001/menu_pelis")
			datos = r.text
			data = json.loads(datos)
			cont = 0
			for item in data:
				title = data[cont][0]
				mode = data[cont][1]
				thumbnail = data[cont][2]
				fanart = data[cont][3]
				desc = "" 
				#desc = tmdb.traer_desc_serie(ide_serie,api_key)
				url = "http://prueba.com" 
				if thumbnail == "":
					thumbnail = poster
				if fanart == "":
				   fanart = fanArt     
				year = "2000"
				genre = ""             
				add_item( mode , title  , desc  , url  , thumbnail  , fanart  , year , genre , False , True )
				cont = cont + 1
			xbmcplugin.endOfDirectory(HANDLE)

#Funcion para mostrar el menu drama
def crear_menu_drama():
			r = requests.get("http://146.190.143.193:5001/menu_drama")
			datos = r.text
			data = json.loads(datos)
			cont = 0
			for item in data:
				title = data[cont][0]
				url = data[cont][1]
				thumbnail = data[cont][2]
				fanart = data[cont][3]
				mode = data[cont][4]
				year = data[cont][6]
				genre = data[cont][7]
				id_tmdb = data[cont][8]
				desc = data[cont][9]
				#infopeli = tmdb.traer_infopeli(id_tmdb , api_key)
				#genre = tmdb.traer_genre(infopeli)
				#desc = infopeli['overview']
				#fan_art = infopeli['backdrop_path']
				#fanart = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+fan_art
				#thumb_nail = infopeli['poster_path']
				#thumbnail = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+thumb_nail
				add_item( mode , title  , desc  , url  , thumbnail  , fanart  , year , genre , True , False )
				cont = cont + 1
			xbmcplugin.endOfDirectory(HANDLE)

#Funcion para mostrar el menu terror
def crear_menu_terror():
			r = requests.get("http://146.190.143.193:5001/menu_terror")
			datos = r.text
			data = json.loads(datos)
			cont = 0
			for item in data:
				title = data[cont][0]
				url = data[cont][1]
				thumbnail = data[cont][2]
				fanart = data[cont][3]
				mode = data[cont][4]
				year = data[cont][6]
				genre = data[cont][7]
				id_tmdb = data[cont][8]
				desc = data[cont][9]
				#infopeli = tmdb.traer_infopeli(id_tmdb , api_key)
				#genre = tmdb.traer_genre(infopeli)
				#desc = infopeli['overview']
				#fan_art = infopeli['backdrop_path']
				#fanart = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+fan_art
				#thumb_nail = infopeli['poster_path']
				#thumbnail = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+thumb_nail
				add_item( mode , title  , desc  , url  , thumbnail  , fanart  , year , genre , True , False )
				cont = cont + 1
			xbmcplugin.endOfDirectory(HANDLE)

#Funcion para mostrar el menu accion
def crear_menu_accion():
			r = requests.get("http://146.190.143.193:5001/menu_accion")
			datos = r.text
			data = json.loads(datos)
			cont = 0
			for item in data:
				title = data[cont][0]
				url = data[cont][1]
				thumbnail = data[cont][2]
				fanart = data[cont][3]
				mode = data[cont][4]
				year = data[cont][6]
				genre = data[cont][7]
				id_tmdb = data[cont][8]
				desc = data[cont][9]
				#infopeli = tmdb.traer_infopeli(id_tmdb , api_key)
				#genre = tmdb.traer_genre(infopeli)
				#desc = infopeli['overview']
				#fan_art = infopeli['backdrop_path']
				#fanart = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+fan_art
				#thumb_nail = infopeli['poster_path']
				#thumbnail = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+thumb_nail
				add_item( mode , title  , desc  , url  , thumbnail  , fanart  , year , genre , True , False )
				cont = cont + 1
			xbmcplugin.endOfDirectory(HANDLE)

#Funcion para mostrar el menu comedia
def crear_menu_comedia():
			r = requests.get("http://146.190.143.193:5001/menu_comedia")
			datos = r.text
			data = json.loads(datos)
			cont = 0
			for item in data:
				title = data[cont][0]
				url = data[cont][1]
				thumbnail = data[cont][2]
				fanart = data[cont][3]
				mode = data[cont][4]
				year = data[cont][6]
				genre = data[cont][7]
				id_tmdb = data[cont][8]
				desc = data[cont][9]
				#infopeli = tmdb.traer_infopeli(id_tmdb , api_key)
				#genre = tmdb.traer_genre(infopeli)
				#desc = infopeli['overview']
				#fan_art = infopeli['backdrop_path']
				#fanart = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+fan_art
				#thumb_nail = infopeli['poster_path']
				#thumbnail = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+thumb_nail
				add_item( mode , title  , desc  , url  , thumbnail  , fanart  , year , genre , True , False )
				cont = cont + 1
			xbmcplugin.endOfDirectory(HANDLE)

def crear_menu_western():
			r = requests.get("http://146.190.143.193:5001/menu_western")
			datos = r.text
			data = json.loads(datos)
			cont = 0
			for item in data:
				title = data[cont][0]
				url = data[cont][1]
				thumbnail = data[cont][2]
				fanart = data[cont][3]
				mode = data[cont][4]
				year = data[cont][6]
				genre = data[cont][7]
				id_tmdb = data[cont][8]
				desc = data[cont][9]
				#infopeli = tmdb.traer_infopeli(id_tmdb , api_key)
				#genre = tmdb.traer_genre(infopeli)
				#desc = infopeli['overview']
				#fan_art = infopeli['backdrop_path']
				#fanart = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+fan_art
				#thumb_nail = infopeli['poster_path']
				#thumbnail = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+thumb_nail
				add_item( mode , title  , desc  , url  , thumbnail  , fanart  , year , genre , True , False )
				cont = cont + 1
			xbmcplugin.endOfDirectory(HANDLE)

def crear_menu_fantasia():
			r = requests.get("http://146.190.143.193:5001/menu_fantasia")
			datos = r.text
			data = json.loads(datos)
			cont = 0
			for item in data:
				title = data[cont][0]
				url = data[cont][1]
				thumbnail = data[cont][2]
				fanart = data[cont][3]
				mode = data[cont][4]
				year = data[cont][6]
				genre = data[cont][7]
				id_tmdb = data[cont][8]
				desc = data[cont][9]
				#infopeli = tmdb.traer_infopeli(id_tmdb , api_key)
				#genre = tmdb.traer_genre(infopeli)
				#desc = infopeli['overview']
				#fan_art = infopeli['backdrop_path']
				#fanart = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+fan_art
				#thumb_nail = infopeli['poster_path']
				#thumbnail = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+thumb_nail
				add_item( mode , title  , desc  , url  , thumbnail  , fanart  , year , genre , True , False )
				cont = cont + 1
			xbmcplugin.endOfDirectory(HANDLE)

def crear_menu_ciencia_ficcion():
			r = requests.get("http://146.190.143.193:5001/menu_ciencia_ficcion")
			datos = r.text
			data = json.loads(datos)
			cont = 0
			for item in data:
				title = data[cont][0]
				url = data[cont][1]
				thumbnail = data[cont][2]
				fanart = data[cont][3]
				mode = data[cont][4]
				year = data[cont][6]
				genre = data[cont][7]
				id_tmdb = data[cont][8]
				desc = data[cont][9]
				#infopeli = tmdb.traer_infopeli(id_tmdb , api_key)
				#genre = tmdb.traer_genre(infopeli)
				#desc = infopeli['overview']
				#fan_art = infopeli['backdrop_path']
				#fanart = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+fan_art
				#thumb_nail = infopeli['poster_path']
				#thumbnail = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+thumb_nail
				add_item( mode , title  , desc  , url  , thumbnail  , fanart  , year , genre , True , False )
				cont = cont + 1
			xbmcplugin.endOfDirectory(HANDLE)
 
def crear_menu_artes_marciales():
			r = requests.get("http://146.190.143.193:5001/menu_artes_marciales")
			datos = r.text
			data = json.loads(datos)
			cont = 0
			for item in data:
				title = data[cont][0]
				url = data[cont][1]
				thumbnail = data[cont][2]
				fanart = data[cont][3]
				mode = data[cont][4]
				year = data[cont][6]
				genre = data[cont][7]
				id_tmdb = data[cont][8]
				desc = data[cont][9]
				#infopeli = tmdb.traer_infopeli(id_tmdb , api_key)
				#genre = tmdb.traer_genre(infopeli)
				#desc = infopeli['overview']
				#fan_art = infopeli['backdrop_path']
				#fanart = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+fan_art
				#thumb_nail = infopeli['poster_path']
				#thumbnail = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+thumb_nail
				add_item( mode , title  , desc  , url  , thumbnail  , fanart  , year , genre , True , False )
				cont = cont + 1
			xbmcplugin.endOfDirectory(HANDLE)

def crear_menu_romance():
			r = requests.get("http://146.190.143.193:5001/menu_romance")
			datos = r.text
			data = json.loads(datos)
			cont = 0
			for item in data:
				title = data[cont][0]
				url = data[cont][1]
				thumbnail = data[cont][2]
				fanart = data[cont][3]
				mode = data[cont][4]
				year = data[cont][6]
				genre = data[cont][7]
				id_tmdb = data[cont][8]
				desc = data[cont][9]
				#infopeli = tmdb.traer_infopeli(id_tmdb , api_key)
				#genre = tmdb.traer_genre(infopeli)
				#desc = infopeli['overview']
				#fan_art = infopeli['backdrop_path']
				#fanart = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+fan_art
				#thumb_nail = infopeli['poster_path']
				#thumbnail = "https://image.tmdb.org/t/p/w600_and_h900_bestv2"+thumb_nail
				add_item( mode , title  , desc  , url  , thumbnail  , fanart  , year , genre , True , False )
				cont = cont + 1
			xbmcplugin.endOfDirectory(HANDLE)

#Funcin para agregar una opcion a los menus           
def add_item(mode="",title="",desc="",url="",thumbnail="",fanart="",year ="",genre="", isPlayable = False , folder=True ):
	
	genero = []
	anio = int(year)
	date = anio
	xbmcplugin.setContent(HANDLE, 'movies')
	listitem = xbmcgui.ListItem(title)
	icon = thumbnail
	poster = thumbnail
	#info_labels = { "Title" : title, "FileName" : title, "Plot" : desc }
	#listitem.setInfo( "video", info_labels )
	listitem.setArt({"icon": icon , "poster" : poster , "fanart" : fanart})
	info_tag = listitem.getVideoInfoTag()
	info_tag.setMediaType('movie')
	info_tag.setTitle(title)
	info_tag.setGenres(genero)
	info_tag.setPlot(desc)
	info_tag.setYear(date)

	if isPlayable:
		listitem.setProperty("Video", "true")
		listitem.setProperty('IsPlayable', 'true')
		# Example: plugin://plugin.video.example/?action=play&video=https%3A%2F%2Fia600702.us.archive.org%2F3%2Fitems%2Firon_mask%2Firon_mask_512kb.mp4
		itemurl = '%s?mode=%s&url=%s&title=%s&thumbnail=%s&desc=%s&fanart=%s' % ( sys.argv[ 0 ] , mode ,  url , title ,thumbnail , desc , fanart)
		xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)
	else:
		# Example: plugin://plugin.video.example/?action=play&video=https%3A%2F%2Fia600702.us.archive.org%2F3%2Fitems%2Firon_mask%2Firon_mask_512kb.mp4
		itemurl = '%s?mode=%s&url=%s&title=%s&thumbnail=%s&desc=%s&fanart=%s' % (sys.argv[ 0 ] , mode ,  url , title ,thumbnail , desc , fanart)
		xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)


#Logica principal se ejecuta al dar clik en alguna opcion de los menus
params = get_params()
try:
	action = params["mode"]
except:
	pass 

try:
	url = params["url"]
	url = url.replace("%3a",":")
	url = url.replace("%2f","/")
except:
	pass

try:
	message = mode
except:
	message = "Inicio del Programa"


if not params:
	crear_menu_pelis()
elif(action == "cmenudrama"):
	crear_menu_drama()
elif(action == "cmenuterror"):
	crear_menu_terror()
elif(action == "cmenucomedia"):
	crear_menu_comedia()   
elif(action == "cmenuaccion"):
	crear_menu_accion()   
elif(action == "cmenuwestern"):
	crear_menu_western()   
elif(action == "cmenufantasia"):
	crear_menu_fantasia()
elif(action == "cmenucienciaficcion"):
	crear_menu_ciencia_ficcion()
elif(action == "cmenuartesmarciales"):
	crear_menu_artes_marciales()
elif(action == "cmenuromance"):
	crear_menu_romance()
elif(action == "play"):
	play_video(url)