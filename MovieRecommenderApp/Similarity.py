import pandas as pd
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDFS,FOAF,OWL
from langdetect import detect
from DataMovies import MovieList
import nltk

MovieList = MovieList()
def similar(title):
    similarMovie=""
    #Find the selected movie from the movie list
    for movie in MovieList:
        if movie.title == title:
            myTitle = movie.title
            myUri = movie.uri
            myGenres = movie.genre.split()

    #Compare with the rest of the movies by genre
    sameGenres = []
    for movie in MovieList:
        if myTitle != movie.title:
            gen = []
            gen = movie.genre.split()
            if set(myGenres) == set(gen):
                sameGenres.append(movie.uri)
    #If there are other movies with the same genre
    if len(sameGenres) != 0:
        myAbstract = ""
        myDirector = ""
        obj = ""
        obje = ""
        #najdi gi directors i abstract
        g = globals()
        i = 0
        director = URIRef("http://dbpedia.org/ontology/director")
        directors_dict = {}
        abstract = URIRef("http://dbpedia.org/ontology/abstract")
        abstract_dict = {}
        for sg in sameGenres:
            graph = Graph()
            graph.parse(sg)
            for s, p, o in graph.triples((None, director, None)):
                obj = o.encode('utf-8')
            directors_dict[sg] = obj
            for s, p, o in graph.triples((None, abstract, None)):
                if detect(o) == 'en':
                    obje = o.encode('utf-8')
            abstract_dict[sg] = obje
            g['graph_{0}'.format(i)] = graph
            i += 1

        #najdi go mojot abstract i director
        myGraph = Graph()
        myGraph.parse(myUri)
        for s, p, o in myGraph.triples((None, director, None)):
            obj = o.encode('utf-8')
        myDirector = obj
        for s, p, o in myGraph.triples((None, abstract, None)):
            if detect(o) == 'en':
                obje = o.encode('utf-8')
                myAbstract = obje

        #lista dali ima filmovi so ist director kako mojot
        sameDirector = []
        for key in directors_dict.keys():
            if myDirector == directors_dict[key]:
                sameDirector.append(key)

        max_similarity = 0
        maxsimURI = ""
        if len(sameDirector) != 0:
            #ako ima filmovi so ist director kako mojot
            for sd in sameDirector:
                #najdi go abstractot za sekoj od listata na sameDirector vo dic od abstracti so ist genre i najdi max jaccard similarity
                for key in abstract_dict.keys():
                    if sd == key:
                        similarity = nltk.jaccard_distance(set(myAbstract.split()), set(abstract_dict[key].split()))
                        if similarity > max_similarity:
                            max_similarity = similarity
                            maxsimURI = key
            for movie in MovieList:
                if maxsimURI == movie.uri:
                    similarMovie = movie.title

        #ako nema ist director a ima ist genre
        else:
            #sekoj abstract od same genre najdi max jaccard similarity so mojot film
            for key in abstract_dict.keys():
                    similarity = nltk.jaccard_distance(set(myAbstract.split()), set(abstract_dict[key].split()))
                    if similarity > max_similarity:
                        max_similarity = similarity
                        maxsimURI = key
            for movie in MovieList:
                if maxsimURI == movie.uri:
                    similarMovie = movie.title

    #ako nema drug film so ist genre kako selektiraniot(mojot)
    else:
        myAbstract = ""
        myDirector = ""
        obj = ""
        obje = ""
        g = globals()
        i = 0
        director = URIRef("http://dbpedia.org/ontology/director")
        directors_dict = {}
        abstract = URIRef("http://dbpedia.org/ontology/abstract")
        abstract_dict = {}
        for ml in MovieList:
            if myTitle != ml.title:
                graph = Graph()
                graph.parse(ml.uri)
                for s, p, o in graph.triples((None, director, None)):
                    obj = o.encode('utf-8')
                directors_dict[ml.uri] = obj
                for s, p, o in graph.triples((None, abstract, None)):
                    if detect(o) == 'en':
                        obje = o.encode('utf-8')
                abstract_dict[ml.uri] = obje
                g['graph_{0}'.format(i)] = graph
                i += 1

        # najdi go mojot abstract i director
        myGraph = Graph()
        myGraph.parse(myUri)
        for s, p, o in myGraph.triples((None, director, None)):
            obj = o.encode('utf-8')
        myDirector = obj
        for s, p, o in myGraph.triples((None, abstract, None)):
            if detect(o) == 'en':
                obje = o.encode('utf-8')
                myAbstract = obje

        # lista dali ima filmovi so ist director kako mojot
        sameDirector = []
        for key in directors_dict.keys():
            if myDirector == directors_dict[key]:
                sameDirector.append(key)

        max_similarity = 0
        maxsimURI = ""
        if len(sameDirector) != 0:
            # ako ima filmovi so ist director kako mojot
            for sd in sameDirector:
                # najdi go abstractot za sekoj od listata na sameDirector vo dic od abstracti so ist genre i najdi max jaccard similarity
                for key in abstract_dict.keys():
                    if sd == key:
                        similarity = nltk.jaccard_distance(set(myAbstract.split()), set(abstract_dict[key].split()))
                        if similarity > max_similarity:
                            max_similarity = similarity
                            maxsimURI = key
            for movie in MovieList:
                if maxsimURI == movie.uri:
                    similarMovie = movie.title

        # ako nema ist director
        else:
            # sekoj abstract najdi max jaccard similarity so mojot film
            for key in abstract_dict.keys():
                similarity = nltk.jaccard_distance(set(myAbstract.split()), set(abstract_dict[key].split()))
                if similarity > max_similarity:
                    max_similarity = similarity
                    maxsimURI = key
            for movie in MovieList:
                if maxsimURI == movie.uri:
                    similarMovie = movie.title



    return (similarMovie)









