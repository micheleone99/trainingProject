#Program umożliwia:
#  -wyświetlenie listy kolejnych liczb pierwszych
#  -wyświetlenie rozkładu liczy na czynniki pierwsze

def input_integer(prompt):
    '''Funkcja służąca do pobierania z konsoli liczb całkowitych.\n''' \
    '''W przypadku, gdy wpeowadzony ciąg konwertuje się do liczby całkowitej, ''' \
    '''zwraca tę liczbę. W przeciwnym przypadku zwraca None.'''
    num = input(prompt)
    try:
        return int(num)
    except ValueError:
        return None

def prime_generator():
    '''Funkcja generująca bez końca liczby pierwsze.\n''' \
    '''Zastosowanie instrukcji yield pozwala na użycie jej jako iteratora ''' \
    '''i ograniczenie czasu wykonania w zależności od potrzeb.'''
    prime_list = [] # lista kolejnych znalezionych liczb pierwszych
    l = 0 # indeks liczby pierwszej
    n = 2 # liczba testowana
    while True:
        for m in prime_list:
            if n % m == 0:
                break
                # wyjście z pętli for poprzez instrukcję break oznacza, że
                # n dzieli się bez reszty przez którąś z licz pierwszych mniejszych
                # od niej, czyli n nie jest liczbą pierwszą.
        else:
            # dojście w to miejsce oznacza, że n nie dzieli się bez
            # reszty przez żadną liczbę pierwszą, która jest mniejsza
            # od niej, a co za tym idzie, n jest kolejną liczbą pierwszą.
            prime_list.append(n)
            yield (l, n)
            l += 1
        n += 1

def proceed(option):
    while True:
        n = input_integer('Podaj n:')
        if n is not None:
            for v in prime_generator():
                if (v[0] < n and option == 1) or (v[1] <= n and option == 2):  # odpowiednio dobiera, kiedy wyjść z pętli
                    print(f'Liczba pierwsza #{v[0] + 1}: {v[1]}')
                else:
                    break
            break
        else:
            print('Nieprawidłowa wartość liczbowa.')

def factorize(n):
    '''Funkcja wykonująca rozkład liczby n na czynniki pierwsze.\n''' \
    '''Wykorzystuje gnerator liczb pierwszych. Zwraca listę, której elementami jest słownik postaci ''' \
    '''{'prime': p, 'exp': e}, gdzie p to czynnik pierwszy, a e to wykładnik, z którym p występuje w ''' \
    '''iloczynie tworzącym n.'''
    if n >= 2:
        l = []
        for v in prime_generator():
            if n == 1:  # ja wiem, że można by przerwać, kiedy V[1] * v[1] > n i wtedy wiadomo by było, że n jest liczbą pierwszą, ale chciałem, żeby wszystkie liczby pierwsze pochodziły z generatora
                break
            if n % v[1] == 0:
                n //= v[1]  # jeżeli n dzieli się bez reszty przez liczbę pierwswzą ta liczba jest dpoisywana do listy
                p = {'prime': v[1], 'exp': 1}
                l.append(p)
                while n % v[1] == 0:  # następnie testowane jest ile razy dzieli się przez tę liczbę pirewszą.
                    n //= v[1]
                    p['exp'] += 1
        return l
    raise ValueError('Liczba musi być co najmniej równa 2, żeby ją rozłożyć na czynniki pierwsze.')

def factorization():
    while True:
        n = input_integer('Podaj n:')
        if n is not None:
            try:
                print(factorize(n))
            except ValueError as exc:
                print(exc.args[0])
            break
        else:
            print('Nieprawidłowa wartość liczbowa')

def main_menu():
    '''Menu główne.\n''' \
    '''Pisane w Python 3.9, dlatego nie używam match.'''
    while True:
        print('Menu:\n\t1. n najmniejszych liczb pierwszych\n\t2. Wszystkie iczby pierwsze nieprzekraczające n\n\t3. Rozkład liczby naturalnej na czynniki pierwsze\n\t4. Koniec')
        command = input('Podaj opcję:')
        if command == '1' or command == '2':
            proceed(int(command))
        elif command == '3':
            factorization()
        elif command == '4':
            break
        else:
            print('Nieprawidłowa wartość opcji.')

main_menu()
