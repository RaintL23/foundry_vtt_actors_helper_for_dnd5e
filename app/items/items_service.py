"""."""
import re
import copy
import random
import app.static.constants as app_constants
from app.endpoints import external_api_routes

def get_value_by_key_in_dict(dictionary, key_text):
    """."""
    for key, value in dictionary.items():
        if key_text in key:
            return value
    return None

async def set_items(new_npc, template, urls):
    """."""
    loaded_data_json_data = await external_api_routes.get_constant_data(urls)
    weapons = next((item for item in loaded_data_json_data if item.get("name") == "weapons"), None)
    armors = next((item for item in loaded_data_json_data if item.get("name") == "armor"), None)
    items_list = next((item for item in loaded_data_json_data if item.get("name") == "items"), None)
    items_list = await process_items_data_by_5etools_api(items_list)

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

def fill_item_data(npc_data, item, item_data, item_type_name, action_type, ability_item):
    """This method is to fill in the items using the format of https://api.open5e.com/."""
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

async def process_items_data_by_5etools_api(init_data):
    """This method is for populating items using the link formatting used by 5etools Foundry."""

    items_processed = ()

    items = init_data.get("items")
    if not items:
        return items_processed

    items_0_dict = items[0].get("item", [])
    items_base = items[1].get("baseitem", [])
    magic_variants = items[2].get("magicvariant", [])
    # print(type(items_base))
    # print(items[0].keys())

    # We are going to use the items_magic_variant to generate
    # new base_items but with its designated variant
    if items_base and magic_variants:
        for item_magic_variant in magic_variants:
            requires = item_magic_variant.get("requires")
            inherits = item_magic_variant.get("inherits")

            if requires and inherits:
                for requieres_type in requires:
                    req_type = requieres_type.get("type")

                    if req_type:
                        filtered_data = [d for d in items_base if d.get("type") == req_type]

                        for item_to_add_variant in filtered_data:
                            items_processed += (
                                apply_item_magic_variant(
                                    copy.deepcopy(item_to_add_variant), inherits
                                ),
                            )
                        # print(requieres_type["type"])
                        # print(filtered_data)
                        # print(item_magic_variant["inherits"])

    print(len(items_processed))
    print(len(magic_variants))
    # print(items_processed)
    return items_processed


def apply_item_magic_variant(item, variant):
    """."""
    variant_name_prefix = variant.get("namePrefix", "") or ""
    variant_name_suffix = variant.get("nameSuffix", "") or ""
    item_name = item.get("name")

    # Datos nuevos que vienen desde la Magic Variant
    item["name"] += f"{variant_name_prefix}{item_name}{variant_name_suffix}"
    item["tier"] = variant.get("tier")
    item["rarity"] = variant.get("rarity")
    item["bonusWeapon"] = variant.get("bonusWeapon")
    item["entries"] = variant.get("entries")
    item["lootTables"] = variant.get("lootTables")
    item["basicRules"] = variant.get("basicRules")
    item["bonusAc"] = variant.get("bonusAc")
    item["reqAttune"] = variant.get("reqAttune")
    item["reqAttuneTags"] = variant.get("reqAttuneTags")
    item["attachedSpells"] = variant.get("attachedSpells")
    item["hasRefs"] = variant.get("hasRefs")
    item["charges"] = variant.get("charges")
    item["resist"] = variant.get("resist")
    item["valueExpression"] = variant.get("valueExpression")
    item["recharge"] = variant.get("recharge")
    item["rechargeAmount"] = variant.get("rechargeAmount")
    item["wondrous"] = variant.get("wondrous")
    item["bonusSpellDamage"] = variant.get("bonusSpellDamage")
    item["nameRemove"] = variant.get("nameRemove")
    item["type"] = variant.get("type")
    item["weightMult"] = variant.get("weightMult")
    item["weightExpression"] = variant.get("weightExpression")
    item["valueMult"] = variant.get("valueMult")
    item["barding"] = variant.get("barding")
    item["strength"] = variant.get("strength")
    item["stealth"] = variant.get("stealth")
    item["modifySpeed"] = variant.get("modifySpeed")
    item["curse"] = variant.get("curse")
    item["bonusWeaponDamage"] = variant.get("bonusWeaponDamage")
    item["otherSources"] = variant.get("otherSources")
    item["bonusSavingThrow"] = variant.get("bonusSavingThrow")
    item["grantsProficiency"] = variant.get("grantsProficiency")

    # Datos del baseItem que son iguales al de itemMagicVariant
    item["source"] = variant.get("source")
    item["srd"] = variant.get("srd")
    item["basicRules"] = variant.get("basicRules")
    item["page"] = variant.get("page")
    item["type"] = variant.get("type")
    item["rarity"] = variant.get("rarity")
    item["entries"] = variant.get("entries")
    item["strength"] = variant.get("strength")
    item["stealth"] = variant.get("stealth")

    # Datos del baseItem que pueden si o no estar en el registro
    item["weight"] = item.get("weight")
    item["weaponCatego"] = item.get("weaponCatego")
    item["age"] = item.get("age")
    item["property"] = item.get("property")
    item["range"] = item.get("range")
    item["reload"] = item.get("reload")
    item["dmg1"] = item.get("dmg1")
    item["dmg2"] = item.get("dmg2")
    item["dmgType"] = item.get("dmgType")
    item["firearm"] = item.get("firearm")
    item["weapon"] = item.get("weapon")
    item["ammoType"] = item.get("ammoType")
    item["value"] = item.get("value")
    item["mace"] = item.get("mace")
    item["arrow"] = item.get("arrow")
    item["packContents"] = item.get("packContents")
    item["axe"] = item.get("axe")
    item["ac"] = item.get("ac")
    item["armor"] = item.get("armor")
    item["bolt"] = item.get("bolt")
    item["scfType"] = item.get("scfType")
    item["club"] = item.get("club")
    item["dagger"] = item.get("dagger")
    item["sword"] = item.get("sword")
    item["hasFluff"] = item.get("hasFluff")
    item["hasFluffImag"] = item.get("hasFluffImag")
    item["polearm"] = item.get("polearm")
    item["crossbow"] = item.get("crossbow")
    item["spear"] = item.get("spear")
    item["hammer"] = item.get("hammer")
    item["net"] = item.get("net")
    item["bow"] = item.get("bow")
    item["mace"] = item.get("mace")
    item["staff"] = item.get("staff")

    return item
