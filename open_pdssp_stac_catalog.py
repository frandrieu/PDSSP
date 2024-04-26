#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:47:54 2024

Read a STAC catalog from PDSSP using pystac
  
@author: fandrieu
"""
# Import necessary libraries
from pystac_client import Client
from scipy.io import readsav
import urllib.request
import matplotlib.pyplot as plt
import numpy as np

# Example: PDSSP Mars catalogs
# Define the URL of the STAC catalog
#url = "https://pdssp.ias.universite-paris-saclay.fr/catalogs/mars"
url="https://raw.githubusercontent.com/pdssp/pdssp-stac-repo/test/ias/mars/catalog.json"


# Open the STAC catalog using pystac_client
cat = Client.open(url)

print(f"ID: {cat.id}")
print(f"Title: {cat.title or 'N/A'}")
print(f"Description: {cat.description or 'N/A'}")

# Get collections from the catalog
collections=list(cat.get_collections())
print(f"Number of collections: {len(collections)}")
print("Collections IDs:")
for collection in collections:
    print(f"- {collection.id}")

# Get the first collection
collection=cat.get_collection(collections[0].id)


# Check if the catalog conforms to the ITEM_SEARCH standard and add it if not
cat.conforms_to("ITEM_SEARCH")
cat.add_conforms_to("ITEM_SEARCH")

# Get items from the collection
items=collection.get_items()
#get first item 
item=next(items)


#collection_items = list(cat.search(collections=collection.id, max_items=10).items())
#item = collection.get_item(collection_items[0].id)
#item=collection_items[0]

print(item.geometry)
print(item.bbox)
print(item.datetime)
print(item.collection_id)
print(item.common_metadata.instruments)
print(item.common_metadata.platform)
print(item.stac_extensions)
print(item.assets)
#items = list(collection.get_items())

url_sav_file=item.assets['sav_data_file'].href
sav_fname=item.id+".sav"
urllib.request.urlretrieve(url_sav_file,sav_fname)
print(".sav file downloaded successfully")

data=sav_data = readsav(sav_fname)


cube=data['carte']
wave=data['wave']
lat=data['lati']
lon=data['longi']

canal0=cube[:,10,:]
canal1=cube[:,25,:]
canal2=cube[:,64,:]

img=np.zeros((canal0.shape[0],canal0.shape[1],3))
img[:,:,0]=canal0
img[:,:,1]=canal1
img[:,:,2]=canal2

plt.imshow(img)
plt.show()


roi=cube[60:100,:,50:75]

plt.imshow(img[60:100,50:75])
plt.show()

spectrum=np.mean(roi, axis=(0,2))
plt.plot(wave,spectrum)
plt.show()
plt.plot(wave,spectrum)
plt.plot(wave, np.mean(roi, axis=0))
plt.show()


#function to display info about 10 items
def get_ten_items(items):
    for i, item in enumerate(items):
        print(f"{i}: {item}", flush=True)
        if i == 9:
            return

print('First page', flush=True)
get_ten_items(items)

print('Second page', flush=True)
get_ten_items(items)