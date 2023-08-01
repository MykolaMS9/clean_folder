from pathlib import Path
import shutil
import os
import re

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def normalize(namef):
    word = []
    for val in namef:
        if re.findall('[а-яА-ЯіІїЇґ]', val):
            word.append(TRANS[ord(val)])
        elif re.findall('[a-zA-Z0-9]', val):
            word.append(val)
        else:
            word.append('_')
    return ''.join(word)

current_directory = Path().absolute()

# Створення нових каталогів
FOLDERS = (str(current_directory) + '\\images',
           str(current_directory) + '\\video',
           str(current_directory) + '\\documents',
           str(current_directory) + '\\audio',
           str(current_directory) + '\\archives')
EXTENSIONS = [['.jpeg', '.png', '.jpg', '.svg'],
              ['.avi', '.mp4', '.mov', '.mkv'],
              ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.ppt'],
              ['.mp3', '.ogg', '.wav', '.amr', '.flac'],
              ['.zip', '.gz', '.tar']]


def create_folders(folders):
    for val in folders:
        if not Path(val).exists():
            os.mkdir(val)



# Пошук та перенесення файлів
newname = 1
unknownFiles = []
deletedDir = []
exFolders = [[], [], [], [], []]
exUnknown = []

def find_unknown_files(dir):
    for val in dir.iterdir():
        if not val.is_dir() and not val.suffix in EXTENSIONS:
            unknownFiles.append(str(val))
            exUnknown.append(val.suffix)

def check_name(exsistPath, destinationPath):
    global newname
    if os.path.exists(os.path.join(destinationPath, exsistPath.name)):
        newname += 1
        name = f'{str(exsistPath.name).replace(exsistPath.suffix, "")}_{newname}'
    else:
        name = str(exsistPath.name).replace(exsistPath.suffix, "")
    return name

def replace_files(p):
    for ind in range(5):
        flag = False
        for val in p.iterdir():
            if val.suffix in EXTENSIONS[ind]:
                if not flag:  # для виводу шляху
                    flag = True
                    print(f'From folder {str(p)} removed to {FOLDERS[ind]} next files:')
                namefile = Path(os.path.join(FOLDERS[ind], f'{normalize(check_name(val, FOLDERS[ind]))}{val.suffix}'))
                shutil.move(val, namefile)
                exFolders[ind].append(val.suffix)
                if val.name == namefile.name:
                    print('{:^10}{:<40}'.format('', f'{val.name}'))
                else:
                    print('{:^10}{:<40}{:^7}{:<40}'.format('Renamed', f'{val.name}', '-->', f'{namefile.name}'))
        if flag:
            print('-' * 100)
    for val in p.iterdir():  #рекурсія
        if val.is_dir() and not str(val) in FOLDERS:
            replace_files(val)
    find_unknown_files(p)
    if not os.listdir(p):
        deletedDir.append(str(p))
        os.rmdir(p)



def print_files(path, text):
    if path:
        print(text)
        for val in path.iterdir():
            print('{:^10}{:<40}'.format('', f'{val.name}'))


def print_extensions(Value, text):
    if Value:
        print(text)
        print('{:^15}{:<50}'.format('', f'{", ".join(set(Value))}'))



def run():
    create_folders(FOLDERS)
    replace_files(Path(str(current_directory)))

    [print_files(Path(v1), v2) for v1, v2 in zip(FOLDERS, ['Photo:', 'Video:', 'Documents:', 'Music:', 'Archives:'])]
    if unknownFiles:
        print('Next unknown file:') if len(unknownFiles) == 1 else print(f'Next unknown files:')
        for val in unknownFiles:
            print('{:^10}{:<40}'.format('', f'{val}'))

    [print_extensions(v1, v2) for v1, v2 in zip(exFolders,
                                               ['Image extensions:', 'Video extensions:', 'Documents extensions:',
                                                'Audio extensions:', 'Archives extensions:'])]
    print_extensions(exUnknown, 'Unknown extensions:')

    # розпаковка архівів
    for val in Path(FOLDERS[4]).iterdir():
        if val.suffix in EXTENSIONS[4]:
            name = val.name.split('.')
            fold_dir = os.path.join(FOLDERS[4], name[0])
            if not Path(fold_dir).exists():
                os.mkdir(fold_dir)
            shutil.unpack_archive(str(val), str(fold_dir))
            if val.exists():
                os.remove(val)

if __name__ == '__main__':
    run()