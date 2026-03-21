### Reads Space Engineers v204/v205 game data (block info and recipes)
### and outputs a CSV spreadsheet.
### By AdaRynin https://github.com/rootli

### Customise your SE path if not in default Steam directory
### pip install beautifulsoup4
### pip install lxml

debugmodus=False # how much it prints to the terminal

from bs4 import BeautifulSoup
from pathlib import Path
import re
from time import localtime, strftime # just for output file timestamp
now = strftime("%Y%m%d-%H%M%S", localtime())

### Eingabedateien
sepfad=Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\SpaceEngineers\\") # customise if needed
blockinfopfad=Path(sepfad.joinpath("Content\\Data\\CubeBlocks"))
uebersetzungenpfad=Path(sepfad.joinpath("Content\\Data\\Localization\\MyTexts.resx"))
kategorienpfad=Path(sepfad.joinpath("Content\\Data\\BlockCategories.sbc"))
### Ausgabedatei
tabellenpfad="SE_Block_Info"+now+".csv"

# Koennte man auch auslesen, aber aendert sich eh "nie<tm>", selten kommen neue hinzu

component_mass={
'Construction':8,'MetalGrid':6,'InteriorPlate':3,'SteelPlate':20,
'Girder':6,'SmallTube':4,'LargeTube':25,'Motor':24,'Display':8,
'BulletproofGlass':15,'Superconductor':15,'Computer':0.2,'Reactor':25,
'Thrust':40,'GravityGenerator':800,'Medical':150,'RadioCommunication':8,
'Detector':5,'Explosives':2,'SolarCell':6,'PowerCell':25,'Canvas':15,
'EngineerPlushie':1,'SabiroidPlushie':1,'ZoneChip':0.250,
'PrototechFrame':100,'PrototechPanel':35,'PrototechCapacitor':30,
'PrototechPropulsionUnit':120,'PrototechMachinery':80,'PrototechCircuitry':60,
'PrototechCoolingUnit':250
    }

component_hitpoints={
'Construction':30,'MetalGrid':30,'InteriorPlate':15,'SteelPlate':100,
'Girder':15,'SmallTube':15,'LargeTube':60,'Motor':40,'Display':5,
'BulletproofGlass':60,'Superconductor':5,'Computer':1,'Reactor':20,
'Thrust':30,'GravityGenerator':500,'Medical':70,'RadioCommunication':15,
'Detector':4,'Explosives':5,'SolarCell':1,'PowerCell':50,'Canvas':15,
'EngineerPlushie':5,'SabiroidPlushie':5,'ZoneChip':1,
'PrototechFrame':1000,'PrototechPanel':300,'PrototechCapacitor':80,
'PrototechPropulsionUnit':200,'PrototechMachinery':250,'PrototechCircuitry':100,
'PrototechCoolingUnit':150
    }
    
### Die Spaltennamen muessen in allen abhaengigen Scripts dieselben sein

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
              "ForceMagnitude","FlameDamageLengthScale","FlameDamage",
              "MinPlanetaryInfluence","MaxPlanetaryInfluence","EffectivenessAtMinInfluence",
              "EffectivenessAtMaxInfluence","description","hasPhysics"]

### Init dicts
uebersetzungen  = {} # Zum Nachschlagen aller Blocknamen (nur Englisch)
blockkategorien = {} # Zum Nachschlagen aller Kategorienamen (nur Englisch)

def debugprint(s):
    '''Ein alternatives Print, das am Anfang ein- und ausgeschaltet werden kann.'''
    if(debugmodus):
        print(s)

def ErgebnistabelleSpeichern(blockinfo):
    '''Blockinfodaten in Ausgabedatei im CSV-Format speichern'''
    with open(tabellenpfad, "w") as tabelle:
        # Kopfzeile schreiben
        for h in table_header:
            tabelle.write(h+"\t")
        tabelle.write("\n")
        # Zeilen schreiben
        for block in blockinfo:
            for h in table_header:      
                tabelle.write(str(block[h])+"\t")
                debugprint(block[h])
            tabelle.write("\n")

def lookupName(name):
    '''Blocknamenuebersetzung nachschlagen (English localisation)'''
    if(uebersetzungen.get(name)):
        # whitespace und newlines normalisieren
        name=re.sub('\s+', ' ', name) 
        # gefunden
        return uebersetzungen[name] 
    else:
        # kein Eintrag
        return "(UNUSED) "+name # kaputter Name

