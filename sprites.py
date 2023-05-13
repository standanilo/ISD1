import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path


class Aki(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    # real time pretraga - ima bagova ako se zapetlja
    # def get_agent_path(self, game_map, goal):
    #     path = [game_map[self.row][self.col]]
    #     row = self.row
    #     col = self.col
    #     while True:
    #         neighbours = list()
    #         if row != goal[0] or col != goal[1]:
    #             if row == 0 and col == 0:
    #                 south = game_map[row + 1][col]
    #                 east = game_map[row][col + 1]
    #                 neighbours.append(east)
    #                 neighbours.append(south)
    #             elif row == len(game_map)-1 and col == len(game_map[0])-1:
    #                 north = game_map[row - 1][col]
    #                 west = game_map[row][col - 1]
    #                 neighbours.append(north)
    #                 neighbours.append(west)
    #             elif row == 0 and col == len(game_map[0])-1:
    #                 south = game_map[row + 1][col]
    #                 west = game_map[row][col - 1]
    #                 neighbours.append(south)
    #                 neighbours.append(west)
    #             elif row == len(game_map)-1 and col == 0:
    #                 north = game_map[row - 1][col]
    #                 east = game_map[row][col + 1]
    #                 neighbours.append(north)
    #                 neighbours.append(east)
    #             elif row == 0:
    #                 south = game_map[row + 1][col]
    #                 east = game_map[row][col + 1]
    #                 west = game_map[row][col - 1]
    #                 neighbours.append(east)
    #                 neighbours.append(south)
    #                 neighbours.append(west)
    #             elif col == 0:
    #                 north = game_map[row - 1][col]
    #                 south = game_map[row + 1][col]
    #                 east = game_map[row][col + 1]
    #                 neighbours.append(north)
    #                 neighbours.append(east)
    #                 neighbours.append(south)
    #             elif row == len(game_map)-1:
    #                 north = game_map[row - 1][col]
    #                 east = game_map[row][col + 1]
    #                 west = game_map[row][col - 1]
    #                 neighbours.append(north)
    #                 neighbours.append(east)
    #                 neighbours.append(west)
    #             elif col == len(game_map[0])-1:
    #                 north = game_map[row - 1][col]
    #                 south = game_map[row + 1][col]
    #                 west = game_map[row][col - 1]
    #                 neighbours.append(north)
    #                 neighbours.append(south)
    #                 neighbours.append(west)
    #             else:
    #                 north = game_map[row - 1][col]
    #                 south = game_map[row + 1][col]
    #                 east = game_map[row][col + 1]
    #                 west = game_map[row][col - 1]
    #                 neighbours.append(north)
    #                 neighbours.append(east)
    #                 neighbours.append(south)
    #                 neighbours.append(west)
    #             temp = list()
    #             for neighbour in neighbours:
    #                 if neighbour not in path:
    #                     temp.append(neighbour)
    #             next_path = temp[0]
    #             for neighbour in temp:
    #                 if neighbour.cost() < next_path.cost():
    #                     next_path = neighbour
    #             row = next_path.row
    #             col = next_path.col
    #         else:
    #             break
    #         path.append(next_path)
    #     return path

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]
        row = self.row
        col = self.col
        graph = {}
        i = 0

        # pravljenje matrice suseda
        for i in range(0, len(game_map)):
            j = 0
            for j in range(0, len(game_map[0])):
                if i == 0 and j == 0:
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [east, south]
                elif i == len(game_map) - 1 and j == len(game_map[0]) - 1:
                    north = game_map[i - 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, west]
                elif i == 0 and j == len(game_map[0]) - 1:
                    south = game_map[i + 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [south, west]
                elif i == len(game_map) - 1 and j == 0:
                    north = game_map[i - 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [north, east]
                elif i == 0:
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [east, south, west]
                elif j == 0:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [north, east, south]
                elif i == len(game_map) - 1:
                    north = game_map[i - 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, east, west]
                elif j == len(game_map[0]) - 1:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, south, west]
                else:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, east, south, west]
                j += 1
            i += 1

        # inicijalizacija steka
        stack = []
        visited = []
        stack.append([game_map[row][col]])

        # pretraga
        while stack:

            # ekspandovanje cvora
            temp_path = stack.pop()
            node = temp_path[-1]
            visited.append(node)

            # provera da li je ciljni
            if node.row == goal[0] and node.col == goal[1]:
                path = temp_path
                break
            temp_node = graph.get(node).copy()
            i = 0
            temp_cost = list()
            p = 0
            q = 0

            # provera da li je u susedima neki vec ekspandovan cvor
            for temp in temp_node:
                if temp in visited:
                    temp_node.remove(temp)
            for neighbour in temp_node:
                temp_cost.append(neighbour.cost())

            # sortiramo susedna polja u odnosu na njihovu cenu
            for p in range(len(temp_node)):
                for q in range(p + 1, len(temp_node)):
                    if temp_cost[p] > temp_cost[q]:
                        temp_node[p], temp_node[q] = temp_node[q], temp_node[p]
                        temp_cost[p], temp_cost[q] = temp_cost[q], temp_cost[p]
            temp_node.reverse()

            # dodavanje u stek putanja
            for neighbour in temp_node:
                if neighbour in temp_path:
                    continue
                new_path = list()
                l = 0
                for tile in temp_path:
                    new_path.append(temp_path[l])
                    l += 1
                new_path.append(neighbour)
                stack.append(new_path)
        for p in path:
            row = p.row
            col = p.col
        return path


