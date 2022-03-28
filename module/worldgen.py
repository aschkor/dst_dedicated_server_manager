from enum import Enum
from typing import Union
from . import constant
from . import ssh
try:
    from pathlib import PurePosixPath as Path
except:
    print('install pathlib module')
    import os
    try:
        os.system('python3 -m pip install pathlib')
    except:
        try:
            os.system('python -m pip install pathlib')
        except:
            print('Pip might not be installed, please install pip')
            import sys
            sys.exit()
    from pathlib import PurePosixPath as Path
try:
    import slpp
except:
    print('install slpp module')
    import os
    try:
        os.system('python3 -m pip install slpp')
    except:
        try:
            os.system('python -m pip install slpp')
        except:
            print('Pip might not be installed, please install pip')
            import sys
            sys.exit()
    import slpp


class EnumOption(Enum):
    def __str__(self) -> str:
        return self.value


class Preset(EnumOption):
    TOGETHER = 'SURVIVAL_TOGETHER'
    MOD_MISSING = 'MODE_MISSING'
    TOGETHER_CLASSIC = 'SURVIVAL_TOGETHER_CLASSIC'
    DEFAULT_PLUS = 'SURVIVAL_TOGETHER_PLUS'
    DARKNESS = 'COMPLETE_DARKNESS'
    TERRARIA = 'TERRARIA'
    CAVE = 'DST_CAVE'
    CAVE_PLUS = 'DST_CAVE_PLUS'
    TERRARIA_CAVE = 'TERRARIA_CAVE'
    DEFAULT = TOGETHER


class SpeEvents(EnumOption):
    NONE = 'none'
    DEFAULT = 'default'


class Events(EnumOption):
    DEFAULT = 'default'
    ENABLED = 'enabled'


class NeverDefault(EnumOption):
    NEVER = 'never'
    DEFAULT = 'default'


class DefaultAlways(EnumOption):
    DEFAULT = 'default'
    ALWAYS = 'always'


class NeDefAl(EnumOption):
    NEVER = 'never'
    DEFAULT = 'default'
    ALWAYS = 'always'


class SeasonDuration(EnumOption):
    NO = 'noseason'
    VERY_SHORT = 'veryshortseason'
    SHORT = 'shortseason'
    DEFAULT = 'default'
    LONG = 'longseason'
    VERY_LONG = 'verylongseason'
    RANDOM = 'random'


class Day(EnumOption):
    DEFAULT = 'default'
    LONG_DAY = 'longday'
    LONG_DUSK = 'longdusk'
    LONG_NIGHT = 'longnight'
    NO_DAY = 'noday'
    NO_DUSK = 'nodusk'
    NO_NIGHT = 'nonight'
    ONLY_DAY = 'onlyday'
    ONLY_DUSK = 'onlydusk'
    ONLY_NIGHT = 'onlynight'


class Frequency(EnumOption):
    NEVER = 'never'
    RARE = 'rare'
    DEFAULT = 'default'
    OFTEN = 'often'
    ALWAYS = 'always'


class Speed(EnumOption):
    VERY_SLOW = 'veryslow'
    SLOW = 'slow'
    DEFAULT = 'default'
    FAST = 'fast'
    VERY_FAST = 'veryfast'


class Quantities(EnumOption):
    NONE = 'none'
    FEW = 'few'
    DEFAULT = 'default'
    MANY = 'many'
    MAX = 'max'


class Season(EnumOption):
    DEFAULT = 'default'
    WINTER = 'winter'
    SPRING = 'spring'
    SUMMER = 'summer'
    AUTOMN_SPING = 'autumn|sping'
    WINTER_SUMMER = 'winter|summer'
    ALL = 'autumn|winter|spring|summer'


class GenPreset(EnumOption):
    DEFAULT = 'default'
    CAVE = 'cave_default'
    QUAGMIRE = 'quagmire_taskset'
    CLASSIC = 'classic'
    LAVAARENA = 'lavaarena_taskset'


class StartingLocation(EnumOption):
    LAVAARENA = 'lavaarena'
    PLUS = 'plus'
    DARKNESS = 'darkness'
    QUAGMIRE = 'quagmire_startlocation'
    CAVE = 'CAVES'
    DEFAULT = 'default'


