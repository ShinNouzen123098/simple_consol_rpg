import json
import random
from abc import ABC, abstractmethod
import sys
import time

#Выгрузка файла с показателями героя
def load_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

#КЛАССЫ_________________________________________________________________________________________________________________
#Персонаж
class Character(ABC):
    def __init__(self, name, hp, attack_damage, defense):
        self.name = name
        self.hp = hp
        self.attack_damage = attack_damage
        self.defense = defense

    @abstractmethod
    def is_alive(self):
        pass

    @abstractmethod
    def take_damage(self, damage):
        pass

    @abstractmethod
    def attack(self, target):
        pass

    def __str__(self):
        return f'{self.name}: \nHP = {self.hp}\nGamage = {self.attack_damage}\nDefense = {self.defense}'

#Герой
class Hero(Character):
    def __init__(self, name, hp=100, attack_damage=5, defense=0, lvl=1, exp=0, items=None):
        super().__init__(name, hp, attack_damage, defense)
        self.lvl = lvl
        self.exp = exp
        self.crit = 0.1 * lvl
        self.items = items if items is not None else []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        Game.save_game(hero)
        return f'Текущее HP {self.name} = {self.hp}'

    def attack(self, target):
        while True:
            chose = input('Выберите тип атаки:\n'
                          '1. Удар в голову\n'
                          '2. Обычный удар\n'
                          '3. Случайный удар\n').lower()
            if chose == '1' or chose == 'удар в голову':
                if random.random() < 0.1:
                    damage = target.hp
                    print(f'Вы попали {target.name}у в голову!')
                    time.sleep(1.5)
                    break
                else:
                    return 'Вы промахнулись'

            elif chose == '2' or chose == 'обычный удар':
                damage = self.attack_damage
                if random.random() < self.crit:
                    damage *= 2
                    print('Критический Удар!')
                    time.sleep(1.5)
                break

            elif chose == '3' or chose == 'случайный удар':
                damage = random.randint(int(self.attack_damage * 0.1), int(self.attack_damage * 2))
                if random.random() < self.crit:
                    damage *= 2
                    print('Критический Удар!')
                    time.sleep(1.5)
                break
        damage = max(1, damage - target.defense)
        print(target.take_damage(damage))

        if not target.is_alive():
            return f'{self.name} атакует {target.name} и убивает его!\n'
        return f'{self.name} атакует {target.name} и наносит {damage} урона!\n'

    def __str__(self):
        items_str = "\n".join([f"- {list(item.keys())[0]}: {list(item.values())[0]}" for item in self.items]) if self.items else "Нет"
        return (f'{self.name}: '
                f'\nHP = {self.hp}\n'
                f'Gamage = {self.attack_damage}\n'
                f'Defense = {self.defense}\n'
                f'LVL = {self.lvl}\n'
                f'Exp = {self.exp}\n'
                f'Crit_chans = {self.crit}\n'
                f'Items:\n{items_str}\n')

#Враг
class Enemy(Character):
    def __init__(self, name, hp, attack_damage, defense):
        super().__init__(name, hp, attack_damage, defense)

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return f'Текущее HP {self.name} = {self.hp}'

    def attack(self, target):
        damage = max(1, self.attack_damage - target.defense)
        print(target.take_damage(damage))

        if not target.is_alive():
            return f'{self.name} атакует {target.name} и убивает его!\n'
        return f'{self.name} атакует {target.name} и наносит {damage} урона!\n'

    def __str__(self):
        return (f'{self.name}: '
                f'\nHP = {self.hp}\n'
                f'Gamage = {self.attack_damage}\n'
                f'Defense = {self.defense}\n')

#Предметы
class Items:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def take_item(self, target):
        target.items.append({self.name: self.value})
        for v in self.value:
            if v == 'Damage':
                target.attack_damage += self.value['Damage']
            elif v == 'HP':
                target.hp += self.value['HP']
            elif v == 'Defense':
                target.defense += self.value['Defense']
    def __str__(self):
        return (f'{self.name}\n'
                f'{self.value}\n')
