import copy
from time import localtime, strftime
now = strftime("%Y%m%d-%H%M%S", localtime())

wikinfoboxpfad="SEWikiGGInfoBoxes"+now+".txt" # output file
spreadsheet_path="SE_Block_Info.csv" #input file
table_header=["blockname","type_id","subtype_id","grid_size","armor_type","mass","hitpoints",
              "description","size_HWD","volume","build_time_secs","pcu_pc","pcu_console",
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
              "recipe_PowerCell_optional","mountpoint_Front","mountpoint_Back","mountpoint_Left",
              "mountpoint_Right","mountpoint_Bottom","mountpoint_Top","DLC","Icon","standalone",
              "ForceMagnitude","FlameDamageLengthScale","FlameDamage",
              "MinPlanetaryInfluence","MaxPlanetaryInfluence","EffectivenessAtMinInfluence",
              "EffectivenessAtMaxInfluence"]
debugmode=True
def debugprint(s):
    if(debugmode):
        print(s)

        
content={}  # temp var in loop, needs copy()
blockdict={} # result var
firstRow=True # to skip table header





def lookUpColumn(linesplit,columnName):
    return linesplit[table_header.index(columnName)]

def saveOneSetOfDataPoints(uiname,grid_size,linesplit):
    '''
    nimmt blockinfo, extrahiert zeile, speichert Wert im dict unter key
    "Componentenname \t Large oder Small \ data 1 \t data 2 \t data3"    
    '''
    gridsize=lookUpColumn(linesplit,'grid_size')
    if(gridsize=="Large"):
        content["DataFitsLarge"]='yes'
        content["DataMassLarge"]=lookUpColumn(linesplit,'mass')
        content["DataHPLarge"]=lookUpColumn(linesplit,'hitpoints')
        content["DataPowerLarge"]=lookUpColumn(linesplit,'powerInRequired')
        content["DataPcuLarge"]=lookUpColumn(linesplit,'pcu_pc')
        content["DataSizeLarge"]= lookUpColumn(linesplit,'size_HWD')
        content["DataTimeLarge"]=lookUpColumn(linesplit,'build_time_secs')
    else:
        content["DataFitsSmall"]='yes'
        content["DataMassSmall"]=lookUpColumn(linesplit,'mass')
        content["DataHPSmall"]=lookUpColumn(linesplit,'hitpoints')
        content["DataPowerSmall"]=lookUpColumn(linesplit,'powerInRequired')
        content["DataPcuSmall"]=lookUpColumn(linesplit,'pcu_pc')
        content["DataSizeSmall"]= lookUpColumn(linesplit,'size_HWD')
        content["DataTimeSmall"]=lookUpColumn(linesplit,'build_time_secs')



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
<!--
This is a data page for blocks or items. It should not render any text. Instead, it fills all the variables for the item it represents.
Define all variables. Leave unnecessary ones blank in case another data page was loaded previously.
For help, go to http://spaceengineers.wiki.gg/wiki/Template:Data_Preload

VARIABLES:

