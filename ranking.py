"""this is a script for scraping tyres ranks"""
import re
import json
import requests
from bs4 import BeautifulSoup
GET_URL="https://www.twt.co.za/shop/?filter_tyre-width=205&filter_tyre-profile=60&filter_tyre-diameter=16"
def scraping_tyres(url):
    """this function gets the html of the target page,
    extract the information from it,
    and returns it in a dict format
    """
    with requests.Session() as session:
        page=session.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        result_count=soup.find("p",class_="woocommerce-result-count").text
        numbers=re.findall('[0-9]+',result_count)
        page_size=int(numbers[1])-int(numbers[0])+1
        print (page_size)
        max_rank=int(numbers[2])
        print (max_rank)
        parent=soup.find("div",class_="row products g-3")
        tyres=parent.findChildren("div",recursive=False)
        i=1
        tyres_array=[]
        for tyre in tyres:
            premoteid=int(re.findall('[0-9]+',tyre['class'][6])[0])
            print (premoteid)
            rank=i
            print (rank)
            keyword=tyre.find("div",class_="product_sub_title").text
            print (keyword)
            tyre_info ={
                        "premoteid":int(re.findall('[0-9]+',tyre['class'][6])[0]),
                        "rank":i,
                        "keyword":tyre.find("div",class_="product_sub_title").text,
                        "page_size":page_size,
                        "max_rank" : max_rank
                    }
            i+=1
            tyres_array.append(tyre_info)
        pages_button=soup.findAll("a",class_="page-numbers")
        for button in pages_button:
            if button.text:
                print (button)
                page=session.get(button['href'])
                soup = BeautifulSoup(page.text, 'html.parser')
                result_count=soup.find("p",class_="woocommerce-result-count").text
                numbers=re.findall('[0-9]+',result_count)
                page_size=int(numbers[1])-int(numbers[0])+1
                print (page_size)
                max_rank=int(numbers[2])
                print (max_rank)
                parent=soup.find("div",class_="row products g-3")
                tyres=parent.findChildren("div",recursive=False)
                for tyre in tyres :
                    premoteid=int(re.findall('[0-9]+',tyre['class'][6])[0])
                    print (premoteid)
                    rank=i
                    print (rank)
                    keyword=tyre.find("div",class_="product_sub_title").text
                    print (keyword)
                    tyre_info={
                            "premoteid":int(re.findall('[0-9]+',tyre['class'][6])[0]),
                            "rank":i,
                            "keyword":tyre.find("div",class_="product_sub_title").text,
                            "page_size":page_size,
                            "max_rank" : max_rank
                        }
                    i+=1
                    tyres_array.append(tyre_info)
    return tyres_array
def main():
    """main function"""
    tyres_array=scraping_tyres(GET_URL)
    with open('TyresRankings.json', 'w') as outfile:
        json.dump(tyres_array, outfile)
    print("File Saved !!!!")
if __name__ == "__main__":
    main()