class Size(EnumOption):
    SMALL = 'small'
    MEDIUM = 'medium'
    DEFAULT = 'default'
    HUGE = 'huge'


class Branching(EnumOption):
    NEVER = 'never'
    LEAST = 'least'
    DEFAULT = 'default'
    MOST = 'most'
    RANDOM = 'random'


class Rarities(EnumOption):
    NEVER = 'never'
    RARE = 'rare'
    UNCOMMON = 'uncommon'
    DEFAULT = 'default'
    OFTEN = 'often'
    MOSTLY = 'mostly'
    ALWAYS = 'always'
    INSANE = 'insane'


class StartingItem(EnumOption):
    CLASSIC = 'classic'
    DEFAULT = 'default'
    RANDOM = 'highly random'


class SeaRarities(EnumOption):
    NEVER = 'ocean_never'
    RARE = 'ocean_rare'
    UNCOMMON = 'ocean_uncommon'
    DEFAULT = 'ocean_default'
    OFTEN = 'ocean_often'
    MOSTLY = 'ocean_mostly'
    ALWAYS = 'ocean_always'
    INSANE = 'ocean_insane'


class ExtraItem(EnumOption):
    NO = '0'
    FEW = '5'
    DEFAULT = 'default'
    MANY = '15'
    MAX = '20'
    NONE = 'none'


class Key:
    def __init__(self, name, option, cat):
        self.name = name
        self.option = option
        self.cat = cat


OVERRIDE = 'override'


def _check_type(key, forbiden_1, forbiden_2, val=None) -> None:
    if isinstance(key, forbiden_1) or isinstance(key, forbiden_2):
        raise TypeError('Key {} dont exist for overworld'.format(key.name))

    if val is None:
        return

    if not isinstance(val, key.value.option):
        try:
            option_type = key.value.option.name
        except:
            option_type = type(key.value.option)
            raise TypeError('Value must be a {}'.format(option_type))


class Global(Enum):
    GENERATION_PRESET = Key('worldgen_preset', Preset, None)
    OVERRIDE = Key('override_enabled', bool, None)
    SETTING_PRESET = Key('settings_preset', Preset, None)


class Settings(Enum):
    TREEGUARDS = Key('liefs', Frequency, OVERRIDE)
    SPIDER_QUEEN = Key('spiderqueen', Frequency, OVERRIDE)
    LORD_OF_THE_FRUIT_FLIES = Key('fruitfly', Frequency, OVERRIDE)
    SPIDER_WARRIORS = Key('spider_warriors', Frequency, OVERRIDE)
    MERMS = Key('merms', Frequency, OVERRIDE)
    PIGS = Key('pigs_setting', Frequency, OVERRIDE)
    MUSH_GNOMES = Key('mushgnome', Frequency, OVERRIDE)
    MOLES = Key('moles_setting', Frequency, OVERRIDE)
    GRASS_GEKKO_MORPHING = Key('grassgekkos', Frequency, OVERRIDE)
    BUNNYMEN = Key('bunnymen_setting', Frequency, OVERRIDE)
    REGROWTH_MULTIPLIER = Key('regrowth', Speed, OVERRIDE)
    RAIN = Key('weather', Frequency, OVERRIDE)
    SPIDERS = Key('spiders_setting', Frequency, OVERRIDE)


