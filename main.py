# Main run file. Holds the user interface

import add_character, attribute_manager, inventory_manager, selecter, skill_manager, view, text
from menu import menu
import os
from data_visualization import DataVisualization
from statistical_analyzer import StatisticalAnalyzer
from random_generator import RandomGenerator

stat_labels = ["Damage", "Dexterity", "Intelligence", "Constitution", "Charisma"]

def main():
    text.bubble("Welcome to our program! This is our RPG Character Manager. Use up/down arrow keys to change options, left and right to change values, and options with ':' are writable (If you need more help click on the help option to tell you what everything does)", speed= 0.01)
    selected_character = "example character 1"
    options = ["Add Character", "Manage Skills", "Manage Inventory", "Manage Attributes", "View / Compare Characters", "Select / Search Characters", "Help", "Data Visualization", "Statistical Analysis", "Random Generator", f' (Your current selected character is "{selected_character}")']
    classes = [{"name": "rogue", "dmg": 1.2, "dex": 1.5, "int": 1.1, "con": 0.9, "cha": 1.2}, {"name": "warrior", "dmg": 1.5, "dex": 0.9, "int": 0.8, "con": 1.4, "cha": 1.0}, {"name": "mage", "dmg": 1.3, "dex": 0.8, "int": 1.6, "con": 0.7, "cha": 1.1}, {"name": "paladin", "dmg": 1.2, "dex": 0.9, "int": 1.0, "con": 1.3, "cha": 1.4 }, {"name": "ranger", "dmg": 1.3, "dex": 1.4, "int": 1.0, "con": 1.0, "cha": 1.0 }, {"name": "bard", "dmg": 0.9, "dex": 1.1, "int": 1.2, "con": 0.9, "cha": 1.6}, {"name": "tank", "dmg": 0.9, "dex": 0.7, "int": 0.8, "con": 1.7, "cha": 0.9}]
    races = [{"name": "Human", "dmg": 1.0, "dex": 1.0, "int": 1.0, "con": 1.0, "cha": 1.0}, {"name": "Elf", "dmg": 0.9, "dex": 1.2, "int": 1.1, "con": 0.9, "cha": 1.1}, {"name": "Ork", "dmg": 1.3, "dex": 0.8, "int": 0.7, "con": 1.2, "cha": 0.8}, {"name": "Dwarf", "dmg": 1.1, "dex": 0.8, "int": 0.9, "con": 1.3, "cha": 0.9}, {"name": "Halfling", "dmg": 0.8, "dex": 1.3, "int": 1.0, "con": 0.9, "cha": 1.2}]
    items = [{"name": "Iron Sword", "dmg": 1.2, "weight": 5.0, "value": 150, "effects": "Sharp edge, reliable weapon"}, {"name": "Dagger", "dex": 1.3, "weight": 1.5, "value": 75, "effects": "Lightweight, easy to conceal"}, {"name": "Wizard Staff", "int": 1.4, "weight": 3.0, "value": 300, "effects": "Channeling magic, arcane focus"}, {"name": "Heavy Armor", "con": 1.5, "weight": 25.0, "value": 500, "effects": "High protection, reduced mobility"}, {"name": "Silver Amulet", "cha": 1.3, "weight": 0.2, "value": 200, "effects": "Enchanted charm, noble appearance"}]
    characters = ({
        "name": "example character 1",
        "class": "rogue",
        "level": 15,
        "race": "Elf",
        "attributes": [],
        "base_attributes": [5, 5, 5, 5, 5],
        "skills": set(),
        "skill_levels": {},
        "inventory": []
    },)
    saved_skills = skill_manager.initialize_default_skills()

    def lookup(data_list):
        index = {entry["name"]: entry for entry in data_list}
        def find(name):
            return index.get(name)
        return find
    
    def attribute_applier():
        keys = ["dmg", "dex", "int", "con", "cha"]
        def apply(attributes, source):
            if source:
                for i, key in enumerate(keys):
                    if key in source:
                        attributes[i] *= source[key]
        return apply
    
    find_race = lookup(races)
    find_class = lookup(classes)
    apply_multipliers = attribute_applier()

    for character in characters:
        character["attributes"] = [float(val) for val in character["base_attributes"]]
        race_data = find_race(character["race"])
        class_data = find_class(character["class"])
        for item in character["inventory"]:
            apply_multipliers(character["attributes"], item)
        apply_multipliers(character["attributes"], race_data)
        apply_multipliers(character["attributes"], class_data)

    while True:
        choice = menu(options)
        if choice.get('index') == 0:
            characters = add_character.add_menu(characters, classes, races, items)
        
        elif choice.get('index') == 1:
            if selected_character != "":
                characters, selected_character = skill_manager.skill_menu(saved_skills, characters, selected_character)
            else:
                print("Please select a character before entering this function.")
                input("Press Enter to continue...")
                continue

        elif choice.get('index') == 2:
            if selected_character != "":
                characters, selected_character = inventory_manager.inventory_menu(items, characters, selected_character)
            else:
                print("Please select a character before entering this function.")
                input("Press Enter to continue...")
                continue

        elif choice.get('index') == 3:
            if selected_character != "":
                characters, selected_character = attribute_manager.attribute_menu(characters, selected_character)
            else:
                print("Please select a character before entering this function.")
                input("Press Enter to continue...")
                continue

        elif choice.get('index') == 4:
            if selected_character != "":
                characters, selected_character = view.view_menu(characters, selected_character, classes, races, items)
            else:
                print("Please select a character before entering this function.")
                input("Press Enter to continue...")
                continue

        elif choice.get('index') == 5:
            characters, selected_character = selecter.selecter_menu(characters, selected_character)

        elif choice.get('index') == 6:
            os.system('cls')

            # General Navigation
            text.bubble("Welcome to the Help Menu! Use the up and down arrow keys to navigate through menu options. Press Enter to select an option. For writable fields (marked with ':'), you can type directly. For number fields (shown with <>), use left and right arrows to adjust values. For toggle fields, use left and right arrows to cycle through options.", speed=0.01)
            result = menu(["Add Character", "Manage Skills", "Manage Inventory", "Manage Attributes", "View / Compare Characters", "Select / Search Characters"])
            selected_index = result['index']
            os.system('cls')

            # Add Character
            if selected_index == 1:
                text.bubble("Add Character: This function lets you create a new character for your RPG. You'll set your character's name, choose their class and race, and set their starting level. You can also assign initial attribute points like damage, dexterity, intelligence, constitution, and charisma. Additionally, you can select starting skills and inventory items. Don't worry - all of these choices can be changed later through other menu options!", speed=0.01)
                os.system('cls')

            # Manage Skills
            elif selected_index == 2:
                text.bubble("Manage Skills: This is where you control your character's abilities and powers. You can add new skills from a saved library, create completely custom skills with unique effects, or edit existing skills your character already knows. Each skill has a name, description, effect type (Attack, Defense, or Health), strength amount, and target (Enemy, Self, or Ally). You can also view all your character's current skills and remove any you no longer want.", speed=0.01)
                os.system('cls')

            # Manage Inventory
            elif selected_index == 3:
                text.bubble("Manage Inventory: Use this menu to equip your character with powerful items! You can add items from the available item list to your character's inventory, remove items you no longer need, or view all the items your character is currently carrying. Each item provides stat bonuses like increased damage, dexterity, intelligence, constitution, or charisma. Build the perfect loadout for your character's playstyle!", speed=0.01)
                os.system('cls')

            # Manage Attributes
            elif selected_index == 4:
                text.bubble("Manage Attributes: This function allows you to modify your character's core stat values. You can change your character's strength as they progress and grow stronger, change your character's constitution for a more beefy build, and other values. You can also view a complete summary of all your character's attributes one convenient display.", speed=0.01)
                os.system('cls')

            # Compare Characters
            elif selected_index == 5:
                text.bubble("View / Compare Characters: This feature lets you compare two characters side by side or just one. You can select your currently active character and view it or use it and another character from your roster to compare. You'll be able to see their StatisticalAnalyzer(), skills, and equipment to help you decide which character is better suited for different situations.", speed=0.01)
                os.system('cls')

            # Search Characters
            elif selected_index == 6:
                text.bubble("Select / Search Characters: This function lets you search for a character to select and change for all the rest of the functions.", speed=0.01)
                os.system('cls')

        elif choice.get('index') == 7:
            _compute_all_attrs(characters, classes, races, items)
            char_list = list(characters)
            os.system('cls')
            result = menu([
                "Radar Chart (selected character)",
                "Bar Chart (selected character)",
                "Compare All Characters",
                "Class Distribution Chart",
                "Level Progression Chart",
                "Back",
            ])
            sub = result['index']
            if sub < 5:
                char = next((c for c in char_list if c["name"] == selected_character), char_list[0])
                if sub == 0:
                    path = DataVisualization().radar_chart(char)
                elif sub == 1:
                    path = DataVisualization().bar_chart(char)
                elif sub == 2:
                    path = DataVisualization().comparison_chart(char_list)
                elif sub == 3:
                    path = DataVisualization().class_distribution_chart(char_list)
                elif sub == 4:
                    path = DataVisualization().level_progression_chart(char_list)
                print(f"\nChart saved to: {path}")
                input("Press Enter to continue...")

        elif choice.get('index') == 8:
            _compute_all_attrs(characters, classes, races, items)
            os.system('cls')
            result = menu([
                "Roster Summary (mean/median/max/min)",
                "Top Characters by Stat",
                "Average Stats by Class",
                "Full Data Table",
                "Export Roster to CSV",
                "Optimization Tips (selected character)",
                "Back",
            ])
            sub = result['index']
            os.system('cls')
            sa = StatisticalAnalyzer()
            sa.load_characters(characters)
            if sub == 0:
                print(sa.summary_stats())
            elif sub == 1:
                print("Which stat? (0=Damage 1=Dexterity 2=Intelligence 3=Constitution 4=Charisma)")
                raw = input("> ").strip()
                sidx = int(raw) if raw.isdigit() and int(raw) < 5 else 0
                print(sa.top_characters(stat_labels[sidx]))
            elif sub == 2:
                print(sa.class_averages())
            elif sub == 3:
                sa.print_dataframe()
            elif sub == 4:
                path = sa.export_csv()
                print(f"Exported to: {path}")
            elif sub == 5:
                char = next((c for c in characters if c["name"] == selected_character), list(characters)[0])
                print(sa.optimization_tip(char))
            if sub < 6:
                input("\nPress Enter to continue...")

        elif choice.get('index') == 9:
            os.system('cls')
            result = menu([
                "Generate Random Name",
                "Generate Backstory (selected character)",
                "Generate Random Quest",
                "Generate Random Equipment",
                "Add Random Character to Roster",
                "Back",
            ])
            sub = result['index']
            os.system('cls')
            if sub == 0:
                print(f"\nGenerated name: {RandomGenerator().random_name()}")
            elif sub == 1:
                char = next((c for c in characters if c["name"] == selected_character), list(characters)[0])
                bs = RandomGenerator().random_backstory(char["name"], char.get("race","Human"), char.get("class","warrior"))
                print(f"\n{bs}")
            elif sub == 2:
                print(RandomGenerator().format_quest(RandomGenerator().random_quest()))
            elif sub == 3:
                print(f"\nEquipment: {RandomGenerator().random_equipment()}")
            elif sub == 4:
                template = RandomGenerator().random_character_template()
                characters = list(characters)
                characters.append(template)
                characters = tuple(characters)
                print(f"\nAdded '{template['name']}' to roster!")
            if sub < 5:
                input("\nPress Enter to continue...")

def _compute_all_attrs(characters, classes, races, items):
    keys = ["dmg", "dex", "int", "con", "cha"]
    for c in characters:
        c["attributes"] = [float(v) for v in c["base_attributes"]]
        for item_name in c.get("inventory", []):
            item = next((i for i in items if i["name"] == item_name), None)
            if item:
                for idx, key in enumerate(keys):
                    if key in item:
                        c["attributes"][idx] *= item[key]
        race_data  = next((r for r in races   if r["name"] == c.get("race","")),  None)
        class_data = next((cl for cl in classes if cl["name"] == c.get("class","")), None)
        for src in (race_data, class_data):
            if src:
                for idx, key in enumerate(keys):
                    if key in src:
                        c["attributes"][idx] *= src[key]

main()