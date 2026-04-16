from wonderwords import RandomWord

rw = RandomWord()

def generate_join_code():
    shared_settings = {"exclude_with_spaces":True, "word_max_length":9}
    
    w1 = rw.word(**shared_settings, include_parts_of_speech=["adjectives"])
    w2 = rw.word(**shared_settings, include_parts_of_speech=["adjectives", "nouns"])
    w3 = rw.word(**shared_settings, include_parts_of_speech=["nouns"])

    return f"{w1}-{w2}-{w3}"


def is_jcode_unique(join_code: str, db) -> bool:
    current_join_codes = db.session.execute("SELECT join_code FROM groups")
    return join_code not in current_join_codes