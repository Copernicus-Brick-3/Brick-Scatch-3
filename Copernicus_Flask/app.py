import cdsapi
import datetime
from flask import Flask
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

app = Flask(__name__)

@app.route("/")
def hello_world():
    return datetime.datetime.now().strftime("%H:%M:%S")

@app.route("/download")
def download():
    #connexion a l'api de copernicus
    c = cdsapi.Client(url='https://ads.atmosphere.copernicus.eu/api/v2', key='5729:f5324f2d-ebed-4932-b892-dea8bca853f3')   # <---- renseigner sa propre clé API

    #Recupere et telecharge en local les donnée sous le format nc
    #TODO: Recuperer des valeur et modifier les valeur present dans cette requetes.
    c.retrieve(
        'efas-forecast',
        {
            'format' : 'netcdf',
        },
        'download.nc')
        return "download done"
    

@app.route("/convertimg")
def NcToPng():
    #recupere le fichier en local
    data = Dataset('download.nc')

    #different valeur stocker dans le fichier nc
    lats = data.variables['latitude'][:]
    lons = data.variables['longitude'][:]
    time = data.variables['time'][:]
    #valeur qui differe pour les different theme 
    t2m = data.variables['t2m'][:]
    #TODO:Pouvoir faire changer la valeur pour chaque themes donné en parametres

    #Creer une carte avec leur coordonées
    mp=Basemap(projection='mill',lat_ts=10,llcrnrlon=lons.min(), \
    urcrnrlon=lons.max(),llcrnrlat=lats.min(),urcrnrlat=lats.max(), \
    resolution='c')
    lon, lat = np.meshgrid(lons, lats)
    x,y = mp(lon, lat)

    #Rajoute les code couleur et 
    c_scheme = mp.pcolor(x, y,np.squeeze(t2m[0,:,:]),shading='flat',cmap=plt.cm.jet)
    #Dessine les frontieres avec les different pays
    mp.drawcoastlines()
    mp.drawstates()
    mp.drawcountries()
    #Rajoute une legende sous forme de barre
    cbar = mp.colorbar(c_scheme, location = 'right', pad = '10%')

    #TODO:Le titre en en-tete et le nom de l'images doit etre changer avec la date et le themes stocker dans le fichier nc
    plt.title('TEST')
    #telecharge un fichier en png
    plt.savefig('image.png')

@app.route("/img")
#TODO:Recuperer des images et les envoyer vers mblock


@app.after_request
def add_header(response):
    #permet de pouvoir faire des requetes http depuis un site web(Cross-origin resource sharing)
    response.headers['Access-Control-Allow-Origin'] = '*' 
    return response