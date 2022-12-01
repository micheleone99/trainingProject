import urllib.request
import html.parser

# Porogram, korzystając z protokołu HTTP wczytuje z podanej lokalizacji dokument HTML i pozwala użytkownikowi obejrzeć
# podstawowe  dane o obrazach (element IMG) zawartych w tym dokumencie (lokalizacja, rozmiar pliku w bajtach, wymiary
# obrazu na stronie).
# Znane ograniczenia:
#   -obsługa tylko protokołu HTTP,
#   -oczekuje się, że wśród nagłówków odpowiedzi jest 'Content-Length' (m. in. nieprzewidziane działanie,
#    gdy Tranfer-Encodigng = chunked)
#   -nie ma sprawdzenia, czy dane w zasobie sieciowym są w formacie HTML
#   -zakłada się, że dokument HTML jest kodowany w utf-8
#   -linki w atrybutach src obrazów są traktowane jako bezwzględne
# Testowane na lokalizacj http://www.onet.pl/

def input_integer(prompt):
    '''Funkcja służąca do pobierania z konsoli liczb całkowitych.\n''' \
    '''W przypadku, gdy wpeowadzony ciąg konwertuje się do liczby całkowitej, ''' \
    '''zwraca tę liczbę. W przeciwnym przypadku zwraca None.'''
    num = input(prompt)
    try:
        return int(num)
    except ValueError:
        return None

def find_attr(l:list, argname:str):
    for v in l:
        if v[0].lower() == argname.lower():
            return v[1]
    return None

class MyParser(html.parser.HTMLParser):
    '''parser HTML, którego celem jest znalezienie wszystkich elementów IMG i zapamiętanie ich atrybutów'''
    def __init__(self, List):
        super().__init__()
        self.List = List

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'img':
            self.addImage(attrs)

    def addImage(self, attrs):
        self.List.append(attrs)

class Processor():
    '''Klasa, która wczytuje plik i zapamiętuje dane zawartych w nim obrazów'''
    def __init__(self, url):
        self.url = url
        self.imageList = []

    @property
    def imageCount(self):
        return len(self.imageList)

    def start(self):
        r = urllib.request.Request(url=self.url, method="GET")
        resp = urllib.request.urlopen(r)
        l = resp.getheader('Content-Length')
        if l is not None:
            B = resp.read(int(l))
            parser = MyParser(self.imageList)
            parser.feed(B.decode('utf-8'))
            result = True
        else:
            result = False
        resp.close()
        return result

    def getImageDetails(self, index):
        url = find_attr(self.imageList[index], 'src')
        h = find_attr(self.imageList[index], 'height')
        w = find_attr(self.imageList[index], 'width')
        r = urllib.request.Request(url, method='HEAD')
        resp = urllib.request.urlopen(r)  # żeby nie marnować zasobów, rozmiar pliku obrazu jest odczytywany nie dla
                                          # każdego z obrazów na etapie parsowania dokumentu, ale dopiero w momencie,
                                          # kiedy jest potrzebny, bo użytkownik o to zapytał. Pozostałe dane były w
                                          # załadowanym dokumencie HTML )
        l = resp.getheader('Content-Length')
        resp.close()
        if l is None:
            l = 'brak atrybutu'
        if h is None:
            h = 'nie określono'
        if w is None:
            w = 'nie określono'
        return f'url: {url}, rozmiar: {l}, szerokość: {w}, wysokość: {h}'


class Main():
    '''klasa, która steruje wykonaniem programu'''
    def __init__(self):
        self.proc = None

    def input_url(self):
        return input('Podaj url:')

    def getImangeIndex(self):
        while True:
            imageIndex = input_integer(f'Numer obrazu (1 - {self.proc.imageCount})')
            if imageIndex == None:
                print('Należy podać wartość liczbową.')
            elif imageIndex < 1 or imageIndex > self.proc.imageCount:
                print('Wartość liczbowa spoza wskazanego zakresu.')
            else:
                print(self.proc.getImageDetails(imageIndex))
                break

    def image_menu(self, url):
        self.proc = Processor(url)
        if self.proc.start():
            while True:
                print('Menu:\n\t1. Podaj numer obrazu\n\t2. Koniec')
                command = input('Podaj opcję:')
                if command == '1':
                    self.getImangeIndex()
                elif command == '2':
                    break
                else:
                    print('Nieprawidłowa wartość opcji')
        else:
            print('Nie można wczytać.')

    def main_menu(self):
        while True:
            print('Menu:\n\t1. Podaj nowy url\n\t2. Koniec')
            command = input('Podaj opcję:')
            if command == '1':
                url = self.input_url()
                self.image_menu(url)
            elif command == '2':
                break
            else:
                print('Nieprawidłowa wartość opcji')

Main().main_menu()
