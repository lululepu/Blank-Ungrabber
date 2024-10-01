from pystyle import *  
from typing import Generator
from Crypto.Cipher import AES
import os
import base64
import zlib
import time
import string
import codecs
import lzma
import httpx
import ast
import io
import zipfile
import sys
from utils import Extract  


if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')


asciiart = '''
______ _             _           _   _                       _     _               
| ___ \ |           | |         | | | |                     | |   | |              
| |_/ / | __ _ _ __ | | ________| | | |_ __   __ _ _ __ __ _| |__ | |__   ___ _ __ 
| ___ \ |/ _` | '_ \| |/ /______| | | | '_ \ / _` | '__/ _` | '_ \| '_ \ / _ \ '__|
| |_/ / | (_| | | | |   <       | |_| | | | | (_| | | | (_| | |_) | |_) |  __/ |   
\____/|_|\__,_|_| |_|_|\_\       \___/|_| |_|\__, |_|  \__,_|_.__/|_.__/ \___|_|   
                                              __/ |                               
                                             |___/                                 '''

System.Title('Blank-Ungrabber')
print(Colorate.Vertical(Colors.yellow_to_red, Center.XCenter(asciiart)))


executable = input('\n' + Colorate.Vertical(Colors.red_to_yellow, 'Executable Path:') + ' ')

start_time = time.time()


extracted = Extract(executable)


def log(message) -> None:
    print(Colorate.Vertical(Colors.red_to_yellow, message))


def strings(data: str) -> Generator:
    data = str(data)
    result = ''
    for c in data:
        if c in string.printable:
            result += c
            continue
        if len(result) >= 4:
            yield result
        result = ''
    if len(result) >= 4:
        yield result


def get_var(code: str, var: str) -> str:
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == var:
                    return node.value.value
    return


def get_file(name) -> bytearray:
    if name in extracted:
        return extracted[name]
    return False


if not os.path.isfile(executable):
    log('Please input a valid file')
    sys.exit(1)
if not get_file('blank.aes'):
    log('This is not a blank grabber file')
    sys.exit(1)


try:
    data = get_file('loader-o')
except:
    for i, v in extracted.items():
        if len(i) >= 35:
            data = v


data = data.split(b'stub-oz,')[-1].split(b'\x63\x03')[0].split(b'\x10')
print('')

try:
    key = base64.b64decode(data[0].split(b'\xDA')[0])
    iv = base64.b64decode(data[-1])
    log('[+] Got Key and IV')
except:
    log('[!] Invalid file. If you think it’s an error, please contact via Discord: lululepu.off')
    sys.exit(1)


def decrypt(key, iv, ciphertext) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted


ciphertext = get_file('blank.aes')
try:
    decrypted = decrypt(key, iv, zlib.decompress(ciphertext[::-1]))
    with io.BytesIO(decrypted) as zip_buffer:
        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            with zip_ref.open('stub-o.pyc', 'r') as f:
                content = f.read()
    parsed = lzma.decompress(b'\xFD\x37\x7A\x58\x5A\x00' + content.split(b'\xFD\x37\x7A\x58\x5A\x00')[-1])
    log('[+] Decrypted the blank file')
except:
    log('[!] An error occurred while decrypting the file. Please contact via Discord: lululepu.off')
    sys.exit(1)


try:
    ____ = get_var(parsed, '____')
    _____ = get_var(parsed, '_____')
    ______ = get_var(parsed, '______')
    _______ = get_var(parsed, '_______')
    deobfuscated = base64.b64decode(codecs.decode(____, 'rot13') + _____ + ______[::-1] + _______)
    content = deobfuscated.decode('utf-8', errors='replace')
    log('[+] Deobfuscated the code')
except:
    log('[!] Error occurred during deobfuscation. Please contact via Discord: lululepu.off')
    sys.exit(1)


webhook = None
for i in strings(content):
    i = bytes(i, encoding='utf8')
    try:
        decoded = base64.b64decode(i)
        if 'discord.com/api/webhooks/' in decoded.decode():
            webhook = decoded.decode()
    except:
        pass

if not webhook:
    log('[?] Webhook not found. Please contact via Discord: lululepu.off')
    sys.exit(1)


log('[+] Got the webhook')
log('[*] Process completed in {:0.5f} seconds'.format(time.time() - start_time))
log('[*] Testing the webhook...')


res = httpx.get(webhook)
if res.status_code != 404:
    log('[+] The webhook is working:')
    log(webhook)
else:
    rp = input(Colorate.Vertical(Colors.red_to_yellow, '[!] The webhook is not working. Do you want to get it anyway [y/n]: ') + ' ')
    if rp.lower() == 'y':
        log(webhook)
