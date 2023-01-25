import copy


class Glators:
    def __init__(self, star: int, name: str, *tags):
        self.star = star
        self.tags = tags
        self.name = name

    def __str__(self):
        return self.name


# 狙击
Exusiai = Glators(6, "能天使", "输出")
Schwarz = Glators(6, "黑", "输出")
BluePoison = Glators(5, "蓝毒", "输出")
GrayThroat = Glators(5, "灰喉", "输出")
Executor = Glators(5, "送葬人", "群攻")
FireWatch = Glators(5, "守林人", "输出", "爆发")
Provence = Glators(5, "普罗旺斯", "输出")
Meteorite = Glators(5, "陨星", "群攻", "削弱")
Platinum = Glators(5, "白金", "输出")
Sesa = Glators(5, "慑砂", "群攻", "削弱")
Ambriel = Glators(4, "安比尔", "输出", "减速")
May = Glators(4,"梅", "输出", "减速")
Vermeil = Glators(4, "红云", "输出")
Meteor = Glators(4, "流星", "输出", "削弱")
ShiraYuki = Glators(4, "白雪", "群攻", "减速")
Jessica = Glators(4, "杰西卡", "输出", "生存")
Catapult = Glators(3, "空爆", "群攻")
Adnachiel = Glators(3, "安德切尔", "输出")
Kroos = Glators(3, "克洛丝", "输出")
Rangers = Glators(2, "巡林者")
JusticeKnight = Glators(1, "正义骑士号", "支援")

shooters = {
               BluePoison, GrayThroat, Executor, FireWatch, Provence,
               Meteorite, Platinum, Sesa, Ambriel, May, Vermeil, Meteor, ShiraYuki, Jessica, Catapult,
               Adnachiel, Kroos
           }

# 术士
Mostima = Glators(6, "莫斯提马", "群攻", "支援", "控场")
Ifrit = Glators(6, "伊芙利特", "群攻", "削弱")
Ceobe = Glators(6, "刻俄柏", "输出", "控场")
Nightmare = Glators(5, "夜魔", "输出", "治疗", "减速")  # ##### 特殊
Leizi = Glators(5, "惊蛰", "输出")
Greyy = Glators(4, "格雷伊", "群攻", "减速")
Haze = Glators(4, "夜烟", "输出", "削弱")
Gitano = Glators(4, "远山", "群攻")
Lava = Glators(3, "炎熔", "群攻")
Steward = Glators(3, "史都华德", "输出")
Durin = Glators(2, "杜林")
_12F = Glators(2, "12F")

mages = {
    Nightmare, Leizi, Greyy, Haze, Gitano, Lava, Steward, Durin, _12F
}

# 先锋,费用回复
Siege = Glators(6, "推进之王", "输出")
Bagpipe = Glators(6, "风笛", "输出")
Texas = Glators(5, "德克萨斯", "控场")
Reed = Glators(5, "苇草", "输出")
_3nma = Glators(5, "凛冬", "支援")
Elysium = Glators(5, "极境", "支援")
Myrtle = Glators(4, "桃金娘", "治疗")  # ##### 特殊
Vigna = Glators(4, "红豆", "输出")
Scavenger = Glators(4, "清道夫", "输出")
Fang = Glators(3, "芬")
Vanilla = Glators(3, "香草")
Plume = Glators(3, "翎羽", "输出")
Yato = Glators(2, "夜刀")

vanguard = {Texas, Reed, _3nma, Elysium, Myrtle, Vigna, Scavenger, Fang, Vanilla, Plume, Yato}

# 近卫

