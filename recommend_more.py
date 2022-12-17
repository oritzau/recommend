import numpy as np
import csv
import os
from getpass import getpass

class Book:
    def __init__(self, author, title) -> None:
        self.title = title
        self.author = author
def is_guest(username):
    if username.lower() == "guest":
        return True
    else:
        return False

def read_books(file_name):
    book_list = []
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            a, b = line.split(',')[0], line.split(',')[1]
            b = b.replace('\n', '')
            temp_book = Book(a, b)
            book_list.append(temp_book)
    return book_list

def read_ratings(file_name):
    with open(file_name) as file:
        ratings = list(csv.reader(file))
        ratings_data = np.array(ratings)
        ratings_data = np.transpose(ratings_data)
        name_tuple = tuple(ratings_data[0, :])
        final_ratings_data = ratings_data[1:, :].astype(int)
    return name_tuple, final_ratings_data

# #Task 5
def recommend(reader):
    similarity_list = []
    for row in user_ratings:
        similarity = np.dot(user_ratings[reader], row)
        similarity_list.append(similarity)
    similarity_second_max = sorted(similarity_list)[-2]
    similarity_max_index = similarity_list.index(similarity_second_max)
    return similarity_max_index
    
def recommend_more(reader):
    similarity_list = []
    indices_list = []
    for row in user_ratings:
        similarity = np.dot(user_ratings[reader], row)
        similarity_list.append(similarity)
    for item in sorted(similarity_list)[-6:-1]:
        index = similarity_list.index(item)
        indices_list.append(index)
    return reversed(indices_list)

if __name__ == '__main__':
    os.system('clear')
    book_list = read_books('books.txt')
    names, ratings = read_ratings('ratings.csv')
    user_ratings = np.transpose(ratings)
    user_not_done = True
    user_not_in_list = True
    while True:
        username = input("Username: ")
        if username.lower() == "guest":
            break
        password = getpass()
        if username in names:
            if password == "Password!":
                break
    print("Welcome to Recommend. Type a username to get started or type 'done' to exit.", end = '\n'*2)
    while user_not_done:
        recommended_list = []
        while user_not_in_list:
            if is_guest(username):
                for n, name in enumerate(names):
                    if (n % 8 == 0 and n > 0) or n == (len(names) - 1):
                        print(name)
                    else:
                        print(name + ',', end = ' ')
                    
                suggestions_for = input("Enter Username or type 'done' to exit: ")
                if suggestions_for in names or suggestions_for.lower() == 'done':
                    user_not_in_list = False
                if suggestions_for.lower() == 'done':
                    user_not_done = False
                elif suggestions_for not in names:
                    os.system('clear')
                    print("Sorry, that name is not in our library. Enter a username from below or type 'done'.", end = '\n' * 2)
            else:
                suggestions_for = username
                user_not_in_list = False
        try:
            suggestion_for_index = names.index(suggestions_for)
            for suggestion_to_index in recommend_more(suggestion_for_index):
                for a, b in enumerate(user_ratings[suggestion_to_index]):
                    if user_ratings[suggestion_for_index][a] == 0 and (len(recommended_list) < 5):
                        if user_ratings[suggestion_to_index][a] == 5:
                            if a not in recommended_list:
                                recommended_list.append(a)
            os.system('clear')
            if is_guest(username):
                print(f'For {suggestions_for} we recommend:')
            else:
                print("For you we recommend:")
            for book_index in recommended_list:
                print(book_list[book_index].title)
            print()
            if is_guest(username):
                user_not_in_list = True
            else:
                not_done = True
                while not_done:
                    more_info = input("'?' for more info, or type 'done' to exit. ")
                    print()
                    if more_info == '?':
                        for book_index in recommended_list:
                            print(f'{book_list[book_index].title}, {book_list[book_index].author}')
                    elif more_info.lower() == "done":
                        break
                    else:
                        continue
                break
            if suggestions_for.lower() == 'done':
                user_not_done = False
        except ValueError:
            if suggestions_for.lower() == 'done':
                print('Thank you for using Recommend.', end = '\n' * 2)
                user_not_done = False
        
