import sys
import re
import shutil
from pathlib import Path



JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
MY_OTHER = []
ARCHIVES = []

REGISTER_EXTENSION = {
    'jpeg': JPEG_IMAGES,
    'jpg': JPG_IMAGES,
    'png': PNG_IMAGES,
    'svg': SVG_IMAGES,    
    'avi': AVI_VIDEO,
    'mp4': MP4_VIDEO,
    'mov': MOV_VIDEO,
    'mkv': MKV_VIDEO,
    'doc': DOC_DOCUMENTS,
    'docx': DOCX_DOCUMENTS,
    'txt': TXT_DOCUMENTS,
    'pdf': PDF_DOCUMENTS,
    'xlsx': XLSX_DOCUMENTS,
    'pptx': PPTX_DOCUMENTS,
    'mp3': MP3_AUDIO,
    'ogg': OGG_AUDIO,
    'wav': WAV_AUDIO,
    'amr': AMR_AUDIO,
    'zip': ARCHIVES,
    'gz': ARCHIVES,
    'tar': ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()  # suffix[1:] -> .jpg -> jpg

def scan(folder: Path):
    for item in folder.iterdir():
        # Робота з папкою
        if item.is_dir():  # перевіряємо чи обєкт папка
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue
        # Робота з файлом
        extension = get_extension(item.name)  # беремо розширення файлу
        full_name = folder / item.name  # беремо повний шлях до файлу
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                REGISTER_EXTENSION[extension]
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)  # .mp4, .mov, .avi
                MY_OTHER.append(full_name)


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()


def normalize(name: str) -> str:
    translate_name = re.sub(r'[^\w.]', '_', name.translate(TRANS))
    return translate_name


def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok = True, parents = True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok = True, parents = True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ""))
    folder_for_file.mkdir(exist_ok = True, parents = True)
    try:
        shutil.unpack_archive(str(file_name.absolut()), str(folder_for_file.absolut()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()


def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / "images / JPEG")
    for file in JPG_IMAGES:
        handle_media(file, folder / "images / JPG")
    for file in PNG_IMAGES:
        handle_media(file, folder / "images / PNG")
    for file in SVG_IMAGES:
        handle_media(file, folder / "images / SVG")
    for file in MP4_VIDEO:
        
        handle_media(file, folder / "video/ MP4_VIDEO")
    for file in AVI_VIDEO:
        handle_media(file, folder / "video/ AVI_VIDEO")
    for file in MOV_VIDEO:
        handle_media(file, folder / "video/ MOV_VIDEO")
    for file in MKV_VIDEO:
        handle_media(file, folder / "video/ MKV_VIDEO")

    for file in DOC_DOCUMENTS:
        handle_media(file, folder / "documents/ DOC_DOCUMENTS")
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / "documents/ DOCX_DOCUMENTS")
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / "documents/ TXT_DOCUMENTS")
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / "documents/ PDF_DOCUMENTS")
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / "documents/ XLSX_DOCUMENTS")
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / "documents/ PPTX_DOCUMENTS")

    for file in MP3_AUDIO:
        handle_media(file, folder / "audio/ MP3_AUDIO")
    for file in OGG_AUDIO:
        handle_media(file, folder / "audio/ OGG_AUDIO")
    for file in WAV_AUDIO:
        handle_media(file, folder / "audio/ WAV_AUDIO")
    for file in AMR_AUDIO:
        handle_media(file, folder / "audio/ AMR_AUDIO")
    
    for file in MY_OTHER:
        handle_media(file, folder / "MY_OTHER")
    
    for file in ARCHIVES:
        handle_archive(file, folder / "ARCHIVES")

    for folder in FOLDERS[::-1]:
        # видаляємо пусті папки після сортування
        try:
            folder.rmdir()
        except OSError:
            print(f"Error during remove filder{folder}")


def start():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process) 

