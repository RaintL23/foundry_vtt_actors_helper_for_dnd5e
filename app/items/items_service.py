"""."""
import copy
import random
# import json
import app.static.constants as app_constants
from app.endpoints import external_api_routes

def get_value_by_key_in_dict(dictionary, key_text):
    """."""
    for key, value in dictionary.items():
        if key_text in key:
            return value
    return None

async def set_items(new_npc, template, urls):
    """
    Set items for a new NPC based on the provided template and external data.

    Args:
        new_npc (dict): The NPC to which items will be added.
        template (dict): The template containing item information.
        urls (list): The URLs to fetch the data from.

    Returns:
        dict: The updated NPC with items added.
    """
    rarity_selected = ("uncommon")
    tier_selected = ("major")
    loaded_data = await external_api_routes.get_constant_data(urls)
    items_list = next((item for item in loaded_data if item.get("name") == "items"), None)
    items_list = await process_items_data_by_5etools_api(items_list, rarity_selected, tier_selected)
    # nombre_archivo = "datos_2.json"
    # with open(nombre_archivo, "w", encoding='utf-8') as archivo:
    #     json.dump(items_list, archivo)

    if items_list:
        weapon_templates = [("ml_s_wp"),("ml_mt_wp"),("rg_s_wp"),("rg_mt_wp")]
        for wp_key in weapon_templates:
            weapon_name = template.get(wp_key)
            if weapon_name:
                selected_weapon = find_selected_items(weapon_name, items_list, "name")
                if selected_weapon:
                    new_npc["items"].append(selected_weapon)

        armor_type = template.get("armor")
        if armor_type:
            selected_armor = find_selected_items(armor_type, items_list, "type")
            if selected_armor:
                new_npc["items"].append(selected_armor)

    return new_npc


def find_selected_items(key_options, options_dict, key_for_search):
    """."""
    item_options = tuple(
        item_item for type_i in key_options if type_i is not None
        for item_item in options_dict
        if item_item.get(key_for_search)
        and isinstance(item_item[key_for_search], str)
        and type_i.lower() in item_item[key_for_search].lower()
    )
    if item_options is not None and len(item_options) > 0:
        selected_item_index = 0
        if len(item_options) > 1:
            selected_item_index = random.randint(0, len(item_options)-1)
        selected_item = item_options[selected_item_index]
        return selected_item
    return None

async def process_items_data_by_5etools_api(init_data, rarity_selected, tier_selected):
    """This method is for populating items using the link formatting used by 5etools Foundry."""
    items_final_not_processed = ()
    items_final_processed = ()

    items = init_data.get("items")
    if not items:
        return items_final_processed

    items_base = items[1].get("baseitem", [])
    items_property = items[1].get("itemProperty", [])
    items_type = items[1].get("itemType", [])

    items_0_dict = items[0].get("item", [])
    magic_variants = items[2].get("magicvariant", [])

    items_0_dict = apply_types_properties(items_0_dict, items_property ,items_type)
    items_base = apply_types_properties(items_base, items_property ,items_type)
    magic_variants = apply_types_properties(magic_variants, items_property ,items_type)

    items_base_with_variants = create_magic_variants(items_base, magic_variants)

    if items_base_with_variants:
        for item_base in items_base_with_variants:
            items_final_not_processed += (apply_item_base_to_item_0(item_base),)
    if items_0_dict:
        for item_0 in items_0_dict:
            items_final_not_processed += (apply_item_base_to_item_0(item_0),)

    if items_final_not_processed and len(items_final_not_processed) > 0:
        for item in items_final_not_processed:
            i_rarity = item.get("rarity")
            i_tier = item.get("tier")
            if (i_rarity is not None and i_rarity in rarity_selected and i_tier is not None and i_tier in tier_selected):
                items_final_processed += (apply_item_final_foundry_item_template(item),)

    return items_final_processed

