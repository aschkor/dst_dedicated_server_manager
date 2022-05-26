from enum import Enum
from typing import Union
from . import constant
from .slpp import slpp
from . import ssh

class EnumOption(Enum):
    def __str__(self) -> str:
        return self.value[0]

class Preset(EnumOption):
    TOGETHER = 'SURVIVAL_TOGETHER',
    MOD_MISSING = 'MODE_MISSING',
    TOGETHER_CLASSIC = 'SURVIVAL_TOGETHER_CLASSIC',
    DEFAULT_PLUS = 'SURVIVAL_TOGETHER_PLUS',
    DARKNESS = 'COMPLETE_DARKNESS',
    TERRARIA = 'TERRARIA',
    CAVE = 'DST_CAVE',
    CAVE_PLUS = 'DST_CAVE_PLUS',
    TERRARIA_CAVE = 'TERRARIA_CAVE',
    DEFAULT = TOGETHER


class SpeEvents(EnumOption):
    NONE= 'none',
    DEFAULT = 'default',

class Events(EnumOption):
    DEFAULT = 'default',
    ENABLED = 'enabled'

class NeverDefault(EnumOption):
    NEVER = 'never',
    DEFAULT = 'default'

class DefaultAlways(EnumOption):
    DEFAULT = 'default',
    ALWAYS = 'always'

class NeDefAl(EnumOption):
    NEVER = 'never',
    DEFAULT = 'default',
    ALWAYS = 'always'

class SeasonDuration(EnumOption):
    NO = 'noseason',
    VERY_SHORT = 'veryshortseason',
    SHORT = 'shortseason',
    DEFAULT = 'default',
    LONG = 'longseason',
    VERY_LONG = 'verylongseason',
    RANDOM = 'random'

class Day (EnumOption):
    DEFAULT = 'default',
    LONG_DAY = 'longday',
    LONG_DUSK = 'longdusk',
    LONG_NIGHT = 'longnight',
    NO_DAY = 'noday',
    NO_DUSK = 'nodusk',
    NO_NIGHT = 'nonight',
    ONLY_DAY = 'onlyday',
    ONLY_DUSK = 'onlydusk',
    ONLY_NIGHT = 'onlynight'

class Frequency(EnumOption):
    NEVER = 'never',
    RARE = 'rare',
    DEFAULT = 'default',
    OFTEN = 'often',
    ALWAYS = 'always'

class Speed(EnumOption):
    VERY_SLOW = 'veryslow',
    SLOW = 'slow',
    DEFAULT = 'default',
    FAST = 'fast',
    VERY_FAST = 'veryfast'

class Quantities(EnumOption):
    NONE = 'none',
    FEW = 'few',
    DEFAULT = 'default',
    MANY = 'many',
    MAX = 'max'

class Season(EnumOption):
    DEFAULT = 'default',
    WINTER = 'winter',
    SPRING = 'spring',
    SUMMER = 'summer',
    AUTOMN_SPING = 'autumn|sping',
    WINTER_SUMMER = 'winter|summer',
    ALL = 'autumn|winter|spring|summer'

class GenPreset(EnumOption):
    DEFAULT = 'default',
    CAVE = 'cave_default',
    QUAGMIRE = 'quagmire_taskset',
    CLASSIC = 'classic',
    LAVAARENA = 'lavaarena_taskset'

class StartingLocation(EnumOption):
    LAVAARENA = 'lavaarena',
    PLUS = 'plus',
    DARKNESS = 'darkness',
    QUAGMIRE = 'quagmire_startlocation',
    CAVE = 'CAVES',
    DEFAULT = 'default'

class Size(EnumOption):
    SMALL = 'small',
    MEDIUM = 'medium',
    DEFAULT = 'default',
    HUGE = 'huge'

class Branching(EnumOption):
    NEVER = 'never',
    LEAST = 'least',
    DEFAULT = 'default',
    MOST = 'most',
    RANDOM = 'random'

class Rarities(EnumOption):
    NEVER = 'never',
    RARE = 'rare',
    UNCOMMON = 'uncommon',
    DEFAULT = 'default',
    OFTEN = 'often',
    MOSTLY = 'mostly',
    ALWAYS = 'always',
    INSANE = 'insane'

class StartingItem(EnumOption):
    CLASSIC = 'classic',
    DEFAULT = 'default',
    RANDOM = 'highly random'


class SeaRarities(EnumOption):
    NEVER = 'ocean_never',
    RARE = 'ocean_rare',
    UNCOMMON = 'ocean_uncommon',
    DEFAULT = 'ocean_default',
    OFTEN = 'ocean_often',
    MOSTLY = 'ocean_mostly',
    ALWAYS = 'ocean_always',
    INSANE = 'ocean_insane'

class ExtraItem(EnumOption):
    NO = '0',
    FEW = '5',
    DEFAULT = 'default',
    MANY = '15',
    MAX = '20',
    NONE = 'none'

class Key:
    def __init__(self, name, option, cat):
        self.name = name
        self.option = option
        self.cat = cat
        
OVERRIDE = 'override'

class Global(Enum):
    GENERATION_PRESET = Key('worldgen_preset', Preset, None),
    OVERRIDE = Key('override_enabled', bool, None),
    SETTING_PRESET = Key('settings_preset', Preset, None),


class Generation(Enum):
    BIOMES = Key('task_set', GenPreset, OVERRIDE),
    SPAWN_AREA = Key('start_location', StartingLocation, OVERRIDE),
    WORLD_SIZE = Key('world_size', Size, OVERRIDE),
    BRANCHES = Key('branching', Branching, OVERRIDE),
    LOOPS = Key('loop', NeDefAl, OVERRIDE),
    STARTING_SEASON = Key('season_start',Season,  OVERRIDE),
    ROADS = Key('roads', NeverDefault, OVERRIDE),
    TOUCH_STONES = Key('touchstone', Rarities, OVERRIDE),
    FAILED_SURVIVORS = Key('boons', Rarities, OVERRIDE),
    SINKHOLE_LIGHTS = Key('cavelight', Speed, OVERRIDE),
    STARTING_RESSOURCE_VARIETY = Key('prefabswaps_start', StartingItem, OVERRIDE),
    CELESTIAL_FISSURES = Key( 'moon_fissure', Rarities, OVERRIDE),
    TERRAUIM = Key('terrariumchest', NeverDefault, OVERRIDE),
    BERRY_BUSHES = Key('berrybush', Rarities, OVERRIDE),
    BOULDERS = Key('rock', Rarities, OVERRIDE),
    CAVE_BANANAS = Key('banana', Rarities, OVERRIDE),
    CAVE_FERNS = Key('fern', Rarities, OVERRIDE),
    FLINT = Key('flint', Rarities, OVERRIDE),
    GLOW_BERRIES = Key('wormlights', Rarities, OVERRIDE),
    GRASS = Key('grass', Rarities, OVERRIDE),
    LICHEN = Key('lichen', Rarities, OVERRIDE),
    LIGHT_FLOWERS = Key('flower_cave', Rarities, OVERRIDE),
    MUSHROOM_TREES = Key('mushtree', Rarities, OVERRIDE),
    MUSHROOMS = Key('mushroom', Rarities, OVERRIDE),
    CAVE_PONDS = Key('cave_ponds', Rarities, OVERRIDE),
    REEDS = Key('reeds', Rarities, OVERRIDE),
    SAPLINGS = Key('sapling', Rarities, OVERRIDE),
    SPIKY_BUSHES = Key('marshbush', Rarities, OVERRIDE),
    TREES = Key('trees', Rarities, OVERRIDE),
    ANENEMIES = Key('moon_starfish', Rarities, OVERRIDE),
    BEACHED_BULL_KELP = Key('moon_bullkelp', Rarities, OVERRIDE),
    BULL_KELP = Key('ocean_bullkelp', Rarities, OVERRIDE),
    CACTI = Key('cactus', Rarities, OVERRIDE),
    CARROTS = Key('carrot', Rarities, OVERRIDE),
    FLOWERS = Key('flowers', Rarities, OVERRIDE),
    HOT_SPRINGS = Key('moon_hotspring', Rarities, OVERRIDE),
    LUNAR_ROCKS = Key('moon_rock', Rarities, OVERRIDE),
    LUNAR_SAPLINGS = Key('moon_sapling', Rarities, OVERRIDE),
    LUNE_TREES = Key('moon_tree', Rarities, OVERRIDE),
    METEOR_FIELDS = Key('meteorspawner', Rarities, OVERRIDE),
    MINI_GLACIERS = Key('rock_ice', Rarities, OVERRIDE),
    PONDS = Key('ponds', Rarities, OVERRIDE),
    SEA_STACKS = Key('ocean_seastack', SeaRarities, OVERRIDE),
    STONE_FRUIT_BUSHES = Key('moon_berrybush', Rarities, OVERRIDE),
    TUMBLEWEEDS = Key('tumbleweed', Rarities, OVERRIDE),
    RABBIT_HUTCHES = Key('bunnymen', Rarities, OVERRIDE),
    ROCK_LOBSTERS = Key('rocky', Rarities, OVERRIDE),
    SLURPERS = Key('slurper', Rarities, OVERRIDE),
    SLURTLE_MOUNDS = Key('slurtles', Rarities, OVERRIDE),
    SPLUMONKEY_PODS = Key('monkey', Rarities, OVERRIDE),
    BEE_HIVES = Key('bees', Rarities, OVERRIDE),
    BEEFALOS = Key('beefalo', Rarities, OVERRIDE),
    BUZZARDS = Key('buzzard', Rarities, OVERRIDE),
    CARRATS = Key('moon_carrot', Rarities, OVERRIDE),
    HOLLOW_STUMP = Key('catcoon', Rarities, OVERRIDE),
    MOLE_BORROWS = Key('moles', Rarities, OVERRIDE),
    PIG_HOUSE = Key('pigs', Rarities, OVERRIDE),
    RABBIT_HOLES = Key('rabbits', Rarities, OVERRIDE),
    SALADMANDER = Key('moon_fruitdragon', Rarities, OVERRIDE),
    SHOALS = Key('ocean_shoal', Rarities, OVERRIDE),
    VOLT_GOATS = Key('lightninggoat', Rarities, OVERRIDE),
    WOBSTER_MOUNDS = Key('ocean_wobsterden', Rarities, OVERRIDE),
    BATS = Key('bats', Rarities, OVERRIDE),
    CAVE_WORMS = Key('worms', Rarities, OVERRIDE),
    CLOCKWORKS = Key('chess', Rarities, OVERRIDE),
    NIGHTMARE_FISSURES = Key('fissure', Rarities, OVERRIDE),
    SPIDER_DENS = Key('spiders', Rarities, OVERRIDE),
    SPILAGMITES = Key('cave_spiders', Rarities, OVERRIDE),
    TENTACLES = Key('tentacles', Rarities, OVERRIDE),
    HOUND_MOUNDS = Key('houndmound', Rarities, OVERRIDE),
    KILLER_BEE_HIVES = Key('angrybees', Rarities, OVERRIDE),
    LEAKY_SHACK = Key('merm', Rarities, OVERRIDE),
    MACTUSK_CAMPS = Key('walrus', Rarities, OVERRIDE),
    SEA_WEEDS = Key('ocean_waterplant', SeaRarities, OVERRIDE),
    SHATTERED_SPIDER_HOLES = Key('moon_spiders', Rarities, OVERRIDE),
    TALLBIRDS = Key('tallbirds', Rarities, OVERRIDE),


