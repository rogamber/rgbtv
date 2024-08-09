# -*- coding: utf-8 -*-
import xbmc
import sys
import urllib
import urllib2
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import traceback
import requests
import cookielib,base64
import tmdb
import plugintools
import resolveurl as urlresolver
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
viewmode=None
api_key="2cd2538742da5dcb2d3e0a381a537689&language=es-ES"
link = "http://68.183.120.13"
FANART = "http://rgbtv.net/img/kodi.jpg"
THUMBNAIL = "http://rgbtv.net/img/rgbtv.jpg"
try:
	from xml.sax.saxutils import escape
except: traceback.print_exc()
try:
	import json
except:
	import simplejson as json
import SimpleDownloader as downloader
import time

try:
   import ssl
   ssl._create_default_https_context = ssl._create_unverified_context
except:
   pass
   
tsdownloader=False
hlsretry=False
resolve_url=['180upload.com', 'allmyvideos.net', 'bestreams.net', 'clicknupload.com', 'cloudzilla.to', 'movshare.net', 'novamov.com', 'nowvideo.sx', 'videoweed.es', 'daclips.in', 'datemule.com', 'fastvideo.in', 'faststream.in', 'filehoot.com', 'filenuke.com', 'sharesix.com',  'plus.google.com', 'picasaweb.google.com', 'gorillavid.com', 'gorillavid.in', 'grifthost.com', 'hugefiles.net', 'ipithos.to', 'ishared.eu', 'kingfiles.net', 'mail.ru', 'my.mail.ru', 'videoapi.my.mail.ru', 'mightyupload.com', 'mooshare.biz', 'movdivx.com', 'movpod.net', 'movpod.in', 'movreel.com', 'mrfile.me', 'nosvideo.com', 'openload.io', 'played.to', 'bitshare.com', 'filefactory.com', 'k2s.cc', 'oboom.com', 'rapidgator.net', 'primeshare.tv', 'bitshare.com', 'filefactory.com', 'k2s.cc', 'oboom.com', 'rapidgator.net', 'sharerepo.com', 'stagevu.com', 'streamcloud.eu', 'streamin.to', 'thefile.me', 'thevideo.me', 'tusfiles.net', 'uploadc.com', 'zalaa.com', 'uploadrocket.net', 'uptobox.com', 'v-vids.com', 'veehd.com', 'vidbull.com', 'videomega.tv', 'vidplay.net', 'vidspot.net', 'vidto.me', 'vidzi.tv', 'vimeo.com', 'vk.com', 'vodlocker.com', 'xfileload.com', 'xvidstage.com', 'zettahost.tv']
g_ignoreSetResolved=['plugin.video.dramasonline','plugin.video.f4mTester','plugin.video.shahidmbcnet','plugin.video.SportsDevil','plugin.stream.vaughnlive.tv','plugin.video.ZemTV-shani']

class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
	   return response
   https_response = http_response

REMOTE_DBG=False;
if REMOTE_DBG:
	# Make pydev debugger works for auto reload.
	# Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
	try:
		import pysrc.pydevd as pydevd
	# stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
		pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
	except ImportError:
		sys.stderr.write("Error: " +
			"You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
		sys.exit(1)

addon = xbmcaddon.Addon('plugin.video.rgbtv')
addon_version = addon.getAddonInfo('version')
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))
favorites = os.path.join(profile, 'favorites')
history = os.path.join(profile, 'history')
REV = os.path.join(profile, 'list_revision')
icon = os.path.join(home, 'icon.png')
source_file = os.path.join(home, base64.b64decode('c291cmNlX2ZpbGU='))
functions_dir = profile

communityfiles = os.path.join(profile, 'LivewebTV')
downloader = downloader.SimpleDownloader()
debug = addon.getSetting('debug')
if os.path.exists(favorites)==True:
	FAV = open(favorites).read()
else: FAV = []
if os.path.exists(source_file)==True:
	SOURCES = open(source_file).read()
else: SOURCES = []


def addon_log(string):
	xbmc.log("[addon.rgbtv-%s]: %s" %(addon_version, string), xbmc.LOGNOTICE)


#
#function equalavent to re.sub('\\b' + aa +'\\b', k[c], p)