def apply_types_properties(items_dict, items_property, items_type):
    """."""
    items_processed = []

    for item_1 in items_dict:
        # Process properties
        item_pro = item_1.get("property")
        if item_pro and items_property:
            item_1["property"] = tuple(
                prop_item for prop in item_pro
                for prop_item in items_property
                if prop_item.get("abbreviation") == prop
            )

        # Process type
        item_type = item_1.get("type")
        if item_type and items_type:
            matching_type = next((i_type for i_type in items_type if isinstance(i_type, dict) and i_type.get("abbreviation") == item_type), None)
            if matching_type:
                item_1["type"] = matching_type

        items_processed.append(item_1)
    return tuple(items_processed)

def process_item_base_dict(items_base):
    """Process base item dictionary into a structured format."""
    items_base_processed = []

    # items_additional_entries = items_base_dict.get("itemTypeAdditionalEntries", [])
    # items_entry = items_base_dict.get("itemEntry", [])

    keys_to_copy = [
        "name", "source", "srd", "basicRules", "page", "rarity", "weight",
        "weaponCategory", "age", "range", "reload", "dmg1", "dmg2", "dmgType",
        "firearm", "weapon", "ammoType", "value", "mace", "arrow", "packContents",
        "axe", "entries", "ac", "armor", "strength", "stealth", "bolt", "scfType",
        "club", "dagger", "sword", "hasFluff", "hasFluffImages", "polearm",
        "crossbow", "spear", "hammer", "net", "bow", "staff", "property"
    ]

    for item_1 in items_base:
        new_item_entry = {key: item_1.get(key) for key in keys_to_copy}
        items_base_processed.append(new_item_entry)

    return tuple(items_base_processed)

def apply_item_base_to_item_0(item_data):
    """Create and populate an item dictionary based on item_data."""
    # Claves que se deben copiar directamente
    base_keys = [
        "name", "source", "page", "rarity", "entries", "weight", "hasFluffImages",
        "type", "weaponCategory", "property", "dmg1", "dmg2", "dmgType", "srd", 
        "ac", "basicRules", "value", "scfType", "range", "stealth", "strength", 
        "age", "staff", "ammoType", "firearm", "packContents"
    ]

    # Claves nuevas específicas de item_0
    new_item_keys = [
        "reqAttune", "wondrous", "bonusSpellAttack", "bonusSpellSaveDc", "focus",
        "reqAttuneTags", "baseItem", "bonusWeapon", "tier", "lootTables", "resist",
        "bonusSavingThrow", "detail1", "tattoo", "hasRefs", "_copy", "_mod", "crew",
        "recharge", "rechargeAmount", "charges", "miscTags", "vehAc", "vehHp",
        "vehSpeed", "capPassenger", "capCargo", "conditionImmune", "grantsProficiency",
        "attachedSpells", "modifySpeed", "curse", "optionalfeatures", "vulnerable",
        "poison", "poisonTypes", "ability", "immune", "atomicPackContents", 
        "containerCapacity", "bonusWeaponAttack", "bonusWeaponDamage", "otherSources", 
        "grantsLanguage", "seeAlsoVehicle", "sentient", "vehDmgThresh", "typeAlt",
        "weightNote", "spellScrollLevel", "carryingCapacity", "speed", "critThreshold",
        "dexterityMax", "bonusProficiencyBonus", "reprintedAs", "reach"
    ]

    # Claves adicionales del item_data
    additional_keys = [
        "reload", "weapon", "mace", "arrow", "axe", "armor", "bolt", "club", "dagger",
        "sword", "hasFluff", "polearm", "crossbow", "spear", "hammer", "net", "bow"
    ]

    # Crear el diccionario inicial con _id
    item = {"_id": None}

    # Poblar el diccionario con las claves definidas
    for key in base_keys + new_item_keys + additional_keys:
        item[key] = item_data.get(key)

    # print(item)
    return item

