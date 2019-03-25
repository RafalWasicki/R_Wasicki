import itertools
import math
import copy
import time
from prettytable import PrettyTable

# odczyt z pliku


def odczyt(nazwa):
    theFile = open(nazwa, "r")
    theFloats = []
    for val in theFile.read().split():
        theFloats.append(float(val))
    theFile.close()
    return theFloats

# segregowanie danych do pozniejszego wykorzystania w algorytmie


def przygotowanie_danych(nazwa):
    Wartosci = odczyt(nazwa)
    tabela = []
    n = int(Wartosci[0])
    ilosc = int(Wartosci[1])
    for a in range(2, len(Wartosci), ilosc):
        tabela_pomocnicza = []
        for b in range(0, ilosc):
            tabela_pomocnicza = tabela_pomocnicza+[Wartosci[a+b]]
        tabela.append(tabela_pomocnicza)
    return tabela, n, ilosc

# funkcja kluczujaca do sortowania tabeli


def sortSecond(val):
    return val[1]

# funkcja wyliczajaca Cmax poszczegolnych procesow i sortujaca Cmax malejaco, zwraca kolejnosc wykonywania operacji algorytmu neh


def sortowanie_tabeli(n, ilosc, tabela):
    sortownia = []
    kolejnosc = []

    for i in range(n):
        czas = 0
        for j in range(0, ilosc):
            czas += tabela[i][j]
        sortownia.append([i, czas])
    sortownia.sort(key=sortSecond, reverse=True)
    for i in sortownia:
        kolejnosc.append(i[0])
    return kolejnosc

# funkcja tworzaca permutacje do przegladu


def tworzenie_permutacji(wartosc, lista):
    permutacje = []
    for i in range(len(lista)+1):
        lista.insert(i, wartosc)
        permutacje.append(lista.copy())
        lista.pop(i)
    return permutacje

# funkcja wyliczajaca Cmax , zwraca kolejnosc z najkrotszym czasem i ten czas


def przeglad_zupelny(kolejnosc, ilosc, tabela):
    Cmax = []
    for permutacja in kolejnosc:
        m = [0]*ilosc
        for i in permutacja:
            for j in range(0, ilosc):
                if j == 0:
                    m[j] += tabela[i][j]
                else:
                    m[j] = max(m[j], m[j-1])+tabela[i][j]
        Cmax.append(max(m))
    n = Cmax.index(min(Cmax))
    najlepsza = kolejnosc[n]
    return najlepsza, min(Cmax)

# nie uzywana jesli uwazasz ze mozna to ja wywal


def wypisanie_wynikow(Cmax, permutacje):
    a = int(Cmax.index(min(Cmax)))
    j = 0
    for i in permutacje:
        print(
            f"Dla kolejnosci {i} otrzymano czas na maszynach: {Cmax[j]}")
        j += 1
    print("-"*100)
    print(
        f"Dla kolejnosci {permutacje[a]} otrzymano optymalny czas na maszynach: {min(Cmax)}")


def utworz_graf(Pi, ilosc, tabela):
    graf = []
    for i in Pi:
        graf.append(tabela[i])
    obciazenie = []
    for k in range(len(graf)):
        obciazenie.append([0]*ilosc)

    for i in range(0, len(graf)):
        if i == 0:
            for j in range(0, ilosc):
                if j == 0:
                    obciazenie[i][j] = graf[i][j]
                else:
                    obciazenie[i][j] = obciazenie[i][j-1] + graf[i][j]
        else:
            for j in range(0, ilosc):
                if j == 0:
                    obciazenie[i][j] = obciazenie[i-1][j] + graf[i][j]
                else:
                    obciazenie[i][j] = max([obciazenie[i-1][j], obciazenie[i][j-1]]) + graf[i][j]
 #################################################################
    #print(obciazenie)
    #obciazenie = []
    #for i in range(0, len(graf)):
    #    m = 0
    #    obciazenie_linii = []
    #    for j in range(0, ilosc):
    #        if i == 0:
    #            m += graf[i][j]
    #            obciazenie_linii.extend([m])
    #        elif i == 1:
    #            m = max(m, obciazenie[i - 1][j]) + graf[i][j]
    #            obciazenie_linii.extend([m])
    #        else:
    #            m = max(obciazenie[i - 1][j], m) + graf[i][j]
    #            obciazenie_linii.extend([m])
    #    obciazenie.append(obciazenie_linii)