class Jocke(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]
        row = self.row
        col = self.col
        graph = {}
        cost = {}
        i = 0

        # pravljenje matrice suseda
        for i in range(0, len(game_map)):
            j = 0
            for j in range(0, len(game_map[0])):
                if i == 0 and j == 0:
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [east, south]
                    cost[i, j] = (east.cost() + south.cost()) / 2
                elif i == len(game_map) - 1 and j == len(game_map[0]) - 1:
                    north = game_map[i - 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, west]
                    cost[i, j] = (north.cost() + west.cost()) / 2
                elif i == 0 and j == len(game_map[0]) - 1:
                    south = game_map[i + 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [south, west]
                    cost[i, j] = (west.cost() + south.cost()) / 2
                elif i == len(game_map) - 1 and j == 0:
                    north = game_map[i - 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [north, east]
                    cost[i, j] = (east.cost() + north.cost()) / 2
                elif i == 0:
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [east, south, west]
                    cost[i, j] = (east.cost() + south.cost() + west.cost()) / 3
                elif j == 0:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [north, east, south]
                    cost[i, j] = (east.cost() + south.cost() + north.cost()) / 3
                elif i == len(game_map) - 1:
                    north = game_map[i - 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, east, west]
                    cost[i, j] = (east.cost() + north.cost() + west.cost()) / 3
                elif j == len(game_map[0]) - 1:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, south, west]
                    cost[i, j] = (north.cost() + south.cost() + west.cost()) / 3
                else:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, east, south, west]
                    cost[i, j] = (east.cost() + south.cost() + west.cost() + north.cost()) / 4
                j += 1
            i += 1

        # inicijalizacija reda
        queue = []
        visited = []
        queue.append([game_map[row][col]])

        # pretraga
        while queue:

            # ekspandovanje cvora
            temp_path = queue.pop(0)
            node = temp_path[-1]
            visited.append(node)

            # provera da li je ciljni
            if node.row == goal[0] and node.col == goal[1]:
                path = temp_path
                break
            temp_node = graph.get(node).copy()
            i = 0
            temp_cost = list()

            # izracunavanje cene suseda
            for neighbour in temp_node:
                if len(temp_node) == 2:
                    temp_cost.append(cost[neighbour.row, neighbour.col] - node.cost() / 2)
                elif len(temp_node) == 3:
                    temp_cost.append(cost[neighbour.row, neighbour.col] - node.cost() / 3)
                else:
                    temp_cost.append(cost[neighbour.row, neighbour.col] - node.cost() / 4)
                i += 1
            p = 0
            q = 0

            # provera da li je u susedima neki vec ekspandovan cvor
            for temp in temp_node:
                if temp in visited:
                    temp_node.remove(temp)

            # sortiramo susedna polja u odnosu na njihovu cenu
            for p in range(len(temp_node)):
                for q in range(p + 1, len(temp_node)):
                    if temp_cost[p] > temp_cost[q]:
                        temp_node[p], temp_node[q] = temp_node[q], temp_node[p]
                        temp_cost[p], temp_cost[q] = temp_cost[q], temp_cost[p]

            # dodavanje u red putanja
            for neighbour in temp_node:
                if neighbour in visited:
                    continue
                new_path = list()
                l = 0
                for tile in temp_path:
                    new_path.append(temp_path[l])
                    l += 1
                new_path.append(neighbour)
                queue.append(new_path)
        #     m += 1
        #     for temp in graph[node.row, node.col]:
        #         if temp not in visited:
        #             if temp.row == goal[0] and temp.col == goal[1]:
        #                 k = 0
        #                 break
        #             visited.append(temp)
        #             queue.append(temp)
        #
        for p in path:
            row = p.row
            col = p.col
        return path


