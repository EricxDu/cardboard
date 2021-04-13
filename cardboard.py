#!/usr/bin/env python3
'''
Copyright 2021 Eric Duhamel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import datetime
import os
import random
import re
import shutil
import sys

def main():
    path = os.getcwd()
    cardboard = Cardboard()
    list = ()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        splitted = filename.split(".")
        if "deck" in splitted and "m3u" in splitted:
            print("Constructing a deck from " + filename)
            list = cardboard.list_deck(filename)
            copy_cards(list, ".deck")
        elif "set" in splitted and "m3u" in splitted:
            print("Grabbing 15 boosters from " + filename)
            list = cardboard.list_draft(filename)
            copy_cards(list, ".draft")
        elif os.path.isdir(filename):
            if "deck" in splitted:
                print("Drawing 7 cards from " + filename)
                list = cardboard.get_hand(filename)
                move_cards(list, "YOURHAND")
    else:
        print("Invoked: " + sys.argv[0])
        print("Please provide an m3u file or a folder containing card images")
        print("I will create a .deck folder from a .deck.m3u file")
        print("I will create a .draft folder from a .set.m3u file")
        print("I will move cards from a .deck folder to YOURHAND")

def copy_cards(list, ext):
    isotime = datetime.datetime.now().replace(microsecond=0).isoformat()
    stamp = "".join(re.split("-|T|:", isotime))
    fname = stamp + ext
    if not os.path.isdir(os.path.join(os.getcwd(), fname)):
        print("cardboard: creating folder " + fname)
        os.mkdir(os.path.join(os.getcwd(), fname))
    print("cardboard: copying " + str(len(list)) + " cards to " + fname)
    for i, path in enumerate(list):
        filename = os.path.basename(path)
        name, ext = filename.rsplit(".", 1)
        filename = name + " (" + str(i+1) + ")" + "." + ext
        # should the following paths be absolutized?
        shutil.copy(path, os.path.join(fname, filename))

def move_cards(list, folder):
    if not os.path.isdir(os.path.join(os.getcwd(), folder)):
        print("cardboard: creating folder " + folder)
        os.mkdir(os.path.join(os.getcwd(), folder))
    print("cardboard: moving " + str(len(list)) + " cards to " + folder)
    for i, path in enumerate(list):
        filename = os.path.basename(path)
        shutil.move(path, os.path.join(folder, filename))

def make_list(filename, list):
    f = open(filename, "w")
    for path in list:
        f.write(path + "\n")

class Cardboard():
    def __init__(self):
        return None

    def list(self, path):
        f = open(path, "r")
        list = []
        for path in f.readlines():
            name = path.split("\n")[0]
            list.append(name)
        return list

    def list_deck(self, path):
        ''' Take a decklist and return all the cards.'''
        list = self.list(path)
        return list

    def list_draft(self, path, spread="UUUURCCCCCCCCCC"):
        ''' Take a setlist and open pack of booster cards.

            This method can draw multiples of the same card from a list
            because it is drafting from a randomized booster pack.'''
        list = self.list(path)
        draft_list = []
        for i, rarity in enumerate(spread):
            draft_list.append(random.choice(list))
        return draft_list

    def get_hand(self, filepath, many=7):
        ''' Take a decklist and draw a hand of cards from it.

            This method can only return one of each card in a list
            because it's drawing from a virtual deck of cards.'''
        set_list = self.get_list(filepath)
        draft_list = []
        for i in range(many):
            if len(set_list) > 0:
                card = set_list.pop(random.randrange(len(set_list)))
                draft_list.append(card)
        return draft_list

    def get_list(self, path, ext="gif png"):
        extens = ext.split(" ")
        list = []
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for name in files:
                    splitted = name.split(".")
                    if splitted[len(splitted)-1] in extens:
                        list.append(os.path.join(path, name))
        return list


if __name__ == "__main__":
    main()
    sys.exit()
