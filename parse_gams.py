import re


def parse_gams(gams_file):
    """
    Parse GAMS file and return different block into some lists.
    :param gams_file: path for gams file
    :return: lists for important model parameters
    """
    equation_name_list = []
    binary_var_list = []
    positive_var_list = []
    other_var_list = []
    equation_list = []
    bound_list = []

    find_equation_name = False
    stop_equation_name = False
    find_binary_var = False
    stop_binary_var = False
    find_positive_var = False
    stop_positive_var = False
    find_other_var = False
    stop_other_var = False
    find_equation = False
    stop_equation = False
    find_bound = False
    stop_bound = False

    obj = None

    with open(gams_file) as f:
        print('Start parsing gams file.')
        lines = f.readlines()
        file_length = len(lines)
        print('The gams file has ', file_length, ' lines.')

        nr = 0
        while nr < file_length:
            # Search the block for equations
            if lines[nr] == 'EQUATIONS\n':
                find_equation_name = True
                nr += 1
                continue
            # Read each equation name
            if find_equation_name and ';' not in lines[nr] and not \
                    stop_equation_name:
                equation_name_list.append(lines[nr].lstrip('\t').rstrip('\n'))
            elif find_equation_name and ';' in lines[nr] and not \
                    stop_equation_name:
                equation_name_list.append(lines[nr].lstrip('\t').rstrip(';\n'))
                stop_equation_name = True

            # Search the block for binary variables
            if lines[nr] == 'BINARY VARIABLES\n':
                find_binary_var = True
                nr += 1
                continue
            # Read each equation name
            if find_binary_var and ';' not in lines[nr] and not stop_binary_var:
                binary_var_list.append(lines[nr].lstrip('\t').rstrip('\n'))
            elif find_binary_var and ';' in lines[nr] and not stop_binary_var:
                binary_var_list.append(lines[nr].lstrip('\t').rstrip(';\n'))
                stop_binary_var = True

            # Search the block for positive variables
            if lines[nr] == 'POSITIVE VARIABLES\n':
                find_positive_var = True
                nr += 1
                continue
            # Read each equation name
            if find_positive_var and ';' not in lines[nr] and not \
                    stop_positive_var:
                positive_var_list.append(
                    lines[nr].lstrip('\t').rstrip('\n'))
            elif find_positive_var and ';' in lines[nr] and not \
                    stop_positive_var:
                positive_var_list.append(lines[nr].lstrip('\t').rstrip(';\n'))
                stop_positive_var = True

            # Search the block for other variables
            if lines[nr] == 'VARIABLES\n':
                find_other_var = True
                nr += 1
                continue
            # Read each equation name
            if find_other_var and ';' not in lines[nr] and not stop_other_var:
                other_var_list.append(
                    lines[nr].lstrip('\t').rstrip('\n'))
            elif find_other_var and ';' in lines[nr] and not stop_other_var:
                other_var_list.append(
                    lines[nr].lstrip('\t').rstrip(';\n'))
                stop_other_var = True

            # Search the equations
            if stop_equation_name and stop_binary_var and stop_positive_var \
                    and stop_other_var:
                if equation_name_list[0] in lines[nr]:
                    equation_list.append(lines[nr].rstrip(';\n'))
                    find_equation = True
                elif find_equation and equation_name_list[-1] not in lines[nr] \
                        and not stop_equation:
                    equation_list.append(lines[nr].rstrip(';\n'))
                elif find_equation and equation_name_list[-1] in lines[nr] \
                        and not stop_equation:
                    equation_list.append(lines[nr].rstrip(';\n'))
                    stop_equation = True

            # Search the variable bounds
            if stop_equation:
                if 'up' in lines[nr] or 'lo' in lines[nr]:
                    find_bound = True
            if find_bound and not stop_bound:
                bound_list.append(lines[nr].rstrip(';\n'))
                if 'up' not in lines[nr] and 'lo' not in lines[nr]:
                    stop_bound = True
                    bound_list.pop()

            # Search the
            if stop_bound:
                if 'max' in lines[nr]:
                    obj = 'max'
                elif 'min' in lines[nr]:
                    obj = 'min'

            nr += 1
        # print(equation_name_list)
        # print(binary_var_list)
        # print(positive_var_list)
        # print(other_var_list)
        # print(equation_list)
        # print(bound_list)

        print('Parsing of gams file finish')

        return binary_var_list, positive_var_list, other_var_list, \
               bound_list, equation_name_list, equation_list, obj