class Draza(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]
        row = self.row
        col = self.col
        graph = {}
        i = 0

        # pravljenje matrice suseda
        for i in range(0, len(game_map)):
            j = 0
            for j in range(0, len(game_map[0])):
                if i == 0 and j == 0:
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [east, south]
                elif i == len(game_map) - 1 and j == len(game_map[0]) - 1:
                    north = game_map[i - 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, west]
                elif i == 0 and j == len(game_map[0]) - 1:
                    south = game_map[i + 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [south, west]
                elif i == len(game_map) - 1 and j == 0:
                    north = game_map[i - 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [north, east]
                elif i == 0:
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [east, south, west]
                elif j == 0:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [north, east, south]
                elif i == len(game_map) - 1:
                    north = game_map[i - 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, east, west]
                elif j == len(game_map[0]) - 1:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, south, west]
                else:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, east, south, west]
                j += 1
            i += 1

        # inicijalizacija reda
        queue = []
        visited = []
        partial = []
        queue.append([game_map[row][col]])
        partial.append(game_map[row][col].cost())
        d = 0
        # z = 0

        # pretraga
        while queue:

            # ekspandovanje cvora i njegove parcijalne putanje
            temp_path = queue.pop(0)
            node = temp_path[-1]
            temp_cost = partial.pop(0)
            visited.append(node)
            # ---- Moze i ovo za odabir najbolje putanje ----
            #
            # if node.row == goal[0] and node.col == goal[1]:
            #     path = temp_path
            #     break
            #
            # provera da li je ciljni
            if node.row == goal[0] and node.col == goal[1]:
                if d == 0:
                    best_path = temp_path
                    d += 1
                else:
                    price = 0
                    for pa in best_path:
                        price += pa.cost()
                    if len(best_path) > len(temp_path) or price > temp_cost:
                        best_path = temp_path
            temp_node = graph.get(node).copy()
            i = 0

            # dodavanje u red putanja
            for neighbour in temp_node:
                if neighbour in visited:
                    continue
                new_path = list()
                temp_cost += neighbour.cost()
                l = 0
                for tile in temp_path:
                    new_path.append(temp_path[l])
                    l += 1
                new_path.append(neighbour)
                queue.append(new_path)
                partial.append(temp_cost)
                temp_cost -= neighbour.cost()
            p = 0
            q = 0

            # sortiramo u odnosu na njihovu parcijalnu putanju
            for p in range(len(partial)):
                for q in range(p + 1, len(partial)):
                    if partial[p] > partial[q]:
                        partial[p], partial[q] = partial[q], partial[p]
                        queue[p], queue[q] = queue[q], queue[p]
                    elif partial[p] == partial[q]:
                        if len(queue[p]) > len(queue[q]):
                            partial[p], partial[q] = partial[q], partial[p]
                            queue[p], queue[q] = queue[q], queue[p]
            # z += 1
        path = best_path
        for p in path:
            row = p.row
            col = p.col
        # print('Number of iterations:', z)
        return path


