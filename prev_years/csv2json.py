#!/usr/bin/python

import json, csv, time
from collections import defaultdict

def json_convert(csv_file):
    infile = open(csv_file)
    reader = csv.reader(infile)
    d_list = defaultdict(list)
    dict = {}
    row1 = next(reader)

    for x in reader:
        distance = float(x[2])
        d=x[0]
        p='%Y-%m-%d'
        epoch = int(time.mktime(time.strptime(d,p)) * 1000) 
        tuplist = [epoch,distance]
        name = x[1]
        d_list[name].append(tuplist)

    friend_colour_dict = {}
    friend_colour_file = open('../friend_colour_new.csv')
    colourreader = csv.DictReader(friend_colour_file)
    for line in colourreader:
        friend_colour_dict[line["name"]] = line["colour"]

    outfile = open(csv_file.replace('.csv', '.json'), 'w')
    outfile.write('['+'\n')

    trimmed_d_list = {}
    for name,tuples in d_list.items():
        if name in friend_colour_dict:
            trimmed_d_list[name] = tuples

    for name,tuples in trimmed_d_list.items()[:-1]:
        if name in friend_colour_dict:
            singlenamedic = {}
            singlenamedic["key"] = name
            singlenamedic["values"] = tuples
            singlenamedic["color"] = '#'+str(friend_colour_dict[name])
            json.dump(singlenamedic, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
            outfile.write(','+ '\n')

    for name,tuples in trimmed_d_list.items()[-1:]:
        if name in friend_colour_dict:
            singlenamedic = {}
            singlenamedic["key"] = name
            singlenamedic["values"] = tuples
            singlenamedic["color"] = '#'+str(friend_colour_dict[name])
            json.dump(singlenamedic, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
            outfile.write('\n')

    outfile.write('\n'+']')
    outfile.close()   

        
def main():
    json_convert('distance2017.csv')
           

if __name__ == "__main__":
  main()
