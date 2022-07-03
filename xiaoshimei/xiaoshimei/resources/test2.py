a = 1
lab_list = []


if __name__ == "__main__":

    while a != 0:
        (a, b, c) = input("输入id,count,rate\n").split()
        d = a.split("-")
        if len(d) == 1:
            lab_list.append(f"({a},{b},{c})")
        else:
            for i in range(int(d[0]),int(d[1])+1):
                lab_list.append(f"({i},{b},{c})")
        if len(d) == 3:
            break
    sql = "INSERT INTO labyrinth (item_id,count,rate) VALUES "
    print(sql + ','.join(lab_list))



