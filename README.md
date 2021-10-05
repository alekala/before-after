# before-after
                                              
## USAGE

main.py -t <image/folder> <input>

EXAMPLES

Individual images
INPUT:    main.py -t image before.jpg after.jpg
OUTPUT:   1.png

Folder
INPUT:    main.py -t folder images
OUTPUT:   1.png, 2.png, 3.png, 4.png...

Naming scheme for images inside the folder:
<image number><1=before, 2=after>.jpg
11.jpg, 12.jpg
21.jpg, 22.jpg
31.jpg, 32.jpg
41.jpg, 42.jpg

## OPTIONS / ARGUMENTS

(required)
--type -t
image/folder

(optional)
--language -l (default eng)
fin/eng

(optional)
--output -o
path to output folder (default ./)
