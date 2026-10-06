from collections import Counter

ciphertext = """
VVHWGQUIVYHIRSUPGTWXJSVIPCWIUPHGCIVIVVHPGHWITSDTRSDVUSYITMZL
GFHIXSUCVSDQOSPFGFVLQIOHEVHGMSDGJQRPWAQWGSNXJSPSUHIVGEXIPHVC
OPRPCBGYUSLXVCUIECYITHKIMSBAJSQXJSPIUGDKGPHGQAHWEZHETSQXGFWL
GOFGGGVAQFGIEZLTUS
"""
PLAIN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ciphertext = "".join(
    char for char in ciphertext
    if char.upper() in PLAIN_ALPHABET
)

group1 = ciphertext[0::4]
group2 = ciphertext[1::4]
group3 = ciphertext[2::4]
group4 = ciphertext[3::4]




# find the most common letter in each group
def most_common_letter(ciphertext):
    letters = [char.upper() for char in ciphertext if char.upper() in PLAIN_ALPHABET]
    counts = Counter(letters)
    most_common = counts.most_common(1)[0][0]
    return most_common

print(f"Most common letter in group 1: {most_common_letter(group1)}")
print(f"Most common letter in group 2: {most_common_letter(group2)}")
print(f"Most common letter in group 3: {most_common_letter(group3)}")
print(f"Most common letter in group 4: {most_common_letter(group4)}")


# most common letters in each group is E in plaintext, so we can use that to find the key for each group
def find_key(most_common_letter):
    key = (ord(most_common_letter) - ord('E')) % 26 
    # map the key to a letter
    key = chr(key + ord('A'))
    return key


print(f"Key for group 1: {find_key(most_common_letter(group1))}")
print(f"Key for group 2: {find_key(most_common_letter(group2))}")
print(f"Key for group 3: {find_key(most_common_letter(group3))}")
print(f"Key for group 4: {find_key(most_common_letter(group4))}")

def vigenere_decrypt(ciphertext, key):
    result = ""
    key_length = len(key)
    key_index = 0

    for char in ciphertext:
        if char.upper() in PLAIN_ALPHABET:
            shift = ord(key[key_index % key_length].upper()) - ord('A')
            decrypted_char = chr((ord(char.upper()) - shift - 65) % 26 + 65)
            result += decrypted_char
            key_index += 1
        else:
            result += char

    return result


print(vigenere_decrypt(ciphertext, "CODE"))