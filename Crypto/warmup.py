# encrypt using ceasar cipher
def ceasar_encrypt(text,K):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + K - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + K - 97) % 26 + 97)
        else:
            result += char
    return result

print(ceasar_encrypt("CRYPTO IS FUN UNTIL THE PROFESSOR SAYS QUIZ", 4))


def ceasar_decrypt(text,K):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) - K - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) - K - 97) % 26 + 97)
        else:
            result += char
    return result

print(ceasar_decrypt("GWCL JMBBMZ VWB JM CAQVO BWWTA BW AWTDM BPQA",8))



def ceasar_brute_force(text):
    for K in range(1, 26):
        decrypted_text = ceasar_decrypt(text, K)
        print(f"Key {K}: {decrypted_text}")


print(ceasar_brute_force("ESP VPJ TD FYVYZHY ECJ MCFEP QZCNP"))