class Settings(Enum):
    MIDSUMMER_CAWNIVAL = Key('crow_carnival', Events, OVERRIDE),
    HALLOWED_NIGHT = Key('hallowed_nights', Events, OVERRIDE),
    WINTER_FEAST= Key('winters_feast', Events, OVERRIDE),
    YEAR_OF_THE_GOBBLER= Key('year_of_the_gobbler', Events, OVERRIDE),
    YEAR_OF_THE_VARG= Key('year_of_the_varg', Events, OVERRIDE),
    YEAR_OF_THE_PIG = Key('year_of_the_pig', Events, OVERRIDE),
    YEAR_OF_THE_CARRAT= Key('year_of_the_carrat', Events, OVERRIDE),
    YEAR_OF_THE_BEEFFALO= Key('year_of_the_beefalo', Events, OVERRIDE),
    YEAR_OF_THE_CATCOON= Key('year_of_the_catcoon', Events, OVERRIDE),
    SPE_EVENT = Key('specialevent', SpeEvents, OVERRIDE),
    AUTUMN= Key('autumn', SeasonDuration, OVERRIDE),
    WINTER= Key('winter', SeasonDuration, OVERRIDE),
    SPRING = Key('spring', SeasonDuration, OVERRIDE),
    SUMMER= Key('summer', SeasonDuration, OVERRIDE),
    DAY_TYPE= Key('day', Day, OVERRIDE),
    REGROWTH_MULTIPLIER = Key('regrowth', Speed, OVERRIDE),
    BIRCHNUT_TREE = Key('deciduoustree_regrowth', Speed, OVERRIDE),
    CARROTS = Key('carrots_regrowth', Speed, OVERRIDE),
    EVERGREENS = Key('evergreen_regrowth', Speed, OVERRIDE),
    FLOWERS = Key('flowers_regrowth', Speed, OVERRIDE),
    LUNE_TREES = Key('moon_tree_regrowth', Speed, OVERRIDE),
    SALT_FORMATIONS = Key('saltstack_regrowth', Speed, OVERRIDE),
    TWIGGY_TREES = Key('twiggytrees_regrowth', Speed, OVERRIDE),
    LIGHT_FLOWER = Key( 'flower_cave_regrowth', Speed, OVERRIDE),
    LIGHTBUG_FLOWER = Key('lightflier_flower_regrowth', Speed, OVERRIDE),
    LUNAR_MUSHTREES = Key('mushtree_moon_regrowth', Speed, OVERRIDE),
    MUSHROOM_TREES = Key('mushtree_regrowth', Speed, OVERRIDE),
    EXTRA_ITEMS = Key('extrastartingitems', ExtraItem, OVERRIDE),
    SEASON_ITEM = Key('seasonalstartingitems', NeverDefault, OVERRIDE),
    PROTECT = Key('spawnprotection', DefaultAlways, OVERRIDE),
    DROP = Key('dropeverythingondespawn', DefaultAlways, OVERRIDE),
    HOUNDS = Key('hounds', Frequency, OVERRIDE),
    WINTER_HOUNDS = Key('winterhounds', NeverDefault, OVERRIDE),
    SUMMER_HOUNDS = Key('summerhounds', NeverDefault, OVERRIDE),
    WORM_ATTACKS = Key('wormattacks', Frequency, OVERRIDE),
    ENLIGHTENMENT_MONSTERS = Key('brightmarecreatures', Frequency, OVERRIDE),
    SANITY_MONSTERS= Key('shadowcreatures', Frequency, OVERRIDE),
    BEEFALO_MATING_FREQUENCY = Key('beefaloheat', Frequency, OVERRIDE),
    ANCIENT_GATEWAY = Key('atriumgate', Frequency, OVERRIDE),
    EARTHQUAKES= Key('earthquakes', Frequency, OVERRIDE),
    RAIN = Key('weather', Frequency, OVERRIDE),
    KRAMPII = Key('krampus', Frequency, OVERRIDE),
    PERTIFICATION= Key('petrification', Quantities, OVERRIDE),
    FROG_RAIN= Key('frograin', Frequency, OVERRIDE),
    HUNT_SURPRISES= Key('alternatehunt', Frequency, OVERRIDE),
    HUNT = Key('hunt', Frequency, OVERRIDE),
    LIGHTNING= Key('lightning', Frequency, OVERRIDE),
    METEOR_FREQUENCY = Key('meteorshowers', Frequency, OVERRIDE),
    WILDFIRES= Key('wildfires', Frequency, OVERRIDE),
    BEES = Key('bees_setting', Frequency, OVERRIDE),
    BULBOUS_LIGHTBUGS= Key('lightfliers', Frequency, OVERRIDE),
    BUNNYMEN = Key('bunnymen_setting', Frequency, OVERRIDE),
    BUTTERFLIES = Key('butterfly',Frequency, OVERRIDE),
    DUST_MOTHS = Key('dustmoths', Frequency, OVERRIDE),
    GRASS_GEKKO_MORPHING = Key('grassgekkos', Frequency, OVERRIDE),
    MOLES = Key('moles_setting', Frequency, OVERRIDE),
    MUSH_GNOMES = Key('mushgnome', Frequency, OVERRIDE),
    PIGS = Key('pigs_setting', Frequency, OVERRIDE),
    ROCK_LOBSTERS = Key('rocky_setting', Frequency, OVERRIDE),
    SLURTLES = Key('slurtles_setting', Frequency, OVERRIDE),
    SNURTLES = Key('snurtles', Frequency, OVERRIDE),
    SPLUMONKEYS = Key('monkey_setting', Frequency, OVERRIDE),
    CATCOONS = Key('catcoons',Frequency, OVERRIDE),
    BIRDS = Key('birds', Frequency, OVERRIDE),
    GNARWAILS = Key('gnarwail', Frequency, OVERRIDE),
    GOBBLERS = Key('perd', Frequency, OVERRIDE),
    PENGULLS = Key('penguins', Frequency, OVERRIDE),
    RABBITS = Key('rabbits_setting', Frequency, OVERRIDE),
    WOBSTERS = Key('wobsters', Frequency, OVERRIDE),
    SCHOOLS_OF_FISH = Key('fishschools', Frequency, OVERRIDE),
    BATS = Key('bats_setting', Frequency, OVERRIDE),
    CAVE_SPIDERS = Key('spider_hider', Frequency, OVERRIDE),
    DANGLING_DEPTH_DWELLERS = Key('spider_dropper', Frequency, OVERRIDE),
    MERMS = Key('merms', Frequency, OVERRIDE),
    NAKED_MOLE_BATS = Key('molebats', Frequency, OVERRIDE),
    RUINS_NIGHTMARES = Key('nightmarecreatures', Frequency, OVERRIDE),
    SPIDER_WARRIORS = Key('spider_warriors', Frequency, OVERRIDE),
    SPIDERS = Key('spiders_setting', Frequency, OVERRIDE),
    SPITTER_SPIDERS = Key('spider_spitter', Frequency, OVERRIDE),
    COOKIE_CUTTERS = Key('cookiecutters', Frequency, OVERRIDE),
    FROGS = Key('frogs', Frequency, OVERRIDE),
    HORROR_HOUNDS = Key('mutated_hounds', Frequency, OVERRIDE),
    HOUNDS_MOUNDS = Key('hound_mounds', Frequency, OVERRIDE),
    KILLER_BEES = Key('wasps', Frequency, OVERRIDE),
    LUREPLANTS = Key('lureplants', Frequency, OVERRIDE),
    MACKTUSK = Key('walrus_setting', Frequency, OVERRIDE),
    MOONROCK_PENGULLS = Key('penguins_moon', Frequency, OVERRIDE),
    MOSQUITOS = Key('mosquitos', Frequency, OVERRIDE),
    SHARKS = Key('sharks', Frequency, OVERRIDE),
    SHATTERED_SPIDERS = Key('moon_spider', Frequency, OVERRIDE),
    SKITTERSQUIDS = Key('squid', Frequency, OVERRIDE),
    LORD_OF_THE_FRUIT_FLIES = Key('fruitfly',Frequency, OVERRIDE),
    SPIDER_QUEEN = Key('spiderqueen',Frequency, OVERRIDE),
    TOADSTOOL = Key('toadstool',Frequency, OVERRIDE),
    TREEGUARDS = Key('liefs',Frequency, OVERRIDE),
    ANTLION_TRIBUTE = Key('antliontribute',Frequency, OVERRIDE),
    BEARGER = Key('bearger',Frequency, OVERRIDE),
    BEEQUEEN = Key('beequeen',Frequency, OVERRIDE),
    CRABKING = Key('crabking',Frequency, OVERRIDE),
    DEERCLOPS = Key('deerclops',Frequency, OVERRIDE),
    DRAGONFLY = Key('dragonfly',Frequency, OVERRIDE),
    EYE_OF_TERROR = Key('eyeofterror',Frequency, OVERRIDE),
    KLAUS = Key('klaus',Frequency, OVERRIDE),
    MALBATROSS = Key('malbatross',Frequency, OVERRIDE),
    MEESE_GEESE = Key('goosemoose',Frequency, OVERRIDE),
    POISON_BIRCHNUT_TREES = Key('deciduousmonster', Frequency, OVERRIDE),


