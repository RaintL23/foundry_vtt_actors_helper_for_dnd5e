import re
import copy
import json
import random
import app.static.constants as app_constants
from app.endpoints import external_api_service

async def create(json_template, user_init_data):
    current_template = set_template(user_init_data["template"])
    new_npc = json_template
    new_npc["name"] = user_init_data["name"]
    new_npc["prototypeToken"]["name"] = user_init_data["name"]
    new_npc = set_attributes(new_npc,
                                    current_template,
                                    user_init_data["attribute_array"])
    
    new_npc = set_race(new_npc,user_init_data["race"])
    new_npc = await set_items(new_npc,current_template,user_init_data["urls"])

    # Create JSON file
    nombre_archivo = "datos.json"
    with open(nombre_archivo, "w", encoding='utf-8') as archivo:
        json.dump(new_npc, archivo, indent=4)
    print(new_npc)
    return new_npc

def set_template(template):
    return app_constants.TEMPLATE_OPTIONS[template]

def set_attributes(new_npc, template, attribute_array):
    # Start Seting attribute values
    selected_attribute_array = set_attribute_array_template(attribute_array)
    selected_template_attribute_priority = set_attribute_priority_template(template)
    selected_template_attribute_proficiencies = (
        set_attribute_proficiencies_template(template)
    )

    for i,attribute in enumerate(selected_template_attribute_priority):
        new_npc["system"]["abilities"][attribute]["value"] = selected_attribute_array[i]
        # Set the proficiency at once if applicable.
        if (selected_template_attribute_proficiencies is not None and
            attribute in selected_template_attribute_proficiencies):
            new_npc["system"]["abilities"][attribute]["proficient"] = app_constants.PROFICIENT

    # Next with Skills
    selected_skills_proficiencies = set_skills_proficiencies(template)
    if selected_template_attribute_proficiencies is not None:
        for i,skill in enumerate(selected_skills_proficiencies):
            new_npc["system"]["skills"][skill]["value"] = app_constants.PROFICIENT

    return new_npc

def set_attribute_array_template(attribute_array):
    """."""
    match attribute_array:
        case "terrible":
            selected_attribute_array = app_constants.ATTRIBUTE_ARRAY_TERRIBLE
        case "bad":
            selected_attribute_array = app_constants.ATTRIBUTE_ARRAY_BAD
        case "poor":
            selected_attribute_array = app_constants.ATTRIBUTE_ARRAY_POOR
        case "medium":
            selected_attribute_array = app_constants.ATTRIBUTE_ARRAY_MEDIUM
        case "good":
            selected_attribute_array = app_constants.ATTRIBUTE_ARRAY_GOOD
        case "hero":
            selected_attribute_array = app_constants.ATTRIBUTE_ARRAY_HERO
        case "epic":
            selected_attribute_array = app_constants.ATTRIBUTE_ARRAY_EPIC
        case "standard" | _:
            selected_attribute_array = app_constants.ATTRIBUTE_ARRAY_STANDARD
    return selected_attribute_array

def set_attribute_priority_template(template):
    """."""
    if "attributes_priority_array" in template:
        selected_template_attribute_priority = template["attributes_priority_array"]
        if selected_template_attribute_priority is not None:
            return selected_template_attribute_priority
    return None

def set_attribute_proficiencies_template(template):
    """."""
    if "attributes_proficient_array" in template:
        selected_template_attribute_proficiencies = template["attributes_proficient_array"]
        if selected_template_attribute_proficiencies is not None:
            return selected_template_attribute_proficiencies
    return None

def set_skills_proficiencies(template):
    """."""
    if "skills_proficient_array" in template:
        selected_skills_proficiencies = template["skills_proficient_array"]
        if selected_skills_proficiencies is not None:
            return selected_skills_proficiencies
    return None

def set_race(new_npc, race):
    """."""
    if race is None:
        new_npc["system"]["details"]["race"] = None
        new_npc["system"]["details"]["type"]["value"] = "custom"
        new_npc["system"]["details"]["type"]["custom"] = race
    return new_npc

