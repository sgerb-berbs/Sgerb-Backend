from better_profanity import profanity as bf

# Load profanity list
bf.load_censor_words()

def censor(text: str):
    return bf.censor(text)

def check(text: str):
    return bf.contains_profanity(text)