def create_magic_variants(items_base, magic_variants):
    """Create magic variants of base items."""
    items_base_with_variants = list(items_base)

    if items_base and magic_variants:
        for item_magic_variant in magic_variants:
            requires = item_magic_variant.get("requires")
            inherits = item_magic_variant.get("inherits")

            if requires and inherits:
                filtered_items_base = []

                for require in requires:
                    req_type = require.get("type")
                    req_weapon = require.get("weapon")
                    req_armor = require.get("armor")

                    for item in items_base:
                        item_base_type = item.get("type")
                        item_base_is_weapon = item.get("weapon")
                        item_base_is_armor = item.get("armor")

                        if req_type and item_base_type:
                            if item_base_type == req_type or (isinstance(item_base_type, dict) and
                                                    item_base_type.get("abbreviation") == req_type):
                                filtered_items_base.append(item)
                        elif req_weapon and item_base_is_weapon:
                            filtered_items_base.append(item)
                        elif req_armor and item_base_is_armor:
                            filtered_items_base.append(item)

                for item_to_add_variant in filtered_items_base:
                    items_base_with_variants.append(
                        apply_item_magic_variant(copy.deepcopy(item_to_add_variant), inherits)
                    )

    return tuple(items_base_with_variants)

def apply_item_magic_variant(item, variant):
    """Apply the properties of a variant to an item."""
    variant_name_prefix = variant.get("namePrefix", "") or ""
    variant_name_suffix = variant.get("nameSuffix", "") or ""
    item_name = item.get("name")
    # print(f"item_type {item_type}")

    # Data of the baseItem that is equal to that of itemMagicVariant
    base_keys = [
        "source", "srd", "basicRules", "page", "type", "rarity", "entries",
        "strength", "stealth", "tier"
    ]

    # New data from the Magic Variant
    variant_keys = [
        "rarity", "bonusWeapon", "entries", "lootTables", "basicRules",
        "bonusAc", "reqAttune", "reqAttuneTags", "attachedSpells", "hasRefs",
        "charges", "resist", "valueExpression", "recharge", "rechargeAmount",
        "wondrous", "bonusSpellDamage", "nameRemove", "weightMult",
        "weightExpression", "valueMult", "barding", "strength", "stealth",
        "modifySpeed", "curse", "bonusWeaponDamage", "otherSources",
        "bonusSavingThrow", "grantsProficiency"
    ]

    # Data of the baseItem that may or may not be in the record
    optional_keys = [
        "weight", "weaponCatego", "age", "property", "range", "reload",
        "dmg1", "dmg2", "dmgType", "firearm", "weapon", "ammoType", "value",
        "mace", "arrow", "packContents", "axe", "ac", "armor", "bolt",
        "scfType", "club", "dagger", "sword", "hasFluff", "hasFluffImag",
        "polearm", "crossbow", "spear", "hammer", "net", "bow", "staff", "type"
    ]

    new_item = {"_id": None}
    # Update the item name with the variant prefix and suffix
    new_item["name"] = f"{variant_name_prefix}{item_name}{variant_name_suffix}"
    # Update item with base keys
    for key in base_keys:
        new_item[key] = variant.get(key)

    # Update item with variant keys
    for key in variant_keys:
        new_item[key] = variant.get(key)

    # Update item with optional keys, if they exist
    for key in optional_keys:
        new_item[key] = item.get(key)

    return new_item

def get_item_entries(entries):
    """."""
    description = ""
    for entrie in entries:
        description += "\n"
        if isinstance(entrie, str):
            description += entrie
        elif isinstance(entrie, list):
            description += get_item_entries(entrie)

    return description

