
import random
import string
from itertools import combinations


def normalize_text(text):
    text = text.strip().lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

INTENTS = {
    "greeting": {
        "patterns": ["muraho", "hello", "mwiriwe", "wiriweho"],
        "responses": [
            "Muraho neza! Nishimiye kukubona hano.",
            "Mwiriwe! Ufite ikibazo ushaka kumbaza?"
        ]
    },
    "ask_news": {
        "patterns": ["amakuru", "amakuru yawe", "amakuru y'umunsi", "amakuru y'icyumweru", "amakuru ya mugitondo", "amakuru ya nijoro"],
        "responses": [
            "Amakuru ni meza cyane, urakoze kubaza!",
            "Umunsi wagenze neza, ndashimira Imana. Wowe se?",
            "Icyumweru cyagenze neza rwose, wowe ho?",
            "Mugitondo wagenze neza cyane! Wowe uko byagenze?",
            "Nijoro wagenze neza cyane, ndabashimiye!",
        ]
    },
        "gratitude": {
        "patterns": ["urakoze", "murakoze", "murakoze cyane", "ndashimira", "turabashimira"],
        "responses": [
            "Murakoze cyane! Imana ibahe umugisha.",
            "Twishimiye ko dukorana neza. Urakoze cyane!"
        ]
    },
    "default": {
        "patterns": [],
        "responses": [
            "Ndababarira, sinashoboye kukumva neza. Ongera ugerageze.",
            "Sinabyumvise neza, ushobora gusubiramo ikibazo?",
        ]
    }
}

QA = {
    "ni iki gituma u rwanda rwitwa igihugu cy'imisozi igihumbi": 
        "Kubera ko gifite imisozi myinshi cyane itatse igihugu cyose.",
    "umusozi muremure mu rwanda ni uwuhe": 
        "Ni Karisimbi, ufite uburebure bwa metero 4,507.",
    "ni irihe shyamba rinini riboneka mu rwanda": 
        "Ni ishyamba rya Nyungwe.",
    "ni izihe ndimi zikoreshwa cyane mu rwanda": 
        "Ikinyarwanda, Icyongereza, Igifaransa, n'Igiswahili.",
    "ni iki cyihariye ku muco nyarwanda": 
        "Gukunda igihugu, gusabana, kubaha abakuru, nimigenzo nk'igisabo."
}

KEYWORD_MAP = {}
for question in QA:
    words = normalize_text(question).split()
    for n in [2, 3]:
        if len(words) >= n:
            for combo in combinations(words, n):
                key = " ".join(sorted(combo))
                if key not in KEYWORD_MAP:
                    KEYWORD_MAP[key] = []
                KEYWORD_MAP[key].append(question)

def match_with_keywords(normalized_input):
    words = normalized_input.split()

    for question in QA:
        if normalize_text(question) == normalized_input:
            return question

    potential_matches = {}
    for n in [3, 2]:
        if len(words) >= n:
            for combo in combinations(words, n):
                key = " ".join(sorted(combo))
                if key in KEYWORD_MAP:
                    for question in KEYWORD_MAP[key]:
                        potential_matches[question] = potential_matches.get(question, 0) + n

    if potential_matches:
        return max(potential_matches.items(), key=lambda x: x[1])[0]

    return None

def match_intent(normalized_input):
    for intent, data in INTENTS.items():
        for pattern in data["patterns"]:
            if normalize_text(pattern) in normalized_input:
                return intent
    return "default"

class Hypothesis:
    def __init__(self, text):
        self.text = text

def get_response(user_input):
    if isinstance(user_input, Hypothesis):
        user_input = user_input.text 

    normalized_input = normalize_text(user_input)

    matched_question = match_with_keywords(normalized_input)
    if matched_question:
        return QA[matched_question]

    intent = match_intent(normalized_input)
    return random.choice(INTENTS[intent]["responses"])