def fill_item_data(npc_data, item, item_data, item_type_name, action_type, ability_item):
    """."""
    item["name"] = ""
    if item_data.get('name') is not None:
        item["name"] = item_data.get('name')
    item["_stats"] = npc_data["_stats"]
    item["type"] = item_type_name
    item["system"]["description"] = {
        "value": "",
        "chat": ""
    }
    item["system"]["source"] = {}
    item["system"]["identified"] = True
    item["system"]["unidentified"] = {
        "description": ""
    }
    item["system"]["container"] = None
    item["system"]["quantity"] = 1
    weight = item_data["weight"].split()
    if weight is not None and len(weight) > 0:
        item["system"]["weight"] = int(weight[0].lower())
    else:
        item["system"]["weight"] = 0
    item["system"]["value"] = None
    item["system"]["proficient"] = None
    item["system"]["equipped"] = True
    price = item_data["cost"].split()
    if price is not None and len(price) > 1:
        item["system"]["price"] = {
            "value": int(price[0].lower().replace(",", "")),
            "denomination": price[1].lower()
        }
    item["system"]["rarity"] = "common"
    item_type = item_data["category"].split()
    if item_type:
        if len(item_type) == 2:
            item["system"]["type"] = {
                "value": item_type[0].lower(),
                "baseItem": item_data["name"].lower().replace(" ", "")
            }
        elif len(item_type) > 2:
            item["system"]["type"] = {
                "value": f"{item_type[0].lower()}{item_type[1][0].upper()}",
                "baseItem": item_data["name"].lower().replace(" ", "")
            }
    item["system"]["ability"] = None
    if item_type_name == "weapon":
        item["system"]["ability"] = ability_item
    item["system"]["attunement"] = 0
    item["system"]["properties"] = []
    if (item_data.get('stealth_disadvantage') is not None and
        item_data.get('stealth_disadvantage') is True):
        item["system"]["properties"].append('stealthDisadvantage')
    item["system"]["activation"] = {
        "type": "",
        "cost": None,
        "condition": ""
    }
    if item_type_name == "weapon":
        item["system"]["activation"]["type"] = "action"
        item["system"]["activation"]["cost"] = 1
    item["system"]["duration"] = {
        "value": "",
        "units": ""
    }
    item["system"]["target"] = {
        "value": None,
        "width": None,
        "units": "",
        "type": "",
        "prompt": True
    }
    item["system"]["range"] = {
        "value": None,
        "long": None,
        "units": "ft"
    }
    if action_type == "mwak":
        item["system"]["range"]["value"] = 5
    item["system"]["uses"] = {
        "value": None,
        "max": "",
        "per": None,
        "recovery": "",
        "prompt": True
    }
    item["system"]["actionType"] = action_type
    item["system"]["attack"] = {
        "bonus": "",
        "flat": False
    }
    item["system"]["cover"] = None
    item["system"]["crewed"] = False
    item["system"]["summons"] = None
    item["system"]["chatFlavor"] = ""
    item["system"]["strength"] = None
    item["system"]["formula"] = ""
    item["system"]["consume"] = {
        "type": "",
        "target": None,
        "amount": None,
        "scale": False
    }
    item["system"]["critical"] = {
        "threshold": None,
        "damage": ""
    }
    item["system"]["damage"] = {
        "parts": [],
        "versatile": ""
    }
    if item_data.get('damage_dice') is not None:
        damage = f"{item_data.get('damage_dice')}+@mod"
        item["system"]["damage"]["parts"].append([damage,item_data.get('damage_type')])
    if (item_data.get('properties') is not None and len(item_data.get('properties')) > 0):
        for item_property in item_data.get('properties'):
            item_property_name = get_value_by_key_in_dict(
                app_constants.TEMPLATE_PROPERTY_NAME, item_property
            )
            if item_property_name is not None:
                item["system"]["properties"].append(item_property_name)
            if item_type_name == "weapon":
                if "versatile" in item_property:
                    versatile_damage = item_property
                    if versatile_damage is not None and versatile_damage != "":
                        versatile_damage = re.search(r'\(([^)]+)\)', versatile_damage)
                        item["system"]["damage"]["versatile"] = f"{versatile_damage.group(1)}+@mod"
                if "ammunition" in item_property:
                    range_weapon = item_property
                    if range_weapon is not None and range_weapon != "":
                        range_weapon = re.search(r'\(([^)]+)\)', range_weapon)
                        range_weapon = re.search(r'(\d+)/(\d+)', range_weapon.group(1))
                        ranges_weapon = range_weapon.group(0).split("/")
                        item["system"]["range"]["value"] = int(ranges_weapon[0])
                        item["system"]["range"]["long"] = int(ranges_weapon[1])
    item["system"]["save"] = {
        "ability": "",
        "dc": None,
        "scaling": "spell"
    }
    item["system"]["armor"] = {
        "value": item_data.get('base_ac'),
        "magicalBonus": None,
        "dex": item_data.get('plus_max')
    }
    item["system"]["hp"] = {
        "value": None,
        "max": None,
        "dt": None,
        "conditions": ""
    }
    item["system"]["speed"] = {
        "value": None,
        "conditions": ""
    }
    # print(item)
    # print(item_data)
    return item