#Игра
class Game:
    @staticmethod
    def save_game(hero):
        data = {'Name': hero.name,
                'HP': hero.hp,
                'Damage': hero.attack_damage,
                'Defense': hero.defense,
                'Lvl': hero.lvl,
                'Exp': hero.exp,
                "Items": hero.items}
        with open('Hero.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def new_game():
        global hero
        name = input('Введите имя персонажа\n')
        hero = Hero(name)
        print(f'Текущие показатели\n{hero}')
        Game.save_game(hero)

        while True:
            agree = input('\n___________________________________________________________________\nЖелаете начать бой?(Да/Нет)\n')
            if agree.lower() == 'да':
                Game.battle()
                break
            elif agree.lower() == 'нет':
                Game.save_game(hero)
                sys.exit(0)

    @staticmethod
    def start():
        global hero
        if not load_file('Hero.json'):
            name = input('Введите имя персонажа\n')
            hero = Hero(name)
            print(f'Текущие показатели\n{hero}')
            Game.save_game(hero)
        else:
            hero_stats = load_file('Hero.json')
            hero = Hero(name=hero_stats['Name'],
                        hp=hero_stats['HP'],
                        attack_damage=hero_stats['Damage'],
                        defense=hero_stats['Defense'],
                        lvl=hero_stats['Lvl'],
                        exp=hero_stats['Exp'],
                        items=hero_stats['Items'])
            print(f'Текущие показатели\n{hero}')

        while True:
            agree = input('\n___________________________________________________________________\nЖелаете начать бой?(Да/Нет)\n')
            if agree.lower() == 'да':
                Game.battle()
                break
            elif agree.lower() == 'нет':
                Game.save_game(hero)
                sys.exit(0)

    @staticmethod
    def battle():
        global hero
        while True:
            # Генерация врага
            goblin = Enemy('Гоблин', random.randint(30, 50), random.randint(1, 5), random.randint(0, 3))
            orc = Enemy('Орк', random.randint(60, 120), random.randint(10, 30), random.randint(10, 20))
            dragon = Enemy('Дракон', random.randint(200, 500), random.randint(50, 100), random.randint(30, 70))
            enemies_low_lvl = [goblin, orc]
            enemies = [goblin, orc, dragon]

            print('\n'*3)
            if hero.lvl < 10:
                enemy = goblin
            elif hero.lvl < 20:
                enemy = random.choice(enemies_low_lvl)
            else:
                enemy = random.choice(enemies)
            print(f'На своём пути вы встретили врага - {enemy.name}\n'
                  f'Показатели врага:\n'
                  f'{enemy}')
            print('\n'*2)
            time.sleep(3)
            print('Вы вступаете в бой!\n'
                  '________________________________________________\n'
                  '\n')
            while hero.is_alive and enemy.is_alive:
                time.sleep(1.2)
                print(hero.attack(enemy))
                if enemy.hp == 0:
                    hero.exp += 60
                    if hero.exp >= 100:
                        hero.lvl += 1
                        hero.exp = hero.exp % 100
                    if random.random() < 0.4:
                        print('Вам выпало лечащее зелье! Ваше здоровье величилось на 30!')
                        hero.hp += 10
                    if random.random() < 0.3:
                        item = random.choice(items)
                        print(f'\n'
                              f'Поздравляем! Вам выпало снаряжение - {item}')
                        item.take_item(hero)
                    Game.save_game(hero)
                    break
                print('\n')
                time.sleep(0.8)
                print(enemy.attack(hero))
                if hero.hp == 0:
                    print('Вы проиграли!\n'
                          'Игра окончена')
                    Game.game_over()
            print(f'Поздравляем! Вы успешно одолели врага - {enemy.name}\n'
                  f'Желаете продолжить?(Да/Нет)\n')
            while True:
                agree = input().lower()
                if agree == 'да':
                    print(f'Ваши текущие показатели:\n{hero}')
                    time.sleep(2)
                    break  # Начнётся новый бой (внешний while True)
                elif agree == 'нет':

                    return  # Выход из battle
                else:
                    print('Такой команды нет. Выберите только "Да" или "Нет"')

    @staticmethod
    def game_over():
        sys.exit(0)

    

#ЭКЗЕМПЛЯРЫ КЛАССОВ________________________________________________________________________________________________________________________
goblin = Enemy('Гоблин', random.randint(30, 50), random.randint(1, 5), random.randint(0, 3))
orc = Enemy('Орк', random.randint(60, 120), random.randint(10, 30), random.randint(10, 20) )
dragon = Enemy('Дракон', random.randint(200, 500), random.randint(50, 100), random.randint(30, 70))


simpl_sword = Items('Меч', {'Damage': +5})
simple_shild = Items('Щит', {'Defense': +10})

enemies_low_lvl = [goblin, orc]
enemies = [goblin, orc, dragon]
items = [simpl_sword, simple_shild]

#ОСНОВНАЯ ФУНКЦИЯ ЗАПУСКА___________________________________________________________________________________________________________________
if __name__ == '__main__':
    print(f'__________________Приветствую в RPG мире______________\n')
    while True:
        print(f'_________________Выберите один из пунктов____________')
        chose = input('1. Новая игра\n'
                      '2. Продолжить игру\n'
                      '3. Выход\n')
        if chose.lower() == 'новая игра' or chose.lower() == '1':
            Game.new_game()
        elif chose.lower() == 'продолжить игру' or chose.lower() == '2':
            Game.start()
        elif chose.lower() == 'выход' or chose.lower() == '3':
            Game.game_over()




