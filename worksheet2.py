from microbit import *
import radio

# global variables needed to operate the device
ALPH_MORSE = {
    'a': '.-', 'b': '-...', 'c': '-.-.',
    'd': '-.. ', 'e': '.', 'f': '..-.',
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '10': '-----', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    " ": " "
}
MORSE_ALPH = {value: key for key, value in ALPH_MORSE.items()}
ALPH = [chr(ord('a') + i) for i in range(26)] + [str(i) for i in range(10)] + [" "]
ALPH_INDEX = {char: index for index, char in enumerate(ALPH)}
INDEX_ALPH = {key: value for value, key in ALPH_INDEX.items()}
MAP = [ALPH[x:] + ALPH[:x] for x in range(37)]
KEY = "hello"
KEY_LEN = len(KEY)

# showing microbit is now awake and initiliasing the radio on microbit
display.show("!")
radio.on()
radio.config(channel=1)
radio.RATE_1MBIT


def get_new_key(plain):
    """returns an adjusted key based on the lenght of text"""
    plain_len = len(plain)
    if KEY_LEN > plain_len:
        new_key = KEY[:plain_len]
    elif KEY_LEN < plain_len:
        count = 0
        new_key = KEY
        for char in range(count + KEY_LEN, plain_len):
            new_key += KEY[char % KEY_LEN]
    else:
        new_key = KEY

    return new_key


def encrypt(plain):
    """basic encryption"""
    plain = plain.lower()

    new_key = get_new_key(plain)

    encrypted = ""
    for index, char in enumerate(plain):
        plain_index = ALPH_INDEX[char]
        key_index = ALPH_INDEX[new_key[index]]

        encrypted += MAP[plain_index][key_index]

    return encrypted


def decrypt(cypher):
    """basic decryption"""
    cypher = cypher.lower()
    new_key = get_new_key(cypher)

    plain = ""
    for index, char in enumerate(cypher):
        key_char = new_key[index]
        key_index = ALPH_INDEX[key_char]

        node = MAP[key_index]
        for plain_index, char_2 in enumerate(node):
            if char_2 == char:
                plain += INDEX_ALPH[plain_index]

    return plain


while True: # main loop
    message = "Hello".lower()
    morse_code = None

    if button_a.was_pressed():
        # send message if button a is pressed
        encrypted = encrypt(message)
        morse_code = ""
        for char in encrypted:
            morse_code += ALPH_MORSE[char] + " "
        display_text = "Sending: " + morse_code
        display.scroll(display_text)
        print(morse_code)
        radio.send(morse_code)
        sleep(1000)
        display.clear()

    morse = radio.receive()
    if morse:
        # if radio recieves something, decodes, decrypts and displays
        morse = str(morse)
        display_text = "Recieved: "
        morse_split = morse.split(" ")
        encrypted = ""
        for x in morse_split:
            x = x.replace(" ", "")
            if x == "":
                continue
            try:
                encrypted += MORSE_ALPH[x]
            except KeyError:
                display.scroll(ord(x))
                sleep(1000)
                display.scroll(ord(x))
                
        plain = "Recieved: " + decrypt(encrypted)
        display.scroll(plain)

        sleep(1000)
        display.clear()
