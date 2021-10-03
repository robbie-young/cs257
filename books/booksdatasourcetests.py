'''
    booksdatasourcetest.py
    Original author: Jeff Ondich, 24 September 2021
    Modified by: Kevin Bui, Robbie Young, 2 October 2021
    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import booksdatasource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = booksdatasource.BooksDataSource('testBooks1.csv')

    def tearDown(self):
        pass

    # Testing authors method
    def test_unique_author(self):
        authors = self.data_source.authors('Baldwin')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == booksdatasource.Author('Baldwin', 'James'))

    def test_no_matching_author(self):
        authors = self.data_source.authors('Bui')
        self.assertTrue(len(authors) == 0)
    
    def test_no_argument_author(self):
        authors = self.data_source.authors()
        self.assertTrue(len(authors) == 10)
    
    def test_case_sensitive_author(self):
        authors = self.data_source.authors('bront')
        authors2 = self.data_source.authors('Bront')
        for i in range(len(authors)):
            self.assertTrue(authors[i] == authors2[i])
    
    def test_multiple_matches_author(self):
        searchedName = 'Bront'
        authors = self.data_source.authors(searchedName)
        self.assertTrue(len(authors) == 4, "incorrect number of authors")
        for author in authors:
            self.assertTrue((searchedName in author.surname) or (searchedName in author.given_name), "incorrect Author's name")
    
    def test_space_separated_arg_author(self):
        searchedName = 'Laurence Sterne'
        authors = self.data_source.authors(searchedName)
        self.assertTrue(len(authors) == 1, "incorrect number of books")
        self.assertTrue(authors[0] == booksdatasource.Author('Sterne', 'Laurence'), "incorrect Author's name")
    
    def test_sorted_author(self):
        authors = self.data_source.authors('Bront')
        self.assertTrue(len(authors) == 4)
        self.assertTrue(authors[0] == booksdatasource.Author('Brontë', 'Ann'))
        self.assertTrue(authors[1] == booksdatasource.Author('Brontë', 'Charlotte'))
        self.assertTrue(authors[2] == booksdatasource.Author('Brontë', 'Emily'))
        self.assertTrue(authors[3] == booksdatasource.Author('Tonkin', 'Bront'))
        

    # Testing books method
    def test_unique_book(self):
        title = "To Say Nothing of the Dog"
        books = self.data_source.books(title)
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0] == booksdatasource.Book(title))
    
    def test_empty_args_book(self):
        books = self.data_source.books()
        self.assertTrue(len(books) == 10)

    def test_unique_unsensitive_book(self):
        searchString = 'to say Nothing of the dog'
        title = "To Say Nothing of the Dog"
        books = self.data_source.books(searchString)
        self.assertTrue(len(books) == 1)
        self.assertTrue(books[0] == booksdatasource.Book(title))

    def test_multiple_matches_books(self): 
        searchString = 'vi'
        books = self.data_source.books(searchString)
        self.assertTrue(len(books) == 2) 
        for book in books:
            self.assertTrue(searchString in book.title.lower())

    def test_sorted_books_title(self):
        searchString = 'vi'
        books = self.data_source.books(searchString, 'title') 
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == booksdatasource.Book("The Invisible Life of Addie LaRue"))
        self.assertTrue(books[1] == booksdatasource.Book("Villette"))

    def test_sorted_books_default(self): 
        searchString = 'vi'
        books = self.data_source.books(searchString) 
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == booksdatasource.Book("The Invisible Life of Addie LaRue"))
        self.assertTrue(books[1] == booksdatasource.Book("Villette"))
    
    def test_sorted_books_year(self): 
        searchString = 'vi'
        books = self.data_source.books(searchString, 'year') 
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[1] == booksdatasource.Book("The Invisible Life of Addie LaRue"))
        self.assertTrue(books[0] == booksdatasource.Book("Villette"))
        previousBookYear = -1
        for i in range(len(books)):
            self.assertTrue(int(books[i].publication_year) >= previousBookYear)
            previousBookYear = int(books[i].publication_year)

    # Testing books_between_years method

    def test_year_start_and_end(self): 
        books = self.data_source.books_between_years(2018, 2020)
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0] == booksdatasource.Book("Testing multiple author given name"))
    
    def test_year_start_and_end_string(self):
        books = self.data_source.books_between_years("2018", "2020")
        self.assertTrue(len(books) == 3)
        self.assertTrue(books[0] == booksdatasource.Book("Testing multiple author given name"))
    
    def test_year_sorted(self):
        books = self.data_source.books_between_years(2018, 2020)
        prevYear = -1
        for i in range(len(books)):
            self.assertTrue(int(books[i].publication_year) >= prevYear)
            prevYear = int(books[i].publication_year)
    
    def test_year_start_only(self):
        books = self.data_source.books_between_years(1997)
        self.assertTrue(len(books) == 4)
        self.assertTrue(books[3] == booksdatasource.Book("The Invisible Life of Addie LaRue"))
    
    def test_year_end_only(self):
        books = self.data_source.books_between_years(end_year=1855)
        self.assertTrue(len(books) == 4)
        self.assertTrue(books[0] == booksdatasource.Book("The Life and Opinions of Tristram Shandy, Gentleman"))
    
    def test_year_no_args(self):
        books=self.data_source.books_between_years()
        self.assertTrue(len(books) == 10)
        self.assertTrue(books[9] == booksdatasource.Book("The Invisible Life of Addie LaRue"))
 

if __name__ == '__main__':
    unittest.main()