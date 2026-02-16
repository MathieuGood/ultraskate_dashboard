"""
Mapping of known athlete name variations to their canonical name.

When athletes register under different names across events (nicknames, typos,
middle initials, accented characters, etc.), this map ensures they are
recognized as the same person in the AthleteRegistry.

Keys are lowercase normalized names. Values are the canonical display name.
"""

ATHLETE_ALIASES: dict[str, str] = {
    # Nickname / short name variants
    "joe mazzone": "Joseph Mazzone",
    "tony mao": "Anthony Mao",
    "ben bailey": "Benjamin Bailey",
    "chris slaughter": "Christopher Slaughter",
    "jeff crowe": "Jeffrey Crowe",
    "jeff vyain": "Jeffrey Vyain",
    "joe burnham": "Joseph Burnham",
    "matt ayres": "Matthew Ayres",
    "nick carbot": "Nicholas Carbot",
    "ray st john": "Raymond St John",
    "sam robinson": "Samuel Robinson",
    "cami best": "Camille Best",
    "will bruce": "William Bruce",
    "will frank": "William Frank",
    "monzu haque": "Monzurul Haque",
    "zac johnson": "Zachary Johnson",
    "ron lewis": "Ronald Lewis",
    "jen shyu": "Jennifer Shyu",
    "randall mcclelland": "Randy McClelland",
    "james sands": "Jamie Sands",
    "bill ennis": "William Ennis",
    "bill polewchak": "William Polewchak",
    "tori kennedy": "Victoria Kennedy",
    "alexandra loch-mally": "Lexi Loch-Mally",
    "kenneth spranzo": "Kenny Spranzo",
    "alfredo valdes": "Freddie Valdes",
    # Parenthetical / middle name variants
    "ll (leonard) leffler": "Leonard Leffler",
    "leonard l leffler": "Leonard Leffler",
    "bob (robert) foster": "Bob Foster",
    "blake ( califlorida ) parsons": "Blake Parsons",
    "adrienne smith (pole skate)": "Adrienne Smith",
    # Middle initial variants
    "adrian f rodriguez": "Adrian Rodriguez",
    "adrian f. rodriguez": "Adrian Rodriguez",
    "francisco l. rodriguez": "Francisco Rodriguez",
    "julian f. rodriguez": "Julian Rodriguez",
    "melanie l. castro": "Melanie Castro",
    # Data entry error
    "damen 2 sistrunk": "Damen Sistrunk",
    "damen2 sistrunk": "Damen Sistrunk",
    # Typos
    "hopemare jackson": "Hopemarie Jackson",
    "fransico ramirez": "Francisco Ramirez",
    "katheryn leffler": "Kathryn Leffler",
    # Unicode / accent normalization
    "jo\u00d2o morales": "Joao Morales",
    "cesar nu\u00f1ez": "Cesar Nunez",
    "reinell gonz\u00e1lez": "Reinell Gonzalez",
    # Casing handled automatically via lowercase normalization, but
    # these entries exist for name display normalization where the
    # canonical casing differs from the first occurrence:
    "john odonnell": "John O'Donnell",
    "daniel dimassa": "Daniel DiMassa",
}
