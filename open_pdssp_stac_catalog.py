#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:47:54 2024

Read a STAC catalog from PDSSP using pystac
  
@author: fandrieu
"""
from pystac_client import Client
from scipy.io import readsav
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
#Example : PDSSP Mars catalogs
url = "https://pdssp.ias.universite-paris-saclay.fr/catalogs/mars"
url="https://raw.githubusercontent.com/pdssp/pdssp-stac-repo/test/ias/mars/catalog.json"



cat = Client.open(url)
print(f"ID: {cat.id}")
print(f"Title: {cat.title or 'N/A'}")
print(f"Description: {cat.description or 'N/A'}")

#print(list(cat.get_collections()))

collections=list(cat.get_collections())
print(f"Number of collections: {len(collections)}")
print("Collections IDs:")
for collection in collections:
    print(f"- {collection.id}")
collection=cat.get_collection(collections[0].id)

cat.conforms_to("ITEM_SEARCH")
cat.add_conforms_to("ITEM_SEARCH")
items=collection.get_items()
#get first item 
item=next(items)
def get_ten_items(items):
    for i, item in enumerate(items):
        print(f"{i}: {item}", flush=True)
        if i == 9:
            return

print('First page', flush=True)
get_ten_items(items)

print('Second page', flush=True)
get_ten_items(items)
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

plt.imshow(roi)
plt.show()

spectrum=np.mean(roi, axis=(0,2))
plt.plot(wave,spectrum)
plt.show()
plt.plot(wave,spectrum)
plt.plot(wave, np.mean(roi, axis=0))
plt.show()
'''
#get all children
children = list(cat.get_children())
print("catalog children")
print(children)


#Crawling through Child Catalogs/Collections
ch1=cat.get_child(children[1].id)
print("getting collections")
print(list(ch1.get_collections()))

print("getting children")
chch=list(ch1.get_children())
chch0=ch1.get_child(chch[0].id)
print(chch)

print("getting collections")
print(list(chch0.get_collections()))
print("getting children")
chchch=list(chch0.get_children())
chchch0=chch0.get_child(chchch[0].id)
print(chchch)

print("getting collections")
print(list(chchch0.get_collections()))
print("getting children")
#chchchch=list(chchch0.get_children())
#chchchch0=chchch0.get_child(chchchch[0].id)

'''