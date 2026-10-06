# Substitution alphabet used in tasks 1 and 2.
from collections import Counter

text = """EKT YTJRTE BTYYQFT PY KPZZTO PO EKPY NQRQFRQNK.
STEETR GRTCVTOJD ZXTY OXE RTHTQS EKT IKXST LTD,
MVE PE FPHTY Q FXXZ YEQRE.
SXXL GXR JXBBXO IXRZY, RTNTQETZ NQEETROY,
QOZ YKXRE IXRZY.
IKTO DXV RTJXHTR EKT BTYYQFT,
EKT HPFTOTRT LTD KQY GXVR STEETRY."""

PLAIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CIPHER_ALPHABET = "QMJZTGFKPWLSBOXNCRYEVHIADU"


def substitution_encode(text):
    result = ""
    for char in text:
        if char.isupper():
            index = PLAIN_ALPHABET.index(char)
            result += CIPHER_ALPHABET[index]
        elif char.islower():
            index = PLAIN_ALPHABET.index(char.upper())
            result += CIPHER_ALPHABET[index].lower()
        else:
            result += char
    return result


print(substitution_encode("KEEP THE SECRET SAFE"))


def substitution_decode(text):
    result = ""
    for char in text:
        if char.isupper():
            index = CIPHER_ALPHABET.index(char)
            result += PLAIN_ALPHABET[index]
        elif char.islower():
            index = CIPHER_ALPHABET.index(char.upper())
            result += PLAIN_ALPHABET[index].lower()
        else:
            result += char
    return result

print(substitution_decode("ERVYE DXVR SXFPJ"))


def analyze_frequency(ciphertext):
    letters = [char.upper() for char in ciphertext if char.upper() in PLAIN_ALPHABET]
    counts = Counter(letters)
    total_letters = len(letters)

    for letter, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        percentage = count / total_letters * 100
        print(f"{letter}: {count} ({percentage:.2f}%)")


analyze_frequency(text)


frequency_mapping = {
    "T": "E",
    "E": "T",
    "R": "R",
    "X": "O",
    "Y": "S",
    "Q": "A",
    "K": "H",
}


def apply_mapping(ciphertext, mapping):
    return "".join(mapping.get(char, char) for char in ciphertext)


print(apply_mapping(text, frequency_mapping))


"""
THE SECRET MESSAGE IS HIDDEN IN THIS PARAGRAPH.
LETTER FREQUENCY DOES NOT REVEAL THE WHOLE KEY,
BUT IT GIVES A GOOD START.
LOOK FOR COMMON WORDS, REPEATED PATTERNS,
AND SHORT WORDS.
WHEN YOU RECOVER THE MESSAGE,
THE VIGENERE KEY HAS FOUR LETTERS.

"""