class WorldGen:
    def __init__(self, cluster_name: Union[str, None] = None, is_master:bool = True):
        if cluster_name is None:
            self.__dict = {}
        else:
            path = constant.CLUSTER_DIRECTORY / cluster_name
            if is_master:
                path = path / constant.MASTER_NAME_DIR
            else:
                path = path / constant.CAVE_NAME_DIR
            path = path / 'worldgenoverride.lua'
            if not ssh.is_exist(path):
                return
            content = ssh.get_file_content(path)

            if content is None:
                raise RuntimeError('The file {} don\'t exsite'.format(path))
            self.__dict = slpp.slpp.decode(content)

    def __update_override_enabled(self):
        keys = list(self.__dict.keys())
        if not len(keys):
            return

        name = Global.OVERRIDE.value[0].name
        if len(keys) == 1 and keys[0] == name:
            self.__dict.popitem()
            return

        if not keys.count(name):
            self.__dict[name] = True



    def add_or_update(self, key, value) -> None:
        data = key.value[0]

        if value == data.option.DEFAULT or value is None:
            self.remove(key)
            return

        if data.cat is None:
            self.__dict[data.name] = str(value)
        else:
            if data.cat != None and self.__dict.get(data.cat) is None:
                self.__dict.update({data.cat : {}})
            self.__dict[data.cat][data.name] = str(value)

        self.__update_override_enabled()
        
    def get(self, key):
        res = self.__dict.get(key.value[0].name)
        if res is None:
            return key.value[0].options.Default
        return key.value[0].options(res)

    def is_empty(self) -> bool:
        return not bool(self.__dict)

        
    def remove(self, key) -> None:
        data = key.value[0]
        if data.cat is None:
            self.__dict.pop(data.name)
        else:
            self.__dict[data.cat].pop(data.name)
            if not len(list(self.__dict[data.cat].keys())):
                self.__dict.pop(data.cat)

        self.__update_override_enabled()

    def rain(self) -> Frequency:
        return self.get(Settings.RAIN)

    def set_rain(self, rain: Frequency) -> None:
        self.add_or_update(Settings.RAIN, rain)

    def regrowth_multiplier(self) -> Speed:
        return self.get(Settings.REGROWTH_MULTIPLIER)

    def set_regrowth_multiplier(self, regrowth_multiplier: Speed) -> None:
        self.add_or_update(Settings.REGROWTH_MULTIPLIER, regrowth_multiplier)

    def bunnymen(self) -> Frequency:
        return self.get(Settings.BUNNYMEN)

    def set_bunnymen(self, bunnymen: Frequency) -> None:
        self.add_or_update(Settings.BUNNYMEN, bunnymen)

    def grass_gekko_morphing(self) -> Frequency:
        return self.get(Settings.GRASS_GEKKO_MORPHING)

    def set_grass_gekko_morphing(self, grass_gekko_morphing: Frequency) -> None:
        self.add_or_update(Settings.GRASS_GEKKO_MORPHING, grass_gekko_morphing)

    def moles(self) -> Frequency:
        return self.get(Settings.MOLES)

    def set_moles(self, moles: Frequency) -> None:
        self.add_or_update(Settings.MOLES, moles)

    def mush_gnomes(self) -> Frequency:
        return self.get(Settings.MUSH_GNOMES)

    def set_mush_gnomes(self, mush_gnomes: Frequency) -> None:
        self.add_or_update(Settings.MUSH_GNOMES, mush_gnomes)

    def pigs(self) -> Frequency:
        return self.get(Settings.PIGS)

    def set_pigs(self, pigs: Frequency) -> None:
        self.add_or_update(Settings.PIGS, pigs)

    def preset_generation(self) -> Preset:
        return self.get(Global.GENERATION_PRESET)

    def set_preset_generation(self, preset: Preset) -> None:
        self.add_or_update(Global.GENERATION_PRESET, preset)

    def preset_settings(self) -> Preset:
        return self.get(Global.SETTING_PRESET)

    def set_preset_settings(self, preset: Preset) -> None:
        self.add_or_update(Global.SETTING_PRESET, preset)

    def biomes(self) -> GenPreset:
        return self.get(Generation.BIOMES)

    def set_biomes(self, biomes: GenPreset) -> None:
        self.add_or_update(Generation.BIOMES, biomes)

    def merms(self) -> Frequency:
        return self.get(Settings.MERMS)

    def set_merms(self, merms: Frequency) -> None:
        self.add_or_update(Settings.MERMS, merms)

    def spider_warriors(self) -> Frequency:
        return self.get(Settings.SPIDER_WARRIORS)

    def set_spider_warriors(self, spider_warriors: Frequency) -> None:
        self.add_or_update(Settings.SPIDER_WARRIORS, spider_warriors)

    def spiders(self) -> Frequency:
        return self.get(Settings.SPIDERS)

    def set_spiders(self, spiders: Frequency) -> None:
        self.add_or_update(Settings.SPIDERS, spiders)

    def lord_of_the_fruit_flies(self) -> Frequency:
        return self.get(Settings.LORD_OF_THE_FRUIT_FLIES)

    def set_lord_of_the_fruit_flies(self, lord_of_the_fruit_flies: Frequency) -> None:
        self.add_or_update(Settings.LORD_OF_THE_FRUIT_FLIES, lord_of_the_fruit_flies)

    def spider_queen(self) -> Frequency:
        return self.get(Settings.SPIDER_QUEEN)

    def set_spider_queen(self, spider_queen: Frequency) -> None:
        self.add_or_update(Settings.SPIDER_QUEEN, spider_queen)

    def treeguards(self) -> Frequency:
        return self.get(Settings.TREEGUARDS)

    def set_treeguards(self, treeguards: Frequency) -> None:
        self.add_or_update(Settings.TREEGUARDS, treeguards)

    def world_size(self) -> Size:
        return self.get(Generation.WORLD_SIZE)

    def set_world_size(self, world_size: Size) -> None:
        self.add_or_update(Generation.WORLD_SIZE, world_size)

    def branches(self) -> Branching:
        return self.get(Generation.BRANCHES)

    def set_branches(self, branches: Branching) -> None:
        self.add_or_update(Generation.BRANCHES, branches)

    def loops(self) -> NeDefAl:
        return self.get(Generation.LOOPS)

    def set_loops(self, loops: NeDefAl) -> None:
        self.add_or_update(Generation.LOOPS, loops)

    def spawn_area(self) -> StartingLocation:
        return self.get(Generation.SPAWN_AREA)

    def set_spawn_area(self, spawn_area: StartingLocation) -> None:
        self.add_or_update(Generation.SPAWN_AREA, spawn_area)

    def touch_stones(self) -> Rarities:
        return self.get(Generation.TOUCH_STONES)

    def set_touch_stones(self, touch_stones: Rarities) -> None:
        self.add_or_update(Generation.TOUCH_STONES, touch_stones)

    def failed_survivors(self) -> Rarities:
        return self.get(Generation.FAILED_SURVIVORS)

    def set_failed_survivors(self, failed_survivors: Rarities) -> None:
        self.add_or_update(Generation.FAILED_SURVIVORS, failed_survivors)

    def starting_ressource_variety(self) -> StartingItem:
        return self.get(Generation.STARTING_RESSOURCE_VARIETY)

    def set_starting_ressource_variety(self, starting_ressource_variety: StartingItem) -> None:
        self.add_or_update(Generation.STARTING_RESSOURCE_VARIETY, starting_ressource_variety)

    def berry_bushes(self) -> Rarities:
        return self.get(Generation.BERRY_BUSHES)

    def set_berry_bushes(self, berry_bushes: Rarities) -> None:
        self.add_or_update(Generation.BERRY_BUSHES, berry_bushes)

    def boulders(self) -> Rarities:
        return self.get(Generation.BOULDERS)

    def set_boulders(self, boulders: Rarities) -> None:
        self.add_or_update(Generation.BOULDERS, boulders)

    def flint(self) -> Rarities:
        return self.get(Generation.FLINT)

    def set_flint(self, flint: Rarities) -> None:
        self.add_or_update(Generation.FLINT, flint)

    def grass(self) -> Rarities:
        return self.get(Generation.GRASS)

    def set_grass(self, grass: Rarities) -> None:
        self.add_or_update(Generation.GRASS, grass)

    def mushrooms(self) -> Rarities:
        return self.get(Generation.MUSHROOMS)

    def set_mushrooms(self, mushrooms: Rarities) -> None:
        self.add_or_update(Generation.MUSHROOMS, mushrooms)

    def reeds(self) -> Rarities:
        return self.get(Generation.REEDS)

    def set_reeds(self, reeds: Rarities) -> None:
        self.add_or_update(Generation.REEDS, reeds)

    def saplings(self) -> Rarities:
        return self.get(Generation.SAPLINGS)

    def set_saplings(self, saplings: Rarities) -> None:
        self.add_or_update(Generation.SAPLINGS, saplings)

    def spiky_bushes(self) -> Rarities:
        return self.get(Generation.SPIKY_BUSHES)

    def set_spiky_bushes(self, spiky_bushes: Rarities) -> None:
        self.add_or_update(Generation.SPIKY_BUSHES, spiky_bushes)

    def trees(self) -> Rarities:
        return self.get(Generation.TREES)

    def set_trees(self, trees: Rarities) -> None:
        self.add_or_update(Generation.TREES, trees)

    def clockworks(self) -> Rarities:
        return self.get(Generation.CLOCKWORKS)

    def set_clockworks(self, clockworks: Rarities) -> None:
        self.add_or_update(Generation.CLOCKWORKS, clockworks)

    def spider_dens(self) -> Rarities:
        return self.get(Generation.SPIDER_DENS)

    def set_spider_dens(self, spider_dens: Rarities) -> None:
        self.add_or_update(Generation.SPIDER_DENS, spider_dens)

    def __str__(self):
        return 'return ' + str(slpp.slpp.encode(self.__dict))


