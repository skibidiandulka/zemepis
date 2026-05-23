# Projekt: Vizualizace Parlamentních Voleb
**URL:** zemepis.roth1.cz
**Datum zahájení:** 25.10.2025

## Přehled projektu
Interaktivní webová aplikace pro grafickou vizualizaci dat z parlamentních voleb. Projekt využívá 3D model zeměkoule pro atraktivní a přehledné zobrazení volebních výsledků.

## Technologie
- **Frontend:** HTML5, CSS3, JavaScript
- **3D grafika:** Three.js r128 (WebGL knihovna)
- **Hosting:** Cloudflare Tunnel
- **Port:** 8080 (testovací), produkce dle Cloudflare nastavení

## Fáze vývoje

### Fáze 1: Základní struktura (DOKONČENO ✓)
- [x] Vytvoření prázdného projektu
- [x] Dokumentační soubor
- [x] HTML stránka s tmavým pozadím (#0a0a0a)
- [x] Implementace 3D zeměkoule (černobílý model)
- [x] Interaktivní ovládání (otáčení myší - OrbitControls)
- [x] Hover efekt s informacemi o zemi (název, počet obyvatel, hlavní město)
- [x] Auto-rotace zeměkoule
- [x] Zoom funkcionalita
- [x] 8 testovacích zemí s daty

### Fáze 2: Data parlamentních voleb (PLÁNOVÁNO)
- Čeká se na data od uživatele
- Integrace volebních dat
- Vizualizace výsledků na mapě

## Struktura projektu
```
zemepis_projekt_adam/
├── PROJEKT_DOKUMENTACE.md  # Tento soubor
├── index.html              # Hlavní stránka
├── css/
│   └── style.css          # Styly
├── js/
│   ├── main.js            # Hlavní aplikační logika
│   └── globe.js           # 3D zeměkoule logika
└── data/
    └── countries.json     # Data o zemích (název, populace, geo)
```

## Jak spustit projekt

### Lokální testování
```bash
cd /home/andulkapilulka/zemepis_projekt_adam
python3 -m http.server 8080
```
Pak otevřete prohlížeč na: `http://localhost:8080`

### Produkční nasazení na Cloudflare Tunnel
✓ NAKONFIGUROVÁNO!

Ingress rule přidáno do `/etc/cloudflared/config.yml`:
```yaml
- hostname: zemepis.roth1.cz
  service: http://127.0.0.1:8080
```

Cloudflared služba restartována. Stránka by měla být dostupná na: `https://zemepis.roth1.cz`

**DŮLEŽITÉ:** Pokud stále vidíš Error 1000, zkontroluj na Cloudflare Dashboard (DNS):
- DNS záznam pro `zemepis.roth1.cz` by NEMĚL existovat (je řízeno tunelem)
- Nebo by měl být typu CNAME s hodnotou: `<tunnel-id>.cfargotunnel.com`
- Proxy status by měl být: "Proxied" (oranžový mráček)

## Funkce aplikace (Fáze 1)
- **3D zeměkoule:** Plně interaktivní 3D model s černobílým designem
- **Otáčení:** Levé tlačítko myši + tažení
- **Zoom:** Kolečko myši (min 2, max 8 jednotek)
- **Auto-rotace:** Automatické pomalé otáčení (rychlost 0.5)
- **Hover efekt:** Při najetí myší na zemi:
  - Zvětšení markeru (1.5x)
  - Změna barvy na červenou (#ff6b6b)
  - Zobrazení info panelu s daty
- **Info panel:** Název země, počet obyvatel, hlavní město

## Poznámky
- **DŮLEŽITÉ:** Projekt je samostatný, nesmí narušit jiné služby na zemepis.roth1.cz
- Tmavé pozadí (#0a0a0a)
- Černobílá zeměkoule s wireframe efektem
- Responzivní design (mobilní i desktop)

## Historie změn

### 26.10.2025 - 20:45 - Finální úpravy: menší body v Evropě, větší zoom
- ✓ Seznam zemí aktualizován na přesných 97 zemí z volebního dokumentu
- ✓ Body v Evropě zmenšeny z 0.015 na 0.008 (50% menší - region lat 35-75, lon -25 až 45)
- ✓ Singapur také zmenšen na 0.008
- ✓ Povolen větší zoom: minDistance změněno z 2 na 1.3 (můžeš zoomovat blíž)
- ✓ Odstraněny země které nejsou v původním seznamu
- ✓ Aktualizovány všechny souřadnice podle uživatelských úprav

### 26.10.2025 - 20:30 - Přidáno 52 nových zemí z volebních dat
- ✓ Přidáno 52 nových zemí z dokumentu Dokument.txt (volební data 2025)
- ✓ Celkem nyní 97 zemí na mapě (původně 45)
- ✓ Nové země z Afriky: Etiopie, Ghana, Konžská dem. rep., Maroko, Senegal, Tunisko, Zambie
- ✓ Nové země z Evropy: Albánie, Belgie, Bělorusko, Bosna a Hercegovina, Bulharsko, Černá Hora, Dánsko, Estonsko, Chorvatsko, Irsko, Kosovo, Kypr, Litva, Lotyšsko, Lucembursko, Maďarsko, Moldavsko, Nizozemsko, Portugalsko, Rumunsko, Řecko, Severní Makedonie, Slovinsko, Srbsko, Vatikán
- ✓ Nové země z Asie: Arménie, Ázerbájdžán, Gruzie, Irák, Izrael, Jordánsko, Kambodža, Katar, Kazachstán, Kuvajt, Libanon, Malajsie, Mongolsko, Myanmar, Singapur, SAE, Sýrie, Tchaj-wan, Uzbekistán
- ✓ Nové země ze S. Ameriky: Kuba
- 📝 Zatím bez volebních dat - jen pozice na mapě

### 26.10.2025 - 20:15 - Finální kalibrace pozic + defaultní rotace 185°
- ✓ Uloženy finálně zkalibrované pozice všech 45 zemí
- ✓ Defaultní rotace textury nastavena na 185° (automaticky se načte)
- ✓ Body přesunuty ze scene místo globe → otáčí se jen textura, ne body
- ✓ Všechny země nyní perfektně sedí na mapě
- 📝 Slider stále funguje pro případné další úpravy

### 26.10.2025 - 19:50 - Přidán slider pro otočení textury + reálné GPS souřadnice
- ✓ Přidán slider v pravém horním rohu pro otočení textury zeměkoule (0-360°)
- ✓ Všechny země mají nyní REÁLNÉ GPS souřadnice (ne manuálně přiřazené)
- ✓ Body jsou nyní správně umístěné podle skutečných geografických pozic
- ✓ Zachováno ovládání bodů šipkami pro případné ruční úpravy
- ✓ Kód pro control panel uložen v CONTROL_PANEL_CODE.md
- 📝 Nyní můžeš otočit texturu sliderem, aby sedla s body

### 26.10.2025 - 19:36 - Zmenšení bodů a aktualizace souřadnic
- ✓ Zmenšeny body na zeměkouli z 0.025 na 0.015 (40% menší)
- ✓ Aktualizovány souřadnice pro 15 zemí (USA, Čína, Rusko, Indie, Brazílie, Kanada, Austrálie, Japonsko, Německo, Francie, UK, Itálie, Španělsko, Polsko, Ukrajina)
- ✓ Změny provedeny v /var/www/zemepis/js/globe.js a /var/www/zemepis/data/countries_averaged.json
- 📝 Lokální test server spuštěn na portu 3000 pro ověření změn

### 25.10.2025 - 20:25 - Manuální mapování zemí
- ✓ Vytvořena mřížka ~144 bodů po celé zeměkouli (každých 15°)
- ✓ Kliknutím na bod lze přiřadit název země
- ✓ Šedé body = nepřiřazené, černé = přiřazené
- ✓ Export funkce - zadej "export" pro získání JSON dat
- ✓ Data pak použijeme místo pevných lat/lon souřadnic
- 📝 Návod: MAPPING_GUIDE.md

### 25.10.2025 - 20:19 - Blank Map - čistá mapa s hranicemi
- ✓ Použita Wikimedia blank world map (equirectangular projection)
- ✓ Pouze černé obrysy kontinentů na bílém pozadí
- ✓ Jednoduchý, minimalistický vzhled
- ✓ Perfektní pro vizualizaci volebních dat

### 25.10.2025 - 20:13 - Politická mapa bez terénu
- ✓ Nahrazena topografická mapa za jednoduchou politickou mapu
- ✓ Pouze obrysy kontinentů a hranice států
- ✓ Bez reliéfu, terénu a topografických detailů
- ✓ Čistý, jednoduchý vzhled pro vizualizaci dat

### 25.10.2025 - 19:37 - Lokální textura zeměkoule
- ✓ Stažena jednoduchá topografická mapa (5400x2700 px)
- ✓ Uložena lokálně v /var/www/zemepis/textures/earth.jpg
- ✓ globe.js upraveno aby používal lokální texturu místo externího URL
- ✓ Řeší problémy s CORS a nedostupnými externími zdroji

### 25.10.2025 - 19:25 - Přidána textura zeměkoule
- ✓ Nahrazena šedá koule za texturu s mapou Země
- ✓ Použita high-res textura z Three.js examples (2048x1024)
- ✓ Odstraněn wireframe overlay
- ✓ Zeměkoule teď vypadá realisticky s kontinenty a oceány

### 25.10.2025 - 19:21 - DNS Route přidána - STRÁNKA FUNGUJE! 🎉
- ✓ Použit příkaz: `cloudflared tunnel route dns roth1-tunnel zemepis.roth1.cz`
- ✓ Cloudflare přidal CNAME záznam který routuje na tunnel
- ✓ HTTP 200 odpověď potvrzena
- ✅ **STRÁNKA JE LIVE: https://zemepis.roth1.cz**

### 25.10.2025 - 19:10 - Apache Virtual Host nakonfigurován
- ✓ Vytvořen Apache virtual host /etc/apache2/sites-available/zemepis.roth1.cz.conf
- ✓ Soubory zkopírovány do /var/www/zemepis
- ✓ Apache naslouchá na 127.0.0.1:8080
- ✓ Python test server zastaven
- ✓ Cloudflare tunnel ingress nakonfigurován (zemepis.roth1.cz → 127.0.0.1:8080)
- ✓ Všechny služby běží: 8080 (zemepis), 8081 (roth1), 8082 (spanelstina)

### 25.10.2025 - 19:03 - Cloudflare Tunnel nakonfigurován
- ✓ Přidáno ingress pravidlo pro zemepis.roth1.cz → port 8080
- ✓ Cloudflared služba restartována

### 25.10.2025 - 18:50 - Fáze 1 dokončena
- ✓ Vytvořena kompletní struktura projektu
- ✓ Implementována 3D zeměkoule s Three.js
- ✓ Přidána interaktivita (otáčení, zoom, hover)
- ✓ 8 testovacích zemí s geografickými daty
- ✓ Info panel s daty o zemích
- ✓ Testovací server spuštěn na portu 8080
