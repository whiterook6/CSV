import json
from pprint import pprint
import re

# returns an array of aliases to values
def getValuesFromStats(stats):
	values={}
	for stat in stats:
		value=stat["-value"]

		if type(stat["alias"]) is list:
			for alias in stat["alias"]:
					name=alias["-name"]
					values[name]=value
		else:
			name=stat["alias"]["-name"]
			values[name]=value

	return values

# remove any values whose keys aren't in the given set
def filterStats(statValues, keys):
	return { key: int(statValues[key]) for key in keys}

# remove any objects with type not in the given set
def filterRules(rules, types):
	return [rule for rule in rules if rule["-type"] in types]

def parseFeats(rules):
	feats=[]
	for rule in rules:
		feat={"Name": rule["-name"].strip(), "Description": rule["#text"].strip()}

		specifics=rule["specific"]
		if type(specifics) is list:
			for specific in specifics:
				if "#text" in specific:
					name=specific["-name"].strip()
					text=specific['#text'].strip()
					if name.find("_")!=0:
						feat[name]=text

		feats.append(feat)
	return feats

def parsePowers(powerStats):
	powers=[]
	for powerStat in powerStats:
		power={"Name": powerStat["-name"].strip()}

		# get specific info about the power: target, range, etc.
		for specific in powerStat["specific"]:
			if "#text" in specific:
				name=specific["-name"].strip()
				text=specific['#text'].strip()
				if name not in ["_Associated Feats", "Class"] and name.find("_")!=0:
					power[name]=text

		# if one or more weapons are used, pick the best (or only) and copy over the important bits
		# (so much trash)
		if "Weapon" in powerStat:
			chosenWeapon={}

			if type(powerStat["Weapon"]) is list:
				first=True
				for weapon in powerStat["Weapon"]:
					if first or int(chosenWeapon["AttackBonus"]) < int(weapon["AttackBonus"]):
						chosenWeapon=weapon
						first=False
			else:
				chosenWeapon=powerStat["Weapon"]

			# copy over important bits
			power["AttackBonus"]=chosenWeapon["AttackBonus"].strip()

			# for weapons used with no damage, damage="Until+0" for some reason, so skip
			chosenWeaponDamage=chosenWeapon["Damage"].strip()
			if len(chosenWeaponDamage)>0 and chosenWeaponDamage.find("Until+0")==-1:
				power["Damage"]=chosenWeapon["Damage"].strip()

			power["CritDamage"]=chosenWeapon["CritDamage"].strip()
			power["Weapon"]=chosenWeapon["-name"]

		if "Keywords" in power:
			power["Keywords"]=[x.strip() for x in power["Keywords"].split(',')]

		powers.append(power)
	return powers

def filterLoot(loots, filters):
	filteredLoot=[]

	for loot in loots:
		rules=loot["RulesElement"]

		if type(rules) is list:
			for rule in rules:
				if rule["-type"] in filters:
					filteredLoot.append(buildLoot(rule))

		elif rules["-type"] in filters:
			filteredLoot.append(buildLoot(rules))

	return filteredLoot

def buildLoot(rule):
	lootItem={"Name": rule["-name"], "Type": rule["-type"]}
	if "#text" in rule:
		lootItem["Description"]=rule["#text"]
		
	# get specific info about the loot
	for specific in rule["specific"]:
		if "#text" in specific:
			name=specific["-name"].strip()
			text=specific['#text'].strip()
			if name not in ["_Associated Feats", "Class"] and name.find("_")!=0:
				lootItem[name]=text

	return lootItem


#build character object
pacha={}

# Read data sheet
json_data = open("Pacha.json", encoding='latin-1').read()
json_data=re.sub('\s+', ' ', json_data).strip()

data=json.loads(json_data);
characterSheet=data["D20Character"]["CharacterSheet"]
details=characterSheet["Details"]
pacha["Details"]={key : details[key].strip() for key in details}

# STATSBLOCK #
# statsblock has final ability scores -- abilities only shows starting scores.
stats=characterSheet["StatBlock"]["Stat"]
statValues=getValuesFromStats(stats)

# organize values by category into objects
abilityKeys=["Strength", "Constitution", "Dexterity", "Intelligence", "Wisdom", "Charisma"]
pacha["Abilities"]=filterStats(statValues, abilityKeys)

defenseKeys=["AC", "Fortitude", "Reflex", "Will"]
pacha["Defenses"]=filterStats(statValues, defenseKeys)

healthKeys=["Hit Points", "Healing Surges"]
pacha["Health"]=filterStats(statValues, healthKeys)

agilityKeys=["Speed", "Initiative"]
pacha["Agility"]=filterStats(statValues, agilityKeys)

senseKeys=["Passive Perception", "Passive Insight"]
pacha["Senses"]=filterStats(statValues, senseKeys)

skillKeys=["Acrobatics","Arcana","Athletics","Bluff",
"Diplomacy","Dungeoneering","Endurance","Heal",
"History","Insight","Intimidate","Nature","Perception",
"Religion","Stealth","Streetwise","Thievery"]
pacha["Skills"]=filterStats(statValues, skillKeys)


# RULES ELEMENTS #
# RulesElements has feats and features
rules=characterSheet["RulesElementTally"]["RulesElement"]
pacha["Feats"]=parseFeats(filterRules(rules, ["Class Feature", "Feat"]))


powerStats=characterSheet["PowerStats"]["Power"]
pacha["Powers"]=parsePowers(powerStats)

loots=characterSheet["LootTally"]["loot"]
pacha["Rituals"]=filterLoot(loots, ["Ritual"])
pacha["Magic Items"]=filterLoot(loots, ["Magic Item"])

print(json.dumps(pacha, sort_keys=True, indent=4, separators=(',', ': ')))