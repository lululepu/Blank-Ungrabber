import struct
import zlib
import sys
import os
from uuid import uuid4 as uniquename

class CTOCEntry:
    def __init__(self, position, cmprsdDataSize, uncmprsdDataSize, cmprsFlag, typeCmprsData, name):
        self.position = position
        self.cmprsdDataSize = cmprsdDataSize
        self.uncmprsdDataSize = uncmprsdDataSize
        self.cmprsFlag = cmprsFlag
        self.typeCmprsData = typeCmprsData
        self.name = name

class PyInstArchive:
    PYINST20_COOKIE_SIZE = 24
    PYINST21_COOKIE_SIZE = 24 + 64
    MAGIC = b'MEI\014\013\012\013\016'

    def __init__(self, path):
        self.barePycList = []
        self.filePath = path
        self.pycMagic = b'\0' * 4
        self.archiveDict = {}

    def open(self):
        try:
            self.fPtr = open(self.filePath, 'rb')
            self.fileSize = os.stat(self.filePath).st_size
        except:
            return False
        return True

    def close(self):
        try:
            self.fPtr.close()
        except:
            pass

    def checkFile(self):
        searchChunkSize = 8192
        endPos = self.fileSize
        self.cookiePos = -1

        if endPos < len(self.MAGIC):
            return False

        while True:
            startPos = endPos - searchChunkSize if endPos >= searchChunkSize else 0
            chunkSize = endPos - startPos

            if chunkSize < len(self.MAGIC):
                break

            self.fPtr.seek(startPos, os.SEEK_SET)
            data = self.fPtr.read(chunkSize)

            offs = data.rfind(self.MAGIC)

            if offs != -1:
                self.cookiePos = startPos + offs
                break

            endPos = startPos + len(self.MAGIC) - 1

            if startPos == 0:
                break

        if self.cookiePos == -1:
            return False

        self.fPtr.seek(self.cookiePos + self.PYINST20_COOKIE_SIZE, os.SEEK_SET)

        if b'python' in self.fPtr.read(64).lower():
            self.pyinstVer = 21
        else:
            self.pyinstVer = 20

        return True

    def getCArchiveInfo(self):
        try:
            if self.pyinstVer == 20:
                self.fPtr.seek(self.cookiePos, os.SEEK_SET)
                (magic, lengthofPackage, toc, tocLen, pyver) = struct.unpack('!8siiii', self.fPtr.read(self.PYINST20_COOKIE_SIZE))
            elif self.pyinstVer == 21:
                self.fPtr.seek(self.cookiePos, os.SEEK_SET)
                (magic, lengthofPackage, toc, tocLen, pyver, pylibname) = struct.unpack('!8sIIii64s', self.fPtr.read(self.PYINST21_COOKIE_SIZE))
        except:
            return False

        self.pymaj, self.pymin = (pyver//100, pyver%100) if pyver >= 100 else (pyver//10, pyver%10)

        tailBytes = self.fileSize - self.cookiePos - (self.PYINST20_COOKIE_SIZE if self.pyinstVer == 20 else self.PYINST21_COOKIE_SIZE)
        self.overlaySize = lengthofPackage + tailBytes
        self.overlayPos = self.fileSize - self.overlaySize
        self.tableOfContentsPos = self.overlayPos + toc
        self.tableOfContentsSize = tocLen

        return True

    def parseTOC(self):
        self.fPtr.seek(self.tableOfContentsPos, os.SEEK_SET)
        self.tocList = []
        parsedLen = 0

        while parsedLen < self.tableOfContentsSize:
            (entrySize, ) = struct.unpack('!i', self.fPtr.read(4))
            nameLen = struct.calcsize('!iIIIBc')
            (entryPos, cmprsdDataSize, uncmprsdDataSize, cmprsFlag, typeCmprsData, name) = struct.unpack('!IIIBc{0}s'.format(entrySize - nameLen), self.fPtr.read(entrySize - 4))

            try:
                name = name.decode("utf-8").rstrip("\0")
            except UnicodeDecodeError:
                newName = str(uniquename())
                name = newName

            if len(name) == 0:
                name = str(uniquename())

            self.tocList.append(
                CTOCEntry(
                    self.overlayPos + entryPos,
                    cmprsdDataSize,
                    uncmprsdDataSize,
                    cmprsFlag,
                    typeCmprsData,
                    name
                )
            )

            parsedLen += entrySize

    def extractFiles(self):
        for entry in self.tocList:
            self.fPtr.seek(entry.position, os.SEEK_SET)
            data = self.fPtr.read(entry.cmprsdDataSize)

            if entry.cmprsFlag == 1:
                try:
                    data = zlib.decompress(data)
                except zlib.error:
                    continue

            if entry.typeCmprsData == b'd' or entry.typeCmprsData == b'o':
                continue

            content = None

            if entry.typeCmprsData == b's':
                if self.pycMagic == b'\0' * 4:
                    self.barePycList.append(entry.name + '.pyc')
                content = self._readPyc(data)

            elif entry.typeCmprsData == b'M' or entry.typeCmprsData == b'm':
                if data[2:4] == b'\r\n':
                    if self.pycMagic == b'\0' * 4:
                        self.pycMagic = data[0:4]
                    content = data
                else:
                    content = self._readPyc(data)

            else:
                content = data

            self.addToDict(entry.name, content)

            if entry.typeCmprsData == b'z' or entry.typeCmprsData == b'Z':
                self._extractPyz(entry.name)

    def addToDict(self, filename, content):
        parts = filename.split(os.path.sep)
        current_dict = self.archiveDict
        for part in parts[:-1]:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
        current_dict[parts[-1]] = content

    def _readPyc(self, data):
        content = bytearray()
        content.extend(self.pycMagic)
        content.extend(b'\0' * 4)  # Pyc header
        content.extend(data)
        return content

    def _extractPyz(self, name):
        pass

def Extract(file):
    arch = PyInstArchive(file)
    if arch.open():
        if arch.checkFile():
            if arch.getCArchiveInfo():
                arch.parseTOC()
                arch.extractFiles()
                arch.close()
                return arch.archiveDict