SilverAsh = Glators(6, "银灰", "输出", "支援")
Chen = Glators(6, "陈", "爆发", "输出")
Blaze = Glators(6, "煌", "输出", "生存")
Hellagur = Glators(6, "赫拉格", "输出", "生存")
Skadi = Glators(6, "斯卡蒂", "输出", "生存")
Specter = Glators(5, "幽灵鲨", "群攻", "生存")
Broca = Glators(5, "布洛卡", "群攻", "生存")
Astesia = Glators(5, "星极", "输出", "防护")  # #####  特殊
Swire = Glators(5, "诗怀雅", "输出", "支援")
Indra = Glators(5, "因陀罗", "输出", "生存")
Beehunter = Glators(4, "猎蜂", "输出")
Mousse = Glators(4, "慕斯", "输出")
Frostleaf = Glators(4, "霜叶", "输出", "减速")
Matoimaru = Glators(4, "缠丸", "输出", "生存")
Dobermann = Glators(4, "杜宾", "输出", "支援")
Estelle = Glators(4, "艾丝黛尔", "群攻", "生存")
Utage = Glators(4, "宴", "输出", "生存")
Cutter = Glators(4, "刻刀", "爆发", "输出")
Midnight = Glators(3, "月见夜", "输出")
Popukar = Glators(3, "泡普卡", "群攻", "生存")
Melantha = Glators(3, "玫兰莎", "输出", "生存")
Castle_3 = Glators(1, "Castle-3", "支援")

warrior = {Specter, Broca, Astesia, Swire, Indra, Beehunter,
           Mousse, Frostleaf, Matoimaru, Dobermann, Estelle, Utage, Cutter, Midnight, Popukar, Melantha}
# 重装,防护

Hoshiguma = Glators(6, "星熊", "输出")
Saria = Glators(6, "塞雷娅", "治疗", "支援")
Hung = Glators(5, "哞", "治疗")
Vulcan = Glators(5, "火神", "输出", "生存")
Croissant = Glators(5, "可颂", "位移")
Liskarm = Glators(5, "雷蛇", "输出")
Asbestos = Glators(5, "石棉", "输出")
Nearl = Glators(5, "临光", "治疗")
_ym = Glators(4, "古米", "治疗")
Cuora = Glators(4, "蛇屠箱")
Matterhorn = Glators(4, "角峰")
Beagle = Glators(3, "米格鲁")
Spot = Glators(3, "斑点","治疗")
NoirCorne = Glators(2, "黑角")

guard = {Hung, Vulcan, Croissant, Liskarm, Asbestos, Nearl, _ym, Cuora,
         Matterhorn, Beagle, Spot, NoirCorne}

# 医疗,治疗

Shining = Glators(6, "闪灵", "支援")
Nightingale = Glators(6, "夜莺", "支援")
Silence = Glators(5, "赫默")
Ptilopsis = Glators(5, "白面鸮", "支援")
Warfarin = Glators(5, "华法琳", "支援")
Purestream = Glators(4, "清流", "支援")
Sussurro = Glators(4, "苏苏洛")
Perfunner = Glators(4, "调香师")
Myrrh = Glators(4, "末药")
Hibiscus = Glators(3, "芙蓉")
Ancel = Glators(3, "安塞尔")
Lancet_2 = Glators(1, "Lancet-2")

doctor = {
    Silence, Ptilopsis, Warfarin, Purestream, Sussurro, Perfunner, Myrrh,
    Hibiscus, Ancel
}

# 辅助
Magallan = Glators(6, "麦哲伦", "支援", "减速", "输出")
Glaucus = Glators(5, "格劳克斯", "减速", "控场")
Nctnha = Glators(5, "真理", "输出", "减速")
Pramanix = Glators(5, "初雪", "削弱")
Shamare = Glators(5, "巫恋", "削弱")
Mayer = Glators(5, "梅尔", "召唤", "控场")
Tsukinogi = Glators(5, "月禾", "支援", "生存")
Earthspirit = Glators(4, "地灵", "减速")
Orchid = Glators(3, "梓兰", "减速")

helper = {
    Glaucus, Nctnha, Pramanix, Shamare, Mayer, Tsukinogi, Earthspirit, Orchid
}