def get_value_by_key_in_dict(dictionary, key_text):
    """."""
    for key, value in dictionary.items():
        if key_text in key:
            return value
    return None

async def set_items(new_npc, template, urls):
    """."""
    loaded_data_json_data = await external_api_service.get_constant_data(urls)
    
    weapons = next((item for item in loaded_data_json_data if item.get("name") == "weapons"), None)
    armors = next((item for item in loaded_data_json_data if item.get("name") == "armor"), None)
    # print(weapons)
    # Weapons
    if weapons is not None and weapons["count"] > 0:
        ml_s_wp = template["ml_s_wp"]
        rg_s_wp = template["rg_s_wp"]
        ml_mt_wp = template["ml_mt_wp"]
        rg_mt_wp = template["rg_mt_wp"]
        # print(weapons["items"])
        if ml_s_wp is not None:
            selected_weapon = find_selected_items(ml_s_wp, weapons, "name")
            new_npc["items"].append(
                fill_item_data(
                    copy.deepcopy(new_npc),
                    copy.deepcopy(app_constants.TEMPLATE_DEFAULT_ITEM),
                    selected_weapon,
                    "weapon",
                    "mwak",
                    "str"
                )
            )
        if ml_mt_wp is not None:
            selected_weapon = find_selected_items(ml_mt_wp, weapons, "name")
            new_npc["items"].append(
                fill_item_data(
                    copy.deepcopy(new_npc),
                    copy.deepcopy(app_constants.TEMPLATE_DEFAULT_ITEM),
                    selected_weapon,
                    "weapon",
                    "mwak",
                    "str"
                )
            )
        if rg_s_wp is not None:
            selected_weapon = find_selected_items(rg_s_wp, weapons, "name")
            new_npc["items"].append(
                fill_item_data(
                    copy.deepcopy(new_npc),
                    copy.deepcopy(app_constants.TEMPLATE_DEFAULT_ITEM),
                    selected_weapon,
                    "weapon",
                    "rwak",
                    "dex"
                )
            )
        if rg_mt_wp is not None:
            selected_weapon = find_selected_items(rg_mt_wp, weapons, "name")
            new_npc["items"].append(
                fill_item_data(
                    copy.deepcopy(new_npc),
                    copy.deepcopy(app_constants.TEMPLATE_DEFAULT_ITEM),
                    selected_weapon,
                    "weapon",
                    "rwak",
                    "dex"
                )
            )

    # Armor
    armor_type = template["armor"]
    if armors is not None and armors["count"] > 0 and armor_type is not None:
        selected_armor = find_selected_items(armor_type, armors, "category")
        new_npc["items"].append(
            fill_item_data(
                copy.deepcopy(new_npc),
                copy.deepcopy(app_constants.TEMPLATE_DEFAULT_ITEM),
                selected_armor,
                "equipment",
                "", None
            )
        )

    return new_npc

def find_selected_items(key_options, options_dict, key_for_search):
    """."""
    item_options = tuple(
        item_item
        for type_i in key_options if type_i is not None
        for item_item in options_dict["items"]
        if type_i.lower() in item_item[key_for_search].lower()
    )
    if item_options is not None and len(item_options) > 0:
        selected_item_index = 0
        if len(item_options) > 1:
            selected_item_index = random.randint(0, len(item_options)-1)
        selected_item = item_options[selected_item_index]
        return selected_item
    return None


