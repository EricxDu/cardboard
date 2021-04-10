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

import os
import random
import sys

def main():
    path = os.getcwd()
    cardboard = Cardboard()
    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + " draft filename.m3u")
        print("       " + sys.argv[0] + " draw filename.m3u")
        print("       " + sys.argv[0] + " make .ext\n")
        print("Note: make generates m3u files for all subfolders, so be careful")
    else:
        filepath = os.path.join(path, sys.argv[2])
        if sys.argv[1] == "draft":
            list = cardboard.get_draft(filepath)
        elif sys.argv[1] == "draw":
            list = cardboard.get_draw(filepath)
        elif sys.argv[1] == "make":
            list = makelists(path, sys.argv[2])
        for name in list:
            print(name)

def makelists(path, ext):
    list = []
    for root, dirs, files in os.walk(path):
        for i, set_name in enumerate(dirs):
            set_path = os.path.join(path, set_name)
            for root, dirs, files in os.walk(set_path):
                set_filename = set_name.replace(" ", "") + ".m3u"
                f = open(set_filename, "w")
                for card_name in files:
                    if card_name.endswith(ext):
                        f.write(os.path.join(set_path, card_name) + "\n")
                        list.append(card_name)
    return list


class Cardboard():
    def __init__(self):
        return None

    def get_draft(self, filepath, spread="UUUURCCCCCCCCCC"):
        ''' Take a setlist and open pack of booster cards.

            This method can draw multiples of the same card from a list
            because it is drafting from a randomized booster pack.'''
        set_list = self.get_list(filepath)
        draft_list = []
        for i, rarity in enumerate(spread):
            draft_list.append(random.choice(set_list))
        return draft_list

    def get_draw(self, filepath, many=7):
        ''' Take a decklist and draw a hand of cards from it.

            This method can only return one of each card in a list
            because it's drawing from a virtual deck of cards.'''
        set_list = self.get_list(filepath)
        draft_list = []
        for i in range(many):
            draft_list.append(random.choice(set_list))
        return draft_list

    def get_list(self, filepath):
        f = open(filepath, "r")
        set_list = []
        for filepath in f.readlines():
            set_list.append(filepath.split("\n")[0])
        return set_list


if __name__ == "__main__":
    main()
    quit()