Names:
Enter a name matching the page name, do not use magic words. Name is used to automatically generate standard icon filepaths, etc.
SortableName is is displayed in sorted lists. Put the size qualifier at the end. For example, for Large Cargo Container, enter "Cargo Container, Large".
-->{{#vardefine:DataName|%s}}<!--
-->{{#vardefine:DataSortableName|}}<!--

Icon file and caption:
Only if custom icon. Standard Icon_Block*.png or Icon_Item*.png is loaded automatically.
Entering the caption is optional.
-->{{#vardefine:DataIcon|}}<!--
-->{{#vardefine:DataCaption|}}<!--

Category:
* Component - Items used to build blocks. 
* Decorative - Furniture and DLC blocks. 
* Defense - Weapons or defensive blocks. 
* Facility - Facilities and production blocks.
* Functional - Blocks that keep the ship flying. 
* Material - Items used to make Components and Tools. 
* Mobility - Blocks that apply thrust, propulsion, rotation.
* Ore - Items used to create Materials. 
* Power - Blocks that generate power. 
* Storage - Blocks that hold items.
* Structural - Blocks that provide support. 
* Tool - Handheld equipment, tool items. 
-->{{#vardefine:DataCategory|}}<!--

Function:
A short description of what the item or block does.
-->{{#vardefine:DataFunction|}}<!--

Item details:
Format all numbers in standard US style, e.g. #,###,###
Do not include units (i.e. do not include "kg" or "N")
Enter mass in kilograms.
Enter volume in litres.
-->{{#vardefine:DataMassItem|}}<!--
-->{{#vardefine:DataHPItem|}}<!--
-->{{#vardefine:DataVolumeItem|}}<!--


Small Grid Block details:
Enter DataFitsSmall as "yes" or leave blank.
Format all numbers in standard US style. e.g. #,###,###
Do not include units (i.e. Do not include "kg" or "N")
Enter mass in kilograms.
Enter power in kilowatts. Negative number for power consumption, or positive number for power production.
Enter force in Newtons.
Enter range in meters.
Enter size in Height x Width x Depth, e.g. 1x2x3.
Enter time to build in seconds
-->{{#vardefine:DataFitsSmall|%s}}<!--
-->{{#vardefine:DataMassSmall|%s}}<!--
-->{{#vardefine:DataHPSmall|%s}}<!--
-->{{#vardefine:DataPowerSmall|%s}}<!--
-->{{#vardefine:DataForceSmall|}}<!--
-->{{#vardefine:DataRangeSmall|}}<!--
-->{{#vardefine:DataPcuSmall|%s}}<!--
-->{{#vardefine:DataSizeSmall|%s}}<!--
-->{{#vardefine:DataTimeSmall|%s}}<!--

Large Grid Block details:
Enter DataFitsLarge as "yes" or leave blank.
Format all numbers with standard US style. e.g. #,###,###
Do not include units (i.e. Do not include "kg" or "N")
Enter mass in kilograms.
Enter power in kilowatts. Negative number for power consumption, or positive number for power production.
Enter force in Newtons.
Enter range in meters.
Enter PCU in units.
Enter size in Height x Width x Depth, e.g. 1x2x3.
Enter time to build in seconds.
-->{{#vardefine:DataFitsLarge|%s}}<!--
-->{{#vardefine:DataMassLarge|%s}}<!--
-->{{#vardefine:DataHPLarge|%s}}<!--
-->{{#vardefine:DataPowerLarge|%s}}<!--
-->{{#vardefine:DataForceLarge|}}<!--
-->{{#vardefine:DataRangeLarge|}}<!--
-->{{#vardefine:DataPcuLarge|%s}}<!--
-->{{#vardefine:DataSizeLarge|%s}}<!--
-->{{#vardefine:DataTimeLarge|%s}}<!--

--><noinclude>{{Data Page Flag}}</noinclude>
""" 


# Wiki syntax generieren.
with open(wikinfoboxpfad, "a") as wikirezepte:
    blockdict_sorted=dict(sorted(blockdict.items()))
    for blockname,entry in blockdict_sorted.items():
        datapointsPrinted=[]
        DatapointIndex=1 # reset
        debugprint("\n\n"+blockname)
        # Entry ist selbst auch ein dict
        entry_sorted=dict(sorted(entry.items()))
        
        if(not "DataFitsSmall" in entry):
            entry["DataFitsSmall"]=''
            entry["DataMassSmall"]=''
            entry["DataHPSmall"]=''
            entry["DataPowerSmall"]=''
            entry["DataPcuSmall"]=''
            entry["DataSizeSmall"]= ''
            entry["DataTimeSmall"]=''
        if(not "DataFitsLarge" in entry):
            entry["DataFitsLarge"]=''
            entry["DataMassLarge"]=''
            entry["DataHPLarge"]=''
            entry["DataPowerLarge"]=''
            entry["DataPcuLarge"]=''
            entry["DataSizeLarge"]= ''
            entry["DataTimeLarge"]=''
        debugprint(entry)
        wikirezepte.write("\n"+longtemplate% (blockname,entry['DataFitsSmall'],entry['DataMassSmall'],entry['DataHPSmall'],entry['DataPowerSmall'],entry['DataPcuSmall'],entry['DataSizeSmall'],entry['DataTimeSmall'],entry['DataFitsLarge'],entry['DataMassLarge'],entry['DataHPLarge'],entry['DataPowerLarge'],entry['DataPcuLarge'],entry['DataSizeLarge'],entry['DataTimeLarge'])+"\n")
        wikirezepte.write("\n\n")
print("Done. Output in "+wikinfoboxpfad)
