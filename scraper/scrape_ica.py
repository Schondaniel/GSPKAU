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
URL = "https://www.ica.se/butiker/maxi/karlstad/maxi-ica-stormarknad-karlstad-11010/erbjudanden/"

response = requests.get(URL)
page_content = BeautifulSoup(response.content, "html.parser")
kategorier = page_content.find_all("section", class_="offer-category details open")

for x in range(0,len(kategorier)):
    cat_name = kategorier[x].find("header", class_="offer-category__header summary active")
    products = kategorier[x].find_all("div", class_="offer-category__item")
    for i in range(0,len(products)):
        product_name = products[i].find("h2", class_=["offer-type__product-name splash-bg icon-store-pseudo", "offer-type__product-name splash-bg icon-store-pseudo no-price"])
        product_price = products[i].find("div", class_="product-price__price-value")
        product_info = products[i].find("p", class_="offer-type__product-info")
        product_price_sup = products[i].find("div", class_="product-price__decimal")
        product_price_pre = products[i].find("div", class_="product-price__amount")
        product_price_add = products[i].find("div", class_="product-price__unit-item")

        product_price_ = product_price.text.strip()
        
        ####### LÄGGA TILL ÖREN, FUNKAR INTE

        # if product_price_sup is not None:
        #     product_price_sup_ = product_price_sup.text.strip()
        #     price = int(product_price_) + (int(product_price_sup_)/100)
        # else:
        
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
        # #namn
        # # if(product_price_pre is not None):    
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
        # print("-----")
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
            collection_id = "test ica",
            document_id = f"{time}" + " nummer: " + str(x) + ":" + str(i),
            data = data
        )
    
print("-------------------------------------------------------")
print("Succecfully updated Database")
print("-------------------------------------------------------")
