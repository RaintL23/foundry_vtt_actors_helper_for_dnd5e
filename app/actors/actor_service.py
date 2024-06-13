"""."""
import json
import os
from fastapi import HTTPException
import app.static.constants as app_constants
import app.items.items_service as ItemsService

async def load_json_template():
    """."""
    try:
        # Ideally the user should upload the address of the file but for now we will
        # hardcode it to simplify the development of the functionality, this can be
        # solved when there is a frontend.
        json_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../files/test2.json"))
        if not os.path.exists(json_file_path):
            raise HTTPException(
                status_code=500, 
                detail="Could not find the base json file to create the actor")
        json_data = {}
        with open(json_file_path, encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        return json_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}") from e

async def create(user_init_data):
    """."""
    json_template = await load_json_template()
    current_template = set_template(user_init_data["template"])
    new_npc = json_template
    new_npc["name"] = user_init_data["name"]
    new_npc["prototypeToken"]["name"] = user_init_data["name"]
    new_npc = set_attributes(new_npc,
                                    current_template,
                                    user_init_data["attribute_array"])

    new_npc = set_race(new_npc,user_init_data["race"])
    new_npc = await ItemsService.set_items(new_npc,current_template,user_init_data["urls"])

    # Create JSON file
    # nombre_archivo = "datos.json"
    # with open(nombre_archivo, "w", encoding='utf-8') as archivo:
    #     json.dump(new_npc, archivo, indent=4)
    # print(new_npc)
    return new_npc

def set_template(template):
    """."""
    return app_constants.TEMPLATE_OPTIONS[template]

def set_attributes(new_npc, template, attribute_array):
    """."""
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
