### Reads output of rocket-science.py: CSV file containing Space Engineers v205 game data.
### Converts block recipe fields into mediawiki syntax and outputs them as text file.
### By AdaRynin https://github.com/rootli

### Place CSV file into same directory.
### Example for output:
'''
{{Recipeinfo
|product=Some Block Name
|component1=Construction Comp.
  |optional1=5
  |required1=5
  |smloptional1=5
  |smlrequired1=5
|component2=Interior Plate
  |required2=10
  |smlrequired2=10
}}
'''

import copy # for complex dict
from time import localtime, strftime # just for output file timestamp
now = strftime("%Y%m%d-%H%M%S", localtime())

wikirezeptepfad="SEWikiGGRezepte"+now+".txt" # output file
spreadsheet_path="SE_Block_Info.csv" # input file
table_header=["blockname","type_id","subtype_id","grid_size","armor_type","mass","blockCategory",
              "hitpoints","size_HWD","volume","build_time_secs","pcu_pc","pcu_console",
              "airtightness","rangeMaxMeters","powerDrainBroadcastMaxkW",
              "powerInRequired","powerInIdle","powerOutMax","powerConsumeOperational",
              "powerConsumeStandby", "powerConsumeMax","powerConsumeMin",
              "recipe_SteelPlate","recipe_MetalGrid","recipe_Construction",
              "recipe_LargeTube","recipe_Thrust","recipe_Motor","recipe_Reactor",
              "recipe_BulletproofGlass","recipe_Computer","recipe_Detector",
              "recipe_Display","recipe_Explosives","recipe_Girder",
              "recipe_GravityGenerator","recipe_InteriorPlate","recipe_SmallTube",
              "recipe_Medical","recipe_SolarCell","recipe_Superconductor",
              "recipe_RadioCommunication","recipe_ZoneChip","recipe_PowerCell",
              "recipe_EngineerPlushie","recipe_SabiroidPlushie","recipe_SteelPlate_optional",
              "recipe_MetalGrid_optional","recipe_Construction_optional",
              "recipe_LargeTube_optional","recipe_Thrust_optional","recipe_Motor_optional",
              "recipe_Reactor_optional","recipe_BulletproofGlass_optional",
              "recipe_Computer_optional","recipe_Detector_optional","recipe_Display_optional",
              "recipe_Explosives_optional","recipe_Girder_optional",
              "recipe_GravityGenerator_optional","recipe_InteriorPlate_optional",
              "recipe_SmallTube_optional","recipe_Medical_optional",
              "recipe_SolarCell_optional","recipe_Superconductor_optional",
              "recipe_RadioCommunication_optional","recipe_ZoneChip_optional",
              "recipe_PowerCell_optional","recipe_PrototechFrame","recipe_PrototechPanel",
              "recipe_PrototechCapacitor","recipe_PrototechPropulsionUnit",
              "recipe_PrototechMachinery","recipe_PrototechCircuitry","recipe_PrototechCoolingUnit",
              "mountpoint_Front","mountpoint_Back","mountpoint_Left",
              "mountpoint_Right","mountpoint_Bottom","mountpoint_Top","DLC","Icon","standalone",
              "ForceMagnitude","FlameDamageLengthScale","FlameDamage","DeformationRatio",
              "MinPlanetaryInfluence","MaxPlanetaryInfluence","EffectivenessAtMinInfluence",
              "EffectivenessAtMaxInfluence","description","hasPhysics"]

debugmode=False
def debugprint(s):
    if(debugmode):
        print(s)

content={}  # a temp var in loop, needs copy()!!
blockdict={} # result dict to be generated, 
firstRow=True # used to skip the table header

def lookUpColumn(linesplit,columnName):
    '''Linesplit ist "Komponentenname \t Large oder Small \t req oder opt"'''
    return linesplit[table_header.index(columnName)]

def saveOneRow(uiname,dataname,linesplit,opt):
    '''
    Fuegt dem lookup blockdict einen Eintrag hinzu.
    Nimmt Blockinfo, extrahiert Zeile, speichert Wert im blockdict unter key
    Linesplit ist "Komponentenname \t Large oder Small \t req oder opt"
    '''
    gridsize=lookUpColumn(linesplit,'grid_size')
    content[uiname+"\t"+gridsize+"\t"+opt] = lookUpColumn(linesplit,dataname)

