from flask import Flask

import datetime
import cdsapi

app = Flask(__name__)

@app.route("/")
def index():
    return datetime.datetime.now().strftime("%H:%M:%S")

@app.route("/download")
def download():
    #connexion a l'api de copernicus
    c = cdsapi.Client(url='https://ads.atmosphere.copernicus.eu/api/v2', key='5729:f5324f2d-ebed-4932-b892-dea8bca853f3')   # <---- renseigner sa propre clé API

    #Recupere et telecharge en local les donnée sous le format nc
    #TODO: Recuperer des valeur et modifier les valeur present dans cette requetes.
    c.retrieve(
        'cams-global-reanalysis-eac4',
        {
            'date': '2003-01-01/2003-01-01',
            'format': 'netcdf',                                 
            'variable': '2m_temperature',
            'time': '00:00',
        },
        'download.nc')
    return "download done"

if __name__ == "__main__":
    app.run()