#########################################################
# Function  : GUIEditExportName                         #
#########################################################
# Parameter :                                           #
#                                                       #
# name        sugested name for export                  #
#                                                       # 
# Returns   :                                           #
#                                                       #
# name        name of export excluding any extension    #
#                                                       #
#########################################################

   
#########################################################

class InputWindow(xbmcgui.WindowDialog):
	def __init__(self, *args, **kwargs):
		self.cptloc = kwargs.get('captcha')
		self.img = xbmcgui.ControlImage(335,30,624,60,self.cptloc)
		self.addControl(self.img)
		self.kbd = xbmc.Keyboard()

	def get(self):
		self.show()
		time.sleep(2)
		self.kbd.doModal()
		if (self.kbd.isConfirmed()):
			text = self.kbd.getText()
			self.close()
			return text
		self.close()
		return False

def getEpocTime():
	import time
	return str(int(time.time()*1000))

def getEpocTime2():
	import time
	return str(int(time.time()))

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


def add_item( mode="" , idtmdb="", title="" , sinopsis="" , url="" , thumbnail="" , fanart="" , idserie="" , idcategoria="" , capitulo="", temporada="", info_labels = None, isPlayable = False , folder=True ):
	#addon_log("add_item action=["+action+"] title=["+title+"] url=["+url+"] thumbnail=["+thumbnail+"] fanart=["+fanart+"] show=["+show+"] episode=["+episode+"] extra=["+extra+"] page=["+page+"] isPlayable=["+str(isPlayable)+"] folder=["+str(folder)+"]")

	listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	if info_labels is None:
		info_labels = { "Title" : title, "FileName" : title, "Plot" : sinopsis }
	listitem.setInfo( "video", info_labels )

	if fanart!="":
		listitem.setProperty('fanart_image',fanart)
		xbmcplugin.setPluginFanart(int(sys.argv[1]), fanart)
	
	if isPlayable:
		listitem.setProperty("Video", "true")
		listitem.setProperty('IsPlayable', 'true')
		itemurl = '%s?mode=%s&idtmdb=%s&title=%s&url=%s&thumbnail=%s&sinopsis=%s&capitulo=%s&idcategoria=%s&idserie=%s&temporada=%s&fanart=%s' % ( sys.argv[ 0 ] , mode , idtmdb , urllib.quote_plus( title.encode('utf-8')) , urllib.quote_plus(url.encode('utf-8')) , urllib.quote_plus( thumbnail.encode('utf-8')) , urllib.quote_plus( sinopsis.encode('utf-8')), capitulo , idcategoria , urllib.quote_plus(idserie.encode('utf-8')), temporada , urllib.quote_plus(fanart.encode('utf-8')))
		xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)
	else:
		itemurl = '%s?mode=%s&idtmdb=%s&title=%s&url=%s&thumbnail=%s&sinopsis=%s&capitulo=%s&idcategoria=%s&idserie=%s&temporada=%s&fanart=%s' % ( sys.argv[ 0 ] , mode , idtmdb , urllib.quote_plus( title.encode('utf-8')) , urllib.quote_plus(url.encode('utf-8')) , urllib.quote_plus( thumbnail.encode('utf-8')) , urllib.quote_plus( sinopsis.encode('utf-8')), capitulo , idcategoria , urllib.quote_plus(idserie.encode('utf-8')), temporada , urllib.quote_plus(fanart.encode('utf-8')))
		xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)


	   

## Thanks to daschacka, an epg scraper for http://i.teleboy.ch/programm/station_select.php
##  http://forum.xbmc.org/post.php?p=936228&postcount=1076


def crear_menu_inicio():
			url = link+"/get_menu_inicio/"
			r = requests.get(url)
			data = r.text
			datos = json.loads(data)
			desc=""
			cont=0
			for i in datos:
				data = i
				name = data["fields"]["TITULO"]
				thumbnail = data["fields"]["THUMBNAIL"]
				fanArt = data["fields"]["FANART"]
				mode = data["fields"]["MODE"] 
				if thumbnail == None:
				   thumbnail = THUMBNAIL
				if fanArt == None:
				   fanArt = FANART
				add_item( mode , "", name  , desc  , url  , thumbnail  , fanArt  , "" , "" , "", "", None, False , True )
				#add_item( mode="" , idtmdb="", title="" , sinopsis="" , url="" , thumbnail="" , fanart="" , idserie="" , idcategoria="" , grupo="", temporadas="", info_labels = None, isPlayable = False , folder=True ):

