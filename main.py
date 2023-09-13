from zipfile import ZipFile
import os, base64, zlib, shutil, string, codecs, lzma, httpx, time
from pystyle import *
from Crypto.Cipher import AES
os.system("cls") if os.name == "nt" else os.system("clear")
asciiart="""______ _             _           _   _                       _     _               
| ___ \ |           | |         | | | |                     | |   | |              
| |_/ / | __ _ _ __ | | ________| | | |_ __   __ _ _ __ __ _| |__ | |__   ___ _ __ 
| ___ \ |/ _` | '_ \| |/ /______| | | | '_ \ / _` | '__/ _` | '_ \| '_ \ / _ \ '__|
| |_/ / | (_| | | | |   <       | |_| | | | | (_| | | | (_| | |_) | |_) |  __/ |   
\____/|_|\__,_|_| |_|_|\_\       \___/|_| |_|\__, |_|  \__,_|_.__/|_.__/ \___|_|   
                                              __/ |                                
                                             |___/                                 """
System.Title("Blank-Ungrabber")
print(Colorate.Vertical(Colors.yellow_to_red, Center.XCenter(asciiart)))
executable=input("\n"+Colorate.Vertical(Colors.red_to_yellow, "Executable Path:")+" ")
be=time.time()
os.system("py extract.py "+executable+" >nul")
try:
    os.chdir(f"{os.path.basename(executable)}_extracted")
except:
    print(Colorate.Vertical(Colors.red_to_yellow, "Please input a valid file"))
    quit()
try:
    shutil.copyfile("./blank.aes", "../blank.aes")
except:
    print(Colorate.Vertical(Colors.red_to_yellow, "This is not a blank grabber file"))
    quit()
try:
    f=open("loader-o.pyc", "rb")
    data=f.read()
    f.close()
except:
    for i in os.listdir():
            if len(i) >= 40 and i.endswith(".pyc"):
                f=open(i, "rb")
                data=f.read()
                f.close()
os.chdir("..")

data=data.split(b"stub-oz,")[-1].split(b"\x63\x03")[0].split(b"\x10")
print("")
try:
    key = base64.b64decode(data[0].split(b"\xDA")[0])
    iv = base64.b64decode(data[-1])
    zipfile = os.path.join('./blank.aes')
    print(Colorate.Vertical(Colors.red_to_yellow, "[+] Got Key and IV"))
except:
    print(Colorate.Vertical(Colors.red_to_yellow, "[!] Invalid file if you think its an error please contact on discord: lululepu."))

def decrypt(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted

if os.path.isfile(zipfile):
    with open(zipfile, "rb") as f:
        ciphertext = f.read()
    decrypted = decrypt(key, iv, zlib.decompress(ciphertext[::-1]))
    with open("stub.zip", "wb") as f:
        f.write(decrypted)
    try:
        with ZipFile('stub.zip', 'r') as f:
            f.extractall()
        print(Colorate.Vertical(Colors.red_to_yellow, "[+] Decrypted the blank file"))
    except:
        print(Colorate.Vertical(Colors.red_to_yellow, "[!] An error occured while decrypting the file please contact on discord: lululepu."))


f=open("stub-o.pyc", "rb")
data=f.read()
a=b"\xFD\x37\x7A\x58\x5A\x00"+data.split(b"\xFD\x37\x7A\x58\x5A\x00")[-1]
last=lzma.decompress(a).decode()
print(Colorate.Vertical(Colors.red_to_yellow, "[+] Decompressed the lzma compression"))
l=last.split(";")[:-1]
for i in range(len(l)):
    l[i]=l[i]+";"
exec("".join(l))

with open("last.pyc", "wb") as f:
    try:
        f.write(base64.b64decode(codecs.decode(____, "rot13")+_____+______[::-1]+_______))
        print(Colorate.Vertical(Colors.red_to_yellow, "[+] Deobfuscated the code"))
    except:
        print(Colorate.Vertical(Colors.red_to_yellow, "[!] Error occured while deobfuscating please contact on discord: lululepu."))
def strings(filename, min=4):
    with open(filename, errors="ignore") as f:
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                yield result
            result = ""
        if len(result) >= min:
            yield result


for i in strings("last.pyc"):
    i=bytes(i, encoding="utf8")
    try:
        a=base64.b64decode(i)
        if "discord.com/api/webhooks/" in a.decode():
            webhook=a.decode()
    except:...

print(Colorate.Vertical(Colors.red_to_yellow, "[*] Cleaning files..."))
os.remove("stub.zip")
os.remove("stub-o.pyc")
os.remove("last.pyc")
os.remove("blank.aes")
shutil.rmtree(f"{os.path.basename(executable)}_extracted")
print(Colorate.Vertical(Colors.red_to_yellow, "[+] Got the webhook"))
print(Colorate.Vertical(Colors.red_to_yellow, "[*] Found in {:0.5f}".format(time.time()-be)))
print(Colorate.Vertical(Colors.red_to_yellow, "[*] Testing the webhook..."))
res=httpx.get(webhook)
if res.status_code != 404:
    print(Colorate.Vertical(Colors.red_to_yellow, "[+] The webhooks is working :"))
    print(Colorate.Vertical(Colors.red_to_yellow, webhook))
else:
    rp=input(Colorate.Vertical(Colors.red_to_yellow, "[!] The webhooks is not working do you want to get it anyway [y/n]: ")+" ")
    if rp.lower() == "y":
        print(Colorate.Vertical(Colors.red_to_yellow, webhook))