class Overworld(WorldGen):
    def __init__(self, cluster_name: Union[str, None] = None, is_master:bool = True):
        super().__init__(cluster_name, is_master)

    def starting_season(self) -> Season:
        return self.get(Generation.STARTING_SEASON)

    def set_starting_season(self, starting_season: Season) -> None:
        self.add_or_update(Generation.STARTING_SEASON, starting_season)

    def roads(self) -> NeverDefault:
        return self.get(Generation.ROADS)

    def set_roads(self, roads: NeverDefault) -> None:
        self.add_or_update(Generation.ROADS, roads)

    def celestial_fissures(self) -> Rarities:
        return self.get(Generation.CELESTIAL_FISSURES)

    def set_celestial_fissures(self, celestial_fissures: Rarities) -> None:
        self.add_or_update(Generation.CELESTIAL_FISSURES, celestial_fissures)

    def terrauim(self) -> NeverDefault:
        return self.get(Generation.TERRAUIM)

    def set_terrauim(self, terrauim: NeverDefault) -> None:
        self.add_or_update(Generation.TERRAUIM, terrauim)

    def anenemies(self) -> Rarities:
        return self.get(Generation.ANENEMIES)

    def set_anenemies(self, anenemies: Rarities) -> None:
        self.add_or_update(Generation.ANENEMIES, anenemies)

    def beached_bull_kelp(self) -> Rarities:
        return self.get(Generation.BEACHED_BULL_KELP)

    def set_beached_bull_kelp(self, beached_bull_kelp: Rarities) -> None:
        self.add_or_update(Generation.BEACHED_BULL_KELP, beached_bull_kelp)

    def bull_kelp(self) -> Rarities:
        return self.get(Generation.BULL_KELP)

    def set_bull_kelp(self, bull_kelp: Rarities) -> None:
        self.add_or_update(Generation.BULL_KELP, bull_kelp)

    def cacti(self) -> Rarities:
        return self.get(Generation.CACTI)

    def set_cacti(self, cacti: Rarities) -> None:
        self.add_or_update(Generation.CACTI, cacti)

    def carrots(self) -> Rarities:
        return self.get(Generation.CARROTS)

    def set_carrots(self, carrots: Rarities) -> None:
        self.add_or_update(Generation.CARROTS, carrots)

    def flowers(self) -> Rarities:
        return self.get(Generation.FLOWERS)

    def set_flowers(self, flowers: Rarities) -> None:
        self.add_or_update(Generation.FLOWERS, flowers)

    def hot_springs(self) -> Rarities:
        return self.get(Generation.HOT_SPRINGS)

    def set_hot_springs(self, hot_springs: Rarities) -> None:
        self.add_or_update(Generation.HOT_SPRINGS, hot_springs)

    def lunar_rocks(self) -> Rarities:
        return self.get(Generation.LUNAR_ROCKS)

    def set_lunar_rocks(self, lunar_rocks: Rarities) -> None:
        self.add_or_update(Generation.LUNAR_ROCKS, lunar_rocks)

    def lunar_saplings(self) -> Rarities:
        return self.get(Generation.LUNAR_SAPLINGS)

    def set_lunar_saplings(self, lunar_saplings: Rarities) -> None:
        self.add_or_update(Generation.LUNAR_SAPLINGS, lunar_saplings)

    def lune_trees(self) -> Rarities:
        return self.get(Generation.LUNE_TREES)

    def set_lune_trees(self, lune_trees: Rarities) -> None:
        self.add_or_update(Generation.LUNE_TREES, lune_trees)

    def meteor_fields(self) -> Rarities:
        return self.get(Generation.METEOR_FIELDS)

    def set_meteor_fields(self, meteor_fields: Rarities) -> None:
        self.add_or_update(Generation.METEOR_FIELDS, meteor_fields)

    def mini_glaciers(self) -> Rarities:
        return self.get(Generation.MINI_GLACIERS)

    def set_mini_glaciers(self, mini_glaciers: Rarities) -> None:
        self.add_or_update(Generation.MINI_GLACIERS, mini_glaciers)

    def ponds(self) -> Rarities:
        return self.get(Generation.PONDS)

    def set_ponds(self, ponds: Rarities) -> None:
        self.add_or_update(Generation.PONDS, ponds)

    def sea_stacks(self) -> SeaRarities:
        return self.get(Generation.SEA_STACKS)

    def set_sea_stacks(self, sea_stacks: SeaRarities) -> None:
        self.add_or_update(Generation.SEA_STACKS, sea_stacks)

    def stone_fruit_bushes(self) -> Rarities:
        return self.get(Generation.STONE_FRUIT_BUSHES)

    def set_stone_fruit_bushes(self, stone_fruit_bushes: Rarities) -> None:
        self.add_or_update(Generation.STONE_FRUIT_BUSHES, stone_fruit_bushes)

    def tumbleweeds(self) -> Rarities:
        return self.get(Generation.TUMBLEWEEDS)

    def set_tumbleweeds(self, tumbleweeds: Rarities) -> None:
        self.add_or_update(Generation.TUMBLEWEEDS, tumbleweeds)

    def bee_hives(self) -> Rarities:
        return self.get(Generation.BEE_HIVES)

    def set_bee_hives(self, bee_hives: Rarities) -> None:
        self.add_or_update(Generation.BEE_HIVES, bee_hives)

    def beefalos(self) -> Rarities:
        return self.get(Generation.BEEFALOS)

    def set_beefalos(self, beefalos: Rarities) -> None:
        self.add_or_update(Generation.BEEFALOS, beefalos)

    def buzzards(self) -> Rarities:
        return self.get(Generation.BUZZARDS)

    def set_buzzards(self, buzzards: Rarities) -> None:
        self.add_or_update(Generation.BUZZARDS, buzzards)

    def carrats(self) -> Rarities:
        return self.get(Generation.CARRATS)

    def set_carrats(self, carrats: Rarities) -> None:
        self.add_or_update(Generation.CARRATS, carrats)

    def hollow_stump(self) -> Rarities:
        return self.get(Generation.HOLLOW_STUMP)

    def set_hollow_stump(self, hollow_stump: Rarities) -> None:
        self.add_or_update(Generation.HOLLOW_STUMP, hollow_stump)

    def mole_borrows(self) -> Rarities:
        return self.get(Generation.MOLE_BORROWS)

    def set_mole_borrows(self, mole_borrows: Rarities) -> None:
        self.add_or_update(Generation.MOLE_BORROWS, mole_borrows)

    def pig_house(self) -> Rarities:
        return self.get(Generation.PIG_HOUSE)

    def set_pig_house(self, pig_house: Rarities) -> None:
        self.add_or_update(Generation.PIG_HOUSE, pig_house)

    def rabbit_holes(self) -> Rarities:
        return self.get(Generation.RABBIT_HOLES)

    def set_rabbit_holes(self, rabbit_holes: Rarities) -> None:
        self.add_or_update(Generation.RABBIT_HOLES, rabbit_holes)

    def saladmander(self) -> Rarities:
        return self.get(Generation.SALADMANDER)

    def set_saladmander(self, saladmander: Rarities) -> None:
        self.add_or_update(Generation.SALADMANDER, saladmander)

    def shoals(self) -> Rarities:
        return self.get(Generation.SHOALS)

    def set_shoals(self, shoals: Rarities) -> None:
        self.add_or_update(Generation.SHOALS, shoals)

    def volt_goats(self) -> Rarities:
        return self.get(Generation.VOLT_GOATS)

    def set_volt_goats(self, volt_goats: Rarities) -> None:
        self.add_or_update(Generation.VOLT_GOATS, volt_goats)

    def wobster_mounds(self) -> Rarities:
        return self.get(Generation.WOBSTER_MOUNDS)

    def set_wobster_mounds(self, wobster_mounds: Rarities) -> None:
        self.add_or_update(Generation.WOBSTER_MOUNDS, wobster_mounds)

    def hound_mounds(self) -> Rarities:
        return self.get(Generation.HOUND_MOUNDS)

    def set_hound_mounds(self, hound_mounds: Rarities) -> None:
        self.add_or_update(Generation.HOUND_MOUNDS, hound_mounds)

    def killer_bee_hives(self) -> Rarities:
        return self.get(Generation.KILLER_BEE_HIVES)

    def set_killer_bee_hives(self, killer_bee_hives: Rarities) -> None:
        self.add_or_update(Generation.KILLER_BEE_HIVES, killer_bee_hives)

    def leaky_shack(self) -> Rarities:
        return self.get(Generation.LEAKY_SHACK)

    def set_leaky_shack(self, leaky_shack: Rarities) -> None:
        self.add_or_update(Generation.LEAKY_SHACK, leaky_shack)

    def mactusk_camps(self) -> Rarities:
        return self.get(Generation.MACTUSK_CAMPS)

    def set_mactusk_camps(self, mactusk_camps: Rarities) -> None:
        self.add_or_update(Generation.MACTUSK_CAMPS, mactusk_camps)

    def sea_weeds(self) -> SeaRarities:
        return self.get(Generation.SEA_WEEDS)

    def set_sea_weeds(self, sea_weeds: SeaRarities) -> None:
        self.add_or_update(Generation.SEA_WEEDS, sea_weeds)

    def shattered_spider_holes(self) -> Rarities:
        return self.get(Generation.SHATTERED_SPIDER_HOLES)

    def set_shattered_spider_holes(self, shattered_spider_holes: Rarities) -> None:
        self.add_or_update(Generation.SHATTERED_SPIDER_HOLES, shattered_spider_holes)

    def tallbirds(self) -> Rarities:
        return self.get(Generation.TALLBIRDS)

    def set_tallbirds(self, tallbirds: Rarities) -> None:
        self.add_or_update(Generation.TALLBIRDS, tallbirds)

    def midsummer_cawnival(self) -> Events:
        return self.get(Settings.MIDSUMMER_CAWNIVAL)

    def set_midsummer_cawnival(self, midsummer_cawnival: Events) -> None:
        self.add_or_update(Settings.MIDSUMMER_CAWNIVAL, midsummer_cawnival)

    def hallowed_night(self) -> Events:
        return self.get(Settings.HALLOWED_NIGHT)

    def set_hallowed_night(self, hallowed_night: Events) -> None:
        self.add_or_update(Settings.HALLOWED_NIGHT, hallowed_night)

    def winter_feast(self) -> Events:
        return self.get(Settings.WINTER_FEAST)

    def set_winter_feast(self, winter_feast: Events) -> None:
        self.add_or_update(Settings.WINTER_FEAST, winter_feast)

    def year_of_the_gobbler(self) -> Events:
        return self.get(Settings.YEAR_OF_THE_GOBBLER)

    def set_year_of_the_gobbler(self, year_of_the_gobbler: Events) -> None:
        self.add_or_update(Settings.YEAR_OF_THE_GOBBLER, year_of_the_gobbler)

    def year_of_the_varg(self) -> Events:
        return self.get(Settings.YEAR_OF_THE_VARG)

    def set_year_of_the_varg(self, year_of_the_varg: Events) -> None:
        self.add_or_update(Settings.YEAR_OF_THE_VARG, year_of_the_varg)

    def year_of_the_pig(self) -> Events:
        return self.get(Settings.YEAR_OF_THE_PIG)

    def set_year_of_the_pig(self, year_of_the_pig: Events) -> None:
        self.add_or_update(Settings.YEAR_OF_THE_PIG, year_of_the_pig)

    def year_of_the_carrat(self) -> Events:
        return self.get(Settings.YEAR_OF_THE_CARRAT)

    def set_year_of_the_carrat(self, year_of_the_carrat: Events) -> None:
        self.add_or_update(Settings.YEAR_OF_THE_CARRAT, year_of_the_carrat)

    def year_of_the_beeffalo(self) -> Events:
        return self.get(Settings.YEAR_OF_THE_BEEFFALO)

    def set_year_of_the_beeffalo(self, year_of_the_beeffalo: Events) -> None:
        self.add_or_update(Settings.YEAR_OF_THE_BEEFFALO, year_of_the_beeffalo)

    def year_of_the_catcoon(self) -> Events:
        return self.get(Settings.YEAR_OF_THE_CATCOON)

    def set_year_of_the_catcoon(self, year_of_the_catcoon: Events) -> None:
        self.add_or_update(Settings.YEAR_OF_THE_CATCOON, year_of_the_catcoon)

    def spe_event(self) -> SpeEvents:
        return self.get(Settings.SPE_EVENT)

    def set_spe_event(self, spe_event: SpeEvents) -> None:
        self.add_or_update(Settings.SPE_EVENT, spe_event)

    def autumn(self) -> SeasonDuration:
        return self.get(Settings.AUTUMN)

    def set_autumn(self, autumn: SeasonDuration) -> None:
        self.add_or_update(Settings.AUTUMN, autumn)

    def winter(self) -> SeasonDuration:
        return self.get(Settings.WINTER)

    def set_winter(self, winter: SeasonDuration) -> None:
        self.add_or_update(Settings.WINTER, winter)

    def spring(self) -> SeasonDuration:
        return self.get(Settings.SPRING)

    def set_spring(self, spring: SeasonDuration) -> None:
        self.add_or_update(Settings.SPRING, spring)

    def summer(self) -> SeasonDuration:
        return self.get(Settings.SUMMER)

    def set_summer(self, summer: SeasonDuration) -> None:
        self.add_or_update(Settings.SUMMER, summer)

    def day_type(self) -> Day:
        return self.get(Settings.DAY_TYPE)

    def set_day_type(self, day_type: Day) -> None:
        self.add_or_update(Settings.DAY_TYPE, day_type)

    def birchnut_tree(self) -> Speed:
        return self.get(Settings.BIRCHNUT_TREE)

    def set_birchnut_tree(self, birchnut_tree: Speed) -> None:
        self.add_or_update(Settings.BIRCHNUT_TREE, birchnut_tree)

    def carrots_grow(self) -> Speed:
        return self.get(Settings.CARROTS)

    def set_carrots_grow(self, carrots: Speed) -> None:
        self.add_or_update(Settings.CARROTS, carrots)

    def evergreens(self) -> Speed:
        return self.get(Settings.EVERGREENS)

    def set_evergreens(self, evergreens: Speed) -> None:
        self.add_or_update(Settings.EVERGREENS, evergreens)

    def flowers_grow(self) -> Speed:
        return self.get(Settings.FLOWERS)

    def set_flowers_regrow(self, flowers: Speed) -> None:
        self.add_or_update(Settings.FLOWERS, flowers)

    def lune_trees_grow(self) -> Speed:
        return self.get(Settings.LUNE_TREES)

    def set_lune_trees_grow(self, lune_trees: Speed) -> None:
        self.add_or_update(Settings.LUNE_TREES, lune_trees)

    def salt_formations(self) -> Speed:
        return self.get(Settings.SALT_FORMATIONS)

    def set_salt_formations(self, salt_formations: Speed) -> None:
        self.add_or_update(Settings.SALT_FORMATIONS, salt_formations)

    def twiggy_trees(self) -> Speed:
        return self.get(Settings.TWIGGY_TREES)

    def set_twiggy_trees(self, twiggy_trees: Speed) -> None:
        self.add_or_update(Settings.TWIGGY_TREES, twiggy_trees)

    def extra_items(self) -> ExtraItem:
        return self.get(Settings.EXTRA_ITEMS)

    def set_extra_items(self, extra_items: ExtraItem) -> None:
        self.add_or_update(Settings.EXTRA_ITEMS, extra_items)

    def season_item(self) -> NeverDefault:
        return self.get(Settings.SEASON_ITEM)

    def set_season_item(self, season_item: NeverDefault) -> None:
        self.add_or_update(Settings.SEASON_ITEM, season_item)

    def protect(self) -> DefaultAlways:
        return self.get(Settings.PROTECT)

    def set_protect(self, protect: DefaultAlways) -> None:
        self.add_or_update(Settings.PROTECT, protect)

    def drop(self) -> DefaultAlways:
        return self.get(Settings.DROP)

    def set_drop(self, drop: DefaultAlways) -> None:
        self.add_or_update(Settings.DROP, drop)

    def hounds(self) -> Frequency:
        return self.get(Settings.HOUNDS)

    def set_hounds(self, hounds: Frequency) -> None:
        self.add_or_update(Settings.HOUNDS, hounds)

    def winter_hounds(self) -> NeverDefault:
        return self.get(Settings.WINTER_HOUNDS)

    def set_winter_hounds(self, winter_hounds: NeverDefault) -> None:
        self.add_or_update(Settings.WINTER_HOUNDS, winter_hounds)

    def summer_hounds(self) -> NeverDefault:
        return self.get(Settings.SUMMER_HOUNDS)

    def set_summer_hounds(self, summer_hounds: NeverDefault) -> None:
        self.add_or_update(Settings.SUMMER_HOUNDS, summer_hounds)

    def worm_attacks(self) -> Frequency:
        return self.get(Settings.WORM_ATTACKS)

    def set_worm_attacks(self, worm_attacks: Frequency) -> None:
        self.add_or_update(Settings.WORM_ATTACKS, worm_attacks)

    def enlightenment_monsters(self) -> Frequency:
        return self.get(Settings.ENLIGHTENMENT_MONSTERS)

    def set_enlightenment_monsters(self, enlightenment_monsters: Frequency) -> None:
        self.add_or_update(Settings.ENLIGHTENMENT_MONSTERS, enlightenment_monsters)

    def sanity_monsters(self) -> Frequency:
        return self.get(Settings.SANITY_MONSTERS)

    def set_sanity_monsters(self, sanity_monsters: Frequency) -> None:
        self.add_or_update(Settings.SANITY_MONSTERS, sanity_monsters)

    def beefalo_mating_frequency(self) -> Frequency:
        return self.get(Settings.BEEFALO_MATING_FREQUENCY)

    def set_beefalo_mating_frequency(self, beefalo_mating_frequency: Frequency) -> None:
        self.add_or_update(Settings.BEEFALO_MATING_FREQUENCY, beefalo_mating_frequency)

    def krampii(self) -> Frequency:
        return self.get(Settings.KRAMPII)

    def set_krampii(self, krampii: Frequency) -> None:
        self.add_or_update(Settings.KRAMPII, krampii)

    def pertification(self) -> Quantities:
        return self.get(Settings.PERTIFICATION)

    def set_pertification(self, pertification: Quantities) -> None:
        self.add_or_update(Settings.PERTIFICATION, pertification)

    def frog_rain(self) -> Frequency:
        return self.get(Settings.FROG_RAIN)

    def set_frog_rain(self, frog_rain: Frequency) -> None:
        self.add_or_update(Settings.FROG_RAIN, frog_rain)

    def hunt_surprises(self) -> Frequency:
        return self.get(Settings.HUNT_SURPRISES)

    def set_hunt_surprises(self, hunt_surprises: Frequency) -> None:
        self.add_or_update(Settings.HUNT_SURPRISES, hunt_surprises)

    def hunt(self) -> Frequency:
        return self.get(Settings.HUNT)

    def set_hunt(self, hunt: Frequency) -> None:
        self.add_or_update(Settings.HUNT, hunt)

    def lightning(self) -> Frequency:
        return self.get(Settings.LIGHTNING)

    def set_lightning(self, lightning: Frequency) -> None:
        self.add_or_update(Settings.LIGHTNING, lightning)

    def meteor_frequency(self) -> Frequency:
        return self.get(Settings.METEOR_FREQUENCY)

    def set_meteor_frequency(self, meteor_frequency: Frequency) -> None:
        self.add_or_update(Settings.METEOR_FREQUENCY, meteor_frequency)

    def wildfires(self) -> Frequency:
        return self.get(Settings.WILDFIRES)

    def set_wildfires(self, wildfires: Frequency) -> None:
        self.add_or_update(Settings.WILDFIRES, wildfires)

    def bees(self) -> Frequency:
        return self.get(Settings.BEES)

    def set_bees(self, bees: Frequency) -> None:
        self.add_or_update(Settings.BEES, bees)

    def butterflies(self) -> Frequency:
        return self.get(Settings.BUTTERFLIES)

    def set_butterflies(self, butterflies: Frequency) -> None:
        self.add_or_update(Settings.BUTTERFLIES, butterflies)

    def catcoons(self) -> Frequency:
        return self.get(Settings.CATCOONS)

    def set_catcoons(self, catcoons: Frequency) -> None:
        self.add_or_update(Settings.CATCOONS, catcoons)

    def birds(self) -> Frequency:
        return self.get(Settings.BIRDS)

    def set_birds(self, birds: Frequency) -> None:
        self.add_or_update(Settings.BIRDS, birds)

    def gnarwails(self) -> Frequency:
        return self.get(Settings.GNARWAILS)

    def set_gnarwails(self, gnarwails: Frequency) -> None:
        self.add_or_update(Settings.GNARWAILS, gnarwails)

    def gobblers(self) -> Frequency:
        return self.get(Settings.GOBBLERS)

    def set_gobblers(self, gobblers: Frequency) -> None:
        self.add_or_update(Settings.GOBBLERS, gobblers)

    def pengulls(self) -> Frequency:
        return self.get(Settings.PENGULLS)

    def set_pengulls(self, pengulls: Frequency) -> None:
        self.add_or_update(Settings.PENGULLS, pengulls)

    def rabbits(self) -> Frequency:
        return self.get(Settings.RABBITS)

    def set_rabbits(self, rabbits: Frequency) -> None:
        self.add_or_update(Settings.RABBITS, rabbits)

    def wobsters(self) -> Frequency:
        return self.get(Settings.WOBSTERS)

    def set_wobsters(self, wobsters: Frequency) -> None:
        self.add_or_update(Settings.WOBSTERS, wobsters)

    def schools_of_fish(self) -> Frequency:
        return self.get(Settings.SCHOOLS_OF_FISH)

    def set_schools_of_fish(self, schools_of_fish: Frequency) -> None:
        self.add_or_update(Settings.SCHOOLS_OF_FISH, schools_of_fish)

    def cookie_cutters(self) -> Frequency:
        return self.get(Settings.COOKIE_CUTTERS)

    def set_cookie_cutters(self, cookie_cutters: Frequency) -> None:
        self.add_or_update(Settings.COOKIE_CUTTERS, cookie_cutters)

    def frogs(self) -> Frequency:
        return self.get(Settings.FROGS)

    def set_frogs(self, frogs: Frequency) -> None:
        self.add_or_update(Settings.FROGS, frogs)

    def horror_hounds(self) -> Frequency:
        return self.get(Settings.HORROR_HOUNDS)

    def set_horror_hounds(self, horror_hounds: Frequency) -> None:
        self.add_or_update(Settings.HORROR_HOUNDS, horror_hounds)

    def hounds_mounds(self) -> Frequency:
        return self.get(Settings.HOUNDS_MOUNDS)

    def set_hounds_mounds(self, hounds_mounds: Frequency) -> None:
        self.add_or_update(Settings.HOUNDS_MOUNDS, hounds_mounds)

    def killer_bees(self) -> Frequency:
        return self.get(Settings.KILLER_BEES)

    def set_killer_bees(self, killer_bees: Frequency) -> None:
        self.add_or_update(Settings.KILLER_BEES, killer_bees)

    def lureplants(self) -> Frequency:
        return self.get(Settings.LUREPLANTS)

    def set_lureplants(self, lureplants: Frequency) -> None:
        self.add_or_update(Settings.LUREPLANTS, lureplants)

    def macktusk(self) -> Frequency:
        return self.get(Settings.MACKTUSK)

    def set_macktusk(self, macktusk: Frequency) -> None:
        self.add_or_update(Settings.MACKTUSK, macktusk)

    def moonrock_pengulls(self) -> Frequency:
        return self.get(Settings.MOONROCK_PENGULLS)

    def set_moonrock_pengulls(self, moonrock_pengulls: Frequency) -> None:
        self.add_or_update(Settings.MOONROCK_PENGULLS, moonrock_pengulls)

    def mosquitos(self) -> Frequency:
        return self.get(Settings.MOSQUITOS)

    def set_mosquitos(self, mosquitos: Frequency) -> None:
        self.add_or_update(Settings.MOSQUITOS, mosquitos)

    def sharks(self) -> Frequency:
        return self.get(Settings.SHARKS)

    def set_sharks(self, sharks: Frequency) -> None:
        self.add_or_update(Settings.SHARKS, sharks)

    def shattered_spiders(self) -> Frequency:
        return self.get(Settings.SHATTERED_SPIDERS)

    def set_shattered_spiders(self, shattered_spiders: Frequency) -> None:
        self.add_or_update(Settings.SHATTERED_SPIDERS, shattered_spiders)

    def skittersquids(self) -> Frequency:
        return self.get(Settings.SKITTERSQUIDS)

    def set_skittersquids(self, skittersquids: Frequency) -> None:
        self.add_or_update(Settings.SKITTERSQUIDS, skittersquids)

    def antlion_tribute(self) -> Frequency:
        return self.get(Settings.ANTLION_TRIBUTE)

    def set_antlion_tribute(self, antlion_tribute: Frequency) -> None:
        self.add_or_update(Settings.ANTLION_TRIBUTE, antlion_tribute)

    def bearger(self) -> Frequency:
        return self.get(Settings.BEARGER)

    def set_bearger(self, bearger: Frequency) -> None:
        self.add_or_update(Settings.BEARGER, bearger)

    def beequeen(self) -> Frequency:
        return self.get(Settings.BEEQUEEN)

    def set_beequeen(self, beequeen: Frequency) -> None:
        self.add_or_update(Settings.BEEQUEEN, beequeen)

    def crabking(self) -> Frequency:
        return self.get(Settings.CRABKING)

    def set_crabking(self, crabking: Frequency) -> None:
        self.add_or_update(Settings.CRABKING, crabking)

    def deerclops(self) -> Frequency:
        return self.get(Settings.DEERCLOPS)

    def set_deerclops(self, deerclops: Frequency) -> None:
        self.add_or_update(Settings.DEERCLOPS, deerclops)

    def dragonfly(self) -> Frequency:
        return self.get(Settings.DRAGONFLY)

    def set_dragonfly(self, dragonfly: Frequency) -> None:
        self.add_or_update(Settings.DRAGONFLY, dragonfly)

    def eye_of_terror(self) -> Frequency:
        return self.get(Settings.EYE_OF_TERROR)

    def set_eye_of_terror(self, eye_of_terror: Frequency) -> None:
        self.add_or_update(Settings.EYE_OF_TERROR, eye_of_terror)

    def klaus(self) -> Frequency:
        return self.get(Settings.KLAUS)

    def set_klaus(self, klaus: Frequency) -> None:
        self.add_or_update(Settings.KLAUS, klaus)

    def malbatross(self) -> Frequency:
        return self.get(Settings.MALBATROSS)

    def set_malbatross(self, malbatross: Frequency) -> None:
        self.add_or_update(Settings.MALBATROSS, malbatross)

    def meese_geese(self) -> Frequency:
        return self.get(Settings.MEESE_GEESE)

    def set_meese_geese(self, meese_geese: Frequency) -> None:
        return self.add_or_update(Settings.MEESE_GEESE, meese_geese)

    def poison_birchnut_trees(self) -> Frequency:
        return self.get(Settings.POISON_BIRCHNUT_TREES)

    def set_poison_birchnut_trees(self, poison_birchnut_trees: Frequency) -> None:
        return self.add_or_update(Settings.POISON_BIRCHNUT_TREES, poison_birchnut_trees)