# 特种
Aak = Glators(6, "阿", "输出", "支援")  # ##### 特殊
Phantom = Glators(6, "傀影", "快速复活", "控场", "输出")
Weedy = Glators(6, "温蒂", "位移", "输出", "控场")
Manticore = Glators(5, "狮蝎", "输出", "生存")
FEater = Glators(5, "食铁兽", "位移", "减速")
WaaiFu = Glators(5, "槐琥", "快速复活", "削弱")
ProjektRed = Glators(5, "红", "快速复活", "控场")
Cliffheart = Glators(5, "崖心", "位移", "输出")
Shaw = Glators(4, "阿消", "位移")
Rope = Glators(4, "暗索", "位移")
Gravel = Glators(4, "砾", "快速复活", "防护")  # ##### 特殊
Thermal_EX = Glators(1, "THRM-EX", "爆发")

commando = {Manticore, FEater, WaaiFu, ProjektRed, Cliffheart, Shaw, Rope, Gravel}

level6 = [{Exusiai, Schwarz}, {Mostima, Ifrit, Ceobe}, {Siege, Bagpipe}, {SilverAsh, Chen, Blaze, Hellagur, Skadi},
          {Hoshiguma, Saria}, {Shining, Nightingale}, {Magallan, }, {Aak, Phantom, Weedy}]
level1 = {JusticeKnight, Castle_3, Lancet_2, Thermal_EX}

occupation = {"狙击干员": shooters, "术师干员": mages, "先锋干员": vanguard, "近卫干员": warrior, "重装干员": guard, "医疗干员": doctor, "辅助干员": helper,
              "特种干员": commando}
occs = [i for i in occupation.keys()]
position = ["近战位", "远程位"]
level5 = set()
level3_5 = set()
for i in occupation.values():
    level3_5 = level3_5.union(i)
for i in level3_5:
    if i.star == 5:
        i.name = "★" + i.name
        level5.add(i)
labels = ["输出","防护","生存","治疗","费用回复","群攻","减速","支援","快速复活","削弱","位移","爆发","控场","召唤","新手"]
labels_g = []
for i in labels:
    labels_g1 = set()
    for j in level3_5:
        if i in j.tags:
            labels_g1.add(j)
    labels_g.append(labels_g1)
labels_g[1] = labels_g[1].union(guard)
labels_g[3] = labels_g[3].union(doctor)
labels_g[4] = vanguard
position_g =[vanguard.union(warrior,guard,commando),shooters.union(mages,doctor,helper)]

all_tags = dict()
all_tags.update(occupation)
all_tags.update({x: y for x, y in zip(labels, labels_g)})
all_tags.update({x: y for x, y in zip(position, position_g)})
all_tags.update({"资深干员":level5})


def printout(sets:set[Glators]):
    out = []
    lv4 = False
    for _i in sets:
        if _i.star == 4:
            lv4 = True
            break
    for _i in sets:
        if _i.star == 5 and lv4:
            continue
        out.append(_i.name)
    return ", ".join(out)


all_cards_lv6 = set()
for i in level6:
    all_cards_lv6 = all_cards_lv6.union(i)

labels_g_6 = []
for i in labels:
    labels_g1 = set()
    for j in all_cards_lv6:
        if i in j.tags:
            labels_g1.add(j)
    labels_g_6.append(labels_g1)
labels_g_6[1].add(Hoshiguma)
labels_g_6[1].add(Saria)
labels_g_6[3].add(Shining)
labels_g_6[3].add(Nightingale)
labels_g_6[4].add(Siege)
labels_g_6[4].add(Bagpipe)
position_g_6 = [level6[2].union(level6[3],level6[4],level6[7]),level6[0].union(level6[1],level6[5],level6[6])]
position_g_6[0].remove(Aak)
position_g_6[1].add(Aak)
all_tags_6 = dict()
all_tags_6.update({occs[i]:level6[i] for i in range(8)})
all_tags_6.update({x: y for x, y in zip(labels, labels_g_6)})
all_tags_6.update({x: y for x, y in zip(position, position_g_6)})
all_tags_6.update({"资深干员":set(),"新手":set()})