def crear_menu_categorias():
			url = link+"/get_categorias/"
			r = requests.get(url)
			data = r.text
			datos = json.loads(data)
			url = ""
			fanArt = ""
			desc=""
			for i in datos:
				data = i
				name = data["fields"]["TITULO"]
				idcategoria = data["fields"]["IDCATEGORIA"]
				thumbnail = data["fields"]["THUMBNAIL"]
				fanArt = data["fields"]["FANART"] 
				mode = data["fields"]["MODE"] 
				if thumbnail == None:
				   thumbnail = THUMBNAIL
				if fanArt == None:
				   fanArt = FANART
				add_item( mode , "", name  , desc  , url  , thumbnail  , fanArt  , "" , idcategoria , "", "", None, False , True )
				#add_item( mode="" , idtmdb="", title="" , sinopsis="" , url="" , thumbnail="" , fanart="" , idserie="" , idcategoria="" , grupo="", temporadas="", info_labels = None, isPlayable = False , folder=True ):

def crear_menu_categoria_serie():
			url = link+"/get_categoria_serie/"
			r = requests.get(url)
			data = r.text
			datos = json.loads(data)
			url = ""
			fanArt = "https://pbs.twimg.com/profile_images/859590453473271808/SSRQ1u9b_400x400.jpg"
			desc=""
			for i in datos:
				data = i
				idcategoria = data["fields"]["IDCATEGORIA"]
				name = data["fields"]["TITULO"]
				thumbnail = data["fields"]["THUMBNAIL"]
				fanArt =  data["fields"]["FANART"]
				mode = data["fields"]["MODE"]
				if thumbnail == None:
				   thumbnail = THUMBNAIL
				if fanArt == None:
				   fanArt = FANART
				add_item( mode , "", name  , desc  , url  , thumbnail  , fanArt  , "" , str(idcategoria) , "" , "", None, False , True )
				#add_item( mode="" , idtmdb="", title="" , sinopsis="" , url="" , thumbnail="" , fanart="" , idserie="" , idcategoria="" , grupo="", temporadas="", info_labels = None, isPlayable = False , folder=True ):


def crear_menuseries(idcategoria):
	addon_log("IDCATEGORIA ="+str(idcategoria))
	url = link+"/get_menuseries/"+idcategoria+"/"
	r = requests.get(url) #descarga archivi json
	datos = r.text #se pasa el archivo json a datos
	info = json.loads(datos) #convierte archivo Json a Diccionario Python
	#cont = 0
	mode = 0
	idtmdb = ""
	for i in info:

		data = i
		idserie = data["fields"]["IDSERIE"]
		idcategoria = data["fields"]["IDCATEGORIA"]
		serie =  data["fields"]["SERIE"]	
		titulo = data["fields"]["TITULO"]	
		mode = data["fields"]["MODE"]
		thumbnail = data["fields"]["THUMBNAIL"]
		fanArt = data["fields"]["FANART"]
		#temporada = 1
		if thumbnail == None:
		   thumbnail = THUMBNAIL
		if fanArt == None:
		   fanArt = FANART
		sinopsis = data["fields"]["DESCRIPCION"]
		add_item( mode , "" , titulo , sinopsis , "" , thumbnail , fanArt , str(idserie) , "" , "" ,"", None, False , True )
		#add_item( mode="" , idtmdb="", title="" , sinopsis="" , url="" , thumbnail="" , fanart="" , idserie="" , idcategoria="" , grupo="", temporada="", info_labels = None, isPlayable = False , folder=True ):