class Underworld(WorldGen):
    def __init__(self, cluster_name: Union[str, None] = None, is_master:bool = False):
        super().__init__(cluster_name, is_master)

    def ancient_gateway(self) -> Frequency:
        return self.get(Settings.ANCIENT_GATEWAY)

    def set_ancient_gateway(self, ancient_gateway: Frequency) -> None:
        self.add_or_update(Settings.ANCIENT_GATEWAY, ancient_gateway)

    def cave_worms(self) -> Rarities:
        return self.get(Generation.CAVE_WORMS)

    def set_cave_worms(self, cave_worms: Rarities) -> None:
        self.add_or_update(Generation.CAVE_WORMS, cave_worms)

    def earthquakes(self) -> Frequency:
        return self.get(Settings.EARTHQUAKES)

    def set_earthquakes(self, earthquakes: Frequency) -> None:
        self.add_or_update(Settings.EARTHQUAKES, earthquakes)

    def light_flowers(self) -> Rarities:
        return self.get(Generation.LIGHT_FLOWERS)

    def set_light_flowers(self, light_flowers: Rarities) -> None:
        self.add_or_update(Generation.LIGHT_FLOWERS, light_flowers)

    def lightbug_flower(self) -> Speed:
        return self.get(Settings.LIGHTBUG_FLOWER)

    def set_lightbug_flower(self, lightbug_flower: Speed) -> None:
        self.add_or_update(Settings.LIGHTBUG_FLOWER, lightbug_flower)

    def lunar_mushtrees(self) -> Speed:
        return self.get(Settings.LUNAR_MUSHTREES)

    def set_lunar_mushtrees(self, lunar_mushtrees: Speed) -> None:
        self.add_or_update(Settings.LUNAR_MUSHTREES, lunar_mushtrees)

    def mushroom_trees(self) -> Rarities:
        return self.get(Generation.MUSHROOM_TREES)

    def set_mushroom_trees(self, mushroom_trees: Rarities) -> None:
        self.add_or_update(Generation.MUSHROOM_TREES, mushroom_trees)

    def bulbous_lightbugs(self) -> Frequency:
        return self.get(Settings.BULBOUS_LIGHTBUGS)

    def set_bulbous_lightbugs(self, bulbous_lightbugs: Frequency) -> None:
        self.add_or_update(Settings.BULBOUS_LIGHTBUGS, bulbous_lightbugs)

    def dust_moths(self) -> Frequency:
        return self.get(Settings.DUST_MOTHS)

    def set_dust_moths(self, dust_moths: Frequency) -> None:
        self.add_or_update(Settings.DUST_MOTHS, dust_moths)

    def slurtles(self) -> Frequency:
        return self.get(Settings.SLURTLES)

    def set_slurtles(self, slurtles: Frequency) -> None:
        self.add_or_update(Settings.SLURTLES, slurtles)

    def snurtles(self) -> Frequency:
        return self.get(Settings.SNURTLES)

    def set_snurtles(self, snurtles: Frequency) -> None:
        self.add_or_update(Settings.SNURTLES, snurtles)

    def splumonkeys(self) -> Frequency:
        return self.get(Settings.SPLUMONKEYS)

    def set_splumonkeys(self, splumonkeys: Frequency) -> None:
        self.add_or_update(Settings.SPLUMONKEYS, splumonkeys)

    def rock_lobsters(self) -> Frequency:
        return self.get(Settings.ROCK_LOBSTERS)

    def set_rock_lobsters(self, rock_lobsters: Frequency) -> None:
        self.add_or_update(Settings.ROCK_LOBSTERS, rock_lobsters)

    def bats(self) -> Frequency:
        return self.get(Settings.BATS)

    def set_bats(self, bats: Frequency) -> None:
        self.add_or_update(Settings.BATS, bats)

    def cave_spiders(self) -> Frequency:
        return self.get(Settings.CAVE_SPIDERS)

    def set_cave_spiders(self, cave_spiders: Frequency) -> None:
        self.add_or_update(Settings.CAVE_SPIDERS, cave_spiders)

    def dangling_depth_dwellers(self) -> Frequency:
        return self.get(Settings.DANGLING_DEPTH_DWELLERS)

    def set_dangling_depth_dwellers(self, dangling_depth_dwellers: Frequency) -> None:
        self.add_or_update(Settings.DANGLING_DEPTH_DWELLERS, dangling_depth_dwellers)

    def naked_mole_bats(self) -> Frequency:
        return self.get(Settings.NAKED_MOLE_BATS)

    def set_naked_mole_bats(self, naked_mole_bats: Frequency) -> None:
        self.add_or_update(Settings.NAKED_MOLE_BATS, naked_mole_bats)

    def ruins_nightmares(self) -> Frequency:
        return self.get(Settings.RUINS_NIGHTMARES)

    def set_ruins_nightmares(self, ruins_nightmares: Frequency) -> None:
        self.add_or_update(Settings.RUINS_NIGHTMARES, ruins_nightmares)

    def spitter_spiders(self) -> Frequency:
        return self.get(Settings.SPITTER_SPIDERS)

    def set_spitter_spiders(self, spitter_spiders: Frequency) -> None:
        self.add_or_update(Settings.SPITTER_SPIDERS, spitter_spiders)

    def toadstool(self) -> Frequency:
        return self.get(Settings.TOADSTOOL)

    def set_toadstool(self, toadstool: Frequency) -> None:
        self.add_or_update(Settings.TOADSTOOL, toadstool)

    def sinkhole_lights(self) -> Speed:
        return self.get(Generation.SINKHOLE_LIGHTS)

    def set_sinkhole_lights(self, sinkhole_lights: Speed) -> None:
        self.add_or_update(Generation.SINKHOLE_LIGHTS, sinkhole_lights)

    def cave_bananas(self) -> Rarities:
        return self.get(Generation.CAVE_BANANAS)

    def set_cave_bananas(self, cave_bananas: Rarities) -> None:
        self.add_or_update(Generation.CAVE_BANANAS, cave_bananas)

    def cave_ferns(self) -> Rarities:
        return self.get(Generation.CAVE_FERNS)

    def set_cave_ferns(self, cave_ferns: Rarities) -> None:
        self.add_or_update(Generation.CAVE_FERNS, cave_ferns)

    def glow_berries(self) -> Rarities:
        return self.get(Generation.GLOW_BERRIES)

    def set_glow_berries(self, glow_berries: Rarities) -> None:
        self.add_or_update(Generation.GLOW_BERRIES, glow_berries)

    def lichen(self) -> Rarities:
        return self.get(Generation.LICHEN)

    def set_lichen(self, lichen: Rarities) -> None:
        self.add_or_update(Generation.LICHEN, lichen)

    def cave_ponds(self) -> Rarities:
        return self.get(Generation.CAVE_PONDS)

    def set_cave_ponds(self, cave_ponds: Rarities) -> None:
        self.add_or_update(Generation.CAVE_PONDS, cave_ponds)

    def light_flower(self) -> Speed:
        return self.get(Settings.LIGHT_FLOWER)

    def set_light_flower(self, light_flower: Speed) -> None:
        self.add_or_update(Settings.LIGHT_FLOWER, light_flower)

    def mushroom_trees_grow(self) -> Speed:
        return self.get(Settings.MUSHROOM_TREES)

    def set_mushroom_trees_grow(self, mushroom_trees_grow: Speed) -> None:
        self.add_or_update(Settings.MUSHROOM_TREES, mushroom_trees_grow)

    def rabbit_hutches(self) -> Rarities:
        return self.get(Generation.RABBIT_HUTCHES)

    def set_rabbit_hutches(self, rabbit_hutches: Rarities) -> None:
        self.add_or_update(Generation.RABBIT_HUTCHES, rabbit_hutches)

    def rock_lobsters_spawner(self) -> Rarities:
        return self.get(Generation.ROCK_LOBSTERS)

    def set_rock_lobsters_spawner(self, rock_lobsters: Rarities) -> None:
        self.add_or_update(Generation.ROCK_LOBSTERS, rock_lobsters)

    def slurpers(self) -> Rarities:
        return self.get(Generation.SLURPERS)

    def set_slurpers(self, slurpers: Rarities) -> None:
        self.add_or_update(Generation.SLURPERS, slurpers)

    def slurtle_mounds(self) -> Rarities:
        return self.get(Generation.SLURTLE_MOUNDS)

    def set_slurtle_mounds(self, slurtle_mounds: Rarities) -> None:
        self.add_or_update(Generation.SLURTLE_MOUNDS, slurtle_mounds)

    def splumonkey_pods(self) -> Rarities:
        return self.get(Generation.SPLUMONKEY_PODS)

    def set_splumonkey_pods(self, splumonkey_pods: Rarities) -> None:
        self.add_or_update(Generation.SPLUMONKEY_PODS, splumonkey_pods)

    def bats_spawner(self) -> Rarities:
        return self.get(Generation.BATS)

    def set_bats_spawner(self, bats: Rarities) -> None:
        self.add_or_update(Generation.BATS, bats)

    def nightmare_fissures(self) -> Rarities:
        return self.get(Generation.NIGHTMARE_FISSURES)

    def set_nightmare_fissures(self, nightmare_fissures: Rarities) -> None:
        self.add_or_update(Generation.NIGHTMARE_FISSURES, nightmare_fissures)

    def spilagmites(self) -> Rarities:
        return self.get(Generation.SPILAGMITES)

    def set_spilagmites(self, spilagmites: Rarities) -> None:
        self.add_or_update(Generation.SPILAGMITES, spilagmites)

    def tentacles(self) -> Rarities:
        return self.get(Generation.TENTACLES)

    def set_tentacles(self, tentacles: Rarities) -> None:
        self.add_or_update(Generation.TENTACLES, tentacles)