def check(*tags:str):
    reply = []
    if "高级资深干员" in tags:
        tags = list(tags)
        tags.remove("高级资深干员")
        cases = []
        cases_name = []
        for tag0 in range(2):
            for tag1 in range(2):
                for tag2 in range(2):
                    for tag3 in range(2):
                        x = all_cards_lv6
                        y = ["高级资深干员"]
                        if tag0:
                            x = x.intersection(all_tags_6[tags[0]])
                            y.append(tags[0])
                        if tag1:
                            x = x.intersection(all_tags_6[tags[1]])
                            y.append(tags[1])
                        if tag2:
                            x = x.intersection(all_tags_6[tags[2]])
                            y.append(tags[2])
                        if tag3:
                            x = x.intersection(all_tags_6[tags[3]])
                            y.append(tags[3])
                        cases.append(x)
                        cases_name.append(y)

        for idx, j in enumerate(cases):
            test = True
            if len(j) == 0:
                continue
            for gl in j:
                if gl.star == 3:
                    test = False
                    break
            if test:
                reply.append((",".join(cases_name[idx]), printout(j)))
        if not len(reply):
            return None
        else:
            return "\n".join([f"{idd[0]} : {idd[1]}" for idd in reply])
    else:
        cases = []
        cases_name = []
        if "支援机械" in tags:
            tags = list(tags)
            tags.remove("支援机械")
            tags.append("新手")
            all_tags_1 = ["支援","爆发","治疗","医疗干员","狙击干员","近卫干员","特种干员","近战位","远程位"]
            all_tags_1_gl = [{JusticeKnight,Castle_3},{Thermal_EX},{Lancet_2},{Lancet_2},{JusticeKnight},{Castle_3},{Thermal_EX},{Castle_3,Thermal_EX},{Lancet_2,JusticeKnight}]
            all_cards_lv1 = level1
            tags_1_dict = {x:y for x,y in zip(all_tags_1,all_tags_1_gl)}
            for tag0 in range(2):
                for tag1 in range(2):
                    for tag2 in range(2):
                        for tag3 in range(2):
                            x1 = all_cards_lv1
                            y1 = ["支援机械"]
                            if tag0:
                                if tags[0] in all_tags_1:
                                    x1 = x1.intersection(tags_1_dict[tags[0]])
                                    y1.append(tags[0])
                                else:
                                    continue
                            if tag1:
                                if tags[1] in all_tags_1:
                                    x1 = x1.intersection(tags_1_dict[tags[1]])
                                    y1.append(tags[1])
                                else:
                                    continue
                            if tag2:
                                if tags[2] in all_tags_1:
                                    x1 = x1.intersection(tags_1_dict[tags[2]])
                                    y1.append(tags[2])
                                else:
                                    continue
                            if tag3:
                                if tags[3] in all_tags_1:
                                    x1 = x1.intersection(tags_1_dict[tags[3]])
                                    y1.append(tags[3])
                                else:
                                    continue
                            cases.append(x1)
                            cases_name.append(y1)


        all_cards = level3_5
        for tag0 in range(2):
            for tag1 in range(2):
                for tag2 in range(2):
                    for tag3 in range(2):
                        for tag4 in range(2):
                            x = all_cards
                            y = []
                            if tag0:
                                x = x.intersection(all_tags[tags[0]])
                                y.append(tags[0])
                            if tag1:
                                x = x.intersection(all_tags[tags[1]])
                                y.append(tags[1])
                            if tag2:
                                x = x.intersection(all_tags[tags[2]])
                                y.append(tags[2])
                            if tag3:
                                x = x.intersection(all_tags[tags[3]])
                                y.append(tags[3])
                            if tag4:
                                x = x.intersection(all_tags[tags[4]])
                                y.append(tags[4])
                            cases.append(x)
                            cases_name.append(y)
        for idx,j in enumerate(cases):
            test = True
            if len(j) == 0:
                continue
            for gl in j:
                if gl.star == 3:
                    test = False
                    break
            if test:
                reply.append((",".join(cases_name[idx]),printout(j)))
        if not len(reply):
            return None
        else:
            return "\n".join([f"{idd[0]} : {idd[1]}" for idd in reply])


if __name__ == "__main__":
    print(check("狙击干员","爆发","减速","支援机械","远程位"))