def crear_menu_fuente_documental():
	url = link+"/documentales/menu_fuente_documental/"
	r = requests.get(url) #descarga archivi json
	datos = r.text #se pasa el archivo json a datos
	info = json.loads(datos) #convierte archivo Json a Diccionario Python
	#cont = 0
	mode = 0
	idtmdb = ""
	for i in info:

		data = i
		idfuente = data["fields"]["IDFUENTE"]
		idserie = idfuente
		nombre_fuente =  data["fields"]["NOMBRE_FUENTE"]
		titulo = nombre_fuente	
		mode = data["fields"]["MODE"]
		thumbnail = data["fields"]["THUMBNAIL"]
		fanArt = data["fields"]["FANART"]
		#temporada = 1
		if thumbnail == None:
		   thumbnail = THUMBNAIL
		if fanArt == None:
		   fanArt = FANART 
		sinopsis = data["fields"]["DESCRIPCION"]
		add_item( mode , "" , titulo , sinopsis , "" , thumbnail , fanArt , str(idserie) , "" , "" ,"", None, False , True )
		#add_item( mode="" , idtmdb="", title="" , sinopsis="" , url="" , thumbnail="" , fanart="" , idserie="" , idcategoria="" , grupo="", temporada="", info_labels = None, isPlayable = False , folder=True ):

def crear_menu_categoria_fuente(idfuente):
	url = link+"/documentales/menu_categoria_fuente/"+idfuente+"/"
	r = requests.get(url) #descarga archivi json
	datos = r.text #se pasa el archivo json a datos
	info = json.loads(datos) #convierte archivo Json a Diccionario Python
	#cont = 0
	mode = 0
	idtmdb = ""
	for i in info:

		data = i
		idfuente = data["fields"]["IDFUENTE"]
		idserie = idfuente 
		idcategoria_fuente = data["fields"]["IDCATEGORIA_FUENTE"]
		idcategoria = idcategoria_fuente
		nombre_categoria =  data["fields"]["TITULO_CATEGORIA"]
		titulo = nombre_categoria	
		mode = data["fields"]["MODE"]
		thumbnail = data["fields"]["THUMBNAIL"]
		fanArt = data["fields"]["FANART"]
		#temporada = 1
		if thumbnail == None:
		   thumbnail = THUMBNAIL
		if fanArt == None:
		   fanArt = FANART 
		sinopsis = data["fields"]["DESCRIPCION"]
		add_item( mode , "" , titulo , sinopsis , "" , thumbnail , fanArt , str(idserie) , str(idcategoria) , "" ,"", None, False , True )
		#add_item( mode="" , idtmdb="", title="" , sinopsis="" , url="" , thumbnail="" , fanart="" , idserie="" , idcategoria="" , grupo="", temporada="", info_labels = None, isPlayable = False , folder=True ):


def crear_menu_documentales(idfuente,idcategoria_fuente):
	url = link+"/documentales/menu_documentales/"+str(idfuente)+"/"+str(idcategoria_fuente)+"/"
	r = requests.get(url) #descarga archivi json
	datos = r.text #se pasa el archivo json a datos
	info = json.loads(datos) #convierte archivo Json a Diccionario Python
	#cont = 0
	mode = 0
	idtmdb = ""
	for i in info:

		data = i
		url = data["fields"]["URL1"]
		nombre_documental =  data["fields"]["TITULO_DOCUMENTAL"]
		titulo = nombre_documental
		mode = data["fields"]["MODE"]
		thumbnail = data["fields"]["THUMBNAIL"]
		fanArt = data["fields"]["FANART"]
		#temporada = 1
		if thumbnail == None:
		   thumbnail = THUMBNAIL
		if fanArt == None:
		   fanArt = FANART 
		sinopsis = data["fields"]["SINOPSIS"]
		add_item( mode , "" , titulo , sinopsis , url , thumbnail , fanArt , "" , "" , "" ,"", None, True , False )
		#add_item( mode="" , idtmdb="", title="" , sinopsis="" , url="" , thumbnail="" , fanart="" , idserie="" , idcategoria="" , grupo="", temporada="", info_labels = None, isPlayable = False , folder=True ):



