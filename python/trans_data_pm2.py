#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import hashlib


# In[2]:


data = pd.read_csv('data.csv')


# In[3]:


columnas_seleccionadas = ['Titular', 'Comunidad', 'Licencia', 'F.Matriculacion', 'F.Adscripcion', 'Licencias', 'Datos de']
data = data[columnas_seleccionadas]
data


# In[4]:


#Pequeño fix
data['Comunidad'].fillna('LA MANCHA', inplace=True)


# In[5]:


# funcion para asignar tamaño de propietario en funcion de tus 'titulos'
def asignar_tamano_propietario(licencias):
    
    if 1 <= licencias <= 4:
        return 'Pequeño'
    elif 5 <= licencias <= 35:
        return 'Mediano'
    elif 35 <= licencias <= 100:
        return 'Alto'
    elif 101 <= licencias <= 5000:
        return 'Grande'
    else:
        return 0

# aplicamos la funcion
data['tamaño_propietario'] = data['Licencias'].apply(asignar_tamano_propietario)


# In[6]:


#DATOS MES
data['Datos de'] = data['Datos de'].map({
    'Mes 1': 'Enero',
    'Mes 2': 'Junio',
    'Mes 3': 'Diciembre'
})
data


# In[7]:


# ANONIMIZANDO LICENCIAS
def anonimizar_licencia(licencia):
    # Convierte el número de licencia a cadena y aplica la función hash
    licencia_str = str(licencia)
    hashed_licencia = hash(licencia_str.encode())

    
    return hashed_licencia

# aplicamos la funcion a nuestra data
data['Licencia'] = data['Licencia'].apply(anonimizar_licencia)
data


# In[8]:


# Función para anonimizar titular, metemos un -5 para aquellos que añaden un SL nos los trunque e identifique bien.
# Esto nos evita el usar fuzzywuzzy. En este caso el cif no es útil ya que tenemos solo el 50-60% del total.

def anonimizar_titular(valor):
    # aplicamos metodo hash previamente truncando las compañias que puedan tener ' S.L.'
    titular_truncado = valor[:-5]
    hash_anonimizado = hash(titular_truncado)
    return hash_anonimizado

# Aplicar la función a la columna especificada
data['Titular'] = data['Titular'].apply(anonimizar_titular)


# In[10]:


# RENOMBRANDO COLUMNAS DATAFRAME

columnas_seleccionadas = ['Titular', 'Comunidad', 'Licencia', 'F.Matriculacion', 'F.Adscripcion', 'Licencias', 'Datos de', 'tamaño_propietario']

nuevos_nombres = {
    'Comunidad': 'Region',
    'F.Matriculacion': 'Antiguedad',
    'F.Adscripcion': 'Fecha_transaccion',
    'Licencia': 'Cantidad_total',
    'Licencia': 'títulos de la compañia',
    'Datos de': 'mes_data',
    
}

data = data[columnas_seleccionadas].rename(columns=nuevos_nombres)


# In[11]:


data


# In[12]:


#lista de comunidades autónomas

comunidades_autonomas = data['Region'].unique()

print(comunidades_autonomas)


# In[13]:


# DataFrame con las coordenadas
coordenadas = {
    'Comunidad Autónoma': ['CATALUÑA', 'MADRID', 'LA MANCHA', 'ANDALUCIA', 'MURCIA', 'EXTREMADURA',
                           'ASTURIAS', 'C.VALENCIANA', 'LA RIOJA', 'CASTILLA LEON', 'ARAGON', 'CANTABRIA',
                           'GALICIA', 'I.BALEARES', 'PAIS VASCO', 'NAVARRA'],
    'Latitud': [41.5912, 40.4168, 39.4015, 37.3833, 37.9924, 39.4753, 43.3623, 39.4699, 42.2871, 41.8333, 41.6500, 43.4573,
                42.5751, 39.5696, 42.9837, 42.8185],
    'Longitud': [1.5209, -3.7038, -3.1149, -5.9833, -1.1307, -6.3761, -5.8458, -0.3763, -2.5396, -4.8333, -0.8833, -3.8196,
                 -8.1339, 2.6502, -2.1012, -1.6447]
}

df_coordenadas = pd.DataFrame(coordenadas)

# Realiza un merge entre tu DataFrame original 'data' y el DataFrame de coordenadas 'df_coordenadas'
data = pd.merge(data, df_coordenadas, left_on='Region', right_on='Comunidad Autónoma', how='left')

# Elimina la columna redundante 'Comunidad Autónoma'
data.drop('Comunidad Autónoma', axis=1, inplace=True)


# In[14]:


data.to_csv('data_.csv')


# In[15]:


data


# In[ ]:





# In[ ]:





# In[ ]:




