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

#Scrape
URL = "https://www.willys.se/erbjudanden/butik"

response = requests.get(URL)
page_content = BeautifulSoup(response.content, "html.parser")
products = page_content.find("div", class_="infinite-scroll-component")

# for i in range(0,len(products)):
#     product_name = products[i].find("div", class_="Productstyles__StyledProductName-sc-16nua0l-5 dqhhbm")
#     product_price = products[i].find("span", class_="PriceLabelstyles__StyledProductPriceText-sc-koui33-2 dzPBER")
#     product_price_sup = products[i].find("span", class_="PriceLabelstyles__StyledProductPriceDecimal-sc-koui33-5 jzJfVO")
#     product_price_pre = products[i].find("span", class_="Productstyles__StyledProductSavePrice-sc-16nua0l-13 iyjqpG")
#     product_price_add = products[i].find("div", class_="PriceLabelstyles__StyledProductPriceUnit-sc-koui33-6 cDUNFW")
#     product_price_ = product_price.text.strip()
    
    
#     if product_price_sup is not None:
#         product_price_sup_ = product_price_sup.text.strip()
#         price = int(product_price_) + (int(product_price_sup_)/100)
#     else:
#         price = product_price.text.strip()

# #prints
#     #namn    
#     print(product_name.text.strip())
#     # pre price (3 för...osv) 
#     if(product_price_pre is not None):
#         print(product_price_pre.text.strip())
#     #price
#     print(price)
#     # sup price (/kg... osv)
#     if(product_price_add is not None):
#         print(product_price_add.text.strip())
#     print()

print(products.prettify())