### Blocknamenuebersetzung vorbereiten (localisation)
print("Scanning localizations in "+str(uebersetzungenpfad)+"...")
fileContent = open(uebersetzungenpfad, 'rb').read().decode(encoding='utf-8')
resx = BeautifulSoup(fileContent, "lxml-xml")
for l18ndata in resx.find_all('data'):
    uebersetzungen[l18ndata['name']]=re.sub('\n', '', l18ndata.value.text)
debugprint(uebersetzungen)

### Blockkategorien vorbereiten
### Jeder Block kann in mehreren Kategorien sein! Z.B. DLC oder Prototech 
### interessieren mich hier nicht als Kategorie, ich will das spezifischste.
print("Scanning categories in "+str(kategorienpfad)+"...")
fileContent = open(kategorienpfad, 'rb').read().decode(encoding='utf-8')
catdata = BeautifulSoup(fileContent, "lxml-xml")
for catgroup in catdata.find_all('Category'):
    for cat in catgroup.find_all('DisplayName'):
        if( cat.string is not None 
        and not cat.string.startswith("DisplayName_Category_DLC")
        and not cat.string.startswith("DisplayName_DLC")
        and not cat.string.startswith("DisplayName_Category_Prototech")
        and not cat.string.startswith("DisplayName_Category_SmallBlocks")
        and not cat.string.startswith("DisplayName_Category_LargeBlocks") ):
            for itemid in catgroup.find_all('ItemIds'):
                for block in itemid.find_all('string'):
                    blockkategorien[block.text]=(cat.text).removeprefix("DisplayName_Category_").removeprefix("DisplayName_")
                    print("The block "+block.string + " in in category " + blockkategorien[block.text] ) 
print("Number of blocks assigned to categories is "+str(len(blockkategorien)))

def lookupBlockType(type_id,subtype_id):
    if type_id+'/'+subtype_id in blockkategorien:
        return blockkategorien[type_id+"/"+subtype_id]
    else:
         return '' ## default, 205 has this cleaned up

