# Návod na manuální mapování zemí

## Jak to funguje

Na zeměkouli je nyní vytvořena **mřížka šedých bodů** (každých 15° latitude/longitude).

Tyto body můžeš **kliknout** a přiřadit jim název země.

## Postup

1. **Otevři stránku:** https://zemepis.roth1.cz
2. **Otevři Developer Console:** Stiskni `F12` (nebo Ctrl+Shift+I)
3. **Otoč zeměkouli** na zemi kterou chceš přiřadit
4. **Klikni na šedý bod** co nejblíže středu té země
5. **Zobrazí se prompt** - zadej název země (např. "Česká republika")
6. **Bod zčerná** = přiřazeno!
7. **Opakuj** pro všechny země které potřebuješ

## Šedé body
- **Šedé (0.6 opacity)** = nepřiřazené
- **Černé (1.0 opacity)** = přiřazené
- **Červené** = pod myší (hover)

## Export dat

Když máš hotovo všechny země:

1. **Klikni na libovolný bod**
2. **Do promptu zadej:** `export`
3. **Data se exportují do Console** (F12)
4. **Zkopíruj JSON** z konzole
5. **Pošli mi ten JSON** a já ho použiju v projektu!

## Tipy

- Nejdřív přiřaď hlavní země (USA, Čína, Rusko, Brazílie, atd.)
- Pak menší země v Evropě
- Můžeš přiřadit i několik bodů pro velké země
- V konzoli vidíš průběžný počet přiřazených zemí

## Příklad výstupu

```json
[
  {
    "name": "Česká republika",
    "lat": 45,
    "lon": 15,
    "theta": 0.2617,
    "phi": 0.7853
  },
  {
    "name": "USA",
    "lat": 45,
    "lon": -90,
    "theta": -1.5707,
    "phi": 0.7853
  }
]
```

## Poznámky

- Celkem je na zeměkouli **~144 bodů** (12 lat × 12 lon)
- Nemusíš přiřadit všechny, jen ty důležité země
- Data pak použijeme pro zobrazení volebních výsledků
