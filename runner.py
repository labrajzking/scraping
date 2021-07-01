"""this is a script for scraping tyre information"""
import re #importing regular expression
import json #importing json
import requests #importing requests
from bs4 import BeautifulSoup #importing beautifulsoup
GET_URL="https://www.twt.co.za/product/assurance-2/"
def get_page(url):
    """this function return the html of the target using requests and beautifulsoup"""
    with requests.Session() as session:
        page=session.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
    return soup
def scraping_price():
    """
    this function scraps the price of the target,the taget is and
     informs us wether its available or.
    and returns a dict containing the information
    """
    soup=get_page(GET_URL)
    number=soup.find("span",class_="woocommerce-Price-amount amount").text
    integer=re.sub("[^1-9]", "",number)
    decimal=re.sub("[^0-0]","",number)
    price=float(integer+'.'+decimal)
    button=soup.find("button",{"type" : "submit" , "name" : "add-to-cart"})
    available=bool(button)
    price = {
        "price" : price,
        "available" : available,
        "premoteid" : int(button['value'])
        }
    print (price)
    return price
def scraping_product():
    """"
    this function scraps the target's id,name,brand,image_url,url.
    return a dict containing these information
    """
    soup=get_page(GET_URL)
    images_div=soup.find('div',class_='single-tyre-tab-item')
    images_url=images_div.findAll('img')
    image_url=[]
    for imgurl in images_url:
        image_url.append(imgurl['src'])
    print (image_url)
    brand_img=soup.find('img',class_='brand-logo-img')['src']
    button=soup.find("button",{"type" : "submit" , "name" : "add-to-cart"})
    brand=str(brand_img.split("/")[-1].split(".")[0][:-1])
    product = {
    "premoteid" : int(button['value']),
    "name" : str(brand+" "+soup.find("h4",class_="desk").text+" "+soup.find("em").text),
    "brand" :brand,
    "image_url" : image_url,
    "url" : str(soup.find("form",class_="cart")['action'])
        }
    print (product)
    return product
def main():
    """ main function """
    price=scraping_price()
    product=scraping_product()
    with open('Price.json', 'w') as outfile:
        json.dump(price, outfile)
    with open('Product.json', 'w') as outfile:
        json.dump(product, outfile)
    print ("Files Saved !!!!!")
if __name__ == "__main__":
    main()
