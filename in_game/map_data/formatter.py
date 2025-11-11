import io, re, time

# global iterator var since were iterating over the definitions file in multiple places but want to keep our progress
global i

# represents the whole definitions file 
class World:
    # dont instantiate the property here thatll fuck it up and children will be added to the first parent initiated
    continents: dict
    # for formatting the output to the file
    # if its not a location all we want to write is a comment, i appent 'MARK:' before the actual name as in my ide vscode that makes it show up in the minimap on the side which helps a lot, the new lines are so that the comments dont overlap on the minimap and its actually readable
    def __str__(self):
        locs = ""
        for k,v in self.continents.items():
            locs += "\n# MARK: " + k + "\n\n\n\n" + str(v)
        return locs
    # the actual 'recursive' loop 
    def __init__(self, defs, locations):
        # a variable not written to the object property till the end
        continents = {}
        # start index of the name of the record
        cstart = 0
        # make sure the global iterator is in scope
        global i
        # actually initialise the global iterator since this is the start of the loop
        i = 0
        while i < len(defs)-1:
            char = defs[i]
            # checking for the start of a def block
            if char == "{":
                # record the name of the block
                name = defs[cstart:i-1].strip()
                # add a new child object to the child dict variable
                continents[name] = Continent(i+1, defs, locations)
                # after the children have been created they have also increased the global iterator and now it shouldve been moved to the start of a new block and so we need to record that point so that we can get the name of the next block
                cstart = i+1
            # iterate
            i += 1
        # finally put the dict variable into the objects dict property
        self.continents = continents

class Continent:
    # for an explanation look at the world class
    subcontinents: dict
    def __repr__(self):
        locs = ""
        for k,v in self.subcontinents.items():
            locs += "\n# MARK: " + k + "\n\n\n\n" + str(v)
        return locs
    def __init__(self, sstart, defs, locations):
        subcontinents = {}
        global i
        i = sstart
        while i < len(defs)-1:
            char = defs[i]
            if char == "{":
                name = defs[sstart:i-1].strip()
                subcontinents[name] = Subcontinent(i+1, defs, locations)
                sstart = i+1
            if char == "}":
                break
            i += 1
        self.subcontinents = subcontinents

class Subcontinent:
    # for an explanation look at the world class
    regions: dict
    def __repr__(self):
        locs = ""
        for k,v in self.regions.items():
            locs += "\n# MARK: " + k + "\n\n\n\n" + str(v)
        return locs
    def __init__(self, rstart, defs, locations):
        regions = {}
        global i
        i = rstart
        while i < len(defs)-1:
            char = defs[i]
            if char == "{":
                name = defs[rstart:i-1].strip()
                regions[name] = Region(i+1, defs, locations)
                rstart = i+1
            if char == "}":
                break
            i += 1
        self.regions = regions

class Region:
    # for an explanation look at the world class
    areas: dict
    def __repr__(self):
        locs = ""
        for k,v in self.areas.items():
            locs += "\n# MARK: " + k + "\n\n\n\n" + str(v)
        return locs
    def __init__(self, astart, defs, locations):
        areas = {}
        global i
        i = astart
        while i < len(defs)-1:
            char = defs[i]
            if char == "{":
                name = defs[astart:i-1].strip()
                areas[name] = Area(i+1, defs, locations)
                astart = i+1
            if char == "}":
                break
            i += 1
        self.areas = areas

class Area:
    # for an explanation look at the world class
    provinces: dict
    def __repr__(self):
        locs = ""
        for k,v in self.provinces.items():
            locs += "\n# MARK: " + k + "\n\n\n\n" + str(v)
        return locs
    def __init__(self, pstart, defs, locations):
        provinces = {}
        global i
        i = pstart
        while i < len(defs)-1:
            char = defs[i]
            if char == "{":
                name = defs[pstart:i-1].strip()
                provinces[name] = Province(i+1, defs, locations)
                pstart = i+1
            if char == "}":
                break
            i += 1
        self.provinces = provinces

class Province:
    # for an explanation look at the world class
    locations: dict
    def __repr__(self):
        locs = ""
        for k,v in self.locations.items():
            locs += "\n" + str(v)
        return locs + "\n\n\n\n"
    def __init__(self, lstart, defs, locationsf):
        locations = {}
        global i
        i = lstart
        while i < len(defs)-1:
            char = defs[i]
            if char == "}":
                # print("'" + defs[lstart:i].strip() + "'")
                plocs = defs[lstart:i].strip()
                for loc in re.split(r'\s+', plocs):
                    if loc in locationsf:
                        locations[loc] = locationsf[loc]
                    else:
                        print(loc + " location does not exist")
                        # locations[loc] = Location(loc + " = { modifer = broken }")
                lstart = i
                # print("locations: " + str(locations))
                break
            i += 1
        self.locations = locations