def apply_item_final_foundry_item_template(item):
    """Apply the final Foundry item template to the given item."""
    item_type = item.get("type")
    item_strength = item.get("strength")
    final_item_json = {
        "_id": item.get("_id"),
        "name": item.get("name"),
        "type": item.get("type"),
        "system": {
            "source": {
                "custom": item.get(""),
                "book": item.get("source"),
                "page": item.get("page"),
                "license": item.get(""),
            },
            "description": {
                "value": "",
                "chat": "",
            },
            "proficient": "",
            "quantity": 1,
            "weight": item.get("weight"),
            "price": {
                "value": item.get("value"),
                "denomination": "gp",
            },
            "identified": True,
            "equipped": True,
            "rarity": item.get("rarity"),
            "type": {
                "value": item_type if isinstance(item_type, str) else 
                        (item_type.get("name") if item_type else ""),
                "baseItem": "",
            },
            "attunement": 0,
            "activation": {
                "type": "",
                "cost": 0,
                "condition": "",
            },
            "duration": {
                "value": "",
                "units": "",
            },
            "target": {
                "value": 0,
                "units": "",
                "type": "",
                "width": None,
                "prompt": True,
            },
            "range": {
                "value": None,
                "long": None,
                "units": "",
            },
            "uses": {
                "value": None,
                "max": "",
                "per": None,
                "recovery": "",
                "prompt": True,
            },
            "actionType": "",
            "attack": {
                "bonus": "",
                "flat": False,
            },
            "chatFlavor": "",
            "critical": {
                "threshold": None,
                "damage": "",
            },
            "damage": {
                "parts": [],
                "versatile": "",
            },
            "formula": "",
            "save": {
                "ability": "",
                "dc": None,
                "scaling": "flat",
            },
            "armor": {
                "value": item.get("ac"),
                "dex": 0 if isinstance(item_type, str) and item_type == "MA" 
                        else None,
                "magicalBonus": None,
            },
            "strength": int(item_strength) if item_strength
                        and isinstance(item_strength, str) else None,
            "consume": {
                "type": "",
                "target": None,
                "amount": None,
                "scale": False,
            },
            "hp": {
                "value": 0,
                "max": 0,
                "dt": None,
                "conditions": "",
            },
            "speed": {
                "value": None,
                "conditions": "",
            },
            "unidentified": {
                "description": "",
            },
            "container": None,
            "cover": None,
            "crewed": False,
            "summons": None,
        },
        "img": "",
        "ownership": {
            "default": 0,
        },
    }

    # Add description value if entries exist
    item_entries = item.get("entries")
    if item_entries:
        final_item_json["system"]["description"]["value"] = get_item_entries(item_entries)

    # Add abilities if they exist
    item_ability = item.get("ability")
    if item_ability:
        for item_key in item_ability.keys():
            if item_key in app_constants.ATTRIBUTES_FOR_DND5E:
                final_item_json["system"]["ability"] = item_key
                break

    # Add properties if they exist
    item_properties = item.get("property")
    if item_properties:
        final_item_json["system"]["properties"] = tuple(
            i_property.get("abbreviation").lower() for i_property in item_properties
        )

    # Check if the item is a weapon and set related fields
    item_is_weapon = item.get("weapon")
    if item_is_weapon:
        final_item_json["system"]["activation"].update({"type": "action", "cost": 1})

        item_w_range = item.get("range")
        if item_w_range:
            item_w_ranges = item_w_range.split("/")
            final_item_json["system"]["range"].update({
                "value": int(item_w_ranges[0]),
                "long": int(item_w_ranges[1]),
                "units": "ft.",
            })
        else:
            final_item_json["system"]["range"].update({
                "value": 5,
                "long": 0,
                "units": "ft.",
            })

        final_item_json["system"]["actionType"] = "mwak" if final_item_json["system"]["range"]["value"] <= 5 else "rwak"

        item_bonus_weapon = item.get("bonusWeapon")
        if item_bonus_weapon:
            final_item_json["system"]["attack"]["bonus"] = item_bonus_weapon

        item_damage_1 = item.get("dmg1")
        item_damage_1_type = item.get("dmgType")
        if item_damage_1 and item_damage_1_type:
            item_damage_1_type_cons = app_constants.DAMAGE_TYPES.get(item_damage_1_type, "")
            final_item_json["system"]["damage"]["parts"].append(
                [f"{item_damage_1}+@mod", item_damage_1_type_cons]
            )

        item_damage_2 = item.get("dmg2")
        if item_damage_2:
            final_item_json["system"]["damage"]["versatile"] = f"{item_damage_2}+@mod"
    # return {}
    return final_item_json
