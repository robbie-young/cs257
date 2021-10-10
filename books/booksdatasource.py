#!/usr/bin/env python3
'''
    booksdatasource.py
    Original author: Jeff Ondich, 24 September 2021
    Modified by: Kevin Bui, Robbie Young, 2 October 2021
    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name
    
    def print_author(self):
        #sorting the book_list to be in alphabetical order in case the title flag is missing
        author_string = self.surname + ' ' + self.given_name + ', ' + self.birth_year + '-' + self.death_year
        print(author_string)

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title
    
    def print_book(self):
        author_string = ''
        for author in self.authors:
            author_string = author_string + author.surname +' '+ author.given_name + ', '
        print('=== ' + self.title + ' (' + self.publication_year + '), ' + 'by ' + author_string)

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        self.authors_list = []
        self.books_list = []
        ''' The books CSV file format looks like this:
                title,publication_year,author_description
            For example:
                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)
            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        with open(books_csv_file_name, newline='') as csv_file:
            #these dictionaries are only used to quickly filter out repeating books/authors based on title/name
            temp_authors_dict = {}
            temp_books_dict = {}

            reader = csv.reader(csv_file)
            for row in reader:
                temp_multiple_authors_list = row[2].split('and')
                this_books_authors = []
                for author in temp_multiple_authors_list:
                    temp_author = author.split(" ")
                    temp_year_list = temp_author[-1].replace("(", "").replace(")", "").split("-")

                    # We are assuming there is only one first name and all other names are stored as a surname
                    surname_list = temp_author[1:-1]
                    surname_string = ''
                    for surname in surname_list:
                        surname_string = surname_string + " " + surname
                        
                    #we know the first char is going to be a space, so just remove it with 1:-1 substr op  
                    new_author = Author(surname_string[1:], temp_author[0], temp_year_list[0], temp_year_list[1])
                    this_books_authors.append(new_author)
                    if(not temp_authors_dict.get(author, False)):
                        temp_authors_dict[author] = new_author

                #if there are 2 books with the same title but different years + authors, we are assuming they're the exact same book thus we're only adding it in once. The FIRST occurrence of such books with this unique title will be added.
                newBook = Book(title=row[0], publication_year=row[1], authors=this_books_authors)
                if(not temp_books_dict.get(row[0], False)):
                    temp_books_dict[row[0]] = newBook
            
            self.authors_list = temp_authors_dict.values()
            self.books_list = temp_books_dict.values()
    
    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        if(search_text == None):
            return sorted(self.authors_list, key=lambda author: author.surname + author.given_name)
        else:
            filtered_authors = []
            search_text = search_text.lower()
            for author in self.authors_list:
                if (search_text in author.surname.lower() + " " + author.given_name.lower()) or (search_text in author.given_name.lower() + " " + author.surname.lower()):
                    filtered_authors.append(author)
            
            return sorted(filtered_authors, key=lambda author: author.surname + author.given_name)
      


    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.
            The list of books is sorted in an order depending on the sort_by parameter:
                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        # sort by alphabetical order
        if (sort_by=='title'):
            if(search_text == None):
                return sorted(self.books_list, key=lambda book: book.title)
            else:
                filtered_books = []
                search_text = search_text.lower()
                for book in self.books_list:
                    if (search_text in book.title.lower()):
                        filtered_books.append(book)
                
                return sorted(filtered_books, key=lambda book: book.title)

        # sort by year
        else:
            if(search_text == None):
                return sorted(self.books_list, key=lambda book: book.publication_year)
            else:
                filtered_books = []
                search_text = search_text.lower()
                for book in self.books_list:
                    if (search_text in book.title.lower()):
                        filtered_books.append(book)
                
                return sorted(filtered_books, key=lambda book: book.publication_year)

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).
            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        filtered_books = []
        if (start_year==None and end_year==None):
            return sorted(self.books_list, key=lambda book: book.publication_year + book.title)

        elif (start_year!=None and end_year==None):
            for book in self.books_list:
                if (int(book.publication_year) >= start_year):
                    filtered_books.append(book)
            return sorted(filtered_books, key=lambda book: book.publication_year + book.title)

        elif (start_year==None and end_year!=None):
            for book in self.books_list:
                if (int(book.publication_year) <= end_year):
                    filtered_books.append(book)
            return sorted(filtered_books, key=lambda book: book.publication_year + book.title)

        else:
            for book in self.books_list:
                if (int(book.publication_year) >= int(start_year) and int(book.publication_year) <= int(end_year)):
                    filtered_books.append(book)
            return sorted(filtered_books, key=lambda book: book.publication_year + book.title)