def gen_model(lists):
    lists = replace_obj_var(lists)

    binary_var_list, positive_var_list, other_var_list, bound_list, \
    equation_name_list, equation_list, obj = lists

    bounds, binary = gen_var(binary_var_list, positive_var_list, other_var_list,
                             bound_list)
    print('Finish generating variable bounds')

    eq_list, ueq_list, obj_func = gen_equation(equation_list, obj)
    print('Finish generating constraints and objective function')

    return eq_list, ueq_list, obj_func, bounds, binary


def replace_obj_var(lists):
    """Replace the GAMS_OBJECTIVE with x0, which could be seen as variable in
    model"""
    for list_nr in range(len(lists)):
        for item_nr in range(len(lists[list_nr])):
            if "GAMS_OBJECTIVE" in lists[list_nr][item_nr]:
                lists[list_nr][item_nr] = lists[list_nr][item_nr].replace(
                    "GAMS_OBJECTIVE", "x0")
    return lists


def gen_equation(eq_list, obj):
    equal_list = []
    unequal_list = []
    obj_func = None
    for eq in eq_list:
        eq = eq.split('..')[1]
        if '=e=' in eq:
            eq_items = eq.split('=e=')
            equal_list.append(eq_items[0] + '-(' + eq_items[1] + ')')
        elif '=l=' in eq:
            # Shouldn't replace =l= with minus, the reason is that the positive
            # and negative signs should be changed.
            eq_items = eq.split('=l=')
            unequal_list.append(eq_items[0] + '-(' + eq_items[1] + ')')

    r_eq = re.compile(r'x[\d]+')

    def repl(match):
        inner_word = match.group()[0] + '[' + str(
            int(match.group()[1:]) - 1) + ']'
        return inner_word

    eq_com = {}
    for eq_nr in range(len(equal_list)):
        eq_com[eq_nr] = r_eq.sub(repl, equal_list[eq_nr])  # replace the index
        # in equation

        if 'x0' not in equal_list[eq_nr]:
            equal_list[eq_nr] = str(eq_com[eq_nr])
            # equal_list[eq_nr] = lambda x: eval(eq_com[eq_nr])
            pass
        else:
            if obj == 'max':
                # delete the first 6 characters ' x[-1]', the hard coding
                # style might cause Problem. If it causes some unwanted
                # problem, using package re to fix it.
                max_obj = eq_com[eq_nr][6:]
                print('The maximal objective for the model is', max_obj)
                obj_func = lambda x: eval(max_obj)

            elif obj == 'min':
                # com = r_eq.sub(repl, equal_list[eq_nr]).lstrip(' x[-1] -')
                min_obj = eq_com[eq_nr][8:]
                print('The minimal objective for the model is', min_obj)
                obj_func = lambda x: eval(min_obj)

            # obj_func = lambda x: eval(com)
            equal_list.pop(eq_nr)


    ueq_com = {}
    for ueq_nr in range(len(unequal_list)):
        ueq_com[ueq_nr] = r_eq.sub(repl, unequal_list[ueq_nr])
        unequal_list[ueq_nr] = str(ueq_com[ueq_nr])
        # ueq_com[ueq_nr] = r_eq.sub(repl, unequal_list[ueq_nr])
        # unequal_list[ueq_nr] = lambda x: eval(ueq_com[ueq_nr])

    return equal_list, unequal_list, obj_func


def gen_var(binary_var_list, positive_var_list, other_var_list, bound_list):
    var_list = binary_var_list + positive_var_list + other_var_list
    var_list.sort()
    var_list.pop(0)  # delete objective variable
    var_bounds = {}
    binary = []

    for var in var_list:
        low_bound = None
        up_bound = None
        if var in binary_var_list:
            low_bound = 0
            up_bound = 1
            binary.append(True)
        elif var in positive_var_list:
            low_bound = 0
            binary.append(False)
        else:
            binary.append(False)

        for bound in bound_list:
            if var + '.' in bound and 'up' in bound:
                up_bound = float(bound.split('=')[1])
            elif var + '.' in bound and 'lo' in bound:
                low_bound = float(bound.split('=')[1])

        var_bounds[var] = (low_bound, up_bound)
    return var_bounds, binary


if __name__ == '__main__':
    import os

    base_path = os.path.dirname(__file__)
    example_path = os.path.join(base_path, 'gams', 'pyomo_gdp.gams')
    contents = parse_gams(example_path)
    gen_model(contents)
