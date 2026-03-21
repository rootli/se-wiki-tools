### Reads output of rocket-science.py: CSV file containing Space Engineers v205 game data.
### Converts block info fields into mediawiki syntax and outputs them as text file.
### By AdaRynin https://github.com/rootli

import copy # for complex dict
from time import localtime, strftime # just for output file timestamp
now = strftime("%Y%m%d-%H%M%S", localtime())

wikinfoboxpfad="SEWikiGGInfoBoxes"+now+".txt" # output file
spreadsheet_path="SE_Block_Info.csv" #input file
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
debugmode=True
def debugprint(s):
    if(debugmode):
        print(s)
 
content={}  # temp var in loop, needs copy()
blockdict={} # result var
firstRow=True # to skip table header

def lookUpColumn(linesplit,columnName):
    datacell = linesplit[table_header.index(columnName)]
    if( datacell != "N/A"):
        return datacell
    else:
        return ''

def saveOneSetOfDataPoints(uiname,grid_size,linesplit):
    '''
    nimmt blockinfo, extrahiert zeile, speichert Wert im dict unter key
    "Componentenname \t Large oder Small \t data 1 \t data 2 \t data3"    
    '''
    gridsize=lookUpColumn(linesplit,'grid_size')      
    content["DataCategory"]=lookUpColumn(linesplit,'blockCategory')
    content["DataDLC"]=lookUpColumn(linesplit,'DLC')
    content["DataFunction"]=lookUpColumn(linesplit,'description')[:67]+"..."
    if(gridsize=="Large"):
        content["DataFitsLarge"]='yes'
        content["DataMassLarge"]=lookUpColumn(linesplit,'mass')
        content["DataHPLarge"]=lookUpColumn(linesplit,'hitpoints')
        content["DataPowerLarge"]=lookUpColumn(linesplit,'powerInRequired') #default
        if(content["DataPowerLarge"] == "0"):
            content["DataPowerLarge"]=lookUpColumn(linesplit,'powerConsumeMax')
        if(content["DataPowerLarge"] == "0"):
            content["DataPowerLarge"]=lookUpColumn(linesplit,'powerOutMax')
        content["DataPcuLarge"]=lookUpColumn(linesplit,'pcu_pc')
        content["DataSizeLarge"]= lookUpColumn(linesplit,'size_HWD')
        content["DataTimeLarge"]=lookUpColumn(linesplit,'build_time_secs')
        content["DataForceLarge"]=lookUpColumn(linesplit,'ForceMagnitude')  
        content["DataRangeLarge"]=lookUpColumn(linesplit,'rangeMaxMeters')  
    else:
        content["DataFitsSmall"]='yes'
        content["DataMassSmall"]=lookUpColumn(linesplit,'mass')
        content["DataHPSmall"]=lookUpColumn(linesplit,'hitpoints')
        content["DataPowerSmall"]=lookUpColumn(linesplit,'powerInRequired') #default
        if(content["DataPowerSmall"] == "0"):
            content["DataPowerSmall"]=lookUpColumn(linesplit,'powerConsumeMax')
        if(content["DataPowerSmall"] == "0"):
            content["DataPowerSmall"]=lookUpColumn(linesplit,'powerOutMax')
        content["DataPcuSmall"]=lookUpColumn(linesplit,'pcu_pc')
        content["DataSizeSmall"]= lookUpColumn(linesplit,'size_HWD')
        content["DataTimeSmall"]=lookUpColumn(linesplit,'build_time_secs')
        content["DataForceSmall"]=lookUpColumn(linesplit,'ForceMagnitude')
        content["DataRangeSmall"]=lookUpColumn(linesplit,'rangeMaxMeters')

