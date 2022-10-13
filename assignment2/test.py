for i in range(0, 9, 3):
    for h in range(0,9,3):
        for j in range(0,3):
            for k in range(3):
                print(i+j, k+h, end="|")
            print(" ", end="")
        print("\n")