import copy

# 1 A list consisting of five empty lists
nested_list = [[], [], [], [], []]
print("Five empty lists:", nested_list)

# 2 A list of length five whose items are lists of three zeros
nested_list = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
print("List of five lists with three zeros:", nested_list)

# 3 Using list comprehensions
zero_list = [0 for _ in range(3)]
nested_list = [[0 for _ in range(3)] for _ in range(5)]
print("zero_list (3 zeros):", zero_list)
print("nested_list (list comprehension):", nested_list)

# 4 Access a specific item with value 7
nested_list = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
item_seven = nested_list[2][1]
print("Item with value 7:", item_seven)

# 5 Reference behavior explanation
# When you do [[0]*3]*5, all inner lists refer to the **same object**
shared_list = [[0]*3]*5
shared_list[0][0] = 99
print("Shared reference example:", shared_list)
print("Explanation: All inner lists refer to the same object in memory.")

# 6 List of five empty dictionaries
list_dicts = [{} for _ in range(5)]
print("List of five empty dictionaries:", list_dicts)

# 7 Function: dict_copies(my_dict, num_copies)
def dict_copies(my_dict, num_copies):
    return [copy.deepcopy(my_dict) for _ in range(num_copies)]

original_dict = {"a": 1, "b": 2}
copies = dict_copies(original_dict, 3)
print("List of copies of a dictionary:", copies)

# 8 Function: make_dict_lists(length)
def make_dict_lists(length):
    return {i: [0]*i for i in range(length)}

dict_lists = make_dict_lists(5)
print("Dictionary with lists of zeros:", dict_lists)

# 9 Challenge: Define grade_table
grade_table = {
    "Joe": [100, 98, 100, 13],
    "Scott": [75, 59, 89, 77],
    "John": [86, 84, 91, 78]
}
print("Grade table:", grade_table)

# 10 Challenge: Function make_grade_table(name_list, grades_list)
def make_grade_table(name_list, grades_list):
    return dict(zip(name_list, grades_list))

names = ["Joe", "Scott", "John"]
grades = [
    [100, 98, 100, 13],
    [75, 59, 89, 77],
    [86, 84, 91, 78]
]
final_grade_table = make_grade_table(names, grades)
print("Final grade table from function:", final_grade_table)
