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
            list = cardboard.get_deck_from_list(filename)
            make_folder("DECK", list)
        elif os.path.isdir(filename):
            if filename.find("DECK") >= 0:
                list = cardboard.get_hand(filename)
                make_folder("HAND", list)
            else:
                list = cardboard.get_draft(filename)
                make_folder("DRAFT", list)
    else:
        print("Please provide an m3u file or a folder containing card images")
        print("I will create a deck for you from a .deck.m3u file")
        print("I will move cards from a DECK folder to your HAND")
        print("I will copy a draft of cards from any other folder")

def make_folder(prefix, list):
    isotime = datetime.datetime.now().replace(microsecond=0).isoformat()
    folder = prefix + "".join(re.split("-|T|:", isotime))
    os.mkdir(os.path.join(os.getcwd(), folder))
    for i, path in enumerate(list):
        splitted = os.path.split(path)
        filename = splitted[len(splitted)-1]
        if prefix == "HAND":
            shutil.move(path, os.path.join(folder, filename))
        else:
            name, ext = filename.rsplit(".", 1)
            filename = name + " (" + str(i+1) + ")" + "." + ext
            shutil.copy(path, os.path.join(folder, filename))
    print("Created " + folder)

def make_list(filename, list):
    f = open(filename, "w")
    for path in list:
        f.write(path + "\n")

class Cardboard():
    def __init__(self):
        return None

    def list(self, filepath):
        f = open(filepath, "r")
        set_list = []
        for filepath in f.readlines():
            set_list.append(filepath.split("\n")[0])
        return set_list

    def get_deck_from_list(self, path):
        ''' Take a decklist and return all the cards.'''
        list = self.list(path)
        return list

    def get_draft(self, filepath, spread="UUUURCCCCCCCCCC"):
        ''' Take a setlist and open pack of booster cards.

            This method can draw multiples of the same card from a list
            because it is drafting from a randomized booster pack.'''
        set_list = self.get_list(filepath)
        draft_list = []
        for i, rarity in enumerate(spread):
            draft_list.append(random.choice(set_list))
        return draft_list

    def get_hand(self, filepath, many=7):
        ''' Take a decklist and draw a hand of cards from it.

            This method can only return one of each card in a list
            because it's drawing from a virtual deck of cards.'''
        set_list = self.get_list(filepath)
        draft_list = []
        for i in range(many):
            draft_list.append(random.choice(set_list))
        return draft_list

    def get_list(self, path, ext="gif png"):
        extens = ext.split(" ")
        if os.path.isdir(path):
            list = []
            for root, dirs, files in os.walk(path):
                for name in files:
                    splitted = name.split(".")
                    if splitted[len(splitted)-1] in extens:
                        list.append(os.path.join(path, name))
        return list


if __name__ == "__main__":
    main()
    quit()