class Bole(Agent):

    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]
        row = self.row
        col = self.col
        graph = {}
        _best_cost = 2

        # heuristika sa prosecnom cenom polja
        # m = 0
        # _best_cost = 0
        # for m in range(0, len(game_map)):
        #     n = 0
        #     for n in range(0, len(game_map[0])):
        #         _best_cost += game_map[m][n].cost()
        # _best_cost /= (len(game_map[0]) * len(game_map))

        # pravljenje matrice suseda
        i = 0
        for i in range(0, len(game_map)):
            j = 0
            for j in range(0, len(game_map[0])):
                if i == 0 and j == 0:
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [east, south]
                elif i == len(game_map) - 1 and j == len(game_map[0]) - 1:
                    north = game_map[i - 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, west]
                elif i == 0 and j == len(game_map[0]) - 1:
                    south = game_map[i + 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [south, west]
                elif i == len(game_map) - 1 and j == 0:
                    north = game_map[i - 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [north, east]
                elif i == 0:
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [east, south, west]
                elif j == 0:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    graph[game_map[i][j]] = [north, east, south]
                elif i == len(game_map) - 1:
                    north = game_map[i - 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, east, west]
                elif j == len(game_map[0]) - 1:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, south, west]
                else:
                    north = game_map[i - 1][j]
                    south = game_map[i + 1][j]
                    east = game_map[i][j + 1]
                    west = game_map[i][j - 1]
                    graph[game_map[i][j]] = [north, east, south, west]
                j += 1
            i += 1

        # inicijalizacija reda
        queue = []
        visited = []
        partial = []
        price = []
        queue.append([game_map[row][col]])
        partial.append(game_map[row][col].cost())
        price.append(0)
        # z = 0

        # pretraga
        while queue:

            # ekspandovanje cvora i njegove parcijalne putanje
            temp_path = queue.pop(0)
            node = temp_path[-1]
            temp_cost = partial.pop(0)
            temp_price = price.pop(0)
            visited.append(node)
            if node.row == goal[0] and node.col == goal[1]:
                path = temp_path
                break
            temp_node = graph.get(node).copy()
            i = 0

            # dodavanje u red putanja
            for neighbour in temp_node:
                if neighbour in visited:
                    continue
                new_path = list()
                temp_cost += neighbour.cost()
                l = 0
                for tile in temp_path:
                    new_path.append(temp_path[l])
                    l += 1
                new_path.append(neighbour)
                queue.append(new_path)
                partial.append(temp_cost)
                temp_cost += (abs(neighbour.row - goal[0]) + abs(neighbour.col - goal[1])) * _best_cost
                price.append(temp_cost)
                temp_cost -= neighbour.cost()
                temp_cost -= (abs(neighbour.row - goal[0]) + abs(neighbour.col - goal[1])) * _best_cost
            p = 0
            q = 0

            # sortiramo u odnosu na njihovu kumulativnu cenu
            for p in range(len(price)):
                for q in range(p + 1, len(price)):
                    if price[p] > price[q]:
                        partial[p], partial[q] = partial[q], partial[p]
                        queue[p], queue[q] = queue[q], queue[p]
                        price[p], price[q] = price[q], price[p]
            # z += 1
        for p in path:
            row = p.row
            col = p.col
        # print('Number of iterations:', z)
        return path

class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