class SettingsOverword(Enum):
    POISON_BIRCHNUT_TREES = Key('deciduousmonster', Frequency, OVERRIDE)
    MEESE_GEESE = Key('goosemoose', Frequency, OVERRIDE)
    MALBATROSS = Key('malbatross', Frequency, OVERRIDE)
    KLAUS = Key('klaus', Frequency, OVERRIDE)
    EYE_OF_TERROR = Key('eyeofterror', Frequency, OVERRIDE)
    DRAGONFLY = Key('dragonfly', Frequency, OVERRIDE)
    DEERCLOPS = Key('deerclops', Frequency, OVERRIDE)
    CRABKING = Key('crabking', Frequency, OVERRIDE)
    BEEQUEEN = Key('beequeen', Frequency, OVERRIDE)
    BEARGER = Key('bearger', Frequency, OVERRIDE)
    ANTLION_TRIBUTE = Key('antliontribute', Frequency, OVERRIDE)
    SKITTERSQUIDS = Key('squid', Frequency, OVERRIDE)
    SHATTERED_SPIDERS = Key('moon_spider', Frequency, OVERRIDE)
    SHARKS = Key('sharks', Frequency, OVERRIDE)
    MOSQUITOS = Key('mosquitos', Frequency, OVERRIDE)
    MOONROCK_PENGULLS = Key('penguins_moon', Frequency, OVERRIDE)
    MACKTUSK = Key('walrus_setting', Frequency, OVERRIDE)
    LUREPLANTS = Key('lureplants', Frequency, OVERRIDE)
    KILLER_BEES = Key('wasps', Frequency, OVERRIDE)
    HOUNDS_MOUNDS = Key('hound_mounds', Frequency, OVERRIDE)
    HORROR_HOUNDS = Key('mutated_hounds', Frequency, OVERRIDE)
    FROGS = Key('frogs', Frequency, OVERRIDE)
    COOKIE_CUTTERS = Key('cookiecutters', Frequency, OVERRIDE)
    SCHOOLS_OF_FISH = Key('fishschools', Frequency, OVERRIDE)
    WOBSTERS = Key('wobsters', Frequency, OVERRIDE)
    RABBITS = Key('rabbits_setting', Frequency, OVERRIDE)
    GOBBLERS = Key('perd', Frequency, OVERRIDE)
    GNARWAILS = Key('gnarwail', Frequency, OVERRIDE)
    BIRDS = Key('birds', Frequency, OVERRIDE)
    CATCOONS = Key('catcoons', Frequency, OVERRIDE)
    BUTTERFLIES = Key('butterfly', Frequency, OVERRIDE)
    WILDFIRES = Key('wildfires', Frequency, OVERRIDE)
    METEOR_FREQUENCY = Key('meteorshowers', Frequency, OVERRIDE)
    LIGHTNING = Key('lightning', Frequency, OVERRIDE)
    HUNT = Key('hunt', Frequency, OVERRIDE)
    HUNT_SURPRISES = Key('alternatehunt', Frequency, OVERRIDE)
    FROG_RAIN = Key('frograin', Frequency, OVERRIDE)
    PERTIFICATION = Key('petrification', Quantities, OVERRIDE)
    KRAMPII = Key('krampus', Frequency, OVERRIDE)
    BEEFALO_MATING_FREQUENCY = Key('beefaloheat', Frequency, OVERRIDE)
    SANITY_MONSTERS = Key('shadowcreatures', Frequency, OVERRIDE)
    ENLIGHTENMENT_MONSTERS = Key('brightmarecreatures', Frequency, OVERRIDE)
    WORM_ATTACKS = Key('wormattacks', Frequency, OVERRIDE)
    SUMMER_HOUNDS = Key('summerhounds', NeverDefault, OVERRIDE)
    WINTER_HOUNDS = Key('winterhounds', NeverDefault, OVERRIDE)
    DROP = Key('dropeverythingondespawn', DefaultAlways, OVERRIDE)
    PROTECT = Key('spawnprotection', DefaultAlways, OVERRIDE)
    SEASON_ITEM = Key('seasonalstartingitems', NeverDefault, OVERRIDE)
    EXTRA_ITEMS = Key('extrastartingitems', ExtraItem, OVERRIDE)
    TWIGGY_TREES = Key('twiggytrees_regrowth', Speed, OVERRIDE)
    SALT_FORMATIONS = Key('saltstack_regrowth', Speed, OVERRIDE)
    LUNE_TREES = Key('moon_tree_regrowth', Speed, OVERRIDE)
    FLOWERS = Key('flowers_regrowth', Speed, OVERRIDE)
    EVERGREENS = Key('evergreen_regrowth', Speed, OVERRIDE)
    CARROTS = Key('carrots_regrowth', Speed, OVERRIDE)
    BIRCHNUT_TREE = Key('deciduoustree_regrowth', Speed, OVERRIDE)
    DAY_TYPE = Key('day', Day, OVERRIDE)
    SUMMER = Key('summer', SeasonDuration, OVERRIDE)
    SPRING = Key('spring', SeasonDuration, OVERRIDE)
    WINTER = Key('winter', SeasonDuration, OVERRIDE)
    AUTUMN = Key('autumn', SeasonDuration, OVERRIDE)
    SPE_EVENT = Key('specialevent', SpeEvents, OVERRIDE)
    YEAR_OF_THE_CATCOON = Key('year_of_the_catcoon', Events, OVERRIDE)
    YEAR_OF_THE_BEEFFALO = Key('year_of_the_beefalo', Events, OVERRIDE)
    YEAR_OF_THE_CARRAT = Key('year_of_the_carrat', Events, OVERRIDE)
    YEAR_OF_THE_PIG = Key('year_of_the_pig', Events, OVERRIDE)
    YEAR_OF_THE_VARG = Key('year_of_the_varg', Events, OVERRIDE)
    YEAR_OF_THE_GOBBLER = Key('year_of_the_gobbler', Events, OVERRIDE)
    WINTER_FEAST = Key('winters_feast', Events, OVERRIDE)
    HALLOWED_NIGHT = Key('hallowed_nights', Events, OVERRIDE)
    MIDSUMMER_CAWNIVAL = Key('crow_carnival', Events, OVERRIDE)
    BEES = Key('bees_setting', Frequency, OVERRIDE)
    HOUNDS = Key('hounds', Frequency, OVERRIDE)
    PENGULLS = Key('penguins', Frequency, OVERRIDE)


