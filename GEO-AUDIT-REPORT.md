# GEO Audit Report: Global Consult

**Audit Date:** 2026-07-09
**URL:** https://global-consult.ro/
**Business Type:** Agency/Services
**Pages Analyzed:** 3

---

## Executive Summary

**Overall GEO Score: 54/100 (Poor)**

Global Consult are o bază tehnică foarte bună, cu acces corect configurat pentru boții AI și un marcaj schema.org (`ProfessionalService`) solid. Totuși, scorul GEO este tras în jos de lipsa de profunzime a conținutului, absența dovezilor concrete de expertiză (E-E-A-T) și a unui fișier `llms.txt`. Site-ul acționează ca o broșură digitală sumară, ceea ce face improbabil ca sistemele AI (ChatGPT, Perplexity, Claude) să citeze sau să recomande activ serviciile firmei în răspunsurile lor.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 50/100 | 25% | 12.5 |
| Brand Authority | 40/100 | 20% | 8.0 |
| Content E-E-A-T | 45/100 | 20% | 9.0 |
| Technical GEO | 85/100 | 15% | 12.75 |
| Schema & Structured Data | 80/100 | 10% | 8.0 |
| Platform Optimization | 40/100 | 10% | 4.0 |
| **Overall GEO Score** | | | **54/100** |

---

## Critical Issues (Fix Immediately)

- **Absența dovezilor de expertiză (E-E-A-T):** Nu există secțiuni dedicate echipei (consultanții seniori), certificărilor sau istoricului profesional. Sistemele AI au nevoie de aceste date pentru a valida "Expertiza" și "Autoritatea" firmei. *Recomandare: Adaugă o secțiune "Echipă" cu biografii și linkuri către profilurile de LinkedIn pe pagina principală.*

## High Priority Issues

- **Lipsa fișierului `llms.txt`:** Fișierul esențial pentru furnizarea de conținut structurat direct către LLM-uri lipsește. *Recomandare: Creează `public/llms.txt` cu o descriere clară în format Markdown a serviciilor, metodologiei și expertizei firmei.*
- **Conținut prea "subțire" (Thin Content):** Lipsesc articolele de thought leadership, studiile de caz (case studies) și răspunsurile la întrebări specifice industriei. *Recomandare: Transformă serviciile în pagini dedicate sau adaugă studii de caz detaliate care prezintă problema, soluția și rezultatele (Metrici).*

## Medium Priority Issues

- **Lipsa marcatului Schema FAQPage:** Există un placeholder HTML (`<!-- GEO_FAQ_PLACEHOLDER -->`), dar nu și conținutul propriu-zis. *Recomandare: Adaugă o secțiune de Întrebări Frecvente (FAQ) pe pagină și implementează schema.org de tip `FAQPage`.*
- **Lipsa "Social Proof":** Nu există testimoniale sau logo-uri ale clienților anteriori. *Recomandare: Adaugă recenzii de la clienți și folosește schema `Review` sau `AggregateRating`.*

## Low Priority Issues

- **Prezență slabă pe platforme terțe:** Lipsesc linkurile vizibile (footer/header) către conturile de social media ale companiei (în special LinkedIn, esențial pentru B2B). *Recomandare: Include linkuri către pagina de companie LinkedIn.*

---

## Category Deep Dives

### AI Citability (50/100)
Conținutul actual este concis și bine structurat cu tag-uri H1/H2/H3, ceea ce este un plus. Totuși, textele sunt exclusiv orientate spre vânzare/prezentare. Sistemele AI citează de obicei "Cum se face", date statistice, metodologii unice sau rezolvări la probleme. Metodologia (Diagnosticare, Proiectare, Implementare, Scalare) este bună, dar prea scurtă pentru a oferi substanță unui LLM.

### Brand Authority (40/100)
Fără pagini de echipă, studii de caz externe sau mențiuni de brand cross-platform, autoritatea de brand pentru recunoașterea entităților (Entity Recognition) de către AI este redusă. Firma trebuie să fie menționată în publicații de business sau pe LinkedIn pentru a crește acest scor.

### Content E-E-A-T (45/100)
Deși se promite "Consultanță senior", lipsa identității autorilor și a credențialelor scade dramatic scorul de E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness). AI-ul nu poate verifica cine stă în spatele acestor servicii.

### Technical GEO (85/100)
Infrastructura este excelentă. Fișierul `robots.txt` este perfect configurat pentru boții AI (permite explicit `Google-Extended`, `GPTBot`, `ClaudeBot`, `PerplexityBot`, `OAI-SearchBot`). Site-ul se încarcă rapid, oferind și meta tag-uri complete (inclusiv Open Graph și Twitter Cards). Singura piesă tehnică lipsă este `llms.txt`.

### Schema & Structured Data (80/100)
Marcajul JSON-LD existent pentru `ProfessionalService` este de foarte bună calitate (include `areaServed`, `serviceType`, `knowsAbout`, date de contact bilingve). Adăugarea schemelor pentru `FAQPage` și `Person` ar aduce acest scor aproape de 100.

### Platform Optimization (40/100)
Site-ul nu este optimizat pentru platformele de referință (ex: răspunsuri detaliate pentru Perplexity, ghiduri pas cu pas pentru ChatGPT). Optimizarea B2B necesită prezență puternică pe platformele profesionale.

---

## Quick Wins (Implement This Week)

1. **Adaugă `llms.txt`:** Creează un fișier text în root care explică detaliat compania, serviciile și expertiza pentru crawlerele LLM.
2. **Implementează Secțiunea FAQ:** Completează placeholder-ul existent pe site cu 5 întrebări frecvente din industrie și adaugă JSON-LD pentru `FAQPage`.
3. **Adaugă Profilurile Echipei:** Listează numele și scurtele biografii ale consultanților seniori direct pe homepage, cu linkuri de LinkedIn.
4. **Adaugă Linkuri Sociale:** Pune link către pagina de companie LinkedIn în footer.
5. **Logo-uri Clienți:** Adaugă 3-4 logo-uri ale clienților reprezentativi pentru a spori încrederea.

## 30-Day Action Plan

### Week 1: E-E-A-T & Technical Basics
- [ ] Creează și publică fișierul `llms.txt` în folderul `public/`.
- [ ] Adaugă secțiunea cu biografii pentru echipa de management/consultanți pe homepage.
- [ ] Integrează linkurile către profilurile oficiale de LinkedIn (Companie + Consultanți).

### Week 2: Schema & Social Proof
- [ ] Redactează 5 întrebări/răspunsuri (FAQ) despre serviciile de consultanță și metodologie.
- [ ] Integrează marcajul schema.org `FAQPage` pentru aceste întrebări.
- [ ] Obține și adaugă 2 testimoniale de la foști clienți.

### Week 3: Content Depth
- [ ] Redactează primul Studiu de Caz detaliat (Problemă, Soluție, Rezultate Măsurabile).
- [ ] Publică studiul de caz fie pe homepage, fie pe o pagină separată.

### Week 4: Brand Authority Distribution
- [ ] Distribuie studiul de caz pe LinkedIn (profil personal și companie).
- [ ] Asigură-te că `sitemap.xml` este actualizat și re-trimis.

---

## Appendix: Pages Analyzed

| URL | Title | GEO Issues |
|---|---|---|
| / | Global Consult \| Consultanță strategică pentru companii | 4 (Missing E-E-A-T, No FAQ, Thin Content, No llms.txt) |
| /politica-confidentialitate.html | Politica de confidențialitate \| Global Consult | 0 |
| /politica-cookies.html | Politica de cookies \| Global Consult | 0 |
