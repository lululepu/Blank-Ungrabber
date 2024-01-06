import os, base64, zlib, shutil, string, codecs, lzma, httpx, time, ast, io, zipfile
from pystyle import *
from Crypto.Cipher import AES

if os.name == 'nt':
  os.system('cls')  
else:
  os.system('clear')

asciiart='''______ _             _           _   _                       _     _               
| ___ \ |           | |         | | | |                     | |   | |              
| |_/ / | __ _ _ __ | | ________| | | |_ __   __ _ _ __ __ _| |__ | |__   ___ _ __ 
| ___ \ |/ _` | '_ \| |/ /______| | | | '_ \ / _` | '__/ _` | '_ \| '_ \ / _ \ '__|
| |_/ / | (_| | | | |   <       | |_| | | | | (_| | | | (_| | |_) | |_) |  __/ |   
\____/|_|\__,_|_| |_|_|\_\       \___/|_| |_|\__, |_|  \__,_|_.__/|_.__/ \___|_|   
                                              __/ |                                
                                             |___/                                 '''
System.Title('Blank-Ungrabber')
print(Colorate.Vertical(Colors.yellow_to_red, Center.XCenter(asciiart)))
executable=input('\n'+Colorate.Vertical(Colors.red_to_yellow, 'Executable Path:')+' ')

be=time.time()

def log(message) -> None:
    print(Colorate.Vertical(Colors.red_to_yellow, message))

def strings(data: str):
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

def get_var(code: str, var: str) -> str: # Get a variable from a given code by name
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == var:
                    return node.value.value
    return

os.system('python extract.py "'+executable+'" >nul 2>&1') # Extract the pyinstaller file

if not os.path.isdir(f'{os.path.basename(executable)}_extracted'):
    log('Please input a valid file')
    quit()
EXT = f'{os.path.basename(executable)}_extracted'
if not os.path.isfile(f'{EXT}\\blank.aes'):
    log('This is not a blank grabber file')
    quit()

# Try to get the file containing the key and IV for decrypting
try:
    f=open(f'{EXT}\\loader-o.pyc', 'rb')
    data=f.read()
    f.close()
except:
    for i in os.listdir(EXT):
        if len(i) >= 40 and i.endswith('.pyc'):
            f=open(f'{EXT}\\{i}', 'rb')
            data=f.read()
            f.close()

# Parse the key and iv from the file
data=data.split(b'stub-oz,')[-1].split(b'\x63\x03')[0].split(b'\x10')
print('')
try:
    key = base64.b64decode(data[0].split(b'\xDA')[0])
    iv = base64.b64decode(data[-1])
    bzip = os.path.join(f'{os.path.basename(executable)}_extracted\\blank.aes')
    log('[+] Got Key and IV')
except:
    log('[!] Invalid file if you think its an error please contact on discord: lululepu.')


def decrypt(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted

# Decrypt the blank.aes file
with open(bzip, 'rb') as f:
    ciphertext = f.read()
try:
    decrypted = decrypt(key, iv, zlib.decompress(ciphertext[::-1]))
    with io.BytesIO(decrypted) as zip_buffer:
        with zipfile.ZipFile(zip_buffer, 'r') as zip:
            with zip.open('stub-o.pyc', 'r') as f:
                content = f.read()
    parsed: str = lzma.decompress(b'\xFD\x37\x7A\x58\x5A\x00'+content.split(b'\xFD\x37\x7A\x58\x5A\x00')[-1])
    log('[+] Decrypted the blank file')
except:
    log('[!] An error occured while decrypting the file please contact on discord: lululepu.')

# Deobfuscate the code from the decrypted blank.aes zip file
try:
    ____ = get_var(parsed, '____')
    _____ = get_var(parsed, '_____')
    ______ = get_var(parsed, '______')
    _______ = get_var(parsed, '_______')
    deobfuscated = base64.b64decode(codecs.decode(____, 'rot13')+_____+______[::-1]+_______)
    with open('last.pyc', 'wb') as f:
      f.write(deobfuscated)
    with open('last.pyc', errors='ignore') as f:
      content = f.read()
    log('[+] Deobfuscated the code')
except:
    log('[!] Error occured while deobfuscating please contact on discord: lululepu.')

# Get the webhook in all deobfuscated file (its compiled python)
for i in strings(content):
    i=bytes(i, encoding='utf8')
    try:
        a=base64.b64decode(i)
        if 'discord.com/api/webhooks/' in a.decode():
            webhook=a.decode()
    except:...

# Clean/End of the process
log('[*] Cleaning files...')
os.remove('last.pyc')
shutil.rmtree(f'{os.path.basename(executable)}_extracted')
log('[+] Got the webhook')
log('[*] Found in {:0.5f}'.format(time.time()-be))
log('[*] Testing the webhook...')

# Test the webhook
res=httpx.get(webhook)
if res.status_code != 404:
    log('[+] The webhooks is working :')
    log(webhook)
else:
    rp=input(Colorate.Vertical(Colors.red_to_yellow, '[!] The webhooks is not working do you want to get it anyway [y/n]: ')+' ')
    if rp.lower() == 'y':
        log(webhook)
