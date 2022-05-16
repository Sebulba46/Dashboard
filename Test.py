

def add_comma(num: int) -> str:
    new_num = ''
    num = str(num)
    count = 1
    for s, j in zip(range(len(num)), num[::-1]):
        if count % 3 == 0:
            new_num += j + ','
        else:
            new_num += j
        count += 1

    return new_num[::-1]



