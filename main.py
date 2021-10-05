# -*- coding: utf-8 -*-

import sys
import getopt
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

error_messages = {
    'syntax': 'Usage: main.py -t <image/folder> <input>',
    'type': 'Filetype: -t only accepts image/folder',
    'language': 'Language: -l only accepts fin/eng',
    'not_found': 'File: folder not found or insufficient permissions',
    'output': 'Folder: output folder not found or insufficient permissions'
}

accepted_args = {
    'type': ['image', 'folder'],
    'language': ['fin', 'eng']
}

languages = {
    'fin': {
        'before': 'Ennen',
        'after': 'Jälkeen'
    },
    'eng': {
        'before': 'Before',
        'after': 'After'
    }
}

def throwError(error_message):
    print(error_message)
    sys.exit(2)

def parseCommand():
    commands = {
        'type': '',
        'language': 'eng',
        'output': './',
        'args': []
    }

    try:
        opts, args = getopt.getopt(sys.argv[1:], 't:l:o:', ['--type', '--language', '--output'])

        if not opts or not args:
            raise getopt.GetoptError(error_messages['syntax'])
    except getopt.GetoptError:
        throwError(error_messages['syntax'])

    for opt, arg in opts:
        if opt not in dict(opts):
            throwError(error_messages['syntax'])
        if opt in ('-t', '--type'):
            if arg in accepted_args['type']:
                commands['type'] = arg
            else:
                throwError(error_messages['type'])
        elif opt in ('-l', '--language'):
            if arg in accepted_args['language']:
                commands['language'] = arg
            else:
                throwError(error_messages['language'])
        elif opt in ('-o', '--output'):
            if Path(arg).is_dir():
                commands['output'] = arg
            else:
                throwError(error_messages['not_found'])

    commands['args'] = args
    return commands

def convertImages(commands):
    def resizeImage(_image):
        _image.thumbnail((1920, 1920), Image.ANTIALIAS)
    
    def addText(_before_after, _image):
        font = ImageFont.truetype('font/RobotoCondensed-Regular.ttf', 150)
        draw = ImageDraw.Draw(_image)
        if _before_after == 'before':
            draw.text((50, 50), languages[commands['language']]['before'], (255, 255, 255), font=font)
        elif _before_after == 'after':
            draw.text((50, 50), languages[commands['language']]['after'], (255, 255, 255), font=font)

    if commands['type'] == 'image':
        unprocessed_before = Image.open(Path(commands['args'][0]))
        resizeImage(unprocessed_before)
        addText('before', unprocessed_before)
        unprocessed_after = Image.open(Path(commands['args'][1]))
        resizeImage(unprocessed_after)
        addText('after', unprocessed_after)

        processed_image = Image.new('RGB', (unprocessed_before.size[0], 2 * unprocessed_before.size[1]), (250, 250, 250))
        processed_image.paste(unprocessed_before, (0, 0))
        processed_image.paste(unprocessed_after, (0, unprocessed_before.size[1]))
        processed_image.save(test_output / 'Test1.png', 'PNG')
    elif commands['type'] == 'folder':
        folder_path = Path(commands['args'][0])
        if folder_path.is_dir():
            files = [x for x in folder_path.iterdir()]
        else:
            throwError(error_messages['not_found'])

        for index, file in enumerate(files):
            if file.suffix != '.jpg' or file.suffix != '.jpeg' or file.suffix != '.png':
                files.pop(index)

        for i in range(0, len(files)):
            processed_image = None
            filename = files[i].stem
            file_suffix = files[i].suffix

            unprocessed_before = Image.open(Path(folder_path / (filename[0] + '1' + file_suffix)))
            resizeImage(unprocessed_before)
            addText('before', unprocessed_before)
            unprocessed_after = Image.open(Path(folder_path / (filename[0] + '2' + file_suffix)))
            resizeImage(unprocessed_after)
            addText('after', unprocessed_after)

            processed_image = Image.new('RGB', (unprocessed_before.size[0], 2 * unprocessed_before.size[1]), (250, 250, 250))
            processed_image.paste(unprocessed_before, (0, 0))
            processed_image.paste(unprocessed_after, (0, unprocessed_before.size[1]))
            processed_image.save(Path(commands['output']) / '{}.png'.format(i + 1), 'PNG') # + 1 so that filenames start from 1 not 0
                
if __name__ == "__main__":
    commands = parseCommand()
    convertImages(commands)
    print('Files successfully converted!')