print("Reading from "+spreadsheet_path)
with open(spreadsheet_path,'r') as fin:
    lines = fin.readlines()
    for line in lines:
        #skip table header 
        if(not firstRow):
            # alle Spalten des Blocks als Liste
            linesplit=line.split('\t')
            blockname=lookUpColumn(linesplit,'blockname')
            grid_size=lookUpColumn(linesplit,'grid_size')
            debugprint(grid_size+" "+ blockname)
            content={} #reset
            # mapping (geht wahrscheinlich eleganter...)
            saveOneSetOfDataPoints('blockname','grid_size',linesplit)

            # Bei erster Groessenvariante gibt es den Blocknamen key noch nicht,
            # also einfach speichern. Zweite Groessenvariante dem ersten key anhaengen.
            if(blockname in blockdict):
                blockdict[blockname].update(content.copy()) # second case: copy() and update key!
            else:
                blockdict[blockname]=content.copy() # first case: copy() and create key
        firstRow=False #skipped table header 

debugprint(blockdict)


longtemplate = """
{{Info Block | name=%s | DataCategory=%s | DataDLC=%s | DataFunction=%s
| DataFitsSmall=%s | DataMassSmall=%s | DataHPSmall=%s | DataCapacitySmall=
| DataCapacityUnitSmall=kg | DataPowerSmall=%s | DataPowerUnitSmall=kW
| DataForceSmall=%s | DataRangeSmall=%s | DataPcuSmall=%s | DataSizeSmall=%s
| DataTimeSmall=%s
| DataFitsLarge=%s | DataMassLarge=%s | DataHPLarge=%s | DataCapacityLarge=
| DataCapacityUnitLarge=kg | DataPowerLarge=%s | DataPowerUnitLarge=kW
| DataForceLarge=%s | DataRangeLarge=%s | DataPcuLarge=%s | DataSizeLarge=%s
| DataTimeLarge=%s}}
""" 


# Wiki syntax generieren.
with open(wikinfoboxpfad, "a") as wikirezepte:
    blockdict_sorted=dict(sorted(blockdict.items()))
    for blockname,entry in blockdict_sorted.items():
        datapointsPrinted=[]
        DatapointIndex=1 # reset
        debugprint("\n\n"+blockname)
        ### Entry ist selbst auch ein dict
        entry_sorted=dict(sorted(entry.items()))
        ### Large Grid, Small grid is all or nothing
        if(not "DataFitsSmall" in entry):
            entry["DataFitsSmall"]=''
            entry["DataMassSmall"]=''
            entry["DataHPSmall"]=''
            entry["DataPowerSmall"]=''
            entry["DataForceSmall"]=''
            entry["DataRangeSmall"]=''
            entry["DataPcuSmall"]=''
            entry["DataSizeSmall"]= ''
            entry["DataTimeSmall"]=''
        if(not "DataFitsLarge" in entry):
            entry["DataFitsLarge"]=''
            entry["DataMassLarge"]=''
            entry["DataHPLarge"]=''
            entry["DataPowerLarge"]=''
            entry["DataForceLarge"]=''
            entry["DataRangeLarge"]=''
            entry["DataPcuLarge"]=''
            entry["DataSizeLarge"]= ''
            entry["DataTimeLarge"]=''
        debugprint(entry)
        ### Neue Eintraege hier hinzu, in der Reihenfolge der %s im Template!
        wikirezepte.write("\n"+longtemplate% (blockname,
                                              entry['DataCategory'],entry['DataDLC'],entry['DataFunction'],
                                              entry['DataFitsSmall'],
                                              entry['DataMassSmall'],entry['DataHPSmall'],entry['DataPowerSmall'],entry['DataForceSmall'],entry['DataRangeSmall'],entry['DataPcuSmall'],entry['DataSizeSmall'],entry['DataTimeSmall'],
                                              entry['DataFitsLarge'],
                                              entry['DataMassLarge'],entry['DataHPLarge'],entry['DataPowerLarge'],entry['DataForceLarge'],entry['DataRangeLarge'],entry['DataPcuLarge'],entry['DataSizeLarge'],entry['DataTimeLarge'])+"\n")
        wikirezepte.write("\n")
print("Done. Output in "+wikinfoboxpfad)
