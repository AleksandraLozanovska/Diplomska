import csv
import pandas



class Movie:
    def __init__(self, id, title, uri, genre):
        self.id = id
        self.title = title
        self.uri = uri
        self.genre = genre

#
def MovieList():
    list = []
    with open('FinalBaza1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        count = 0
        for row in csv_reader:
            if count != 0:
                m = Movie(row[0], row[1], row[2], row[3])
                list.append(m)
            count += 1
    return list




