import pyaes

# Dit encrypt data voor database
def encryptData(input):
    # Zet data om naar versleutelde data met AES (256-bit)
    from auth import aeskey as key
    key = key.encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(key)
    ciphertext = aes.encrypt(input)
    return ciphertext

# Dit decrypt data uit de database
def decryptData(input):
    # Ontsleutel data van AES naar leesbare tekst
    from auth import aeskey as key
    key = key.encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(key)
    output = aes.decrypt(input).decode('utf-8')
    return output

# Dit decrypt data uit de database
def decryptDataWithoutDecode(input):
    # Ontsleutel data van AES naar leesbare tekst
    from auth import aeskey as key
    key = key.encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(key)
    output = aes.decrypt(input)
    return output
