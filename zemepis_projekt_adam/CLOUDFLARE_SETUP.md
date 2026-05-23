# Jak opravit Error 1000 pro zemepis.roth1.cz

## Problém
DNS záznam pro `zemepis.roth1.cz` ukazuje na zakázanou IP, což vytváří smyčku.

## Řešení - 2 metody (zkus METODU 1 nejdřív!)

---

## METODA 1: Přidat route přes Cloudflare Zero Trust (DOPORUČENO)

1. **Přihlas se na:** https://one.dash.cloudflare.com/
2. **Naviguj na:** Zero Trust → Networks → Tunnels
3. **Najdi tunnel:** `roth1-tunnel` (měl by být zelený/aktivní)
4. **Klikni na:** ... (tři tečky) → Configure
5. **V sekci "Public Hostnames":** klikni **Add a public hostname**
6. **Vyplň:**
   - **Subdomain:** `zemepis`
   - **Domain:** `roth1.cz` (vyber z dropdown)
   - **Path:** (nech prázdné)
   - **Type:** HTTP
   - **URL:** `localhost:8080` nebo `127.0.0.1:8080`
7. **Klikni:** Save hostname
8. **Počkej:** 10-30 sekund na propagaci

**Poté:** Zkus přistoupit na https://zemepis.roth1.cz - mělo by to fungovat!

---

## METODA 2: Opravit/Vytvořit DNS záznam ručně

**POUZE pokud METODA 1 nefungovala!**

1. **Přihlas se na:** https://dash.cloudflare.com/
2. **Vyber doménu:** roth1.cz
3. **Jdi na:** DNS → Records
4. **Zkontroluj:** Existuje záznam pro `zemepis`?

### Pokud ANO (už existuje):
   - **Smaž ho** (klikni na něj a Delete)
   - Pokračuj krokem níže "Vytvoř nový CNAME záznam"

### Vytvoř nový CNAME záznam:
   - **Klikni:** Add record
   - **Type:** CNAME
   - **Name:** `zemepis`
   - **Target:** `dd5ad6cf-21b1-4b5b-982d-a22cb6c0821d.cfargotunnel.com`
   - **Proxy status:** Proxied (oranžový mráček) ✓ ZAPNUTO
   - **TTL:** Auto
   - **Klikni:** Save

**Počkej:** 30-60 sekund na propagaci DNS

---

## Ověření

Po nastavení zkus:
```
https://zemepis.roth1.cz
```

Měl by ses vidět tmavou stránku s 3D zeměkoulí!

---

## Info o tunnelu
- **Tunnel ID:** `dd5ad6cf-21b1-4b5b-982d-a22cb6c0821d`
- **Tunnel jméno:** `roth1-tunnel`
- **Status:** ✓ Aktivní (4 připojení: fra07, fra17, 2x prg03)
- **Local port:** 8080
- **Server config:** `/etc/cloudflared/config.yml`

## Další služby na stejném tunnelu
- roth1.cz → localhost:8081
- www.roth1.cz → localhost:8081
- spanelstina.roth1.cz → localhost:8082
- www.spanelstina.roth1.cz → localhost:8082
- **zemepis.roth1.cz → localhost:8080** (NOVÝ)

Všechny tyto služby fungují správně, takže nastavení tunnelu je OK!
