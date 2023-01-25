class Weapon:
    def __init__(self, name="",dmg=0, atk=0, defend=0, agl=0, luk=0, delay=340, *templates):
        self.name = name
        self.dmg = dmg
        self.atk = atk
        self.agl = agl
        self.defend = defend
        self.luk = luk
        self.delay = delay
        self.templates = templates


class Player:
    def __init__(self, atk: int, defend: int, agl: int, luk: int, level: int, maxhp: int, dmg: int = 0, weapon=Weapon(),
                 name: str = "",
                 *status):
        self.name = name
        self.level = level
        self.maxhp = maxhp
        self.dmg = dmg
        self.atk = atk
        self.defend = defend
        self.agl = agl
        self.luk = luk
        self.templates = status
        self.weapon = Weapon()


class Monster:
    def __init__(self, atk: int, defend: int, agl: int, luk: int, level: int, maxhp: int, dmg: int = 0, name: str = "",
                 *status):
        self.name = name
        self.level = level
        self.maxhp = maxhp
        self.dmg = dmg
        self.atk = atk
        self.defend = defend
        self.agl = agl
        self.luk = luk
        self.templates = status