### In der Wikitabelle fuer das Rezept gibt es pro Komponente nur eine Zeile
### mit Spalten fuer Large/Small, Opt/Req. Komponentenzeilen haben indices
### in der Wikisyntax, die Spalten fuer Large/Small und Opt/Req brauchen bloss
### den selben Index haben.
### Der folgende Check verhindert im Output duplizierte Zeilen und appendet:

CompLinesPrinted=[]

ComponentIndex=1 # wird auch in einer Schleife resettet

def thisCompLineWasAlreadyPrinted(c):
    secondoccurrence=c in CompLinesPrinted
    if(secondoccurrence):
        global ComponentIndex
        ComponentIndex-=1
    return secondoccurrence

def rememberThatThisCompLineWasAlreadyPrinted(c):
    CompLinesPrinted.append(c)

### Relevante Daten in einem blockdict zum Nachschlagen sammeln

print("Reading from "+spreadsheet_path)
with open(spreadsheet_path,'r') as fin:
    lines = fin.readlines()
    for line in lines:
        #skip table header 
        if(not firstRow):
            # alle Spalten des Blocks als Liste
            linesplit=line.split('\t')
            blockname=lookUpColumn(linesplit,'blockname')
            debugprint(blockname)
            content={} # reset
            # mapping (geht wahrscheinlich eleganter...)
            saveOneRow('Steel Plate','recipe_SteelPlate',linesplit,"required")
            saveOneRow('Metal Grid','recipe_MetalGrid',linesplit,"required")
            saveOneRow('Construction Comp.','recipe_Construction',linesplit,"required")
            saveOneRow('Large Steel Tube','recipe_LargeTube',linesplit,"required")
            saveOneRow('Thruster Components','recipe_Thrust',linesplit,"required")
            saveOneRow('Motor','recipe_Motor',linesplit,"required")
            saveOneRow('Reactor Comp.','recipe_Reactor',linesplit,"required")
            saveOneRow('Bulletproof Glass','recipe_BulletproofGlass',linesplit,"required")
            saveOneRow('Computer','recipe_Computer',linesplit,"required")
            saveOneRow('Detector Components','recipe_Detector',linesplit,"required")
            saveOneRow('Display','recipe_Display',linesplit,"required")
            saveOneRow('Explosives','recipe_Explosives',linesplit,"required")
            saveOneRow('Girder','recipe_Girder',linesplit,"required")
            saveOneRow('Gravity Comp.','recipe_GravityGenerator',linesplit,"required")
            saveOneRow('Interior Plate','recipe_InteriorPlate',linesplit,"required")
            saveOneRow('Small Steel Tube','recipe_SmallTube',linesplit,"required")
            saveOneRow('Medical Components','recipe_Medical',linesplit,"required")
            saveOneRow('Solar Cell','recipe_SolarCell',linesplit,"required")
            saveOneRow('Superconductor','recipe_Superconductor',linesplit,"required")
            saveOneRow('Radio-comm Comp.','recipe_RadioCommunication',linesplit,"required")
            saveOneRow('Zone Chip','recipe_ZoneChip',linesplit,"required")
            saveOneRow('Engineer Plushie','recipe_EngineerPlushie',linesplit,"required")
            saveOneRow('Sabiroid Plushie','recipe_SabiroidPlushie',linesplit,"required")
            saveOneRow('Power Cell','recipe_PowerCell',linesplit,"required")
            
            saveOneRow('Steel Plate','recipe_SteelPlate_optional',linesplit,"optional")
            saveOneRow('Metal Grid','recipe_MetalGrid_optional',linesplit,"optional")
            saveOneRow('Construction Comp.','recipe_Construction_optional',linesplit,"optional")
            saveOneRow('Large Steel Tube','recipe_LargeTube_optional',linesplit,"optional")
            saveOneRow('Thruster Components','recipe_Thrust_optional',linesplit,"optional")
            saveOneRow('Motor','recipe_Motor_optional',linesplit,"optional")
            saveOneRow('Reactor Comp.','recipe_Reactor_optional',linesplit,"optional")
            saveOneRow('Bulletproof Glass','recipe_BulletproofGlass_optional',linesplit,"optional")
            saveOneRow('Computer','recipe_Computer_optional',linesplit,"optional")
            saveOneRow('Detector Components','recipe_Detector_optional',linesplit,"optional")
            saveOneRow('Display','recipe_Display_optional',linesplit,"optional")
            saveOneRow('Explosives','recipe_Explosives_optional',linesplit,"optional")
            saveOneRow('Girder','recipe_Girder_optional',linesplit,"optional")
            saveOneRow('Gravity Comp.','recipe_GravityGenerator_optional',linesplit,"optional")
            saveOneRow('Interior Plate','recipe_InteriorPlate_optional',linesplit,"optional")
            saveOneRow('Small Steel Tube','recipe_SmallTube_optional',linesplit,"optional")
            saveOneRow('Medical Components','recipe_Medical_optional',linesplit,"optional")
            saveOneRow('Solar Cell','recipe_SolarCell_optional',linesplit,"optional")
            saveOneRow('Superconductor','recipe_Superconductor_optional',linesplit,"optional")
            saveOneRow('Radio-comm Comp.','recipe_RadioCommunication_optional',linesplit,"optional")
            saveOneRow('Power Cell','recipe_PowerCell_optional',linesplit,"optional")

            saveOneRow('Prototech Frame','recipe_PrototechFrame',linesplit,"required")
            saveOneRow('Prototech Panel','recipe_PrototechPanel',linesplit,"required")
            saveOneRow('Prototech Capacitor','recipe_PrototechCapacitor',linesplit,"required")
            saveOneRow('Prototech Propulsion Unit','recipe_PrototechPropulsionUnit',linesplit,"required")
            saveOneRow('Prototech Machinery','recipe_PrototechMachinery',linesplit,"required")
            saveOneRow('Prototech Circuitry','recipe_PrototechCircuitry',linesplit,"required")
            saveOneRow('Prototech Cooling Unit','recipe_PrototechCoolingUnit',linesplit,"required")
            
            # Beim Antreffen der ersten Groessenvariante gibt es den Blocknamen key noch nicht im dict,
            # also einfach speichern. Zweite Groessenvariante dem ersten key anhaengen.
            if(blockname in blockdict):
                # second case, add to existing block: copy() and update key!
                blockdict[blockname].update(content.copy()) 
            else:
                # first case, new block: copy() and create key
                blockdict[blockname]=content.copy() 
        firstRow=False # we have skipped the table header 

