import random
import matplotlib.pyplot as plt
import pygame
import sys

# Funkcija za prikaz teksta na ekranu
def display_text(screen, text, font, color, position):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, rect)

# Funkcija za prikaz gumba na ekranu
def draw_button(screen, text, font, color, rect, hover=False):
    pygame.draw.rect(screen, color, rect)
    display_text(screen, text, font, (255, 255, 255) if not hover else (0, 0, 0), rect.center)

# Inicijalizacija Pygame-a
pygame.init()

# Postavke prozora
WIDTH, HEIGHT = 800, 600
BG_COLOR = (200, 200, 200)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (100, 100, 100)
FPS = 30

# Postavke gumba
BUTTON_WIDTH, BUTTON_HEIGHT = 50, 50
BUTTON_MARGIN = 20

# Postavke fonta
FONT_SIZE = 25
font = pygame.font.SysFont(None, FONT_SIZE)

# Postavke simulacije
trajanje_kampanje = 20
broj_jedinica = 3
broj_mandati = 20

# Funkcija za pokretanje simulacije
def start_simulation(screen):
    stranke = ['Stranka A', 'Stranka B', 'Stranka C', 'Stranka D']
    strategije = {
        1: "Dodaj glasove jedinici gdje stranka ima najviše podrške",
        2: "Dodaj glasove jedinici gdje stranka ima najmanje podrške",
        3: "Dodaj istu količinu glasova svim jedinicama",
        4: "Dodaj glasove nasumično odabranoj jedinici"
    }

    # Definicija strategija za svaku stranku
    strategije_stranaka = {
        'Stranka A': 1,  # Dodaj glasove jedinici gdje stranka ima najviše podrške
        'Stranka B': 2,  # Dodaj glasove jedinici gdje stranka ima najmanje podrške
        'Stranka C': 3,  # Dodaj istu količinu glasova svim jedinicama
        'Stranka D': 4   # Dodaj glasove nasumično odabranoj jedinici
    }

    # Funkcija za generiranje početne teritorijalne podrške
    def generiraj_pocetnu_podrsku():
        pocetna_podrska = {}
        for stranka in stranke:
            pocetna_podrska[stranka] = {'Dani': {1: {}}}
            for jedinica in range(1, broj_jedinica + 1):
                pocetna_podrska[stranka]['Dani'][1][f'Jedinica {jedinica}'] = random.randint(200, 2000)
        return pocetna_podrska

    # Dhontova metoda ppretvorbe glasova u mandate
    def dhont(broj_mandati, glasovi, verbose=False):
        t_glasovi = glasovi.copy()
        mandati = {}

        for kljuc in glasovi:
            mandati[kljuc] = 0

        while sum(mandati.values()) < broj_mandati:
            max_g = max(t_glasovi.values())
            sljedece_sjedalo = list(t_glasovi.keys())[list(t_glasovi.values()).index(max_g)]
            if sljedece_sjedalo in mandati:
                mandati[sljedece_sjedalo] += 1
            else:
                mandati[sljedece_sjedalo] = 1

            if verbose:
                print("{} Sjedalo: {}".format(sum(mandati.values()), sljedece_sjedalo))
                for kljuc in t_glasovi:
                    print("\t{} [{}]: {:.1f}".format(kljuc, mandati[kljuc], t_glasovi[kljuc]))
                print("\b")

            t_glasovi[sljedece_sjedalo] = glasovi[sljedece_sjedalo] / (mandati[sljedece_sjedalo] + 1)

        return mandati

    # Početna teritorijalna podrška
    teritorijalna_podrska = generiraj_pocetnu_podrsku()

    # Funkcija za pronalazak jedinice s najvećom podrškom za određenu stranku
    def pronadi_jedinicu_najvece_podrske(podaci_stranke):
        return max(podaci_stranke.items(), key=lambda x: x[1])

    # Funkcija za pronalazak jedinice s najmanjom podrškom za određenu stranku
    def pronadi_jedinicu_najmanje_podrske(podaci_stranke):
        return min(podaci_stranke.items(), key=lambda x: x[1])

    # Funkcija za dodavanje novih glasova na temelju strategije stranke
    def dodaj_nove_glasove(stranka, strategija, teritorijalna_podrska, dan):
        if strategija == 1:  # Dodaj glasove jedinici s najvećom podrškom
            jedinica, _ = pronadi_jedinicu_najvece_podrske(teritorijalna_podrska[stranka]['Dani'][dan])
            teritorijalna_podrska[stranka]['Dani'][dan + 1] = teritorijalna_podrska[stranka]['Dani'][dan].copy()
            teritorijalna_podrska[stranka]['Dani'][dan + 1][jedinica] += novi_glasovi_fiksno
        elif strategija == 2:  # Dodaj glasove jedinici s najmanjom podrškom
            jedinica, _ = pronadi_jedinicu_najmanje_podrske(teritorijalna_podrska[stranka]['Dani'][dan])
            teritorijalna_podrska[stranka]['Dani'][dan + 1] = teritorijalna_podrska[stranka]['Dani'][dan].copy()
            teritorijalna_podrska[stranka]['Dani'][dan + 1][jedinica] += novi_glasovi_fiksno
        elif strategija == 3:  # Dodaj jednake glasove svim jedinicama
            teritorijalna_podrska[stranka]['Dani'][dan + 1] = teritorijalna_podrska[stranka]['Dani'][dan].copy()
            ukupno_jedinica = len(teritorijalna_podrska[stranka]['Dani'][dan + 1])
            glasovi_po_jedinici = novi_glasovi_fiksno // ukupno_jedinica 
            for jedinica in teritorijalna_podrska[stranka]['Dani'][dan + 1]:
                teritorijalna_podrska[stranka]['Dani'][dan + 1][jedinica] += glasovi_po_jedinici
        elif strategija == 4:  # Dodaj glasove nasumično odabranoj jedinici
            teritorijalna_podrska[stranka]['Dani'][dan + 1] = teritorijalna_podrska[stranka]['Dani'][dan].copy()
            jedinica = random.choice(list(teritorijalna_podrska[stranka]['Dani'][dan + 1].keys()))
            teritorijalna_podrska[stranka]['Dani'][dan + 1][jedinica] += novi_glasovi_fiksno

    # Fiksni broj novih glasova za svaku stranku
    novi_glasovi_fiksno = 200

    # Ispis početne teritorijalne podrške za svaku stranku
    print("Početna Teritorijalna Podrška:")
    for stranka, podaci in teritorijalna_podrska.items():
        print(f"{stranka}:")
        for dan, jedinice in podaci['Dani'].items():
            print(f"Dan {dan}:")
            for jedinica, podrška in jedinice.items():
                print(f"\t{jedinica}: {podrška}")

    # Simulacija kampanje
    for dan in range(1, trajanje_kampanje):
        for stranka in stranke:
            strategija = strategije_stranaka[stranka]
            dodaj_nove_glasove(stranka, strategija, teritorijalna_podrska, dan)

    # Izračunaj dnevne dodjele mandati po jedinici koristeći Dhontovu metodu
    broj_mandati = 20
    for dan in range(1, trajanje_kampanje + 1):
        dnevni_glasovi = {stranka: sum(teritorijalna_podrska[stranka]['Dani'][dan].values()) for stranka in stranke}
        dnevna_mandati = dhont(broj_mandati, dnevni_glasovi)
        print(f"\nDan {dan} Dodjela mandati po Jedinici:")
        for jedinica in teritorijalna_podrska['Stranka A']['Dani'][dan]:
            glasovi_jedinice = {stranka: teritorijalna_podrska[stranka]['Dani'][dan][jedinica] for stranka in stranke}
            mandati_jedinice = dhont(broj_mandati, glasovi_jedinice, verbose=False)
            print(f"Jedinica {jedinica}: {mandati_jedinice}")

    # Grafički prikaz promjena teritorijalne podrške za svaku stranku tijekom 10 dana s opisom strategije u naslovu
    for stranka in stranke:
        plt.figure(figsize=(12, 6))
        plt.title(f"{stranka} - {strategije[strategije_stranaka[stranka]]}")
        for jedinica in teritorijalna_podrska[stranka]['Dani'][1]:
            podrška_jedinice = [teritorijalna_podrska[stranka]['Dani'][dan][jedinica] for dan in range(1, trajanje_kampanje + 1)]
            plt.plot(range(1, trajanje_kampanje + 1), podrška_jedinice, label=f"{jedinica}")
        plt.xlabel('Dan')
        plt.ylabel('Teritorijalna Podrška')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'{stranka}_teritorijalna_podrska.png')

    # Grafički prikaz dodjela mandati po jedinici za svaki dan korištenjem složenih stupčanih dijagrama s oznakama koje prikazuju samo broj mandata po jedinici
    fig, axs = plt.subplots(broj_jedinica, 1, figsize=(10, 12))

    for i, jedinica in enumerate(teritorijalna_podrska['Stranka A']['Dani'][1].keys()):
        ax = axs[i]
        ax.set_title(f"Dodjela mandata za {jedinica}")
        dno = [0] * trajanje_kampanje
        rukovati = []
        oznake = []
        for stranka in stranke:
            mandati_jedinice = []
            for dan in range(1, trajanje_kampanje + 1):
                glasovi_jedinice = {p: teritorijalna_podrska[p]['Dani'][dan][jedinica] for p in stranke}
                dnevna_mandati_jedinice = dhont(broj_mandati, glasovi_jedinice)
                mandati_jedinice.append(dnevna_mandati_jedinice[stranka])
            stupci = ax.bar(range(1, trajanje_kampanje + 1), mandati_jedinice, bottom=dno)
            # Dodaj oznake svakom stupcu u dijagramu prikazujući samo broj mandata po jedinici
            for j, stupac in enumerate(stupci):
                visina_stupca = stupac.get_height()
                ax.annotate(f'{mandati_jedinice[j]}', xy=(stupac.get_x() + stupac.get_width() / 2, dno[j] + visina_stupca / 2),
                            xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')
            # Ažuriraj dno pozicija za sljedeću stranku
            dno = [d + s for d, s in zip(dno, mandati_jedinice)]
            rukovati.append(stupci[0])
            oznake.append(stranka)
        ax.set_xlabel('Dan')
        ax.set_ylabel('Mandati')
        # Dodaj legendu
        ax.legend(rukovati, oznake, loc='upper right')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.6)
    plt.savefig('dodjela_mandata.png')

    # Ukupan broj osvojenih mandata za svaku stranku
    ukupna_mandati = {stranka: 0 for stranka in stranke}
    posljednji_dan = trajanje_kampanje

    # Petlja kroz svaku stranku i svaku jedinicu kako bi se zbrojila osvojena mandati
    for stranka in stranke:
        for jedinica in teritorijalna_podrska[stranka]['Dani'][posljednji_dan]:
            glasovi_jedinice = {p: teritorijalna_podrska[p]['Dani'][posljednji_dan][jedinica] for p in stranke}
            mandati_jedinice = dhont(broj_mandati, glasovi_jedinice)
            ukupna_mandati[stranka] += mandati_jedinice[stranka]

    # Konačan rezultat izbora za svaku stranku
    plt.figure(figsize=(8, 6))
    bars = plt.bar(stranke, [ukupna_mandati[stranka] for stranka in stranke], color=['blue', 'orange', 'green', 'red'] )
    plt.xlabel('Stranka')
    plt.ylabel('Ukupno mandata')
    plt.title('Konačni rezultat izbora')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom')

    plt.savefig('konačni_rezultat.png')

    # Početnu teritorijalna podrška za svaku stranku na prvom danu
    pocetna_podrska = {stranka: [] for stranka in stranke}
    for stranka in stranke:
        for jedinica in teritorijalna_podrska[stranka]['Dani'][1]:
            pocetna_podrska[stranka].append(teritorijalna_podrska[stranka]['Dani'][1][jedinica])

    # Prikaz početne teritorijalne podrške za svaku stranku
    plt.figure(figsize=(10, 6))
    plt.bar(stranke, [sum(pocetna_podrska[stranka]) for stranka in stranke], color=['blue', 'orange', 'green', 'red'])
    plt.xlabel('Stranka')
    plt.ylabel('Teritorijalna podrška')
    plt.title('Početna teritorijalna podrška po strankama')
    plt.savefig('pocetna_podrska.png')
    
    # Primjer:
    print("Simulacija je pokrenuta!")
    display_text(screen, "Rezultati su spremljeni kao slike u Vašem folderu.", font, (0, 0, 0), (WIDTH // 2, 400))

# Stvaranje prozora
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulacija Kampanje")

clock = pygame.time.Clock()

running = True
text_duration_rect = pygame.Rect(50, 50, BUTTON_WIDTH * 3 + BUTTON_MARGIN, BUTTON_HEIGHT)  # Dodan BUTTON_MARGIN
button_increase_duration_rect = pygame.Rect(50 + BUTTON_WIDTH * 3 + BUTTON_MARGIN * 2, 50, BUTTON_WIDTH, BUTTON_HEIGHT)  # Dodan BUTTON_MARGIN * 2
button_decrease_duration_rect = pygame.Rect(50 + BUTTON_WIDTH * 4 + BUTTON_MARGIN * 3, 50, BUTTON_WIDTH, BUTTON_HEIGHT)  # Dodan BUTTON_MARGIN * 3
text_units_rect = pygame.Rect(50, 150, BUTTON_WIDTH * 3 + BUTTON_MARGIN, BUTTON_HEIGHT)  # Dodan BUTTON_MARGIN
button_increase_units_rect = pygame.Rect(50 + BUTTON_WIDTH * 3 + BUTTON_MARGIN * 2, 150, BUTTON_WIDTH, BUTTON_HEIGHT)  # Dodan BUTTON_MARGIN * 2
button_decrease_units_rect = pygame.Rect(50 + BUTTON_WIDTH * 4 + BUTTON_MARGIN * 3, 150, BUTTON_WIDTH, BUTTON_HEIGHT)  # Dodan BUTTON_MARGIN * 3
text_seats_rect = pygame.Rect(50, 250, BUTTON_WIDTH * 3 + BUTTON_MARGIN, BUTTON_HEIGHT)  # Dodan BUTTON_MARGIN
button_increase_seats_rect = pygame.Rect(50 + BUTTON_WIDTH * 3 + BUTTON_MARGIN * 2, 250, BUTTON_WIDTH, BUTTON_HEIGHT)  # Dodan BUTTON_MARGIN * 2
button_decrease_seats_rect = pygame.Rect(50 + BUTTON_WIDTH * 4 + BUTTON_MARGIN * 3, 250, BUTTON_WIDTH, BUTTON_HEIGHT)  # Dodan BUTTON_MARGIN * 3
button_start_rect = pygame.Rect(50, 400, BUTTON_WIDTH * 6 + BUTTON_MARGIN * 5, BUTTON_HEIGHT)  # Dodan BUTTON_MARGIN * 5

while running:
    screen.fill(BG_COLOR)

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_increase_duration_rect.collidepoint(mouse_pos):
                trajanje_kampanje += 1
            elif button_decrease_duration_rect.collidepoint(mouse_pos):
                trajanje_kampanje = max(1, trajanje_kampanje - 1)
            elif button_increase_units_rect.collidepoint(mouse_pos):
                broj_jedinica += 1
            elif button_decrease_units_rect.collidepoint(mouse_pos):
                broj_jedinica = max(1, broj_jedinica - 1)
            elif button_increase_seats_rect.collidepoint(mouse_pos):
                broj_mandati += 1
            elif button_decrease_seats_rect.collidepoint(mouse_pos):
                broj_mandati = max(1, broj_mandati - 1)
            elif button_start_rect.collidepoint(mouse_pos):
                start_simulation(screen)

    display_text(screen, f"Trajanje kampanje: {trajanje_kampanje}", font, (0, 0, 0), text_duration_rect.center)
    draw_button(screen, "+", font, BUTTON_COLOR, button_increase_duration_rect, button_increase_duration_rect.collidepoint(mouse_pos))
    draw_button(screen, "-", font, BUTTON_COLOR, button_decrease_duration_rect, button_decrease_duration_rect.collidepoint(mouse_pos))

    display_text(screen, f"Broj jedinica: {broj_jedinica}", font, (0, 0, 0), text_units_rect.center)
    draw_button(screen, "+", font, BUTTON_COLOR, button_increase_units_rect, button_increase_units_rect.collidepoint(mouse_pos))
    draw_button(screen, "-", font, BUTTON_COLOR, button_decrease_units_rect, button_decrease_units_rect.collidepoint(mouse_pos))

    display_text(screen, f"Broj mandata: {broj_mandati}", font, (0, 0, 0), text_seats_rect.center)
    draw_button(screen, "+", font, BUTTON_COLOR, button_increase_seats_rect, button_increase_seats_rect.collidepoint(mouse_pos))
    draw_button(screen, "-", font, BUTTON_COLOR, button_decrease_seats_rect, button_decrease_seats_rect.collidepoint(mouse_pos))

    draw_button(screen, "Pokreni simulaciju", font, BUTTON_COLOR, button_start_rect, button_start_rect.collidepoint(mouse_pos))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()