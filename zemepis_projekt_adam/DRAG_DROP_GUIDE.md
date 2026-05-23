# Návod: Drag & Drop pro úpravu pozic zemí

## Co jsem udělal

### 1. Upravené pozice
- ✓ **Indie**: posunuta doleva a dolů (lat: 25°, lon: -110°)
- ✓ **Rusko**: posunuto níž (lat: 65°, lon: -60°)

### 2. Přidané země (celkem 47 zemí!)
Z původních 10 zemí jsem vypočítal pozice pro další státy:

**Evropa:** Česká republika, Slovensko, Německo, Francie, Itálie, Španělsko, Velká Británie, Polsko, Ukrajina, Turecko, Švédsko, Norsko, Finsko, Rakousko, Švýcarsko

**Asie:** Japonsko, Jižní Korea, Thajsko, Vietnam, Filipíny, Indonésie, Saúdská Arábie, Írán, Pákistán

**Amerika:** Mexiko, Argentina, Chile, Peru, Kolumbie, Venezuela

**Afrika:** Egypt, Jižní Afrika, Nigérie, Keňa

**Oceánie:** Nový Zéland

### 3. Drag & Drop funkce

## Jak používat

### Posun bodů (Drag & Drop)
1. **Najdi bod** který chceš posunout
2. **Stiskni a drž** levé tlačítko myši na bodu
3. **Přetáhni** bod na správné místo
4. **Pusť** tlačítko myši
5. **V konzoli** (F12) uvidíš novou pozici: `✓ Posunuto: Česká republika → lat=XX°, lon=YY°`

**Tipy:**
- Při draggingu se vypne otáčení globu
- Můžeš posunout jakýkoliv bod
- Body se vždy drží na povrchu koule

### Export upravených pozic
1. **Klikni** na libovolný bod
2. **Do promptu zadej:** `export`
3. **Otevři konzoli** (F12)
4. **Zkopíruj celý JSON** (všechno mezi `[` a `]`)
5. **Pošli mi ho**

## Poznámky
- Všechny země jsou na stránce, jen kontroluj jestli jsou na správných místech
- Pokud některá země chybí nebo je špatně, posuň ji
- Export exportuje VŠECHNY země s jejich aktuálními pozicemi
- Pozice jsou zaokrouhleny na 2 desetinná místa

## Co dělat teď
1. Refresh stránky: https://zemepis.roth1.cz
2. Zkontroluj všechny země (otáčej globem)
3. Posuň ty které jsou špatně
4. Když máš hotovo, klikni na bod a zadej "export"
5. Pošli mi JSON
