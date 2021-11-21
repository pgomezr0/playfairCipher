#!/usr/bin/env python

'''
Created 19 Nov 2021
@author: pgomezr0
'''
# COMPUTER SECURITY ASSIGNMENT 1 EXERCISE 2 - ENCRYPT EXTENDED
# Author: Paola Gomez Reyna

import string


def generate_key_grid(key):

    alphabet = string.ascii_uppercase.replace(
        'J', '.') + string.digits  # Letters and digits
    i_key_grid = ['' for i in range(7)]

    i = 0
    j = 0

    for character in key:
        if character == 'J':
            if 'I' not in i_key_grid:
                i_key_grid[i] += 'I'
                j += 1

        elif character in alphabet:
            i_key_grid[i] += character
            alphabet = alphabet.replace(character, '.')  # . for used
            j += 1

            # Once row has been filled, start to new one
            if j > 4:
                i += 1
                j = 0

    # Fill remaining grid with the unused letters of the alphabet
    in_key_grid = 'I' in i_key_grid

    for character in alphabet:
        if character == 'I' and in_key_grid:
            pass
        elif character != '.':
            i_key_grid[i] += character
            j += 1

            # Once row has been filled, move to new one
            if j > 4:
                i += 1
                j = 0

    # Separate letters in matrix
    key_grid = []
    for row in i_key_grid:
        key_grid.append(list(row))

    return key_grid


def index_find(letter, key_matrix):
    letter_coordinate = []

    # convert the character value from J to I
    if letter == 'J':
        letter = 'I'

    # Indexes the key grid by row
    for i, j in enumerate(key_matrix):
        for m, n in enumerate(j):
            if letter == n:
                letter_coordinate.append(i)
                letter_coordinate.append(m)
                return letter_coordinate


# Encrypts plaintext using Playfair Cipher
def encrypt(text, key):

    encrypted_text = []

    # Create Key Square 5x7 grid
    key_grid = generate_key_grid(key)

    diagraphs = []
    # Rule 1: If both letters are the same (or only one letter is left), add an "X" after the first letter.
    i = 0  # Location of character in text
    while i < len(text):
        char1 = text[i]
        char2 = ''

        if (i + 1) == len(text):  # text with only two letters
            char2 = 'X'
        else:
            char2 = text[i+1]

        if char1 == char2:
            diagraphs.append(char1 + 'X')
            i += 1
        else:
            diagraphs.append(char1+char2)
            i += 2

    diagraphs = ''.join(diagraphs)

    i = 0

    while i < len(diagraphs):

        # Coordinate with format: (row, column)
        n1 = index_find(diagraphs[i], key_grid)  # (n1[0], n1[1])
        n2 = index_find(diagraphs[i+1], key_grid)  # (n2[0], n2[1])

        # Rule 2: If pair of letters (diagraph) appear on the same column of key grid, take letter below
        # each one (going back to the top if at the bottom
        if n1[1] == n2[1]:
            i1 = (n1[0] + 1) % 5
            j1 = n1[1]

            i2 = (n2[0] + 1) % 5
            j2 = n2[1]
            encrypted_text.append(key_grid[i1][j1])
            encrypted_text.append(key_grid[i2][j2])
            encrypted_text.append(' ')

        # Rule 3: If a pair of letters (diagraph) appears on the same row of key grid take the letter to the
        # right of each one (going back to the leftmost if at the rightmost position)
        elif n1[0] == n2[0]:
            i1 = n1[0]
            j1 = (n1[1] + 1) % 7

            i2 = n2[0]
            j2 = (n2[1] + 1) % 7
            encrypted_text.append(key_grid[i1][j1])
            encrypted_text.append(key_grid[i2][j2])
            encrypted_text.append(' ')

        # if making rectangle then
        # [5,2]
        # [1,6] => [5,6]
        #          [2,1]
        # exchange columns of both values
        else:
            i1 = n1[0]
            j1 = n1[1]

            i2 = n2[0]
            j2 = n2[1]

            encrypted_text.append(key_grid[i1][j2])
            encrypted_text.append(key_grid[i2][j1])
            encrypted_text.append(' ')

        i += 2

    encrypted_text = ''.join(encrypted_text)
    return encrypted_text


def main():

    print('\n********* PLAYFAIR CIPHER EXTENDED ENCRYPTION ************\n')

    user_text = input("Input PLAINTEXT and press ENTER once you're done: ")
    user_key = input(
        "Input a KEY (numbers or words) and press ENTER once you're done: ")

    user_text = user_text.replace(' ', '').upper()
    user_key = user_key.replace(' ', '').upper()

    encrypted_message = encrypt(user_text, user_key)

    file_encrypted = open('ciphertext_playfair_extended.txt', 'w')
    file_encrypted.write(encrypted_message)
    file_encrypted.close()

    print('\nThe message has been encrypted.')
    print('The ciphertext has been stored in a .txt file in the current folder.\n')


if __name__ == "__main__":
    main()
