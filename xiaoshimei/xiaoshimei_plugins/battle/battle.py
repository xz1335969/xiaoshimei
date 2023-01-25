from xiaoshimei.xiaoshimei_plugins.battle.player import Player, Monster
import random



class Skill:

    def __init__(self, name=None, damage=1, att_times=1, damage_type=0, extra_atk=0, extra_crit=0, extra_luk=0, delay=0,
                 real_damage=0,*templates):
        self.name = name
        self.damage = damage
        self.att_times = att_times
        self.damage_type = damage_type
        self.extra_atk = extra_atk
        self.extra_luk = extra_luk
        self.extra_crit = extra_crit
        self.templates = templates
        self.delay = delay
        self.real_damage = real_damage


class Battler:

    def __init__(self, battler: Player | Monster):
        self.name = battler.name
        self.delay = 0
        self.level = battler.level
        self.hp = battler.maxhp
        self.maxhp = battler.maxhp
        self.dmg = battler.dmg
        self.atk = battler.atk
        self.defend = battler.defend
        self.agl = battler.agl
        self.luk = battler.luk
        self.is_alive = True
        self.weapon = battler.weapon

    def die(self):
        self.is_alive = False

    def heal(self, num, target=None):
        if not target:
            self.hp = self.hp + num if self.hp + num < self.maxhp else self.maxhp
        else:
            target.hp = target.hp + num if target.hp + num < target.maxhp else target.maxhp

    def attack(self, target, skill=Skill()) -> tuple[int,int]:
        """
        attack
        :param target: attack target
        :param skill: using skill
        :return: is_critical,total damage
        """
        crit_p = skill.extra_crit + 0.45 * (self.luk + skill.extra_luk + 1000) / (self.luk + skill.extra_luk + 3000)
        crit = 1 if random.uniform(0, 1) < crit_p else 0
        crit_dmg_p = 0.5 + (self.luk + skill.extra_luk) / 2000
        base_dmg = int(skill.damage + self.dmg * (1 + (skill.extra_atk + self.atk) / 1000) * (
                1 - target.defend / (target.defend + 500)))
        total_damage = int(base_dmg * (1+crit*crit_dmg_p) + skill.real_damage)
        target.hp -= total_damage
        if target.hp <= 0:
            target.die()
        return crit,total_damage

    def turn_basic_delay(self):
        return int(1440000 / (self.agl + 1200)) + self.atk/10+self.weapon.delay


class Battle:
    total_battle = 0

    def __init__(self, players: list[Player],monsters:list[Monster]):
        self.players = [Battler(i) for i in players]
        self.monsters = [Battler(j) for j in monsters]
        self.turn = 0
        Battle.total_battle += 1
        self.skill = None
        self.battlers = self.players+self.monsters
        self.living_object = len(self.battlers)
        self.turn_player = self.battlers[0]

    def __del__(self):
        Battle.total_battle -= 1

    def first_turn(self):
        for player in self.players:
            player.delay += int(1440000 / (player.agl + 1200))

    def turn_start(self):
        self.turn_player = self.battlers[0]
        for player in self.battlers:
            if self.turn_player.delay > player.delay:
                self.turn_player = player

    def turn_end(self):
        self.turn_player.delay += self.skill.delay + self.turn_player.turn_basic_delay()

    def next_turn(self):
        pass

    def turn_battle(self, skill):
        self.skill = skill
