# from operator import attrgetter
# import numpy as np
# import random
#
# # --------------------------------------------------------------------------------------------
# # Inputs
# # len_indiv = int(input('Длина индивидов: '))
# # len_population = int(input('Длина популяции: '))
# # iterations = int(input('Количество итераций: '))
# # mutation_probability = float(input('Вероятность мутации: '))
# # limit_one = float(input('lim1: '))
# # limit_two = float(input('lim2: '))
# # search_input = input('max \ min: ')
# # number_args = int(input('Количество аргументов: '))
#
# iterations = 10
# limit_one = -100000000
# # limit_two = 100000000
# number_args = 10
#
# # --------------------------------------------------------------------------------------------
# # Static methods
#
# def create_individ(blength: int) -> list:
#     individ = []
#     for _ in range(blength):
#         individ.append(random.randint(0, 1))
#     return individ
#
#
# def function(args):
#     # return 10 * 2 + (args[0] ** 2 - 10 * np.cos(2 * np.pi * args[1]) + (args[0] ** 2 - 10 * np.cos(2 * np.pi * args[1])))
#     # return np.sin(args[1]) + np.sin(args[2]) + np.sin(args[3]) + np.sin(args[0])
#     return sum([(i+1)*x**2 for i, x in enumerate(args)])
#
#
# def split_array(arr, n):
#     size = len(arr) // n
#     result = []
#     for i in range(n):
#         result.append(arr[i * size:(i + 1) * size])
#     return result
#
#
# # TODO need to change this later >:D
#
#
# class Population():
#     def __init__(self, length=10, bit_length=10, mutation=0.1, args=[], nargs=5, lim1=0, lim2=10):
#         self.length = length
#         self.blength = bit_length * nargs
#         self.array = []
#         self.mutation = mutation
#         self.args = args
#         self.nargs = nargs
#         self.lim1 = lim1
#         self.lim2 = lim2
#
#     def get_attr(self):
#         return self.length, self.blength, self.mutation, self.args, self.lim1, self.lim2
#
#     def population(self):
#         return self.array
#
#     def create_population(self):
#         for _ in range(self.length):
#             self.array.append(create_individ(self.blength))
#         return 'Filled successfully'
#
#     def fitness(self, indiv):
#         s_indiv = "".join(map(str, indiv))
#         ints = []
#         floats = []
#         for i in split_array(s_indiv, self.nargs):
#             string = "".join(i)
#             ints.append(int(string, 2))
#
#         for f in ints:
#             floats.append((f / (2 ** (len(indiv) / 2) - 1)) * (self.lim2 - self.lim1) + self.lim1)
#
#         variable = function(floats)
#         return variable
#
#     def av_population_fitness(self):
#         av = 0
#         for i in self.array:
#             av += self.fitness(i)
#
#         return av / len(self.array)
#
#
# popul = Population(nargs=number_args, lim1=limit_one, lim2=limit_two)
# child_population = Population()
#
# popul.create_population()
#
#
# for i in range(2, 15):
#     print(f"i:{i}")
#     minp = 100000000000000000
#     maxp = -1
#     for j in range(100):
#         popul = Population(nargs=number_args, lim1=limit_one, lim2=limit_two, bit_length=i)
#         popul.create_population()
#         pp = popul.av_population_fitness()
#         minp = min(minp, pp)
#         maxp = max(maxp, pp)
#     print(maxp-minp)
#     print("----")
#
# # 10
# # -100
# # 100
# # 240
# """
# i:2
# 16.878347374988152
# ----
# i:3
# 1.0642454636526963
# ----
# i:4
# 0.06385716150907683
# ----
# i:5
# 0.004258152025613526
# ----
# i:6
# 0.000280365331491339
# ----
# i:7
# 1.724925823509693e-05
# ----
# i:8
# 9.045106708072126e-07
# ----
# i:9
# 7.405560609186068e-08
# ----
# i:10
# 4.24279278377071e-09
# ----
# i:11
# 2.673914423212409e-10
# ----
# i:12
# 1.546140993013978e-11
# ----
# i:13
# 1.8189894035458565e-12
# ----
# i:14
# 0.0
# ----
# i:15
# 0.0
# ----
# i:16
# 0.0
# ----
# i:17
# """
# # import random
# #
# # print(random.randint(0, 1)*random.randint(0, 1)*random.randint(0, 1)*random.randint(0, 1)*random.randint(0, 1)*random.randint(0, 1))