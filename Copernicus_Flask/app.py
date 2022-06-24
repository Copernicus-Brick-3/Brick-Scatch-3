#API KEY :
# ads.atmosphere.copernicus.eu (Atmosphere) : 5729:f5324f2d-ebed-4932-b892-dea8bca853f3
# cds.climate.copernicus.eu (Climate) : 138730:2ca5cd16-2d91-4c9c-995d-3735c28863e7 

from flask import Flask
from flask import request
import datetime
import cdsapi
from zipfile import ZipFile
import os

app = Flask(__name__)

def extractFiles(): # Extrait tous les fichiers netcdf de l'archive download.zip
    print("EXTRACT FILES")
    with ZipFile('download.zip', 'r') as zipObj:
        listOfFileNames = zipObj.namelist()
        for fileName in listOfFileNames:
            if fileName.endswith('.nc'):
                zipObj.extract(fileName, '../images')

@app.route("/")
def index():
    return datetime.datetime.now().strftime("%H:%M:%S")
    
@app.route("/download")
def download():
    requestType = request.args.get('request', default='defaultRequest',type=str)
    day = request.args.get('day', default='01',type=str)
    month = request.args.get('month', default='01',type=str)
    year = request.args.get('year', default='01',type=str)
    if requestType == 'aerosol':
        c = cdsapi.Client(url='https://cds.climate.copernicus.eu/api/v2', key='138730:2ca5cd16-2d91-4c9c-995d-3735c28863e7')   # <---- renseigner sa propre clé API
        c.retrieve(
            'satellite-aerosol-properties',
            {
                'time_aggregation': 'daily_average',
                'variable': 'dust_aerosol_optical_depth',
                'sensor_on_satellite': 'iasi_on_metopa',
                'algorithm': 'ens',
                'year': year,
                'month': month,
                'day': day,
                'version': 'v1.1',
                'orbit': 'descending',
                'format': 'zip',
            },
            'download.zip') 
        extractFiles()
        os.remove('download.zip')
    elif requestType == 'nox':
        print("TODO")
    elif requestType == 'melting': 
        print("TODO")
    else:
        return "ERROR ON REQUEST"
    return "Download finished"
    

@app.route("/test")
def test():
    c = cdsapi.Client(url='https://ads.atmosphere.copernicus.eu/api/v2', key='5729:f5324f2d-ebed-4932-b892-dea8bca853f3')
    c.retrieve(
        'cams-global-reanalysis-eac4',
        {
            'date': '2003-01-01/2003-01-01',
            'format': 'netcdf',                                 
            'variable': '2m_temperature',
            'time': '00:00',
        },
        'download.nc')
    return "Téléchargement terminé"


@app.route("/convert")
def convert():
    #Importer les packages
    import xarray as xr 
    import rioxarray as rio
    #Récupérer le fichier .nc
    nc_file = xr.open_dataset('../images/aerosol.nc')
    print(nc_file)
    #Prendre la variable de notre choix
    data_variable = nc_file['DAOD550']
    #Définir les variables spaciales
    data_variable = data_variable.rio.set_spatial_dims(x_dim='longitude', y_dim='latitude')
    #Définir le CRS
    data_variable.rio.write_crs("epsg:4326", inplace=True)
    data_variable.rio.to_raster(r"../images/aerosol.tiff")

    return "convert success"

if __name__ == "__main__":
    app.run()


@app.after_request
def add_header(response):
    #permet de pouvoir faire des requetes http depuis un site web(Cross-origin resource sharing)
    response.headers['Access-Control-Allow-Origin'] = '*' 
    return response