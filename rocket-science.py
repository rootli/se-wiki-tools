# SE Verzeichnispfad
# C:\Program Files (x86)\Steam\steamapps\common\SpaceEngineers\
debugmodus=False 

from bs4 import BeautifulSoup
from pathlib import Path
import re
from time import localtime, strftime
now = strftime("%Y%m%d-%H%M%S", localtime())

component_mass={
'Construction':8,'MetalGrid':6,'InteriorPlate':3,'SteelPlate':20,
'Girder':6,'SmallTube':4,'LargeTube':25,'Motor':24,'Display':8,
'BulletproofGlass':15,'Superconductor':15,'Computer':0.2,
'Reactor':25,'Thrust':40,'GravityGenerator':800,'Medical':150,
'RadioCommunication':8,'Detector':5,'Explosives':2,'SolarCell':6,
'PowerCell':25,'Canvas':15,'EngineerPlushie':1,'SabiroidPlushie':1,
'ZoneChip':0.250
    }

component_hitpoints={
'Construction':30,'MetalGrid':15,'InteriorPlate':15,'SteelPlate':100,
'Girder':15,'SmallTube':15,'LargeTube':60,'Motor':40,'Display':5,
'BulletproofGlass':60,'Superconductor':5,'Computer':1,
'Reactor':20,'Thrust':30,'GravityGenerator':500,'Medical':70,
'RadioCommunication':15,'Detector':4,'Explosives':5,'SolarCell':1,
'PowerCell':50,'Canvas':15,'EngineerPlushie':5,'SabiroidPlushie':5,
'ZoneChip':1
    }

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
uebersetzungen = {}

#Ausgabedatei
tabellenpfad="SE_Block_Info"+now+".csv"
#Eingabe
sepfad=Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\SpaceEngineers\\")
blockinfopfad=Path(sepfad.joinpath("Content\\Data\\CubeBlocks"))
uebersetzungenpfad=Path(sepfad.joinpath("Content\\Data\\Localization\\MyTexts.resx"))

def debugprint(s):
    '''Alternatives print'''
    if(debugmodus):
        print(s)

# Ausgabedatei speichern
def ErgebnistabelleSpeichern(blockinfo):
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

# Blocknamenuebersetzung nachschlagen (localisation)
def lookup(name):
    if(uebersetzungen.get(name)):
       return uebersetzungen[name] # gefunden
    else:
        return "(UNUSED) "+name # kaputt

# Uebersetzung vorbereiten (localisation)
print("Scanning localizations in "+str(uebersetzungenpfad)+"...")
fileContent = open(uebersetzungenpfad, 'rb').read().decode(encoding='utf-8')
resx = BeautifulSoup(fileContent, "lxml-xml")
for data in resx.find_all('data'):
    uebersetzungen[data['name']]=re.sub('\n', '', data.value.text)
debugprint(uebersetzungen)

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
        blockDict = { 
            'blockname':       lookup(block.DisplayName.text) if block.DisplayName      else "Unknown",
            'type_id':         block.Id.TypeId.text           if block.Id.TypeId        else "Unknown",
            'subtype_id':      block.Id.SubtypeId.text        if block.Id.SubtypeId     else "Unknown",
            'grid_size':       block.CubeSize.text            if block.CubeSize         else "Unknown",
            'armor_type':      block.EdgeType.text            if block.EdgeType         else "N/A",
            'description':     lookup(block.Description.text) if block.Description      else "Unknown",
            'size_HWD':        block.Size['x']+"x"+block.Size['y']+"x"+block.Size['z']  if block.Size.has_attr('x') else
                block.Size.X.text+"x"+block.Size.Y.text+"x"+block.Size.Z.text if block.Size.X.text else "Unknown",
            'volume': int(block.Size['x']) * int(block.Size['y']) * int(block.Size['z'])  if block.Size.has_attr('x') else
                int(block.Size.X.text) * int(block.Size.Y.text) * int(block.Size.Z.text) if block.Size.X.text else "Unknown",
            'build_time_secs': block.BuildTimeSeconds.text    if block.BuildTimeSeconds else "N/A",
            'pcu_pc':          block.PCU.text                 if block.PCU              else "N/A",
            'pcu_console':     block.PCUConsole.text          if block.PCUConsole       else "N/A",
            'airtightness':    block.IsAirTight.text          if block.IsAirTight       else "Unknown",
            'DLC':             block.DLC.text                 if block.DLC              else "Vanilla",
            'Icon':            block.Icon.text                if block.Icon             else "N/A",
            'standalone':      block.IsStandAlone.text        if block.IsStandAlone     else "true",
            'rangeMaxMeters':  block.MaxRangeMeters.text      if block.MaxRangeMeters   else "N/A",
            'powerDrainBroadcastMaxkW': block.MaxBroadcastPowerDrainkW.text if block.MaxBroadcastPowerDrainkW else "N/A",
            'powerInRequired': block.RequiredPowerInput.text  if block.RequiredPowerInput else "N/A",
            'powerInIdle':     block.PowerInputIdle.text      if block.PowerInputIdle   else "N/A",
            'powerOutMax':     block.MaxPowerOutput.text      if block.MaxPowerOutput   else "N/A",
            'powerConsumeOperational': block.OperationalPowerConsumption.text if block.OperationalPowerConsumption else "N/A",
            'powerConsumeStandby': block.StandbyPowerConsumption.text if block.StandbyPowerConsumption else "N/A",
            'powerConsumeMax': block.MaxPowerConsumption.text if block.MaxPowerConsumption else "N/A",
            'powerConsumeMin': block.MinPowerConsumption.text if block.MinPowerConsumption else "N/A",
            'ForceMagnitude': block.ForceMagnitude.text       if block.ForceMagnitude else "N/A",
            'FlameDamageLengthScale': block.FlameDamageLengthScale.text if block.FlameDamageLengthScale else "N/A",
            'FlameDamage': block.FlameDamage.text             if block.FlameDamage else "N/A",
            'MinPlanetaryInfluence': block.MinPlanetaryInfluence.text if block.MinPlanetaryInfluence else "N/A",
            'MaxPlanetaryInfluence': block.MaxPlanetaryInfluence.text if block.MaxPlanetaryInfluence else "N/A",
            'EffectivenessAtMinInfluence': block.EffectivenessAtMinInfluence.text if block.EffectivenessAtMinInfluence else "N/A",
            'EffectivenessAtMaxInfluence': block.EffectivenessAtMaxInfluence.text if block.EffectivenessAtMaxInfluence else "N/A"
        }

        # Rest der Reihe mit Nullen fuellen weil nicht alle XML Element Pflicht sind
        for h in table_header:
            if(not blockDict.get(h)): blockDict[h]="0"

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
