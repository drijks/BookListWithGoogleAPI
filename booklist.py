import os
import requests
import io
import datetime
import re


class GBooks():
    googleapikey = "AIzaSyB70dRppmd86Am9xm7HBZfjfd8a8eqgOLY"

    # def search(self, value):
    #     parms = {"q": value, 'key': self.googleapikey}
    #     r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
    #     print(r.url)
    #     rj = r.json()
    #     print(rj["totalItems"])
    #     for i in rj["items"]:
    #         try:
    #             print(repr(i["volumeInfo"]["description"]))
    #         except:
    #             pass
    #         try:
    #             print(repr(i["volumeInfo"]["imageLinks"]["thumbnail"]))
    #         except:
    #             pass

    # gets the first five results from a search
    def getfive(self, value):
        parms = {"q": value, 'key': self.googleapikey}
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
        rj = r.json()
        firstfive = [rj["items"][0], rj["items"][1], rj["items"][2], rj["items"][3], rj["items"][4]]
        return firstfive


# adds a book to the user's list if the user has entered a valid selection
# TODO: adjust mylist function so that duplicate entries can be avoided. Use re and/or a different file format
def mylist(selected):
    currenttime = datetime.datetime.now().timestamp() # Allows users to see when an entry was added
    bookinfo = "Entry number __: \nTime Added: " + datetime.datetime.fromtimestamp(currenttime).isoformat() + "\n Title: " + str(selected["volumeInfo"]["title"]) + "\nAuthor(s): " + str(selected["volumeInfo"]["authors"]) + "\nDescription: " + str(selected["volumeInfo"]["description"]) + "\n" + str(selected["volumeInfo"]["industryIdentifiers"][0]["type"]) + ": " + str(selected["volumeInfo"]["industryIdentifiers"][0]["identifier"]) + "\n\n\n"
    if os.path.exists("my_book_list.txt"):
        mylist = io.open("my_book_list.txt", "r")
        preventries = mylist.read()
        mynewlist = open("my_book_list.txt", "w+")
        mynewlist.write(preventries + bookinfo)
    else:
        mylist = open("my_book_list.txt", "w+")
        mylist.write("Entry Number 1:\n" + bookinfo)
    mylist.close()
    print("This book has been added to your list!")


# decides  if the user's input is valid. If the input is valid, this runs the function to add a new book to the list
# and if the input is invalid, it starts over.
def addtolist(bklst):
    realbook, selectedbook = checkinput()
    if realbook:
        mylist(bklst[selectedbook-1])
    else:
        print("Oops! Try again!")
        addtolist(bklst)


def checkinput():
    print("Add a book to the list by typing its corresponding number (1-5): \n")
    selectedbook = input()
    isonethroughfive = False
    if selectedbook.isnumeric():
        if int(selectedbook) == 1 or int(selectedbook) == 2 or int(selectedbook) == 3 or int(selectedbook) == 4 or int(selectedbook) == 5:
            isonethroughfive = True
            selectedbook = int(selectedbook)
    return [isonethroughfive, selectedbook]


def viewmylist():
    mylst = io.open("my_book_list.txt", "r")
    print(mylst.read())
    mylst.close()


if __name__ == "__main__":
    print("Enter a search query")
    bk = GBooks()
    newbk = input()
    fivebks = bk.getfive(str(newbk))
    for i in range(len(fivebks)):
        print(i+1)
        print(fivebks[i]["volumeInfo"]["title"])
        print(fivebks[i]["volumeInfo"]["authors"])
        print(fivebks[i]["volumeInfo"]["description"])
        print("")
    addtolist(fivebks)

    # Allow users to view their book list
    print("View current list? Y/N")
    viewlst = input()
    if viewlst == "Y" or viewlst == "YES" or viewlst == "yes" or viewlst == "y" or viewlst == "Yes":
        viewmylist()
