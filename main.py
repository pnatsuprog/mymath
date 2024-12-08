from src.core.polynomial import Polynomial


def main():
    p1 = Polynomial({(2, 1): 4.0, (0,): -1.0, (): 3.0})
    print(p1)
    p2 = Polynomial({(): 4.4})
    print(p2)
    p3 = p1 + p2
    print(p3)


if __name__ == "__main__":
    main()
