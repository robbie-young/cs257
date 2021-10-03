'''
    books.py
    Authors: Kevin Bui, Robbie Young, 2 October 2021
    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import argparse
import booksdatasource

def load(fileName):
    dataSource=booksdatasource.BooksDataSource(fileName)
    return dataSource


def getParsedArgument():
    parser = argparse.ArgumentParser()

    parser.add_argument('--filename', '-f')
    parser.add_argument('--title', '-t', help='print all book entries with title containing the specified string')
    parser.add_argument('--author', '-a', help='print all book entries with author\'s name containing the specified string')
    parser.add_argument('--start_year', '-s', type=int, nargs='?', help='print all books published after start_year, inclusive.')
    parser.add_argument('--end_year', '-e', type=int, nargs='?', help='print all books published before end_year, inclusive.')


    return parser.parse_args()

def main():
    arguments = getParsedArgument()
    if(not arguments.filename):
        raise Exception('Filename is missing, use -f flag')
    
    dataSet = load(arguments.filename)

    if(arguments.start_year != None or arguments.end_year != None or arguments.author != None or arguments.title != None):
        # runs the filtering twice, once to remove years greater than start year and other for less than end year if both exist. 
        if(not arguments.start_year == None):
            dataSet.booksList = dataSet.books_between_years(start_year=arguments.start_year)
        if(not arguments.end_year == None):
            dataSet.booksList = dataSet.books_between_years(end_year=arguments.end_year)
        if (not arguments.author == None):
            dataSet.authorsList = dataSet.authors(arguments.author)
        if (not arguments.title == None):
            dataSet.booksList = dataSet.books(arguments.title)
    else:
        raise Exception('No search parameter provided, use -h for usage')
    
    if (not arguments.author == None):
        #sorting the bookList to be in alphabetical order in case the title flag is missing
        dataSet.books()
        for author in dataSet.authorsList:
            authorString = author.surname +' '+ author.given_name + ', ' + author.birth_year + '-' + author.death_year
            
            bookString = ''
            for book in dataSet.booksList:
                for thisBooksAuthor in book.authors:
                     if(thisBooksAuthor == author):
                         bookString = bookString + book.title + ' (' + book.publication_year + ')'
            print(authorString)
            print('===',bookString)
    
    else:
        for book in dataSet.booksList:
            authorsString = ''
            for author in book.authors:
                authorsString = authorsString + author.surname +' '+ author.given_name + ', '
            print(book.title + ' (' + book.publication_year + '), ' + ' by ' + authorsString)


if __name__ == '__main__':
    main()