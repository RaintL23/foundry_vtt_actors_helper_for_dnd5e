"""CONSTANTS"""
# ATTRIBUTES FOR DND5E
# str dex con int wis cha
# SKILL FOR DND5E
# acr ani arc ath dec his ins itm inv med nat prc prf per rel slt ste sur

JSON_USER_INIT_DATA = {}
JSON_NPC_TEMPLATE = {}
"""TEMPLATE FOR APP INSTANCE USE"""

# We are using the 5etools api (https://api.open5e.com/) endpoints because they put everything
# in easy access to get the necessary data.
# URL_ITEMS = "https://5etools-mirror-1.github.io/data/items.json"
# URL_ITEMS_BASE = "https://5etools-mirror-1.github.io/data/items-base.json"
# URL_ITEMS_MAGIC_VARIANTS = "https://5etools-mirror-1.github.io/data/magicvariants.json"
# URL_RACES = "https://5etools-mirror-1.github.io/data/races.json"
# URL_SPELLS = "https://5etools-mirror-1.github.io/data/spells/"
# URL_CLASSES = "https://5etools-mirror-1.github.io/data/class/"
# URL_OPTIONAL_FEATURES = "https://5etools-mirror-1.github.io/data/optionalfeatures.json"
URL_MANIFEST = "https://api.open5e.com/v1/manifest/?format=json"
URL_SPELLS = "https://api.open5e.com/v1/spells/?format=json"
URL_SPELLLIST = "https://api.open5e.com/v1/spelllist/?format=json"
URL_MONSTERS = "https://api.open5e.com/v1/monsters/?format=json"
URL_DOCUMENTS = "https://api.open5e.com/v1/documents/?format=json"
URL_BACKGROUNDS = "https://api.open5e.com/v1/backgrounds/?format=json"
URL_PLANES = "https://api.open5e.com/v1/planes/?format=json"
URL_SECTIONS = "https://api.open5e.com/v1/sections/?format=json"
URL_FEATS = "https://api.open5e.com/v1/feats/?format=json"
URL_CONDITIONS = "https://api.open5e.com/v1/conditions/?format=json"
URL_RACES = "https://api.open5e.com/v1/races/?format=json"
URL_CLASSES = "https://api.open5e.com/v1/classes/?format=json"
URL_MAGICITEMS = "https://api.open5e.com/v1/magicitems/?format=json"
URL_WEAPONS = "https://api.open5e.com/v1/weapons/?format=json"
URL_ARMOR = "https://api.open5e.com/v1/armor/?format=json"
URL_SEARCH = "https://api.open5e.com/v1/search/?format=json"
"""API ENPOINTS"""

ATTRIBUTE_ARRAY_TERRIBLE = (8,8,8,8,7,7)
ATTRIBUTE_ARRAY_BAD = (10,10,10,10,10,8)
ATTRIBUTE_ARRAY_POOR = (12,12,11,10,10,8)
ATTRIBUTE_ARRAY_MEDIUM = (14,12,12,10,10,8)
ATTRIBUTE_ARRAY_STANDARD = (15,14,13,12,10,8)
ATTRIBUTE_ARRAY_GOOD = (16,14,12,11,10,10)
ATTRIBUTE_ARRAY_HERO = (18,16,14,12,10,10)
ATTRIBUTE_ARRAY_EPIC = (20,16,14,14,12,10)
"""ATTRIBUTE ARRAY"""

HIT_DICE_TINY = 4
HIT_DICE_SMALL = 6
HIT_DICE_MEDIUM = 8
HIT_DICE_LARGE = 10
HIT_DICE_HUGE = 12
HIT_DICE_GARGANTUAN = 20
"""HIT DICE SIZE"""

PROFICIENT_HALF = 0.5
PROFICIENT = 1
PROFICIENT_EXPERTISE = 2
"""SKILL PROFICIENT"""