def crear_menu_temporadas(idserie):
	addon_log("IDSERIE ="+str(idserie))
	url = link+"/get_menu_temporadas/"+idserie+"/"
	r = requests.get(url) #descarga archivi json
	datos = r.text #se pasa el archivo json a datos
	info = json.loads(datos) #convierte archivo Json a Diccionario Python
	#cont = 0
	mode = 0
	idtmdb = ""
	for i in info:

		data = i
		idserie = data["fields"]["IDSERIE"]
		idcategoria = data["fields"]["IDCATEGORIA"]
		serie =  data["fields"]["SERIE"]	
		titulo = data["fields"]["TITULO"]	
		mode = data["fields"]["MODE"]
		thumbnail = data["fields"]["THUMBNAIL"]
		fanArt = data["fields"]["FANART"]
		if thumbnail == None:
		   thumbnail = THUMBNAIL
		if fanArt == None:
		   fanArt = FANART 
		sinopsis = data["fields"]["DESCRIPCION"]
		temporada = data["fields"]["TEMPORADA"]
		add_item( mode , "" , titulo , sinopsis , "" , thumbnail , fanArt , str(idserie) , "" , "" , temporada , None, False , True )
		#add_item( mode="" , idtmdb="", title="" , sinopsis="" , url="" , thumbnail="" , fanart="" , idserie="" , idcategoria="" , grupo="", temporada="", info_labels = None, isPlayable = False , folder=True ):
		
		
def crear_menu_capitulos(idserie,temporada,fanart,thumbnail):
	#addon_log("IDCATEGORIA ="+str(idcategoria))
	#+idserie+"/"+temporada+"/"
	url = link+"/get_menu_capitulos/"+str(idserie)+"/"+str(temporada)+"/"
	r = requests.get(url) #descarga archivi json
	datos = r.text #se pasa el archivo json a datos
	info = json.loads(datos) #convierte archivo Json a Diccionario Python
	#cont = 0
	mode = 0
	idtmdb = ""
	fanArt = fanart
	thumbnail = thumbnail
	for i in info:

		data = i
		serie =  data["fields"]["SERIE"]	
		titulo = data["fields"]["TITULO"]
		temporada = data["fields"]["TEMPORADA"]	
		capitulo = data["fields"]["CAPITULO"]
		url = data["fields"]["URL1"]
		#thumbnail = data["fields"]["THUMBNAIL"]
		#fanArt = data["fields"]["FANART"]
		#if fanArt == None:
		   #fanArt = "https://pbs.twimg.com/profile_images/859590453473271808/SSRQ1u9b_400x400.jpg"
		sinopsis = data["fields"]["SINOPSIS"]
		servidor = data["fields"]["SERVIDOR"]
		if str(servidor) == "1":
			mode = 5
		elif str(servidor) == "3":
			mode = 6  
		#addon_log("Datos Json Devueltos"+titulo+url+"mode: "+str(mode))  
		#cont = cont+1
		title = titulo
		if thumbnail == None:
		   thumbnail = THUMBNAIL
		if fanArt == None:
		   fanArt = FANART 
		#title = title+" ("+"[COLOR yellow] Temporada "+temporada+"[/COLOR]"+"[COLOR magenta]--[/COLOR]"+"[COLOR cyan]Episodio "+episodio+"[/COLOR]"+")"
		add_item( mode , idtmdb , title , sinopsis , url , thumbnail , fanArt , serie ,""  , capitulo , temporada, None, True , False )
		#add_item( mode="" , idtmdb="", title="" , sinopsis="" , url="" , thumbnail="" , fanart="" , idserie="" , idcategoria="" , grupo="", temporada="", info_labels = None, isPlayable = False , folder=True ):	

def crear_movielista(idcategoria):
	url = link+"/get_moviejson/"+str(idcategoria)+"/"
	r = requests.get(url) #descarga archivi json
	datos = r.text #se pasa el archivo json a datos
	info = json.loads(datos) #convierte archivo Json a Diccionario Python
	#cont = 0
	mode = 0
	for i in info:
		data = i
		idtmdb = data["fields"]["ID_TMDB"]	
		title =  data["fields"]["TITULO"]	
		date = data["fields"]["ESTRENO"]
		url = data["fields"]["URL1"]
		thumbnail = data["fields"]["THUMBNAIL"]
		fanArt = data["fields"]["FANART"]
		if thumbnail == None:
		   thumbnail = THUMBNAIL
		if fanArt == None:
		   fanArt = FANART 
		sinopsis = data["fields"]["SINOPSIS"]
		servidor = data["fields"]["SERVIDOR"]
		if str(servidor) == "3":#URLsolve
			mode = 6
		title = title+" ("+"[COLOR cyan]"+date+"[/COLOR]"+")"
		add_item( mode , idtmdb , title , sinopsis , url , thumbnail , fanArt , "" , "" ,"", "", None, True , False )
		#add_item( action="" , title="" , plot="" , url="" , thumbnail="" , fanart="" , show="" , episode="" , extra="", page="", info_labels = None, isPlayable = False , folder=True )


