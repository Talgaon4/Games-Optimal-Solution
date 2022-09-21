# from accelasc import accel_asc
from itertools import chain, combinations


class BestMove:

    def __init__(self):

        self.configs = self.powerset(range(1, 10))  # all the permutations of digits from 1 to 9
        self.ways_to_roll = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}  # all rolls options
        self.max_moves = 12
        """ All permutations so that the sum of the elements in each permutation is equal to the sum of a possible toss
         and the elements are digits from 1 to 9 """
        self.move_list = {config: {roll: list(self.gen_moves(config, roll))
                                   for roll in range(2, 13)} for config in self.configs}
        """ The moves are initialized so that for each permutation the number of legal rolls
         that it may lead to are counted if the user chooses this permutation. """
        self.num_moves = {config: {i: 0 for i in range(1, self.max_moves)} for config in self.configs}
        self.best_moves = {}
        self.find_all_moves()
        self.find_best_moves()

    def unique_integer_partitions(self, n):
        for partition in self.number_partitions(n):
            set_partition = frozenset(partition)
            if len(set_partition) == len(partition):  # check each element is unique
                yield set_partition

    def gen_moves(self, config_, n):
        for partition in self.unique_integer_partitions(n):
            if partition.issubset(config_):
                yield partition

    def powerset(self, iterable):
        s = list(iterable)
        subsets = chain.from_iterable(
            combinations(s, size) for size in range(len(s) + 1))
        return [frozenset(subset) for subset in subsets]

    def find_all_moves(self):
        for move_num in range(1, self.max_moves):
            for config in self.configs:
                for roll in range(2, 13):
                    for move in self.move_list[config][roll]:
                        config_after_move = config - move
                        if move_num == 1:
                            if len(config_after_move) == 0:
                                self.num_moves[config][move_num] = self.ways_to_roll[roll]
                        else:
                            num = self.num_moves[config_after_move][move_num - 1]
                            self.num_moves[config][move_num] += self.ways_to_roll[roll] * num

    def find_best_moves(self):

        self.best_moves = {config: {roll: None for roll in range(2, 13)} for config in self.configs}

        for config in self.configs:
            for roll in range(2, 13):
                moves = self.move_list[config][roll]
                if len(moves) == 0:
                    continue
                num_wins = [sum([self.num_moves[config - move][move_num] for move_num in range(1, self.max_moves)])
                            for move in moves]
                best_move = moves[num_wins.index(max(num_wins))]
                self.best_moves[config][roll] = best_move

    def ret_best_move(self, config, n):
        if n == 1 and 1 in config:
            return frozenset({1})
        elif n == 0 or n == 1:
            return None
        return self.best_moves[config][n]

# accel-asc algorithm Generates the integer partitions of n.
    def number_partitions(self, n):
        a = [0 for i in range(n + 1)]
        k = 1
        y = n - 1
        while k != 0:
            x = a[k - 1] + 1
            k -= 1
            while 2 * x <= y:
                a[k] = x
                y -= x
                k += 1
            l = k + 1
            while x <= y:
                a[k] = x
                a[l] = y
                yield a[:k + 2]
                x += 1
                y -= 1
            a[k] = x + y
            y = x + y - 1
            yield a[:k + 1]

best = BestMove()