##################################################################
    i = 0;
    j = 0;
    sciezka = []
    while (i !=len(graf)-1)or(j!=ilosc-1) :
        if obciazenie[len(graf)-i-1][ilosc-j-1]-graf[len(graf)-i-1][ilosc-j-1] == obciazenie[len(graf)-i-2][ilosc-j-1]:
            sciezka.append([len(graf)-i-1, ilosc-j-1])
            i = i+1

        elif obciazenie[len(graf)-i-1][ilosc-j-1]-graf[len(graf)-i-1][ilosc-j-1] == obciazenie[len(graf)-i-1][ilosc-j-2]:
            sciezka.append([len(graf)-i-1, ilosc-j-1])
            j = j+1
    sciezka.append([0, 0])
    return sciezka, graf, obciazenie
def utworz_graf2(Pi, ilosc, tabela):
    graf = []
    for i in Pi:
        graf.append(tabela[i])
    obciazenie = []
    for k in range(len(graf)):
        obciazenie.append([0]*ilosc)

    for i in range(1, len(graf)+1):
        if i == 0:
            for j in range(1, ilosc+1):
                if j == 0:
                    obciazenie[-i][-j] = graf[-i][-j]
                else:
                    obciazenie[-i][-j] = obciazenie[-i][-j+1] + graf[-i][-j]
        else:
            for j in range(1, ilosc+1):
                if j == 0:
                    obciazenie[-i][-j] = obciazenie[-i+1][-j] + graf[-i][-j]
                else:
                    obciazenie[-i][-j] = max([obciazenie[-i+1][-j], obciazenie[-i][-j+1]]) + graf[-i][-j]
    return obciazenie

def dodaj_do_grafu(graf,obciazenie1,obciazenie2,item,tablica):
    for i in range(len(graf)+1):
        graf.insert(i, tablica[item])
        obciazenie1.insert(i,[0] * ilosc)
        obciazenie2.insert(i, [0] * ilosc)
        if i == 0:
            for j in range(0, ilosc):
                if j == 0:
                    obciazenie1[i][j] = graf[i][j]
                else:
                    obciazenie1[i][j] = obciazenie1[i][j - 1] + graf[i][j]
        else:
            for j in range(0, ilosc):
                if j == 0:
                    obciazenie1[i][j] = obciazenie1[i - 1][j] + graf[i][j]
                else:
                    obciazenie1[i][j] = max([obciazenie1[i - 1][j], obciazenie1[i][j - 1]]) + graf[i][j]

        i = i+1
        if i == 0:
            for j in range(1, ilosc+1):
                if j == 0:
                    obciazenie2[-i][-j] = graf[-i][-j]
                else:
                    obciazenie2[-i][-j] = obciazenie2[-i][-j+1] + graf[-i][-j]
        else:
            for j in range(1, ilosc+1):
                if j == 0:
                    obciazenie2[-i][-j] = obciazenie2[-i+1][-j] + graf[-i][-j]
                else:
                    obciazenie2[-i][-j] = max([obciazenie2[-i+1][-j], obciazenie2[-i][-j+1]]) + graf[-i][-j]
        print(obciazenie1)
        print(obciazenie2)
        print(graf)
        graf.remove(tablica[item])


def neh_akceleracja(sciezka,graf,i,kolejnosc):
    kolejka = copy.deepcopy(kolejnosc)
    zadanie_odrzucone = 999
    zadania = [0]*len(kolejnosc)

    for k in range(len(kolejnosc)):
        if i == kolejnosc[k]:
            zadanie_odrzucone = k


    for i in sciezka:
        if i[0] != zadanie_odrzucone:
             zadania[i[0]] += 1
    index = [i for i, x in enumerate(zadania) if x == max(zadania)]
    if index == zadanie_odrzucone:
        return -1
    if len(index) > 1:
        temp = []
        for i in index:
            temp.append(sum(graf[i]))
        ind = temp.index(max(temp))
    return kolejnosc[index[ind]]



# GLOWNY KOD
plik = "data.txt"
tabela, n, ilosc = przygotowanie_danych(plik)
start = time.time_ns() / (10**9)
kolejnosc = sortowanie_tabeli(n, ilosc, tabela)
najlepsza_kolejnosc = []
x = PrettyTable()
graf = []
obciazenie1 = []
obciazenie2 = []
x.field_names = ["Permutacja", "Cmax", "Czas wykonywania"]
for i in kolejnosc:
    dodaj_do_grafu(graf,obciazenie1,obciazenie2,i,tabela)
    permutacje = tworzenie_permutacji(i, najlepsza_kolejnosc)
    najlepsza_kolejnosc, Cmax = przeglad_zupelny(permutacje, ilosc, tabela)
    sciezka, graf1, obciazenie = utworz_graf(najlepsza_kolejnosc, ilosc, tabela)
    #obciazenie2 = utworz_graf2(najlepsza_kolejnosc, ilosc, tabela)



duration = time.time_ns() / (10**9) - start
x.add_row([najlepsza_kolejnosc, Cmax, duration])
print(x)
