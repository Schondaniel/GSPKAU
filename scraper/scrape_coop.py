from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
from datetime import datetime

#firebase
cred = credentials.Certificate("firebase_admin.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
time= datetime.now().strftime("%y-%m-%d %H:%M")

def save(collection_id, document_id, data):
    db.collection(collection_id).document(document_id).set(data)

#SCRAPE
URL = "https://www.coop.se/butiker-erbjudanden/coop/coop-kronoparken/"

response = requests.get(URL)
page_content = BeautifulSoup(response.content, "html.parser")
kategorier = page_content.find_all("div", class_="Grid Grid--gutterA2xsm Grid--equalHeight Grid--gutterH2xsm js-drOffersBlock")

for x in range(0,len(kategorier)-1):
    cat_name = kategorier[x+1].find("h2", class_="u-paddingTxxxsm Heading Heading--h4 u-marginAz u-sizeFull")
    products = kategorier[x].find_all("div", class_="ItemTeaser-content")
    for i in range(0,len(products)):
        product_name = products[i].find("h3", class_="ItemTeaser-heading")
        product_price = products[i].find("span", class_="Splash-priceLarge")
        product_info = products[i].find("span", class_="ItemTeaser-brand")
        product_price_sup = products[i].find("span", class_="Splash-priceSup")
        product_price_pre = products[i].find("span", class_="Splash-pricePre")
        product_price_add = products[i].find("div", class_="Splash-priceSub Splash-priceUnit")

        ####### LÄGGA TILL ÖREN, FUNKAR INTE EFTERSOM COOP LÄGGER TILL TOMMA TAGGAR EFTER
        # product_price_ = product_price.text.strip()
        # if product_price_sup is not None:
        #         product_price_sup_ = product_price_sup.text.strip()
        #         price = int(product_price_) + (int(product_price_sup_)/100)
        # else:
        # price = product_price.text.strip()

    #initz
        cat = ""
        name = ""
        price = ""
        pre = ""
        sup = ""
        add = ""
        info = ""
        #Kategori
        cat = cat_name.text.strip()
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
        #product_info
        if(product_info is not None):
            info = product_info.text.strip()

    #prints
        #namn    
        # print(product_name.text.strip())
        # # pre price (3 för...osv) 
        # if(product_price_pre is not None):
        #     print(product_price_pre.text.strip())
        # #price
        # print(price)
        # # sup price (/kg... osv)
        # if(product_price_add is not None):
        #     print(product_price_add.text.strip())
        # #product_info
        # if(product_info is not None):
        #     print(product_info.text.strip())
        # print()
    #Data
        data = {
                "store" : "Ica Maxi Bergvik",
                "kategori" : cat,
                "offer": name,
                "pre":  pre,
                "add": add,
                "price": price,
                "decimal": sup,
                "info": info
            }

        save(
            collection_id = "coop",
            document_id = f"{time}" + " nummer: " + str(x) + ":" + str(i),
            data = data
        )

print("-------------------------------------------------------")
print("Succecfully updated Database")
print("-------------------------------------------------------")