TEMPLATE_OPTIONS = {
    "follower_soldier": {
        "name": "follower_soldier",
        "attributes_priority_array": ("str", "con", "dex", "wis", "cha","int"),
        "attributes_proficient_array": ("str", "con"),
        "skills_proficient_array": ("ath", "his"),
        "skills_proficient_half_array": ("med", "his"),
        "skills_proficient_expertise_array": ("rel"),
        "ml_s_wp":("Handaxe","Javelin","Spear"),
        "rg_s_wp":("light Crossbow","Shortbow"),
        "ml_mt_wp":("Battleaxe","Glaive","Greataxe","Greatsword",
                    "Halberd","Longsword","Maul","Shortsword","Warhammer"),
        "rg_mt_wp":("Longbow","heavy Crossbow"),
        "rena_rg_wp":("Musket",),
        "armor":("heavy",),
        "shield": True
    },
    "follower_cleric": {
        "name": "follower_cleric",
        "attributes_priority_array": ("str", "con", "dex", "wis", "cha","int"),
        "attributes_proficient_array": ("str", "con"),
        "skills_proficient_array": "follower_soldier",
        "skills_proficient_half_array": ("med"),
        "skills_proficient_expertise_array": ("rel"),
        "ml_s_wp":("Light hammer,Mace,Quarterstaff"),
        "rg_s_wp":("light Crossbow"),
        "ml_mt_wp":("Flail"),
        "rg_mt_wp":None,
        "rena_rg_wp":None,
        "armor":("medium"),
        "shield": True
    },
}
"""TEMPLATE"""

TEMPLATE_DEFAULT_ITEM = {
    "folder": None,
    "name": None,
    "type": None,
    "_id": None,
    "img": None,
    "system": {
        "description": {
        "value": "",
        "chat": ""
        },
        "source": {},
        "identified": True,
        "unidentified": {
        "description": ""
        },
        "container": None,
        "quantity": 1,
        "weight": 0,
        "price": {
        "value": 0,
        "denomination": "gp"
        },
        "rarity": "",
        "attunement": 0,
        "activation": {
        "type": "",
        "cost": None,
        "condition": ""
        },
        "duration": {
        "value": "",
        "units": ""
        },
        "cover": None,
        "crewed": False,
        "target": {
        "value": None,
        "width": None,
        "units": "",
        "type": "",
        "prompt": True
        },
        "range": {
        "value": None,
        "long": None,
        "units": ""
        },
        "uses": {
        "value": None,
        "max": "",
        "per": None,
        "recovery": "",
        "prompt": True
        },
        "consume": {
        "type": "",
        "target": None,
        "amount": None,
        "scale": False
        },
        "ability": None,
        "actionType": "",
        "attack": {
        "bonus": "",
        "flat": False
        },
        "chatFlavor": "",
        "critical": {
        "threshold": None,
        "damage": ""
        },
        "damage": {
        "parts": [],
        "versatile": ""
        },
        "formula": "",
        "save": {
        "ability": "",
        "dc": None,
        "scaling": "spell"
        },
        "summons": None,
        "armor": {
        "value": None,
        "magicalBonus": None,
        "dex": None
        },
        "hp": {
        "value": None,
        "max": None,
        "dt": None,
        "conditions": ""
        },
        "type": {
        "value": "light",
        "baseItem": ""
        },
        "properties": [],
        "speed": {
        "value": None,
        "conditions": ""
        },
        "strength": None,
        "equipped": False,
        "proficient": None
    },
    "effects": [],
    "sort": 0,
    "ownership": {
        "default": 0,
    },
    "flags": {
        "midiProperties": {
        "confirmTargets": "default",
        "autoFailFriendly": False,
        "autoSaveFriendly": False,
        "critOther": False,
        "offHandWeapon": False,
        "magicdam": False,
        "magiceffect": False,
        "concentration": False,
        "noConcentrationCheck": False,
        "toggleEffect": False,
        "ignoreTotalCover": False
        },
        "midi-qol": {
        "rollAttackPerTarget": "default",
        "itemCondition": "",
        "effectCondition": ""
        },
        "core": {
        "sourceId": None
        }
    },
    "_stats": {
        "systemId": None,
        "systemVersion": None,
        "coreVersion": None,
        "createdTime": None,
        "modifiedTime": None,
        "lastModifiedBy": None
    }
}
"""TEMPLATE DEFAULT ITEM"""

TEMPLATE_PROPERTY_NAME = {
    "ammunition":"amm",
    "finesse":"fin",
    "heavy":"hvy",
    "light":"lgt",
    "loading":"lod",
    "range":"",
    "reach":"rch",
    "special":"spc",
    "thrown":"thr",
    "two-handed":"two",
    "versatile":"ver",
    "magic": "mgc"
}
