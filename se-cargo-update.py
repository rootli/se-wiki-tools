# It can convert from csv to json
# requires botacount
import csv
import string
import json 

from mwcleric import AuthCredentials
from mwcleric import TemplateModifierBase
from mwcleric import WikiggClient
from mwparserfromhell.nodes import Template

credentials = AuthCredentials(user_file="me")
wikiname='gg'
#wikiname'spaceengineers'
site = WikiggClient(wikiname, credentials=credentials)
summary = 'Updating infobox from game data' # public commit log
inputfilecsv='demoitems.csv'

#read csv, write json
jsonDict = {}
with open(inputfilecsv, 'r', encoding='utf-8') as gamedata:
    data_csv = csv.DictReader(gamedata, delimiter='\t')
    for blockdata in data_csv:
        key=blockdata['blockname']+"_"+blockdata['grid_size']
        jsonDict[key]=blockdata

        print("Reading CSV data for "+blockdata['blockname'])
        with open(inputfilecsv+'.json', 'w', encoding='utf-8') as jsonf: 
            jsonString = json.dumps(jsonDict, indent=4)
            jsonf.write(jsonString)
        
        with open(inputfilecsv+'.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    print("Converted CSV to JSON in "+inputfilecsv+'.json.')

class TemplateModifier(TemplateModifierBase):
    def update_template(self, template: Template):
        # TemplateModifier is a generic framework for modifying templates
        # It will iterate through all pages containing at least one instance
        # of the specified template in the initialization call below and then
        # update every instance of the template in question with one batched edit per page
        if self.current_page.namespace != 0:
            # don't do anything outside of the main namespace
            # for example, we don't want to modify template documentation or user sandboxes
            return
        print("Processing page: "+ self.current_page.name)

        # determine whether large/small/both block, then set known values
        if(self.current_page.name+"_Small" in data):
            #Defaults
            infoSmall = data[self.current_page.name+"_Small"]
            template.add('name', infoSmall['blockname'])
            template.add('DataPowerUnitSmall','kW')
            template.add('DataCapacityUnitSmall','kg')
            template.add('DataMassSmall', '0')
            template.add('DataHPSmall', '0')
            template.add('DataPcuSmall', '0')
            template.add('DataTimeSmall', '0')
            template.add('DataSizeSmall', '0x0x0')
            template.add('DataCapacitySmall', '')
            template.add('DataPowerSmall', '')
            template.add('DataForceSmall', '')
            template.add('DataRangeSmall', '')
            #Overwrite defaults with values
            template.add('DataCategory', infoSmall['blockCategory'])
            template.add('DataFunction', '')
            template.add('DataFitsSmall', 'yes')
            template.add('DataMassSmall', infoSmall['mass'])
            template.add('DataHPSmall', infoSmall['hitpoints'])
            template.add('DataPcuSmall', infoSmall['pcu_pc'])
            template.add('DataTimeSmall', infoSmall['build_time_secs'])
            template.add('DataSizeSmall', infoSmall['size_HWD'])
            template.add('DataCapacitySmall', '')
            # only list power value if one of these is defined and not 0
            if(float(infoSmall['powerInRequired'])!=0):
                template.add('DataPowerSmall', infoSmall['powerInRequired']) #default
            elif(float(infoSmall['powerConsumeMax'])!=0):
                template.add('DataPowerSmall', infoSmall['powerConsumeMax'])
            elif(float(infoSmall['powerOutMax'])!=0):
                template.add('DataPowerSmall', infoSmall['powerOutMax'])
            # only list force and range if defined and not 0
            if(float(infoSmall['ForceMagnitude'])>0): 
                template.add('DataForceSmall', infoSmall['ForceMagnitude'])
            if(int(infoSmall['rangeMaxMeters'])>0):
                template.add('DataRangeSmall', infoSmall['rangeMaxMeters'])
        else:
            template.add('DataFitsSmall', '') # empty means no
            template.add('DataFunction', '')
            template.add('DataCategory', '')

        if(self.current_page.name+"_Large" in data):
            #Defaults
            infoLarge = data[self.current_page.name+"_Large"]
            template.add('name', infoLarge['blockname'])
            template.add('DataPowerUnitLarge','kW')
            template.add('DataCapacityUnitLarge','kg')
            template.add('DataMassLarge', '0')
            template.add('DataHPLarge', '0')
            template.add('DataPcuLarge', '0')
            template.add('DataTimeLarge', '0')
            template.add('DataSizeLarge', '0x0x0')
            template.add('DataCapacitySmall', '')
            template.add('DataPowerLarge', '')
            template.add('DataForceLarge', '')
            template.add('DataRangeLarge', '')
            #Overwrite defaults with values
            template.add('DataCategory', infoLarge['blockCategory'])
            template.add('DataFunction', '')
            template.add('DataFitsLarge', 'yes')
            template.add('DataMassLarge', infoLarge['mass'])
            template.add('DataHPLarge', infoLarge['hitpoints'])
            template.add('DataPcuLarge', infoLarge['pcu_pc'])
            template.add('DataTimeLarge', infoLarge['build_time_secs'])
            template.add('DataSizeLarge', infoLarge['size_HWD'])
            template.add('DataCapacityLarge', '')
            # only list power value if one of these is defined and not 0
            if(float(infoLarge['powerInRequired'])!=0):
                template.add('DataPowerLarge', infoLarge['powerInRequired']) #default
            elif(float(infoLarge['powerConsumeMax'])!=0):
                template.add('DataPowerLarge', infoLarge['powerConsumeMax'])
            elif(float(infoLarge['powerOutMax'])!=0):
                template.add('DataPowerLarge', infoLarge['powerOutMax'])
            # only list force and range if defined and not 0
            if(float(infoLarge['ForceMagnitude'])>0):
                template.add('DataForceLarge', infoLarge['ForceMagnitude'])
            if(int(infoLarge['rangeMaxMeters'])>0):
                template.add('DataRangeLarge', infoLarge['rangeMaxMeters'])
        else:
            template.add('DataFitsLarge', '') # empty means no  
            template.add('DataFunction', '')
            template.add('DataCategory', '')
            
        #if (recipe := self.get_recipe_text(info)) is None:
        #    return
        #template.add('Recipe', recipe)
##        # any changes made before returning will automatically be saved by the runner
##
##    @staticmethod
##    def get_recipe_text(info):
##        if len(info['ingredients']) == 0:
##            return None
##        recipe_string = '{{{{RecipePart|item={ing}|quantity={q}}}}}'
##        return ''.join(
##            [recipe_string.format(ing=string.capwords(x['ingredient']), q=x['quantity']) for x in info['ingredients']])
##
##
print("Logging on to "+wikiname+".wiki.gg.")
TemplateModifier(site, 'Info Block',summary=summary).run()
print("Logging off from "+wikiname+".wiki.gg.")
