#imports for required API's
from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
from datetime import datetime

#firebase setup
cred = credentials.Certificate("firebase_admin.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
time= datetime.now().strftime("%y-%m-%d %H:%M")

#Save function to push data to database
def save(collection_id, document_id, data):
    db.collection(collection_id).document(document_id).set(data)

#Clear current offers in Database
def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

delete_collection(db.collection("lidl"),100)
print("-------------------------------------------------------")
print("Succesfully Deleted Old Offers ")
print("-------------------------------------------------------")

#Collect data from requested URL
URL = "https://www.lidl.se/veckans-erbjudanden"

response = requests.get(URL)
page_content = BeautifulSoup(response.content, "html.parser")
products = page_content.find_all("div", class_="nuc-a-flex-item nuc-a-flex-item--width-6 nuc-a-flex-item--width-4@sm")

#Find product details requested html document
for i in range(0,len(products)):
    product_name = products[i].find("h3", class_="ret-o-card__headline")
    product_price = products[i].find("span", class_="lidl-m-pricebox__price")
    product_price_add = products[i].find("div", class_="lidl-m-pricebox__basic-quantity")
    product_price_pre = products[i].find("div", class_="lidl-m-pricebox__highlight")
    product_price_sup = products[i].find("div", class_="lidl-m-pricebox__discount-prefix")
    

    #initz
    name = ""
    price = ""
    pre = ""
    sup = ""
    add = ""
    #Name
    name = product_name.text.strip()
    #Price
    price = product_price.text.strip()
    # pre price (3 för...osv)
    if(product_price_pre is not None):
        pre = product_price_pre.text.strip()
    # sup price (decimal)
    if(product_price_sup is not None):
        sup = product_price_sup.text.strip()
    # add price (/kg... osv)
    if(product_price_add is not None):
        add = product_price_add.text.strip()
   
    #Store collected data
    data = {
            "store" : "Ica Maxi Bergvik",
            "offer": name,
            "pre":  pre,
            "add": add,
            "price": price,
            "decimal": sup
        }
    #Push collected data to server
    save(
        collection_id = "lidl",
        document_id = f"{time}" + " nummer: " + str(i),
        data = data
    )
    
print("-------------------------------------------------------")
print("Succecfully updated Database")
print("-------------------------------------------------------")