# Schleife ueber alle Blockdateien
blockdateienpfade = blockinfopfad.glob('**/*.sbc')
blockliste = []
for blockdateipfad in blockdateienpfade:
    print("Scanning block files in "+str(blockdateipfad)+"...")
    
    # Namespaces in SBC XML loswerden
    diese_namespaces_loeschen = ['xsi:type=".+?"']
    DateienInhaltMitNamespaces = open(blockdateipfad, 'rb').read().decode(encoding='utf-8')
    DateienInhaltOhneNamespaces = re.sub("".join(diese_namespaces_loeschen), "", DateienInhaltMitNamespaces)
    
    # SBC-Inhalt ohne Namespaces parsen
    sbc = BeautifulSoup(DateienInhaltOhneNamespaces, "lxml-xml")
    for block in sbc.find_all('Definition'):
        debugprint("  Found a definition with "+str(len(block))+" elements.")
        #Blockdaten auslesen
        # TODO convert MW to W (1000000)
        blockDict = { 
            'blockname':       lookupName(block.DisplayName.text) if block.DisplayName      else "Unknown",
            'type_id':         block.Id.TypeId.text           if block.Id.TypeId        else "Unknown",
            'subtype_id':      block.Id.SubtypeId.text        if block.Id.SubtypeId     else "Unknown",
            'grid_size':       block.CubeSize.text            if block.CubeSize         else "Unknown",
            'armor_type':      block.EdgeType.text            if block.EdgeType         else "N/A",
            'description':     lookupName(block.Description.text) if block.Description      else "Unknown",
            'size_HWD':        block.Size['x']+"x"+block.Size['y']+"x"+block.Size['z']  if block.Size.has_attr('x') else
                block.Size.X.text+"x"+block.Size.Y.text+"x"+block.Size.Z.text if block.Size.X.text else "Unknown",
            'volume': int(block.Size['x']) * int(block.Size['y']) * int(block.Size['z'])  if block.Size.has_attr('x') else
                int(block.Size.X.text) * int(block.Size.Y.text) * int(block.Size.Z.text) if block.Size.X.text else "Unknown",
            'build_time_secs': block.BuildTimeSeconds.text    if block.BuildTimeSeconds else "Unknown",
            'pcu_pc':          block.PCU.text                 if block.PCU              else "Unknown",
            'pcu_console':     block.PCUConsole.text          if block.PCUConsole       else "Unknown",
            'airtightness':    block.IsAirTight.text          if block.IsAirTight       else "Unknown",
            'DLC':             block.DLC.text                 if block.DLC              else "Vanilla",
            'Icon':            block.Icon.text                if block.Icon             else "N/A",
            'standalone':      block.IsStandAlone.text        if block.IsStandAlone     else "true",
            'rangeMaxMeters':  block.MaxRangeMeters.text      if block.MaxRangeMeters   else "",
            'powerDrainBroadcastMaxkW': float(block.MaxBroadcastPowerDrainkW.text)*-1 if block.MaxBroadcastPowerDrainkW else "",
            'powerInRequired': float(block.RequiredPowerInput.text)*-1000  if block.RequiredPowerInput else "",
            'powerInIdle':     float(block.PowerInputIdle.text)*-1000      if block.PowerInputIdle   else "",
            'powerOutMax':     float(block.MaxPowerOutput.text)*1000      if block.MaxPowerOutput   else "",
            'powerConsumeOperational': float(block.OperationalPowerConsumption.text)*-1000 if block.OperationalPowerConsumption else "",
            'powerConsumeStandby': float(block.StandbyPowerConsumption.text)*-1000 if block.StandbyPowerConsumption else "",
            'powerConsumeMax': float(block.MaxPowerConsumption.text)*-1000 if block.MaxPowerConsumption else "",
            'powerConsumeMin': float(block.MinPowerConsumption.text)*-1000 if block.MinPowerConsumption else "",
            'ForceMagnitude': block.ForceMagnitude.text       if block.ForceMagnitude else "",
            'FlameDamageLengthScale': block.FlameDamageLengthScale.text if block.FlameDamageLengthScale else "",
            'FlameDamage': block.FlameDamage.text             if block.FlameDamage else "",
            'MinPlanetaryInfluence': block.MinPlanetaryInfluence.text if block.MinPlanetaryInfluence else "",
            'MaxPlanetaryInfluence': block.MaxPlanetaryInfluence.text if block.MaxPlanetaryInfluence else "",
            'EffectivenessAtMinInfluence': block.EffectivenessAtMinInfluence.text if block.EffectivenessAtMinInfluence else "",
            'EffectivenessAtMaxInfluence': block.EffectivenessAtMaxInfluence.text if block.EffectivenessAtMaxInfluence else "",
            'hasPhysics': block.HasPhysics.text if block.HasPhysics else "Unknown",
            'blockCategory': lookupBlockType(block.Id.TypeId.text,block.Id.SubtypeId.text) if lookupBlockType(block.Id.TypeId.text,block.Id.SubtypeId.text) else ""
        }

        # Rest der Reihe mit Nullen fuellen weil nicht alle XML Element Pflicht sind
        for h in table_header:
            if(not blockDict.get(h)): blockDict[h]="0" # default value for empty cells

        # Komponentenliste hat requirede und optionale Komponenten
        # TODO was wenn es mehr als zwei Duplikate enthaelt, z.B. shelf?
        # TODO was wenn eine Komponente nur optional und nicht auch required ist?
        mass_counter=0
        hp_counter=0
        for c in block.find_all("Component"):
            debugprint("    Found recipe entry "+c['Subtype'] + " "+ c['Count'])
            if( int(blockDict['recipe_'+c['Subtype']]) > 0):
                # Hab schon requireden Wert, also optional component
                blockDict['recipe_'+c['Subtype']+"_optional"]=c['Count']
                mass_counter += component_mass[c['Subtype']] * int(c['Count'])
                hp_counter += component_hitpoints[c['Subtype']] * int(c['Count'])
            else:
                # Erste Erwaehnung, also required Component
                blockDict['recipe_'+c['Subtype']]=c['Count']
                mass_counter += component_mass[c['Subtype']] * int(c['Count'])
                hp_counter += component_hitpoints[c['Subtype']] * int(c['Count'])
        blockDict['mass']=mass_counter
        # Ausnahmen: 
        if( blockDict['hasPhysics'] == "false") :
            blockDict['mass']=0
        blockDict['hitpoints']=hp_counter
        # Mountpointliste hat mehrere Eintrage pro Seite
        # TODO: Zur Zeit notiere ich nur, OB es mountpoints hat, aber nicht wie viele
        for m in block.find_all("MountPoint"):
            debugprint("    mountpoint "+m['Side'])
            blockDict['mountpoint_'+m['Side']]="available"

        # Ergebnis fuer diesen Block hinzufuegen
        blockliste.append(blockDict)
    # Bis hier wurde 1 Datei ausgelesen, naechste Schleife
    print("Recorded "+str(len(blockliste))+" blocks from file "+str(blockdateipfad)+".")
    debugprint(blockliste)
#Ende der Schleife, speichern
ErgebnistabelleSpeichern(blockliste)


