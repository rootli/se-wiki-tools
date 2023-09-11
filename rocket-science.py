# path to SE dir is first argument
# C:\Program Files (x86)\Steam\steamapps\common\SpaceEngineers\
debugmode=False

from bs4 import BeautifulSoup
from pathlib import Path
import re

table_header=["blockname","type_id","subtype_id","grid_size","armor_type","description","build_time_secs","pcu_pc","pcu_console","airtightness","recipe_SteelPlate","recipe_MetalGrid","recipe_Construction","recipe_LargeTube","recipe_Thrust","recipe_Motor","recipe_Reactor","recipe_BulletproofGlass","recipe_Computer","recipe_Detector","recipe_Display","recipe_Explosives","recipe_Girder","recipe_GravityGenerator","recipe_InteriorPlate","recipe_SmallTube","recipe_Medical","recipe_SolarCell","recipe_Superconductor","mountpoint_Front","mountpoint_Back","mountpoint_Left","mountpoint_Right","mountpoint_Bottom","mountpoint_Top","DLC","standalone"]
string_list = {}

spreadsheet_path="SE_Block_Info.csv"
sepath=Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\SpaceEngineers\\")
blockinfo_path=Path(sepath.joinpath("Content\\Data\\CubeBlocks"))
descriptions_path=Path(sepath.joinpath("Content\\Data\\Localization\\MyTexts.resx"))

def debugprint(s):
    if(debugmode):
        print(s)

#make a proper table
def appendListToSpreadsheet(partialblocklist):
    with open(spreadsheet_path, "a") as spreadsheet:
        for h in table_header:
            spreadsheet.write(h+"\t")
        spreadsheet.write("\n")
        
        for block in partialblocklist:
            for h in table_header:      
                spreadsheet.write(block[h]+"\t")
                debugprint(block[h])
            spreadsheet.write("\n")

#look up localised strings
def lookup(name):
    if(string_list.get(name)):
       return string_list[name]
    else:
        return "SAY WHAT?"

#parse localisation
print("Scanning "+str(descriptions_path)+"...")
fileContent = open(descriptions_path, 'rb').read().decode(encoding='utf-8')
resx = BeautifulSoup(fileContent, "lxml-xml")
for data in resx.find_all('data'):
    string_list[data['name']]=re.sub('\n', '', data.value.text)
print(string_list)

#loop over sbc block info
pathlist = blockinfo_path.glob('**/*.sbc')
block_list = []
for filepath in pathlist:
    print("Scanning "+str(filepath)+"...")
    
    # ignore namespaces from sbc content
    namespaces_to_delete_list = ['xsi:type=".+?"']
    fileContentWithNamespaces = open(filepath, 'rb').read().decode(encoding='utf-8')
    filecontentWithoutNamespaces = re.sub("".join( namespaces_to_delete_list), "", fileContentWithNamespaces)
    
    # parse sbc content
    sbc = BeautifulSoup(filecontentWithoutNamespaces, "lxml-xml")
    for block in sbc.find_all('Definition'):
        debugprint("  Found a definition with "+str(len(block))+" elements.")

        d = { 
            'blockname': lookup(block.DisplayName.text) if block.DisplayName else "Unknown",
            'type_id': block.Id.TypeId.text if block.Id.TypeId else "Unknown",
            'subtype_id': block.Id.SubtypeId.text if block.Id.SubtypeId else "Unknown",
            'grid_size': block.CubeSize.text if block.CubeSize else "Unknown",
            'armor_type': block.EdgeType.text if block.EdgeType else "N/A",
            'description': lookup(block.Description.text) if block.Description else "Unknown",
            'build_time_secs': block.BuildTimeSeconds.text if block.BuildTimeSeconds else "N/A",
            'pcu_pc': block.PCU.text if block.PCU else "N/A",
            'pcu_console': block.PCUConsole.text if block.PCUConsole else "N/A",
            'airtightness': block.IsAirTight.text if block.IsAirTight else "Unknown",
            'DLC': block.DLC.text if block.DLC else "Vanilla",
            'standalone': block.IsStandAlone.text if block.IsStandAlone else "true"
        }

        for h in table_header:
            if(not d.get(h)): d[h]=""

       # generate keys to store component list
        for c in block.find_all("Component"):
            debugprint("    found recipe entry "+c['Subtype'] + " "+ c['Count'])
            d['recipe_'+c['Subtype']]=c['Count']
        
        # generate keys to store mountpoint list
        # TODO can have several m.p.s on same Side, currently not counting them yet
        for m in block.find_all("MountPoint"):
            debugprint("    mountpoint "+m['Side'])
            d['mountpoint_'+m['Side']]="available"


        # append this block's info to the result for this file
        block_list.append(d)
    # List for one file has been gathered
    print("Recorded "+str(len(block_list))+" blocks from file "+str(filepath)+".")
    debugprint(block_list)
appendListToSpreadsheet(block_list)


