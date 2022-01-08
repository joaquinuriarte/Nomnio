# --------------------------------------------preScanning--------------------------------------------------------------#
"""
    * Method to scan paragraph for width and length
    *
    * @param filepath file path of file
    * @return dictionary with keys as lines and value as their corresponding width
"""  # getWidthAndLength()


def getWidthAndLength(filepath):
    size = {}
    lCount = 0
    with open(filepath, 'r') as file:
        for line in file.readlines():
            size[lCount] = len(line)
            lCount += 1
    return size


# --------------------------------------------CoordinateBuilder--------------------------------------------------------#
"""
     * Methods returns list of coordinates (tuples) for nomnio provided dimensions of paragraph
     * Method name corresponds to figure drawn
     *
     * @param size dimensions of paragraph
     * @return list of nomnio's coordinates (tuples)
     */
"""  # getXCoordinates()


def getPyramidCoordinates(size):
    ls = size[0] // 2
    rs = size[0] // 2
    lsA = -1
    rsA = 1
    coords = [(0, ls)]
    if len(size) == 1:
        return coords
    elif len(size) >= 2:
        for l in size:
            if l == '0':
                continue
            elif ls + lsA < 0 or rs + rsA > size[l]:
                break
            else:
                ls += lsA
                rs += rsA
                coords.append((int(l), ls))
                coords.append((int(l), rs))
    return coords


# TODO: Find way to relate length to amount of coordinates on quadrants so it forms complete circle
def getCircleCoordinates(size):
    ls = size['0'] // 2
    rs = size['0'] // 2
    lsA = -1
    rsA = 1
    coords = [(0, ls)]
    if len(size) == 1 or len(size) == 2:
        return coords
    elif len(size) == 3 or len(size) == 4:  # This is wrong
        coords.append((int(size[2]), 0))
        coords.append((3, size[2]))
        coords.append((3, size[3] // 2))
        return coords
    elif len(
            size) >= 5:
        for l in size:
            if len(size) == 1:
                coords.append((1, size[1] // 2))
            elif (ls + lsA < 0) or (rs + rsA > size[l]):
                lsA = 1
                rsA = -1
                ls += lsA
                rs += rsA
                coords.append((l, ls))
                coords.append((l, rs))
            else:
                ls += lsA
                rs += rsA
                coords.append((l, ls))
                coords.append((l, rs))
    return coords


# --------------------------------------------Rewrite&Nomniate---------------------------------------------------------#
"""
    * Method rewrites file into another file with correct nomnio alignment to form desired figure
    *
    * @param filepath file path of file
    * @param outFilepath file path of output file
    * @param filename name of output file
    * @param shape desired nomnio shape. Currently supports: 
        - Pyramid
        - Circle (not completed)
    * @param w length of each line
    * @return 1 if successful 0 otherwise
"""
"""
    * Method adds \n to file for formatting purposes. Intended to be a temporary fix to alignment issue.
    *
    * @param filepath file path of file
    * @param w length of each line
    * @return name of new filepath
"""


# TODO: Find way to save alignment so that when you expand file it doesn't mess up nomnio (replace align())
# TODO: Find way to calculate appropriate w for line length
# TODO: Find way to keep words together and shift them entirely instead of characters
# TODO: Check if manipulating font size helps align hard nomnios or a specific w
def nomnioAlign(filepath, outFilepath, filename, shape, w):
    size = getWidthAndLength(align(filepath, w))
    coords = []
    if shape == "Circle":
        coords = getCircleCoordinates(size)
    elif shape == "Pyramid":
        coords = getPyramidCoordinates(size)
    else:
        print("Provided Shape not supported :(\n")
        return 0
    length = 1
    nomnified = open(outFilepath + filename, 'w')
    with open(align(filepath, w), 'r') as infile:
        for line in infile:
            width = 1
            for character in line:
                if (length, width) in coords:
                    nomnified.write(" ")
                    nomnified.write(character)
                    width += 2
                else:
                    nomnified.write(character)
                    width += 1
            length += 1
    nomnified.close()
    return 1


def align(filepath, w):
    with open(filepath, "r") as temp:
        exit = open(filepath[0:filepath.find(".")] + "Real.txt", "w")
        count = 0
        for line in temp:
            for f in line:
                if count % w == 0 and count != 0:
                    exit.write("\n")
                exit.write(f)
                count += 1
        exit.close()
    newFileName = filepath[0:filepath.find(".")] + "Real.txt"
    return newFileName


# --------------------------------------------------Run----------------------------------------------------------------#

filePath = "/Users/joaquinuriarte/Desktop/pilot.txt"  # Path of file to manipulate
outFilePath = "/Users/joaquinuriarte/Desktop/"  # Path to destination of nomnated file
nameOfNewFile = "pilotCompleted.txt"  # Name of nomnated file
shape = "Pyramid"  # Shape of nomnio
leng = 100

print(nomnioAlign(filePath, outFilePath, nameOfNewFile, shape, leng))
