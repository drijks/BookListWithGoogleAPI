import os
import re
import requests
import io
import datetime


def search_for_item(value):
    parms = {"q": value}
    r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
    rj = r.json()
    if rj.get("items"):
        return get_five(rj)
    else:
        print("Oops! No books found! Try again: ")
        new_value = str(input())
        return search_for_item(new_value)


def get_five(rj):
    first_five = []
    for i in range(min(5, len(rj["items"]))):
        first_five.append(rj["items"][i])
    for i in range(len(first_five)):
        print(i + 1)
        if first_five[i]["volumeInfo"].get("title"):
            print(first_five[i]["volumeInfo"]["title"])
        else:
            print("Title not found.")
        if first_five[i]["volumeInfo"].get("authors"):
            print(first_five[i]["volumeInfo"]["authors"])
        else:
            print("Author not found.")
        if first_five[i]["volumeInfo"].get("publisher"):
            print(first_five[i]["volumeInfo"]["publisher"])
        else:
            print("Publisher  not found.")
        if first_five[i]["volumeInfo"].get("description"):
            print(first_five[i]["volumeInfo"]["description"])
        else:
            print("Description not found.")
    return first_five


def add_to_list(bklst):
    print("\nAdd a book to the list by typing its corresponding number (1-5) or try a new search by typing 0: \n")
    real_book, selected_book = check_input(bklst)
    if real_book and selected_book != 0:
        add_selection_to_list(bklst[selected_book - 1])
    elif real_book and selected_book == 0:
        print("Please enter a search query such as author, title, subject, or ISBN")
        new_search = str(input())
        add_to_list(search_for_item(new_search))
    else:
        print("Oops! Try again!")
        add_to_list(bklst)


def check_input(bklst):
    selected_book = input()
    is_one_thru_five = False
    if selected_book.isnumeric():
        if 0 <= int(selected_book) <= len(bklst):
            is_one_thru_five = True
            selected_book = int(selected_book)
    return [is_one_thru_five, selected_book]


def check_list_for_duplicates(selected):
    if selected["volumeInfo"].get("industryIdentifiers"):
        id_type = str(selected["volumeInfo"]["industryIdentifiers"][0]["type"])
        book_id = str(selected["volumeInfo"]["industryIdentifiers"][0]["identifier"])
        selected_id = "Identifier: \n" + id_type + ": " + book_id
    else:
        selected_id = "Identifier not found."
    word_pattern = re.compile(r'Identifier: \n.*')
    number_of_entries = 1
    with io.open("my_book_list.txt") as f:
        text = f.read()
        prev_entries = word_pattern.findall(text)
    for entry in prev_entries:
        if entry == selected_id:
            return [False, number_of_entries]
        number_of_entries += 1
        f.close()
    return [True, number_of_entries]


def add_selection_to_list(selected):
    ct = datetime.datetime.now().timestamp()  # Allows users to see when an entry was added
    current_time = datetime.datetime.fromtimestamp(ct).isoformat()
    title = str(selected["volumeInfo"]["title"])
    if selected["volumeInfo"].get("authors"):
        authors = str(selected["volumeInfo"]["authors"])
    else:
        authors = "Author not found."
    if selected["volumeInfo"].get("description"):
        description = str(selected["volumeInfo"]["description"])
    else:
        description = "Description not found."
    if selected["volumeInfo"].get("publisher"):
        publisher = str(selected["volumeInfo"]["publisher"])
    else:
        publisher = "Publisher not found."
    if selected["volumeInfo"].get("industryIdentifiers"):
        id_type = str(selected["volumeInfo"]["industryIdentifiers"][0]["type"])
        book_id = str(selected["volumeInfo"]["industryIdentifiers"][0]["identifier"])
    else:
        id_type = "Unique identifier"
        book_id = "Not found."
    book_info = "\nTime Added: " + current_time + "\nTitle: " + title + \
                "\nAuthor(s): " + authors + "\nPublisher: " + publisher + "\nDescription: " + description + \
                "\nIdentifier: \n" + id_type + ": " + book_id + "\n\n\n"

    if os.path.exists("my_book_list.txt"):
        unique_item, entry_number = check_list_for_duplicates(selected)
        if unique_item:
            my_list = io.open("my_book_list.txt", "r")
            prev_entries = my_list.read()
            my_new_list = open("my_book_list.txt", "w+")
            new_book_info = "Entry number " + str(entry_number) + book_info
            my_new_list.write(prev_entries + new_book_info)
            my_list.close()
            print("This book has been added to your list!")
        else:
            print("This book is already on your list!")
    else:
        my_list = open("my_book_list.txt", "w+")
        my_list.write("Entry Number 1" + book_info)
        my_list.close()
        print("This book has been added to your list!")


def view_my_list():
    view_list = input()
    if view_list == "Y" or view_list == "YES" or view_list == "yes" or view_list == "y" or view_list == "Yes":
        my_list = io.open("my_book_list.txt", "r")
        print(my_list.read())
        my_list.close()


def run_program():
    print("Please enter a search query such as author, title, subject, or ISBN")
    newbk = input()
    five_bks = search_for_item(str(newbk))
    add_to_list(five_bks)
    # Allow users to view their book list
    print("View current list? Y/N")
    view_my_list()
    print("Do you want to keep searching? Y/N")
    new_search = input()
    if new_search.lower() == "y" or new_search.lower() == "yes":
        run_program()


if __name__ == "__main__":
    if os.path.exists("my_book_list.txt"):
        print("Welcome back! Would you like to view your book list? Y/N")
        view_my_list()
    else:
        print("Welcome!")
    run_program()
    print("Okay! Come back soon!")
