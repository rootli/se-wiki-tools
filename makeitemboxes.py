### Reads Item table: tabbed CSV file containing Space Engineers v206 game data.
### Converts item info fields into mediawiki template syntax and outputs them as text file.
### By AdaRynin https://github.com/rootli

import copy # for complex dict
from time import localtime, strftime # just for output file timestamp
now = strftime("%Y%m%d-%H%M%S", localtime())

wikitemboxpfad="SEWikiGGItemBoxes"+now+".txt" # output file
spreadsheet_path="SE_Items.csv" #input file
table_header=["title","image","caption","type","mass","volume","craft","price","hitpoints","nutrition","healing","ammo","damage","firerate","trigger","reload","range","spread","speed","reach"]
debugmode=True
def debugprint(s):
    if(debugmode):
        print(s)
 
content={}  # temp var in loop, needs copy()
itemdict={} # result var
firstRow=True # to skip table header

def lookUpColumn(linesplit,columnName):
    datacell = linesplit[table_header.index(columnName)]
    if( datacell and datacell != "N/A"):
        return datacell
    else:
        return ''

def saveOneSetOfDataPoints(uiname,linesplit):
    '''
    nimmt item info, extrahiert zeile, speichert Wert im dict unter key
    "item name \t data0 \t data1 \t data2 \t data3"    
    '''
    content["title"]=lookUpColumn(linesplit,'title')
    content["image"]=lookUpColumn(linesplit,'image')
    content["caption"]=lookUpColumn(linesplit,'caption')
    content["type"]=lookUpColumn(linesplit,'type')
    content["mass"]=lookUpColumn(linesplit,'mass')
    content["volume"]=lookUpColumn(linesplit,'volume')
    content["price"]=lookUpColumn(linesplit,'price')
    content["craft"]=lookUpColumn(linesplit,'craft') 
    content["hitpoints"]=lookUpColumn(linesplit,'hitpoints')
    content["nutrition"]= lookUpColumn(linesplit,'nutrition')
    content["healing"]=lookUpColumn(linesplit,'healing')
    content["ammo"]=lookUpColumn(linesplit,'ammo')
    content["damage"]=lookUpColumn(linesplit,'damage')
    content["firerate"]=lookUpColumn(linesplit,'firerate')
    content["trigger"]=lookUpColumn(linesplit,'trigger')
    content["reload"]=lookUpColumn(linesplit,'reload')
    content["range"]=lookUpColumn(linesplit,'range')
    content["spread"]=lookUpColumn(linesplit,'spread')
    content["speed"]=lookUpColumn(linesplit,'speed')
    content["reach"]=lookUpColumn(linesplit,'reach')

print("Reading from "+spreadsheet_path)
with open(spreadsheet_path,'r') as fin:
    lines = fin.readlines()
    for line in lines:
        #skip table header 
        if(not firstRow):
            # alle Spalten des items als Liste
            linesplit=line.split('\t')
            title=lookUpColumn(linesplit,'title')
            debugprint("processing ..." +title)
            content={} #reset
            # mapping (geht wahrscheinlich eleganter...)
            saveOneSetOfDataPoints('title',linesplit) # inits content
            itemdict[title]=content.copy() # copy() and create key
        firstRow=False #skipped table header 

debugprint(itemdict)


longtemplate = """{{Item Box
|title=%s 
|image=%s 
|caption=%s 
|type=%s 
|mass=%s 
|volume=%s 
|price=%s 
|craft=%s 
|hitpoints=%s 
|nutrition=%s 
|healing=%s 
|ammo=%s 
|damage=%s 
|firerate=%s 
|trigger=%s 
|reload=%s 
|range=%s 
|spread=%s 
|speed=%s 
|reach=%s 
}}
""" 

# Wiki syntax generieren.
with open(wikitemboxpfad, "a") as wikitems:
    itemdict_sorted=dict(sorted(itemdict.items()))
    for title,entry in itemdict_sorted.items():
        debugprint(entry)
        ### Neue Eintraege hier hinzu, in der Reihenfolge der %s im Template!
        wikitems.write("\n"+longtemplate% (title,entry['image'],entry['caption'],
                                              entry['type'],entry['mass'],entry['volume'],entry['price'],
                                              entry['craft'],entry['hitpoints'],entry['nutrition'],
                                              entry['healing'],entry['ammo'],entry['damage'],
                                              entry['firerate'],entry['trigger'],entry['reload'],
                                              entry['range'],entry['spread'],entry['speed'],entry['reach']))
        wikitems.write("\n")
print("Done. Output in "+wikitemboxpfad)