# holds a location so that it can be formatted like the 
class Location:
    name = ""
    modifier = None
    topography = None
    vegetation = None
    climate = None
    religion = None
    culture = None
    raw_material = None
    movement_assistance = None
    natural_harbor_suitability = None

    # we just get the location line as a string and split it up all easy like
    def __init__(self, line):
        # i hope you know regex if you wanna edit this
        match = re.match(r"^(?P<name>\w+)\s=\s\{\s(?P<properties>[\w\s=\-.\{\}]+)\}$", line)
        self.name = match.group(1)
        properties_match = match.group(2)
        # split the location properties up by the whitespace between them, wait no not the white space between the numbers in the movement_assistance bit
        properties_spl = re.split(r"(?<=[a-zA-Z])\s(?=[a-zA-Z])", properties_match)
        properties_arr = []
        # split on all the = between the prop name and value
        # there was def a better way to do this that i saw and ignored cause i thought this was more interesting
        for prop in properties_spl:
            for i in prop.split(" = "):
                properties_arr.append(i)
        # with all the key values in a 1D array we can filter out only the keys which have an even numbered index and all the values which dont
        properties_keys = properties_arr[::2]
        properties_values = properties_arr[1::2]
        # and then smash those together into a dict
        properties_dict = {k: v for k, v in zip(properties_keys, properties_values)}
        # and then put that dict into the objects properties
        self.modifier = properties_dict["modifier"] if "modifier" in properties_dict else ""
        self.topography = properties_dict["topography"] if "topography" in properties_dict else ""
        self.vegetation = properties_dict["vegetation"] if "vegetation" in properties_dict else ""
        self.climate = properties_dict["climate"] if "climate" in properties_dict else ""
        self.religion = properties_dict["religion"] if "religion" in properties_dict else ""
        self.culture = properties_dict["culture"] if "culture" in properties_dict else ""
        self.raw_material = properties_dict["raw_material"] if "raw_material" in properties_dict else ""
        self.movement_assistance = properties_dict["movement_assistance"] if "movement_assistance" in properties_dict else ""
        self.natural_harbor_suitability = properties_dict["natural_harbor_suitability"] if "natural_harbor_suitability" in properties_dict else ""

    # builds a string representation of this object which should be almost identical to the input (i put some trailing whitespace on the end of the properties bit cause that bothered me)
    def __repr__(self):
        str = self.name + " = {"
        if self.modifier:
            str += " modifier = " + self.modifier + ""
        if self.topography:
            str += " topography = " + self.topography + ""
        if self.vegetation:
            str += " vegetation = " + self.vegetation + ""
        if self.climate:
            str += " climate = " + self.climate + ""
        if self.religion:
            str += " religion = " + self.religion + ""
        if self.culture:
            str += " culture = " + self.culture + ""
        if self.raw_material:
            str += " raw_material = " + self.raw_material + ""
        if self.movement_assistance:
            str += " movement_assistance = " + self.movement_assistance
        if self.natural_harbor_suitability:
            str += " natural_harbor_suitability = " + self.natural_harbor_suitability
        return str + " }"

# and this is the stuff that actually uses all that crap

# so just instantiate an empty dict for the locations to be parsed into from the original file
locations = {}

# feel free to chenge this to get a different source locations file
with open("in_game/map_data/location_templates.txt", 'r') as file:
    for location in file:
        # i think this isnt on one line in case you want to filter or something
        new_loc = Location(location)
        locations[new_loc.name] = new_loc

# initialise the definitions as an empty string
definition = ""

# feel free to chenge this to get a different source definitions file (remember the encoding tho thats important)
with open("in_game/map_data/definitions.txt", 'r', encoding="utf-8-sig") as file:
    for line in file:
        # filter out any whitespace or comments on each line that might mess with any of the splitting we'll be doing later on
        line = line.replace("\n", "")
        line = line.replace("\t", " ")
        line = line.replace(" = ", "=")
        line = re.sub(r'\#.+$', '', line)
        definition += line

# build the object build the structure
world = World(definition, locations)

# print(world)

# and again just write it wherever, but probably not into an existing locations file, check it before you load it yknow..
with open("in_game/map_data/output.txt", "w+") as world_file:
    world_file.write(str(world))