def crear_menu_canalestv():
	url = link+"/get_menu_canalestv/"
	r = requests.get(url) #descarga archivi json
	datos = r.text #se pasa el archivo json a datos
	info = json.loads(datos) #convierte archivo Json a Diccionario Python
	#cont = 0
	mode = 0
	for i in info:
		data = i
		title =  data["fields"]["TITULO"]	
		url = data["fields"]["URL1"]
		thumbnail = data["fields"]["THUMBNAIL"]
		fanArt = data["fields"]["FANART"]
		if thumbnail == None:
		   thumbnail = THUMBNAIL
		if fanArt == None:
		   fanArt = "https://pbs.twimg.com/profile_images/859590453473271808/SSRQ1u9b_400x400.jpg"
		descripcion = data["fields"]["DESCRIPCION"]
		mode = data["fields"]["MODE"]
		mode = 15
		#cont = cont+1
		add_item( mode , "" , title , descripcion , url , thumbnail , fanArt , "" , "" ,"", "", None, True , False )
		#add_item( action="" , title="" , plot="" , url="" , thumbnail="" , fanart="" , show="" , episode="" , extra="", page="", info_labels = None, isPlayable = False , folder=True )


def play_link(link,name,desc,genre,iconimage):
	addon_log('Playing Link: |%s|' % (link))
	hmf = urlresolver.HostedMediaFile(url=link)
	if not hmf:
		addon_log('Indirect hoster_url not supported by urlresolver: %s' % (link))
		#kodi.notify('Link Not Supported: %s' % (link), duration=7500)
		return False
	addon_log('Link Supported: |%s|' % (link))

	try:
		stream_url = hmf.resolve()
		if not stream_url or not isinstance(stream_url, basestring):
			try: msg = stream_url.msg
			except: msg = link
			raise Exception(msg)
	except Exception as e:
		try: msg = str(e)
		except: msg = link
		#kodi.notify('Resolve Failed: %s' % (msg), duration=7500)
		return False
		
	addon_log('Link Resolved: |%s|%s|' % (link, stream_url))
		
	#listitem = xbmcgui.ListItem(path=stream_url)
	listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	listitem.setInfo(type='Video', infoLabels={'Title':name , 'Plot':desc , "Genre":genre })
	listitem.setProperty("IsPlayable","true")
	listitem.setPath(stream_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


xbmcplugin.setContent(int(sys.argv[1]), 'movies')	    

try:
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
except:
	pass
try:
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
except:
	pass
try:
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
except:
	pass
try:
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
except:
	pass

params=get_params()
api_key="2cd2538742da5dcb2d3e0a381a537689&language=es-ES"
url=None
name=None
mode=None
playlist=None
iconimage=None
fanart=None
playlist=None
fav_mode=None
regexs=None
desc=None
genre=None
idtmdb=None
idserie=None
idcategoria=None
grupo=None
temporadas=None

try:
	idtmdb=int(params["idtmdb"])
except:
	pass 
try:
	temporada=urllib.unquote_plus(params["temporada"]).decode('utf-8')
except:
	pass  	 
try:
	url=urllib.unquote_plus(params["url"]).decode('utf-8')
except:
	pass
try:
	desc=urllib.unquote_plus(params["sinopsis"]).decode('utf-8')
except:
	pass    
try:
	name=urllib.unquote_plus(params["title"]).decode('utf-8')
except:
	pass
try:
	thumbnail=urllib.unquote_plus(params["thumbnail"]).decode('utf-8')
except:
	pass
try:
	fanart=urllib.unquote_plus(params["fanart"]).decode('utf-8')
except:
	pass	
try:
	idcategoria=urllib.unquote_plus(params["idcategoria"]).decode('utf-8')
except:
	pass
try:
	idserie=urllib.unquote_plus(params["idserie"]).decode('utf-8')
except:
	pass	
try:
	grupo=urllib.unquote_plus(params["grupo"]).decode('utf-8')
except:
	pass	
try:
	mode=int(params["mode"])
except:
	pass
try:
	if idtmdb == None:
		genre = "[COLOR magenta]Serie [/COLOR]"+"[COLOR yellow]"+str(idserie)+"[/COLOR]"
	else:
		genero= requests.get(link+'/get_genero/'+str(idtmdb)+'/')
		genero = genero.text
		genre = "[COLOR magenta]Genero: [/COLOR]"+"[COLOR yellow]"+genero+"[/COLOR]"	
except:
	pass  
	
addon_log("Mode: "+str(mode))

if mode==None:
	#addon_log("getSources")
	crear_menu_inicio()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==1:
	addon_log("Ejecutandose Mode 1")
	crear_menu_categoria_serie()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
elif mode==2:
	addon_log("Ejecutandose Mode 2")
	crear_menu_categorias()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==3:
	addon_log("Ejecutandose Mode 3")
	crear_menu_canalestv()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
elif mode==4:
	#addon_log("Categoria: "+str(name))
	crear_movielista(idcategoria)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	  
elif mode==5:
	addon_log("Ejecutandose mode 5")
	from serviopenload import openload
	addon_log("url "+url)	
	link = openload.get_video_url(url, premium=False, user="", password="", video_password="") 
	addon_log("url resuelta "+str(link))
	url = str(link)
	listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	listitem.setInfo(type='Video', infoLabels={'Title':name , 'Plot':desc , "Genre":genre })
	listitem.setProperty("IsPlayable","true")
	listitem.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

elif mode==6:
	play_link(url,name,desc,genre,iconimage) 
	#link,name,desc,genre,iconimage  
	#playsetresolved(urlsolver(url),name,iconimage,desc,genre,True)

elif mode==7:
	addon_log("Grupo ="+str(grupo))
	crear_menu_gruposerie(grupo)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==8:
	serie = name
	crear_listaTemporadas(serie,thumbnail,fanart,temporadas)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==9:
	listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	listitem.setInfo(type='Video', infoLabels={'Title':name , 'Plot':desc , "Genre":genre })
	listitem.setProperty("IsPlayable","true")
	listitem.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	
elif mode==10:
	addon_log("idcategoria ="+str(idcategoria))
	crear_menuseries(idcategoria)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==11:
	addon_log("idserie ="+str(idserie))
	crear_menu_temporadas(idserie)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==12:
	addon_log("idserie = "+str(idserie)+" temporada = "+str(temporada))
	crear_menu_capitulos(idserie,temporada,fanart,thumbnail)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==13:
	temporada = 1
	addon_log("idserie = "+str(idserie)+" temporada = "+str(temporada))
	crear_menu_capitulos(idserie,temporada,fanart,thumbnail)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==15:
	addon_log("URL = "+str(url))
	url = str(url)
	listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	listitem.setInfo(type='Video', infoLabels={'Title':name , 'Plot':desc , "Genre":genre })
	listitem.setProperty("IsPlayable","true")
	listitem.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

elif mode==20:
	crear_menu_fuente_documental()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==21:
	idfuente = idserie
	crear_menu_categoria_fuente(idfuente)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==22:
	idfuente = idserie
	idcategoria_fuente = idcategoria
	crear_menu_documentales(idfuente,idcategoria_fuente)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
elif mode==60:
	play_link(url,name,desc,genre,iconimage) 
	#link,name,desc,genre,iconimage  
	#playsetresolved(urlsolver(url),name,iconimage,desc,genre,True)

elif mode==61:
	pass 

elif mode==62:
	 from servidaily import servi_daily
	 #servi_daily.login()
	 servi_daily.playVideo(url)

elif mode==63:
	 from serviopenload import openload
	 url = openload.get_video_url(url, premium=False, user="", password="", video_password="") 
	 xbmc.log("sys.argv = "+str(sys.argv[2]), xbmc.LOGNOTICE)
	 playsetresolved(url,name,iconimage,desc,anio,genre,True)                 
if not viewmode==None:
   print 'setting view mode'
   xbmc.executebuiltin("Container.SetViewMode(%s)"%viewmode)
	