class SettingsUnderworld(Enum):
    MUSHROOM_TREES = Key('mushtree_regrowth', Speed, OVERRIDE)
    LIGHT_FLOWER = Key('flower_cave_regrowth', Speed, OVERRIDE)
    TOADSTOOL = Key('toadstool', Frequency, OVERRIDE)
    SPITTER_SPIDERS = Key('spider_spitter', Frequency, OVERRIDE)
    RUINS_NIGHTMARES = Key('nightmarecreatures', Frequency, OVERRIDE)
    NAKED_MOLE_BATS = Key('molebats', Frequency, OVERRIDE)
    DANGLING_DEPTH_DWELLERS = Key('spider_dropper', Frequency, OVERRIDE)
    CAVE_SPIDERS = Key('spider_hider', Frequency, OVERRIDE)
    ROCK_LOBSTERS = Key('rocky_setting', Frequency, OVERRIDE)
    SPLUMONKEYS = Key('monkey_setting', Frequency, OVERRIDE)
    SNURTLES = Key('snurtles', Frequency, OVERRIDE)
    SLURTLES = Key('slurtles_setting', Frequency, OVERRIDE)
    DUST_MOTHS = Key('dustmoths', Frequency, OVERRIDE)
    BULBOUS_LIGHTBUGS = Key('lightfliers', Frequency, OVERRIDE)
    LUNAR_MUSHTREES = Key('mushtree_moon_regrowth', Speed, OVERRIDE)
    LIGHTBUG_FLOWER = Key('lightflier_flower_regrowth', Speed, OVERRIDE)
    EARTHQUAKES = Key('earthquakes', Frequency, OVERRIDE)
    ANCIENT_GATEWAY = Key('atriumgate', Frequency, OVERRIDE)
    BATS = Key('bats_setting', Frequency, OVERRIDE)


