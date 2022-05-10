import requests
from bs4 import BeautifulSoup
import json
import time

all_items = []
#used to make a list to hold the items for export

for item_number in range(1,17239):
#at time of writing, the database had this many items

    url = f'https://plre.folger.edu/booksDetail.php?id={item_number}'
    print(url)

    r = requests.get(url)

    if r.status_code == 200:
        print(url)

        book_title = None
        book_id = None
        book_description = None
        booklist_name = None
        booklist_source = None
      #listing all attributes of the item ensures that there will be no blank or unfilled fields later on

        soup = BeautifulSoup(r.text, features="html.parser")

        booklist_all = soup.find_all("p", {"class":"booklist"})
        #booklist info was in the html separately from the rest of the data

        if len(booklist_all) == 2:
            booklist_namem = booklist_all[0].text
            booklist_sourcem = booklist_all[1].text
        elif len(booklist_all) == 1:
            booklist_namem = booklist_all[0].text
            booklist_sourcem = None
        else:
            print("No booklist info!")
          
        if booklist_namem != None:
          booklist_name = booklist_namem.strip()
        if booklist_sourcem != None:  
          booklist_source = booklist_sourcem.strip()

        bookinfo_all = soup.find_all("span")
        #could also use "td" to separate out headers and contents

        if len(bookinfo_all) == 4:
            book_idm = bookinfo_all[0].text
            space = bookinfo_all[1].text
            book_titlem = bookinfo_all[2].text
            book_descriptionm = bookinfo_all[3].text
        elif len(bookinfo_all) == 3:
            book_idm = bookinfo_all[0].text
            space = bookinfo_all[1].text
            book_titlem = bookinfo_all[2].text
            book_descriptionm = None
        elif len(bookinfo_all) == 2:
            book_idm = bookinfo_all[0].text
            space = bookinfo_all[1].text
            book_titlem = None
            book_descriptionm = None
        elif len(bookinfo_all) == 1:
            book_idm = bookinfo_all[0].text
            space = None
            book_titlem = None
            book_descriptionm = None
        else:
            print("No info found!")
          #because the information may not always be in this order, no info found should be understood as "info not found in this order". check the json file to see if it was pulled

        book_title = book_titlem.strip()
        book_id = book_idm.strip()
        book_descriptionn =                 book_descriptionm.strip()
        book_descriptionu = book_descriptionn.replace("\n","")
        book_description = book_descriptionu.replace("\u00a0","")
        #strips the empty spaces and new lines so it doesn't end up in the json file
      
        list_item = {
        'url': url,
        'title': book_title,
        'id': book_id,
        'description': book_description,
        'booklistname': booklist_name,
        'booklistsource': booklist_source
        }

        all_items.append(list_item)

    with open('plre_books_data1.json','w') as plrefile:
        json.dump(all_items,plrefile,indent=2)
