#Algo Integration
import pathlib
import codecs

from tabulate import tabulate
from SPARQLWrapper import SPARQLWrapper, JSON


def executeSparqlQuery(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def insertColumnDf(listProposition, column,columnValues):
    index = column.rfind('/')
    tmpColumn = column[index + 1:]
    listColumnName = list()

    for columnValue in columnValues:
        columnValue = str(columnValue)
        index = columnValue.rfind('/')
        tmpcolumnValue = columnValue[index + 1:]
        listColumnName.append(tmpcolumnValue)

    listColumnNameProposition = list()
    for proposition in listProposition:
        index = proposition.rfind('/')
        tmpproposition = proposition[index + 1:]
        listColumnNameProposition.append(tmpproposition)
    if tmpColumn not in listColumnNameProposition and tmpColumn not in listColumnName:
        return column

def insertDataDf(df, results, i, item):
    for result in results["results"]["bindings"]:
        predicate = result["object"]["value"]
        #print(predicate)
        if len(str(df.at[i, item])) == 4:
            df.at[i, item] = str(df.at[i, item]).replace("<NA>", "")
        elif len(str(df.at[i, item])) == 3:
            df.at[i, item] = str(df.at[i, item]).replace("nan", "")
            # print(df.at[i, item])
            # print(len(str(df.at[i, item])))
        df.at[i, item] = str(df.at[i, item]) + str(predicate) + " "
    return df

def printDf(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))
    df.to_csv(r'Final Dataset.csv',index=False)
    df.to_excel(r'Final Dataset.xlsx', index=False)

def writeHtmlFile(final_col, final_cta, final_cpa, final_cea, path_filename, path_filename_full):
    i = 0
    nodes = []
    graphNodesContent = ""
    graphLinksContent = ""
    subjectColumnId = ""
    grapheFile = ""
    grapheFileFull = ""
    graphFullNodesContent = ""
    graphFullLinksContent = ""
    sourceIDs = []
    links = ["#"]
    linkNames = [""]

    for col in final_col:
        name = col.split("$")[0]
        id = col
        sourceIDs.append(id)
        nodes.append(id)
        hlink = "#"
        if len(final_cta[i]) > 0:
            cta = final_cta[i][0]
            hlink = cta.split("$")[1]
            name += " ("+hlink.rsplit('/', 1)[-1]+")"
        if i == 0:
            subjectColumnId = id
            graphNodesContent += '{"id": "'+id+'", "name": "'+name+'", "x": 10, "y": 0, "type": "Subject Column", "hlink": "'+hlink+'"},\n'
        else:
            graphNodesContent += '{"id": "'+id+'", "name": "'+name+'", "type": "CTA", "hlink": "'+hlink+'"},\n'

        if i != 0:
            cpa = final_cpa[i]
            if cpa == "":
                linkNames.append("")
                links.append("")
            if cpa != "":
                sp = cpa.split("$")
                linkName = sp[0]
                hlink = sp[1]
                linkName += " ("+hlink.rsplit('/', 1)[-1]+")"
                targetId = id
                linkNames.append(linkName)
                links.append(hlink)
                graphLinksContent += '{"sourceId": "'+subjectColumnId+'", "linkName": "'+linkName+'", "targetId": "'+targetId+'", "hlink": "'+hlink+'"},\n'
        i = i + 1
    graphFullNodesContent = graphNodesContent
    graphFullLinksContent = graphLinksContent

    graphNodesContent = graphNodesContent[:-2]+'\n'
    graphLinksContent = graphLinksContent[:-2]+'\n'

    grapheFile = '{\n ' + '"nodes":[\n'+ graphNodesContent + '],\n' + '"links": [\n' + graphLinksContent + ']\n}'

    for row in final_cea:
        i = 0
        subjCol = ""
        for cell in row:
            sp = cell.split("$")
            name = sp[0]
            hlink = sp[1]
            id = name
            if hlink != "#":
                id = hlink
                name += " ("+hlink.rsplit('/', 1)[-1]+")"

            if i == 0:
                subjCol = id

            if id not in nodes:
                nodes.append(id)
                graphFullNodesContent += '{"id": "'+id+'", "name": "'+name+'", "type": "CEA", "hlink": "'+hlink+'"},\n'
                graphFullLinksContent += '{"sourceId": "'+sourceIDs[i]+'", "linkName": "", "targetId": "'+id+'", "hlink": "#"},\n'

                if i > 0 and linkNames[i] != "":
                    graphFullLinksContent += '{"sourceId": "'+subjCol+'", "linkName": "'+linkNames[i]+'", "targetId": "'+id+'", "hlink": "'+links[i]+'"},\n'

            i = i + 1

    graphFullNodesContent = graphFullNodesContent[:-2]+'\n'
    graphFullLinksContent = graphFullLinksContent[:-2]+'\n'

    grapheFileFull = '{\n ' + '"nodes":[\n'+ graphFullNodesContent + '],\n' + '"links": [\n' + graphFullLinksContent + ']\n}'


    ROOT_DIR = path_filename
    #f = open(ROOT_DIR, "a")
    f = codecs.open(ROOT_DIR, "w", "utf-8")
    f.seek(0)                        # <- This is the missing piece
    f.truncate()
    f.write(grapheFile)
    f.close()

    ROOT_DIR = path_filename_full
    #f = open(ROOT_DIR, "a")
    f = codecs.open(ROOT_DIR, "w", "utf-8")
    f.seek(0)                        # <- This is the missing piece
    f.truncate()
    f.write(grapheFileFull)
    f.close()

    return subjectColumnId