class GenerationOverworld(Enum):
    TALLBIRDS = Key('tallbirds', Rarities, OVERRIDE)
    SHATTERED_SPIDER_HOLES = Key('moon_spiders', Rarities, OVERRIDE)
    SEA_WEEDS = Key('ocean_waterplant', SeaRarities, OVERRIDE)
    MACTUSK_CAMPS = Key('walrus', Rarities, OVERRIDE)
    LEAKY_SHACK = Key('merm', Rarities, OVERRIDE)
    KILLER_BEE_HIVES = Key('angrybees', Rarities, OVERRIDE)
    HOUND_MOUNDS = Key('houndmound', Rarities, OVERRIDE)
    WOBSTER_MOUNDS = Key('ocean_wobsterden', Rarities, OVERRIDE)
    VOLT_GOATS = Key('lightninggoat', Rarities, OVERRIDE)
    SHOALS = Key('ocean_shoal', Rarities, OVERRIDE)
    SALADMANDER = Key('moon_fruitdragon', Rarities, OVERRIDE)
    RABBIT_HOLES = Key('rabbits', Rarities, OVERRIDE)
    PIG_HOUSE = Key('pigs', Rarities, OVERRIDE)
    MOLE_BORROWS = Key('moles', Rarities, OVERRIDE)
    HOLLOW_STUMP = Key('catcoon', Rarities, OVERRIDE)
    CARRATS = Key('moon_carrot', Rarities, OVERRIDE)
    BUZZARDS = Key('buzzard', Rarities, OVERRIDE)
    BEEFALOS = Key('beefalo', Rarities, OVERRIDE)
    TUMBLEWEEDS = Key('tumbleweed', Rarities, OVERRIDE)
    STONE_FRUIT_BUSHES = Key('moon_berrybush', Rarities, OVERRIDE)
    SEA_STACKS = Key('ocean_seastack', SeaRarities, OVERRIDE)
    PONDS = Key('ponds', Rarities, OVERRIDE)
    MINI_GLACIERS = Key('rock_ice', Rarities, OVERRIDE)
    METEOR_FIELDS = Key('meteorspawner', Rarities, OVERRIDE)
    LUNE_TREES = Key('moon_tree', Rarities, OVERRIDE)
    LUNAR_SAPLINGS = Key('moon_sapling', Rarities, OVERRIDE)
    LUNAR_ROCKS = Key('moon_rock', Rarities, OVERRIDE)
    HOT_SPRINGS = Key('moon_hotspring', Rarities, OVERRIDE)
    FLOWERS = Key('flowers', Rarities, OVERRIDE)
    CARROTS = Key('carrot', Rarities, OVERRIDE)
    CACTI = Key('cactus', Rarities, OVERRIDE)
    BULL_KELP = Key('ocean_bullkelp', Rarities, OVERRIDE)
    BEACHED_BULL_KELP = Key('moon_bullkelp', Rarities, OVERRIDE)
    ANENEMIES = Key('moon_starfish', Rarities, OVERRIDE)
    TERRAUIM = Key('terrariumchest', NeverDefault, OVERRIDE)
    CELESTIAL_FISSURES = Key('moon_fissure', Rarities, OVERRIDE)
    ROADS = Key('roads', NeverDefault, OVERRIDE)
    STARTING_SEASON = Key('season_start', Season, OVERRIDE)


class GenerationUnderworld(Enum):
    TENTACLES = Key('tentacles', Rarities, OVERRIDE)
    SPILAGMITES = Key('cave_spiders', Rarities, OVERRIDE)
    NIGHTMARE_FISSURES = Key('fissure', Rarities, OVERRIDE)
    BATS = Key('bats', Rarities, OVERRIDE)
    SPLUMONKEY_PODS = Key('monkey', Rarities, OVERRIDE)
    SLURTLE_MOUNDS = Key('slurtles', Rarities, OVERRIDE)
    SLURPERS = Key('slurper', Rarities, OVERRIDE)
    ROCK_LOBSTERS = Key('rocky', Rarities, OVERRIDE)
    RABBIT_HUTCHES = Key('bunnymen', Rarities, OVERRIDE)
    CAVE_PONDS = Key('cave_ponds', Rarities, OVERRIDE)
    LICHEN = Key('lichen', Rarities, OVERRIDE)
    GLOW_BERRIES = Key('wormlights', Rarities, OVERRIDE)
    CAVE_FERNS = Key('fern', Rarities, OVERRIDE)
    CAVE_BANANAS = Key('banana', Rarities, OVERRIDE)
    SINKHOLE_LIGHTS = Key('cavelight', Speed, OVERRIDE)
    MUSHROOM_TREES = Key('mushtree', Rarities, OVERRIDE)
    LIGHT_FLOWERS = Key('flower_cave', Rarities, OVERRIDE)
    CAVE_WORMS = Key('worms', Rarities, OVERRIDE)


