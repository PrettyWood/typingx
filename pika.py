from typingx import isinstancex, Annotated, Constraints, Union

Gt2Int = Annotated[int, Constraints(gt=2)]


def check(my_set):
    return isinstancex(my_set, Annotated[set[Gt2Int], Constraints(min_length=3)])

print(check({3, 3, 3, 6}))