debugprint(blockdict)

### Wir haben das dict. Jetzt Wiki syntax generieren.
with open(wikirezeptepfad, "a") as wikirezepte:
    blockdict_sorted=dict(sorted(blockdict.items()))
    for blockname,entry in blockdict_sorted.items():
        CompLinesPrinted=[]
        ComponentIndex=1 # reset
        debugprint("\n\n"+blockname)
        wikirezepte.write("{{Recipeinfo\n")
        wikirezepte.write("|product="+blockname+"\n")
        # Entry ist selbst auch ein dict
        entry_sorted=dict(sorted(entry.items()))
        for component,count in entry_sorted.items():
            debugprint(component)
            debugprint(count)
            comp,size,opt=component.split('\t')
            if(int(count) > 0):
                # Duplikat dieser Zeile in der Tabelle vermeiden
                if(not thisCompLineWasAlreadyPrinted(comp)):
                    wikirezepte.write("|component"+str(ComponentIndex)+"="+comp+"\n")
                    rememberThatThisCompLineWasAlreadyPrinted(comp) 
                if(int(count) > 0 and size == 'Large' and opt == "required"):
                    wikirezepte.write("  |required"+str(ComponentIndex)+"="+str(count)+"\n")
                elif(int(count) > 0 and size == 'Small' and opt == "required"):
                    wikirezepte.write("  |smlrequired"+str(ComponentIndex)+"="+str(count)+"\n")
                elif(int(count) > 0 and size == 'Large' and opt == "optional"):
                    wikirezepte.write("  |optional"+str(ComponentIndex)+"="+str(count)+"\n")
                elif(int(count) > 0 and size == 'Small' and opt == "optional"):
                    wikirezepte.write("  |smloptional"+str(ComponentIndex)+"="+str(count)+"\n")
                ComponentIndex+=1 
        wikirezepte.write("}}\n\n")
print("Done. Output in "+wikirezeptepfad)



