# BookListWithGoogleAPI
A small command line application that allows users to submit a search query and get results from the Google Books API. Written in Python.

Latest version is booklist2.py

New users will immediately be given the option to search for books to add to the book list. Returning users will have the option to look at their existing book list before performing a search. Use keywords such as 'title' or 'author' if you're having trouble finding what you want. For example, if you want to find a book by R.A. Salvatore, typing in 'Salvatore author' will return more relevant results than simply typing in 'Salvatore.'

Written and tested in Python 3.7

Dependencies/imports: os, io, datetime, re (regular expressions), requests. Note that because this program uses the Google Books API, a working internet connection is required for use.

My process: I began with a simple search function, then limited the results to the first five matches. From there I added the functionality to add an item to the list, then tidied up the results so that the list was readable to the user.

Example book lists are the results of my manual tests while refactoring the program.
