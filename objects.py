from random import choice, shuffle
import time


class Room:
    def __init__(self, x, y, dirt = None):
        self.x = x
        self.y = y
        if dirt is None:
            self.dirty = choice([True, False])
        else:
            self.dirty = dirt
        return


class House:
    def __init__(self, x, y, dirt = None):
        if dirt is None:
            self.rooms = [[Room(b, a) for b in range(x)] for a in range(y)]
        else:
            if dirt == 'full':
                self.rooms = [[Room(b, a, True) for b in range(x)] for a in range(y)]
            elif dirt == 'empty':
                self.rooms = [[Room(b, a, False) for b in range(x)] for a in range(y)]
            elif isinstance(dirt, int):
                self.rooms = [[Room(b, a, False) for b in range(x)] for a in range(y)]
                sequence = [True for x in range(dirt)]
                for x in range((x+1)*(y+1) - dirt):
                    sequence.append(False)
                shuffle(sequence)
            else:
                self.rooms = [[Room(b, a, False) for b in range(x)] for a in range(y)]
                for j, dimy in enumerate(self.rooms):
                    if len(dirt) == 0:
                        break
                    for i, dimx in enumerate(dimy):
                        if len(dirt) == 0:
                            break
                        self.rooms[j][i].dirty = dirt.pop(0)
        return

    def cleanhouse(self):
        for corridor in self.rooms:
            for room in corridor:
                if room.dirty:
                    return False
        return True


class VacuumCleaner:
    def __init__(self, ambient, position = None):
        if position is not None:
            if position[0] not in list(range(len(ambient.rooms[0]))):
                raise ValueError('vacuum cleaner out of bounds "X dimension"')
            if position[1] not in list(range(len(ambient.rooms))):
                raise ValueError('vacuum cleaner out of bounds "Y dimension"')
            self.x = position[0]
            self.y = position[1]
        else:
            self.x = choice(list(range(len(ambient.rooms[0]))))
            self.y = choice(list(range(len(ambient.rooms))))
        self.performance = 0
        self.ambient = ambient
        self.action = {'up': self.goup, 'down': self.godown, 'left': self.goleft, 'right': self.goright, 'suck': self.suck}
        return

    def suck(self):
        if self.ambient.rooms[self.y][self.x].dirty:
            self.ambient.rooms[self.y][self.x].dirty = False
            self.performance -= 1
        else:
            raise AssertionError('tento suga sujeira que nao existia saporra é burra só pode')
        return

    def goup(self):
        if self.y >= len(self.ambient.rooms):
            raise ValueError('fora da area ')
        self.y += 1
        self.performance += 2
        return

    def godown(self):
        if self.y <= 0:
            raise ValueError('fora da area ')
        self.y -= 1
        self.performance += 2
        return

    def goright(self):
        if self.x >= len(self.ambient.rooms[self.y]):
            raise ValueError('fora da area ')
        self.x += 1
        self.performance += 2
        return

    def goleft(self):
        if self.x <= 0:
            raise ValueError('fora da area ')
        self.x -= 1
        self.performance += 2
        return

    def see(self):
        if self.ambient.rooms[self.y][self.x].dirty:
            return 'suck'
        dise_values = [[[self.x + 1, self.y], [self.x - 1, self.y], [self.x, self.y + 1], [self.x, self.y - 1]], ['right', 'left', 'up', 'down']]
        options = []
        for i, option in enumerate(dise_values[0]):
            try:
                if (option[0] < 0) or (option[1] < 0):
                    raise IndexError
                if self.ambient.rooms[option[1]][option[0]] is not None:
                    pass
                options.append(dise_values[1][i])
            except IndexError:
                continue
        return options

    def randomchose(self):
        options = self.see()
        if not isinstance(options, list):
            return options
        return choice(options)

    def doaction(self):
        self.action[self.randomchose()]()
        return

    def activate(self):
        while True:
            self.doaction()
            time.sleep(1)
            printrooms(self.ambient, self)
            if self.ambient.cleanhouse():
                break
        return


def printrooms(ambient, vacuum):
    for corridor in ambient.rooms:
        for room in corridor:
            if vacuum.x == room.x and vacuum.y == room.y:
                print('[x]' + str(room.dirty) + ' ', end = '\t')
            else:
                print('[ ]' + str(room.dirty) + ' ', end = '\t')
        print()

    print('\n#-------------#--------------#--------------#--------------#\n')
    return


if __name__ == '__main__':
    initialPos = [0, 0]
    houseDimension = [3, 1]
    houseDirt = [True, True, True]
    myHome = House(houseDimension[0], houseDimension[1], houseDirt)
    myVacuum = VacuumCleaner(myHome, initialPos)
    print('INITIAL STATE :\n')
    printrooms(myHome, myVacuum)
    myVacuum.activate()
    pass
