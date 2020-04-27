import random
def check(table, coordinates):
    '''
        This function check if a queen is attacking another queen
    :param table: 2-d list
        A list with coordinates of all queens on chess table
    :param coordinates: 1-d list
        A list with coordinates of the queen tha we check
    :return: list
        A list of quins that are attacked by main queen
    '''
    qeens = []
    for coord in table:
        if coord != coordinates and (coordinates[0] == coord[0] or coordinates[1] == coord[1]):
            qeens.append(table.index(coord))
    i, j = coordinates[0]-1, coordinates[1]-1
    while i >= 0 and j >= 0:
        if [i, j] in table:
            qeens.append(table.index([i, j]))
        i-=1; j-=1
    i, j = coordinates[0] - 1, coordinates[1] + 1
    while i >= 0 and j < len(table):
        if [i, j] in table:
            qeens.append(table.index([i, j]))
        i-=1; j+=1
    i, j = coordinates[0] + 1, coordinates[1] -1
    while i < len(table) and j >= 0:
        if [i, j] in table:
            qeens.append(table.index([i, j]))
        i+=1; j-=1
    i, j = coordinates[0] + 1, coordinates[1] + 1
    while i < len(table) and j < len(table):
        if [i, j] in table:
            qeens.append(table.index([i, j]))
        i+=1; j+=1
    return qeens
def cost(table):
    '''
        This function calculates the cost function of the chess table by finding all pairs on tabe
    :param table: 2-d list
        A list with coordinates of all queens on chess table
    :return: int
        The cost of the chess table
    '''
    queen_pairs = set([])
    for pos in table:
        pairs = [[table.index(pos), q] for q in check(table, pos)]
        for pair in pairs:
            queen_pairs.add(tuple(pair))
    queen_pairs = list(queen_pairs)
    for i in range(len(queen_pairs)):
        queen_pairs[i] = list(queen_pairs[i])
        if queen_pairs[i][0] < queen_pairs[i][1]:
            queen_pairs[i][0], queen_pairs[i][1] = queen_pairs[i][1], queen_pairs[i][0]
        queen_pairs[i] = tuple(queen_pairs[i])
    return len(set(queen_pairs))
def cross_over(population, nb_children):
    '''
        This function apply the crossing-over process on 2 arrys-like lists
    :param population: 2-d array like list
        The population with 2 array that will be uses to create new individuals in the population
    :param nb_children: int
        The number of children that must be created
    :return: 2-d array like list
        Return the population with parents and their children after crossing-over
    '''
    new_generation = []
    for i in range(nb_children//2):
        first = random.randrange(0, len(population[0])-1)
        second = random.randrange(0, len(population[0])-1)
        if first > second:
            first, second = second, first
        new_generation.append(population[0][0:first] + population[1][first: second] + population[0][second:])
        new_generation.append(population[1][0:first] + population[0][first: second] + population[1][second:])
    for gene in new_generation:
        population.append(gene)
    return population
def mutate(table):
    '''
        This function creates a mutation in placement of the queens
    :param table: 2-d list
        A list with coordinates of all queens on chess table
    :return:
        The list with coordinates of all queens on chess table after mutation
    '''
    mutation_range = random.randint(0, len(table)//2)
    mutation_locus = random.randrange(0, len(table) - 1)
    if table[mutation_locus][0] + mutation_range <= len(table)-1 and [table[mutation_locus][0] + mutation_range, table[mutation_locus][1]] not in table:
        table[mutation_locus][0] +=mutation_range
    elif table[mutation_locus][0] - mutation_range >=0 and [table[mutation_locus][0] - mutation_range, table[mutation_locus][1]] not in table:
        table[mutation_locus][0] -=mutation_range
    elif table[mutation_locus][1] + mutation_range <= len(table)-1 and [table[mutation_locus][0], table[mutation_locus][1] + mutation_range] not in table:
        table[mutation_locus][1] +=mutation_range
    elif table[mutation_locus][1] - mutation_range >=0 and [table[mutation_locus][0],table[mutation_locus][1] - mutation_range] not in table:
        table[mutation_locus][1] -= mutation_range
    return table
def GA(tables):
    '''
        This function is the Genetic Algorithm implementation for 8-queens problem
    :param tables: 3-list
        The list of chess tables
    :return: 2-d list
        The best configuration of queens coordinates that solve the problem
    '''
    while True:
        tables = cross_over(tables.copy(), 10)
        for i in range(2,len(tables)):
            tables[i] = mutate(tables[i])
            if cost(tables[i]) == 0:
                return tables[i]
        cost_list = []
        for i in range(len(tables)):
            cost_list.append(cost(tables[i]))
        min_cost = cost_list[0]
        min_index = 0
        for i in range(2,len(cost_list)):
            if cost_list[i] < min_cost:
                min_cost = cost_list[i]
                min_index = i
        min_indexes = [min_index]
        if cost_list.count(min_cost) > 1:
            for i in range(len(cost_list)):
                if cost_list[i] == min_cost and i != min_index:
                    min_indexes.append(i)
                    break
        else:
            min_cost2 = cost_list[0]
            for i in range(2, len(cost_list)):
                if cost_list[i] < min_cost2 and cost_list[i] != min_cost:
                    min_cost2 = cost_list[i]
            min_indexes.append(min_cost2)
        tables = [tables[min_indexes[0]], tables[min_indexes[1]]]
clean_table = [[0 for i in range(8)] for j in range(8)]
chess_tables = []
for i in range(2):
    coordinates = [].copy()
    while True:
        if len(coordinates) == 8:
            break
        new_coordinates = [random.randint(0, 7), random.randint(0, 7)]
        if new_coordinates not in coordinates:
            coordinates.append(new_coordinates)
        else:
            continue
    chess_tables.append(coordinates)
res= GA(chess_tables)
for r in res:
    clean_table[r[0]][r[1]] = 1
for row in clean_table:
    print(row)