class Generation(Enum):
    BIOMES = Key('task_set', GenPreset, OVERRIDE)
    SPAWN_AREA = Key('start_location', StartingLocation, OVERRIDE)
    WORLD_SIZE = Key('world_size', Size, OVERRIDE)
    BRANCHES = Key('branching', Branching, OVERRIDE)
    LOOPS = Key('loop', NeDefAl, OVERRIDE)
    TOUCH_STONES = Key('touchstone', Rarities, OVERRIDE)
    FAILED_SURVIVORS = Key('boons', Rarities, OVERRIDE)
    STARTING_RESSOURCE_VARIETY = Key('prefabswaps_start', StartingItem,
                                     OVERRIDE)
    BERRY_BUSHES = Key('berrybush', Rarities, OVERRIDE)
    BOULDERS = Key('rock', Rarities, OVERRIDE)
    FLINT = Key('flint', Rarities, OVERRIDE)
    GRASS = Key('grass', Rarities, OVERRIDE)
    MUSHROOMS = Key('mushroom', Rarities, OVERRIDE)
    REEDS = Key('reeds', Rarities, OVERRIDE)
    SAPLINGS = Key('sapling', Rarities, OVERRIDE)
    SPIKY_BUSHES = Key('marshbush', Rarities, OVERRIDE)
    TREES = Key('trees', Rarities, OVERRIDE)
    BEE_HIVES = Key('bees', Rarities, OVERRIDE)
    CLOCKWORKS = Key('chess', Rarities, OVERRIDE)
    SPIDER_DENS = Key('spiders', Rarities, OVERRIDE)


class WorldGen:
    def __init__(self):
        self._dict = {}

    def __update_override_enabled(self):
        keys = list(self._dict.keys())
        if not len(keys):
            return

        name = Global.OVERRIDE.value.name
        if len(keys) == 1 and keys[0] == name:
            self._dict.popitem()
            return

        if not keys.count(name):
            self._dict[name] = True

    def _add(self, key, value) -> None:
        data = key.value

        if value == data.option.DEFAULT or value is None:
            self.remove(key)
            return

        if data.cat is None:
            self._dict[data.name] = str(value)
        else:
            if data.cat != None and self._dict.get(data.cat) is None:
                self._dict.update({data.cat: {}})
            self._dict[data.cat][data.name] = str(value)

        self.__update_override_enabled()

    def _get(self, key):
        res = self._dict.get(key.value.name)
        if res is None:
            return key.value.options.Default
        return key.value.options(res)

    def is_empty(self) -> bool:
        return not bool(self._dict)

    def remove(self, key) -> None:
        data = key.value
        if data.cat is None:
            self._dict.pop(data.name)
        else:
            self._dict[data.cat].pop(data.name)
            if not len(list(self._dict[data.cat].keys())):
                self._dict.pop(data.cat)

        self.__update_override_enabled()

    def __str__(self):
        return 'return ' + str(slpp.slpp.encode(self._dict))


class Overworld(WorldGen):
    def __init__(self):
        super().__init__()

    def set(self, key, value) -> None:
        _check_type(key, SettingsUnderworld, GenerationUnderworld, value)
        self._add(key, value)

    def get(self, key):
        _check_type(key, SettingsUnderworld, GenerationUnderworld)
        return self._get(key)


class Underworld(WorldGen):
    def __init__(self):
        super().__init__()

    def set(self, key, value) -> None:
        _check_type(key, SettingsOverword, GenerationOverworld, value)
        self._add(key, value)

    def get(self, key):
        _check_type(key, SettingsOverword, GenerationOverworld)
        return self._get(key)


def remote_install(world_gen: WorldGen, cluster_name: Path,
                   is_master: bool) -> None:
    if is_master:
        shard = constant.MASTER_NAME_DIR
    else:
        shard = constant.CAVE_NAME_DIR
    path = constant.CLUSTER_DIRECTORY / str(
        cluster_name) / shard / 'worldgenoverride.lua'
    ssh.create_file(path, str(world_gen))


def load(content: Union[str, None],
         is_overworld: bool) -> Union[Overworld, Underworld]:
    res = None
    if is_overworld:
        res = Overworld()
    else:
        res = Underworld()
    if content is not None:
        res._dict = slpp.slpp.decode(content)
    return res


def remote_load(cluster_name: Path, is_master: bool,
                is_overworld: bool) -> Union[Overworld, Underworld]:
    path = constant.CLUSTER_DIRECTORY / str(cluster_name).replace(' ', '\ ')
    if is_master:
        path = path / constant.MASTER_NAME_DIR
    else:
        path = path / constant.CAVE_NAME_DIR
    path = path / 'worldgenoverride.lua'

    return load(ssh.get_file_content(path), is_overworld)
