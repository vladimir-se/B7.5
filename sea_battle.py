#!/usr/bin/env python3
#coding: utf-8


import random
import sys
from os import system, name
from time import sleep


from termcolor import colored


class Battlefield():
    '''
    Класс поля боя.
    '''


    empty_field = colored('⦁', 'blue')


    def __init__(self, battle_ships, you_are_human):
        # Кто играет.
        self.you_are_human = you_are_human

        # Игровое поле.
        self.fieldMatrix = {
            0:{0:' ', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6'},
            1:{0:'1', 1:Battlefield.empty_field, 2:Battlefield.empty_field, 3:Battlefield.empty_field, 4:Battlefield.empty_field, 5:Battlefield.empty_field, 6:Battlefield.empty_field},
            2:{0:'2', 1:Battlefield.empty_field, 2:Battlefield.empty_field, 3:Battlefield.empty_field, 4:Battlefield.empty_field, 5:Battlefield.empty_field, 6:Battlefield.empty_field},
            3:{0:'3', 1:Battlefield.empty_field, 2:Battlefield.empty_field, 3:Battlefield.empty_field, 4:Battlefield.empty_field, 5:Battlefield.empty_field, 6:Battlefield.empty_field},
            4:{0:'4', 1:Battlefield.empty_field, 2:Battlefield.empty_field, 3:Battlefield.empty_field, 4:Battlefield.empty_field, 5:Battlefield.empty_field, 6:Battlefield.empty_field},
            5:{0:'5', 1:Battlefield.empty_field, 2:Battlefield.empty_field, 3:Battlefield.empty_field, 4:Battlefield.empty_field, 5:Battlefield.empty_field, 6:Battlefield.empty_field},
            6:{0:'6', 1:Battlefield.empty_field, 2:Battlefield.empty_field, 3:Battlefield.empty_field, 4:Battlefield.empty_field, 5:Battlefield.empty_field, 6:Battlefield.empty_field},
        }

        # Флот игрока. 
        self.battle_ships = battle_ships
        
        # Расстановка флота игрока на поле.
        self.populate_battlefield()


    def display_play_field(self,*args, **kwargs):
        '''
        Отрисовки поля боя.
        player_hints - потери игрока
        player_score - очки игрока
        player_last_shot - координаты последнего выстрела игрока
        player_total_shots - всего выстрелов игрока
        enemy_last_shot - координаты последнего выстрела противника
        enemy_total_shots - всего выстрелов противника
        '''

        print(f"\n\tПотери:[{kwargs['player_hints']}]\tОчки:[{kwargs['player_score']}]")
        try:
            print(f"\n    Ход игрока:{kwargs['player_last_shot']}\n    Ход противника:{kwargs['enemy_last_shot']}")
            print(f"\n    Всего:\n     ходов игрока:{kwargs['player_total_shots']}   хдов противника:{kwargs['enemy_total_shots']}")
        except:
            pass

        print(f"  {'_' * 40}\n")
        for ox in self.fieldMatrix:
            for oy in self.fieldMatrix[ox].values():
                print(f"   {oy}", end = f"{' ' * 2}")
            print('\n')
        try:
            {kwargs['player_last_shot']}
            print(f"{' ' * 6}Палубы: {colored('■', 'cyan')} - три {colored('■', 'magenta')} - две {colored('■', 'yellow')} - одна")
            print('\n')
        except:
            pass


    def populate_battlefield(self):
        '''
        Расстановки кораблей на поле боя.
        '''
        # Выбор корабля
        for ship in self.battle_ships:
            # Выбор начальных координат для размещения корабля.
            ox, oy = self.coordinat_selector(len(ship.get_ship_decks))
            # Размещение корабля.
            ship.set_ship_position(ox, oy)
            # Если играет человек.
            if self.you_are_human:
                for desk in ship.get_ship_decks:
                    self.fieldMatrix[ox][oy] = desk
                    oy += 1


    def coordinat_selector(self, ship_decks):
        '''
        Определение координат для установки корабля в соответствии с количеством палуб,
        ориентацией размещения и наличием кораблей по близости.
        '''
        while True:
            # Условия для 3х и 2х палубных кораблей, чтобы не зайти за края поля.
            if ship_decks == 3:
                oy = random.randrange(1, 4)
                ox = random.randrange(1, 6)
            if ship_decks == 2:
                oy = random.randrange(1, 5)
                ox = random.randrange(1, 6)
            if ship_decks == 1:
                oy = random.randrange(1, 6)
                ox = random.randrange(1, 6)

            ships = [ship for ship in self.battle_ships if len(ship.get_ship_position)]
            if ships:
                if self.search_in_ship_coordinats(ox, oy, ships):
                    return(ox, oy)
                else:
                    continue
            else:
                return(ox, oy)


    def search_in_ship_coordinats(self, ox, oy, ships):
        for ship in ships:
            if f"{ox}{oy}" in [f"{ship.get_ship_position[2][0]}{position}" for position in ship.get_ship_position[3]]:
                return False
            if int(f"{ox}{oy}") == int(f"{ship.get_ship_position[2][0]}{ship.get_ship_position[3][0]}") - 1:
                return False
            if int(f"{ox}{oy}") == int(f"{ship.get_ship_position[2][0]}{ship.get_ship_position[3][-1]}") + 1:
                return False
        return True


class BattleShip():
    '''
    Класс корабля.
    '''


    desk = '■'
    bang = colored('✘', 'red')
    blunder = colored('●', 'cyan')

    def __init__(self, ship_decks):
        self.__ship_decks = []
        self.number_of_ship_decks = self.set_ship_decks(ship_decks)
        # Координаты корабля [ox, oy]
        self.__ship_position = []
        self.__hit = 0


    @property
    def set_hit(self):
        '''
        Определение потерь.
        '''
        self.__hit += 1
    

    @property
    def get_hit(self):
        '''
        Получение потерь.
        '''
        return self.__hit


    @property
    def get_ship_decks(self):
        '''
        Получить список палуб корабля.
        '''
        return self.__ship_decks


    def set_ship_decks(self, ship_decks):
        '''
        Обозначить палубы корабля.
        '''
        ship_colors = {1:"yellow", 2:"magenta", 3:"green"}
        if 0 < ship_decks < 4:
            for _ in range(ship_decks):
                self.__ship_decks.append(colored(BattleShip.desk, ship_colors[ship_decks]))
            return ship_decks
        else:
            raise(IndexError)
            
    
    def set_ship_position(self, ox, oy):
        '''
        Вычисление однозначных координат корабля на поле.
        '''
        self.__ship_position = [ox, oy, [ox], [i if i > 1 else 1 for i in range(oy, oy + len(self.__ship_decks))]]


    @property
    def get_ship_position(self):
        '''
        Сеттер координат корабля.
        '''
        return self.__ship_position


    def blow_up_the__deck(self, desk_number):
        '''
        Пометить палубу как взорванную.
        '''
        self.__ship_decks[desk_number] = BattleShip.bang 
        return(self.__ship_decks)


class DoubleShotException(Exception):
    '''
    Исключение при повторном выстреле по одним координатам.
    '''
    pass


class Player():
    '''
    Класс определяющий действия игроков.
    '''
    def __init__(self, name, fleet, battlefield):
        self.__player_name = name
        self.__score = 0
        self.__hint = 0
        self.last_shot = ''
        self.shot_history = []
        self.fleet = fleet
        self.battlefield = battlefield


    @property
    def player_hint(self):
        '''
        Получить потери игрока.
        '''
        return self.__hint


    @player_hint.setter
    def player_hint(self, hint):
        '''
        Определить потери игрока.
        '''
        self.__hint = hint


    @property
    def player_score(self):
        '''
        Получить очки игрока.
        '''
        return self.__score


    @player_score.setter
    def player_score(self, score):
        '''
        Определить очки игрока.
        '''
        self.__score = score


    @property
    def player_name(self):
        '''
        Узнать имя игрока.
        '''
        return self.__player_name


    @player_name.setter
    def player_name(self, name):
        '''
        Задать имя игрока.
        '''
        self.__player_name = name


    def move(self):
        '''
        Выстрел игрока.
        '''
        while True:
            __move = input(colored(' → ', 'green'))

            # Выход из игры.
            if __move == 'q':
                print(colored("До встречи! ✋\n", 'yellow'))
                sys.exit()

            # Обработка ввода.
            elif __move.isdigit() and (len(__move) == 2 and 0 < (int(__move[0]) and int(__move[1])) < 7):                    
                try:
                    # Проверка выстрела на повтор.
                    self.last_shot = [int(__move[0]), int(__move[1])]
                    if self.last_shot in self.shot_history:
                        raise DoubleShotException()
                    self.shot_history.append(self.last_shot)
                    break
                except DoubleShotException:
                    print(colored(f"Повторная стрельба по одним координатам запрещена! ☝", 'red'))
                    continue

            else:
                print(colored("Введите корректное значение! ☝", 'yellow'))
                continue

        return self.last_shot


class AIPlayer(Player):
    '''
    Класс описывающий действия ИИ во время игры.
    '''
    def __init__(self, name, fleet, battlefield):
        super(AIPlayer, self).__init__(name, fleet, battlefield)


    def get_shot_coordinates(self):
        '''
        Рандомный выбор цели для стрельбы.
        В одно и тоже место стрелять повторно нельзя. 
        '''
        while True:
            ox = random.randint(1, 6)
            oy = random.randint(1, 6)

            self.last_shot = [ox, oy]
            if self.last_shot in self.shot_history:
                continue
            break
        self.shot_history.append(self.last_shot)
        return(self.last_shot)


    def move(self):
        '''
        Рандомное ожидание и выстрел.
        '''
        sleep(random.randint(1, 5))
        return self.get_shot_coordinates()


class TheGame():
    '''
    Класс организации игрового процесса.
    '''


    def __init__(self, player_name):
        # Имя игрока.
        self.player_name = player_name

        # Параметры игры игрока.
        self.human_player_fleet =  self.make_fleet(three_deck = 1, double_deck = 2, single_deck = 4)
        self.human_player_field = Battlefield(self.human_player_fleet,  you_are_human = True)
        self.human_player = Player(self.player_name, self.human_player_fleet, self.human_player_field)


        # Параметры игры компьютера.
        self.ai_player_fleet =  self.make_fleet(three_deck = 1, double_deck = 2, single_deck = 4)
        self.ai_player_field = Battlefield(self.ai_player_fleet, you_are_human = False)
        self.ai_player = AIPlayer("R2D2", self.ai_player_fleet, self.ai_player_field)


        # Список игроков, для удобства.
        self.players = [self.human_player, self.ai_player]


        # Запуск процесса игры.
        self.game_processing()


    def make_fleet(self, *args, **kwargs):
        '''
        Создание флота.
        '''
        number_of_ship_decks = {'three_deck': 3, 'double_deck': 2, 'single_deck': 1}
        fleet = []
        for arg in kwargs.items():
            for _ in range(arg[1]):
                fleet.append(BattleShip(number_of_ship_decks[arg[0]]))
        return fleet


    def clear_screen(self):
        """
        Очистка экрана после каждого хода
        """
        if name == 'nt':
            system('cls')
        else:
            system('clear')


    def select_player_move(self):
        """
        Выбор игрока, который будет осуществлять ход.
        """
        while True:
            value = self.players.pop(0)
            self.players.append(value)
            yield value


    def game_processing(self):
        '''
        Ход игры.
        '''
        for player in self.select_player_move():
            # Определение противника для текущего игрока.
            enemy = [enemy_ for enemy_ in self.players if enemy_ != player][0]
            msg = f"Ход игрока: {player.player_name}"
            while True:
                self.clear_screen()
                '''
                player_hints - потери игрока
                player_score - очки игрока
                player_last_shot - координаты последнего выстрела игрока
                player_total_shots - всего выстрелов игрока
                enemy_last_shot - координаты последнего выстрела противника
                enemy_total_shots - всего выстрелов противника
                '''
                # Поле противника.
                self.ai_player.battlefield.display_play_field(
                    player_hints = self.ai_player.player_hint, 
                    player_score = self.ai_player.player_score,
                )

                # Отображать только поле игрока.
                self.human_player.battlefield.display_play_field(
                    player_hints = self.human_player.player_hint, 
                    player_score = self.human_player.player_score,
                    player_last_shot = self.human_player.last_shot,
                    player_total_shots = len(self.human_player.shot_history),
                    enemy_last_shot =self.ai_player.last_shot,
                    enemy_total_shots = len(self.ai_player.shot_history))
                print(msg)
                move = player.move()
                if move:
                    player.player_score = self.shot(enemy, ox = move[0], oy = move[1])
                self.victory(player, enemy)
                break


    def shot(self, enemy, ox, oy):
        '''
        Выстрел.
        '''
        # Помечаем клетку по которой велась стрельба.
        for battleship in  enemy.fleet:
            if f"{ox}{oy}" in [f"{battleship.get_ship_position[2][0]}{position}" for position in battleship.get_ship_position[3]]:
                battleship.blow_up_the__deck(battleship.get_ship_position[3].index(oy))
                enemy.battlefield.fieldMatrix[ox][oy] = BattleShip.bang
            else:
                if  Battlefield.empty_field == enemy.battlefield.fieldMatrix[ox][oy]:
                    enemy.battlefield.fieldMatrix[ox][oy] = BattleShip.blunder


        for ship in enemy.fleet:
            # Определяем корабль по которому велась стрельбы.
            if ox in ship.get_ship_position[2] and oy in ship.get_ship_position[3]:
                # Засчитываем попадание.
                ship.set_hit
                enemy.player_hint += 1
        return(sum([ship.get_hit for ship in enemy.fleet]))


    def victory(self, player, enemy):
        '''
        Определение победителя.
        '''
        if player.player_score == sum([ship.number_of_ship_decks for ship in enemy.fleet]):
            print(colored(f"🎆 Ура! Пбедил {player.player_name}! 🎆", 'red'))
            sys.exit()


if __name__ == "__main__":
    while True:
        player_name = input("Введите имя игрока: ")
        if len(player_name) < 2:
            continue
        game = TheGame(player_name)