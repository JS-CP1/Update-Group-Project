import random
from faker import Faker
fake = Faker()

classes = ["rogue", "warrior", "mage", "paladin", "ranger", "bard", "tank"]
races = ["Human", "Elf", "Ork", "Dwarf", "Halfling"]
personalities = ["stoic and calculating", "brash and impulsive", "wise beyond their years", "fiercely loyal", "wickedly sarcastic", "deeply empathetic", "ruthlessly ambitious", "eternally optimistic", "shrouded in melancholy", "driven by wanderlust", "haunted by their past", "fueled by righteous fury", "guided by inner peace"]
motivations = ["seeking revenge for a fallen family", "protecting an ancient secret", "hunting down a legendary artifact", "proving their worth to a doubting world", "atoning for a grave mistake", "searching for a lost sibling", "fulfilling a dying mentor's final wish", "breaking a generational curse"]
locations = ["the smoldering ruins of Ashveil", "the frost-bitten peaks of Ironspire", "the sunken city of Marevoss", "a forgotten monastery in the Verdant Reaches", "the bustling docks of Port Calderon", "a cursed hamlet on the Mirewood border", "the underground market beneath Stonehaven", "the crystalline wastes of Shatterfield"]
quests = [("Retrieve", "a stolen grimoire", "from the thieves' guild of {city}"), ("Escort", "a wounded diplomat", "safely through the Whispering Marshes"), ("Slay", "the shadow drake Varethos", "before the next blood moon rises"), ("Uncover", "the truth behind the missing merchant caravans", "along the Old King's Road"), ("Defend", "the village of Harrowmere", "against an encroaching undead horde"), ("Infiltrate","the Crimson Veil cult's stronghold", "and destroy their summoning altar"), ("Recover", "the shattered pieces of the Sunlance", "scattered across five crypts")]
equipments = ["{adj} {material} sword", "{adj} {material} staff", "{adj} {material} dagger", "{adj} {material} shield", "{adj} {material} bow", "{adj} {material} amulet", "{adj} {material} cloak"]
addons = ["ancient", "cursed", "enchanted", "gleaming", "runic", "obsidian", "celestial"]
mats = ["iron", "silver", "moonstone", "shadowsteel", "dragonbone", "starwood", "mithril"]

class RandomGenerator:
    @staticmethod
    def random_name(race: str = "") -> str:
        first = fake.first_name()
        surname_parts = [["iron", "shadow", "storm", "ember", "silver", "moon", "dragon", "frost"], ["blade", "forge", "whisper", "born", "wing", "heart", "claw", "stone"]]
        surname = random.choice(surname_parts[0]).capitalize() + random.choice(surname_parts[1])
        return f"{first} {surname}"
    
    @staticmethod
    def random_backstory(name: str, race: str, char_class: str) -> str:
        origin = random.choice(locations)
        trait = random.choice(personalities)
        motivation = random.choice(motivations)
        age = random.randint(18, 350 if race == "Elf" else 80)
        mentor_name = fake.first_name()
        backstory = (f"{name} is a {age}-year-old {race} {char_class} hailing from {origin}. " f"Known to be {trait}, they have carved a reputation that precedes them " f"wherever they travel. Under the tutelage of the legendary {mentor_name}, " f"{name} honed their craft through years of hardship and perseverance. " f"Now they walk a solitary path, {motivation}, " f"with only their wits and blade to see them through the darkest of days.")
        return backstory
    
    @staticmethod
    def random_quest() -> dict:
        verb, obj, location = random.choice(quests)
        city = fake.city()
        loc_str = location.format(city=city)
        title = f"{verb} {obj}"
        desc = (f"A desperate plea has reached your ears: {verb.lower()} {obj} {loc_str}. " f"The task is fraught with peril, but the reward is said to be " f"{'legendary' if random.random() > 0.5 else 'considerable'}.")
        reward_gold = random.randint(200, 5000)
        reward_xp = random.randint(500, 8000)
        return {"title": title, "description": desc, "reward_gold": reward_gold, "reward_xp": reward_xp, "difficulty": random.choice(["Easy", "Medium", "Hard", "Legendary"]),}

    @staticmethod
    def format_quest(quest: dict) -> str:
        return (
            f"\n  ╔══════════════════════════════════════════╗\n"
            f"  ║  QUEST: {quest['title']:<34}\n"
            f"  ╠══════════════════════════════════════════╣\n"
            f"  ║  Difficulty: {quest['difficulty']:<29}\n"
            f"  ║  Reward: {quest['reward_gold']} gold / {quest['reward_xp']} XP{'':<11}\n"
            f"  ╠══════════════════════════════════════════╣\n"
            f"  ║  {quest['description'][:80]:<42}\n"
            f"  ╚══════════════════════════════════════════╝"
        )
    
    @staticmethod
    def random_equipment() -> str:
        template = random.choice(equipments)
        return template.format(adj=random.choice(addons).capitalize(), material=random.choice(mats).capitalize())

    @classmethod
    def random_character_template(cls) -> dict:
        race = random.choice(races)
        char_class = random.choice(classes)
        name = cls.random_name(race)
        level = random.randint(1, 20)
        base_attrs = [random.randint(3, 18) for _ in range(5)]
        backstory = cls.random_backstory(name, race, char_class)
        equipment = [cls.random_equipment() for _ in range(random.randint(1, 3))]
        trait = random.choice(personalities)

        return {
            "name": name,
            "class": char_class,
            "race": race,
            "level": level,
            "base_attributes": base_attrs,
            "attributes": [float(v) for v in base_attrs],
            "skills": set(),
            "skill_levels": {},
            "inventory": [],
            "backstory": backstory,
            "personality": trait,
            "random_gear": equipment,
        }
    
    @staticmethod
    def random_personality() -> str:
        return random.choice(personalities).capitalize()