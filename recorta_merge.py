### SCRIPT PARA RECORTE DO  SAMET PARA ANO E LATITUDES E LONGITUDES ESPECÍFICAS ###
### SALVA O RESULTADO COMO CSV ###

import pandas as pd
import xarray as xr
import netCDF4 as nc
import numpy as np
import cftime

caminho = "/dados/operacao/merge/CDO.MERGE"
arquivo = "/MERGE_CPTEC_DAILY_SB_PREC_2000_2023.nc"
url = f"{caminho}{arquivo}"
ds =  xr.open_dataset(url, decode_times = False)

# Pegando os atributos da variável time
time_units = ds.time.attrs["units"]  # 'hours since 1-1-1 00:00:00'
calendar = ds.time.attrs.get("calendar", "standard")  # 'standard'

# Convertendo manualmente para datetime
#print("CORRIGINDO O TEMPO")
ds["time"] = [cftime.num2date(t, time_units, calendar) for t in ds.time.values]
#print(ds)
#print("=-"*50)

### DEFININDO AS LATITUDES E LONGITUDES E INTERVALO DE TEMPO A SEREM CORTADAS ###
## IFSC ##
lat_IFSC = -27.6
lon_IFSC = -48.5
## OVNI ##
lat_OVNI = -27.5
lon_OVNI = -48.4
## FUTURO ##
lat_FUTURO = -27.8
lon_FUTURO = -48.6
## DEFININDO UMA LISTA A SER USADA NO LAÇO FOR ##
coords = [("NORTE", lat_OVNI, lon_OVNI),("CENTRO", lat_IFSC, lon_IFSC),("SUL", lat_FUTURO, lon_FUTURO)]
## DATAS LIMITES E RECORTE DO TEMPO ##
data_ii = pd.to_datetime("2023-01-01")
data_ff = pd.to_datetime("2023-12-31")
## RECORTA O TEMPO ##
ds_sel = ds
#ds_sel = ds.sel(time = slice(data_ii, data_ff))

## INICIA O DATAFRAME PARA ARMAZENAMENTO DA SELEÇÃO ##
df = pd.DataFrame ({
"DIA": ds_sel.time.values
})

## INICIA A SELEÇÃO POR EDBC ##
for nome, lat, lon in coords:
	## RECORTA A LATITUDE E LONGITUDE ##
	ds_sel1 = ds_sel.sel(lat=lat, lon=lon, method = "nearest")

	## CRIANDO UM DATAFRAME TEMPORÁRIO QUE SERÁ ADICIONADO AO PRIMEIRO DATAFRAME EM CADA FIM DO LAÇO FOR ##
	df_temp = pd.DataFrame({
	nome: ds_sel1.prec.values
	})
	#print(df_temp)
	## ADICIONA O DF_TEMP AO DF ##
	df = pd.concat([df, df_temp], axis = 1)

df.index = df["DIA"]
df = df.loc[data_ii: data_ff]
print(df)
df.to_csv("dados_merge_1.csv", index = False)
print("Arquivo Salvo com sucesso!")
