'''
    books.py
    Authors: Kevin Bui, Robbie Young, 10 October 2021
    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import argparse
import booksdatasource

def get_parsed_arguments():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--filename', '-f')
    parser.add_argument('--title', '-t')
    parser.add_argument('--author', '-a')
    parser.add_argument('--start_year', '-s', type=int, nargs='?')
    parser.add_argument('--end_year', '-e', type=int, nargs='?')
    parser.add_argument('--by_year', '-Y', default='title', action='store_true')

    parser.add_argument('-h', '--help', action='store_true')


    return parser.parse_args()

def main():
    arguments = get_parsed_arguments()
    if(not arguments.filename):
        raise Exception('Filename is missing, use -f flag')
    
    # load the file
    data_set = booksdatasource.BooksDataSource(arguments.filename)

    #print help statement
    if arguments.help:
        file = open('usage.txt', 'r')
        content = file.read()
        print(content)
        file.close()
        exit()

    if(arguments.start_year is not  None):
        data_set.books_list = data_set.books_between_years(start_year=arguments.start_year)

    if(arguments.end_year is not None):
        data_set.books_list = data_set.books_between_years(end_year=arguments.end_year)

    if (arguments.author is not None):
        data_set.authors_list = data_set.authors(arguments.author)

    if (arguments.title is not None):
        data_set.books_list = data_set.books(arguments.title)


    if (arguments.author is not None):
        #sorting the bookList to be in order in case the title flag is missing
        data_set.books_list = data_set.books(sort_by = arguments.by_year)
        for author in data_set.authors_list:
            author.print_author()
            for book in data_set.books_list:
                for this_books_author in book.authors:
                    if (this_books_author == author):
                        book.print_book()
    
    else:
        #sorting the book_list so that the display is always consistent with the flag
        data_set.books_list = data_set.books(sort_by = arguments.by_year)
        for book in data_set.books_list:
            book.print_book()


if __name__ == '__main__':
    main()