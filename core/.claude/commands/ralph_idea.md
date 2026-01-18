# /ralph:idea - Start Discovery Loop

Autonom utforskning av en produktidé från alla vinklar med web research.

## Usage
```
/ralph:idea "Din produktidé här"
```

## Instructions

**DU SKA KÖRA EN AUTONOM DISCOVERY LOOP**

Utforska idén genom att växla mellan roller. Använd WebSearch aktivt för research.
Iterera tills PRD är komplett och alla frågor besvarade.

---

**FAS 1: INITIAL RESEARCH (Analyst)**

```
🔍 ANALYST MODE
```

1. WebSearch: Sök efter liknande produkter/tjänster
2. WebSearch: Sök efter potentiella integrationer (API:er)
3. Identifiera konkurrenter och deras styrkor/svagheter
4. Dokumentera marknadsstorlek om möjligt

Skriv ner findings i sektion: `## Market Research`

---

**FAS 2: ANVÄNDARE & FLÖDEN (UX)**

```
👤 UX MODE
```

1. Definiera 2-3 personas (vem är användarna?)
2. Skissa huvudsakliga user flows
3. Identifiera kritiska interaktionspunkter
4. Tänk på onboarding-flödet

Skriv ner i sektioner: `## Target Users & Personas`, `## User Flows`

---

**FAS 3: SCOPE & PRIORITERING (PM)**

```
📋 PM MODE
```

1. Lista alla potentiella features
2. Prioritera: Vad är MVP? Vad kan vänta?
3. Definiera "done" för MVP
4. Identifiera risker och beroenden

Skriv ner i sektion: `## Core Features (MVP)`, `## Future Features`

---

**FAS 4: TEKNISK DESIGN (Architect)**

```
🏗️ ARCHITECT MODE
```

1. WebSearch: Sök efter relevanta API:er och dokumentation
2. Välj tech stack baserat på requirements
3. Lista alla externa integrationer
4. Identifiera tekniska utmaningar

Skriv ner i sektioner: `## Technical Requirements`, `## Integrations Required`

---

**FAS 5: AFFÄR & JURIDIK (Business)**

```
💼 BUSINESS MODE
```

1. Definiera affärsmodell (hur tjänar vi pengar?)
2. WebSearch: Sök efter juridiska krav (GDPR, PCI-DSS etc)
3. Identifiera compliance-krav
4. Uppskatta kostnader (API:er, hosting)

Skriv ner i sektioner: `## Business Model`, `## Legal/Compliance`

---

**FAS 6: SYNTES & VALIDERING**

```
✅ VALIDATION MODE
```

1. Läs igenom alla sektioner
2. Finns det öppna frågor? → Lägg till i `## Open Questions`
3. Finns det konflikter mellan sektioner? → Lös dem
4. Är tech stack konsistent med requirements? → Verifiera

**ITERERA** om Open Questions inte är tom:
- Gå tillbaka till relevant roll
- Gör mer research
- Uppdatera sektioner

---

**EXIT CRITERIA**

Loopen är klar när:
- [ ] Alla sektioner har meningsfullt innehåll
- [ ] `## Open Questions` är tom eller innehåller endast "nice-to-have"
- [ ] Tech stack är beslutad och dokumenterad
- [ ] Alla kritiska integrationer är identifierade
- [ ] MVP scope är tydligt definierat

---

**OUTPUT**

Skapa `docs/PRD.md` med följande struktur:

```markdown
# [Produktnamn] - PRD

## Vision & Problem
{Vad löser vi? Varför behövs detta?}

## Market Research
{Konkurrenter, marknad, möjligheter}

## Target Users & Personas
{Vem är användarna? 2-3 personas}

## User Flows
{Huvudsakliga flöden, steg för steg}

## Core Features (MVP)
{Prioriterad lista, vad måste finnas}

## Future Features
{Vad kan vänta till v2?}

## Technical Requirements
{Stack, arkitektur, constraints}

## Integrations Required
{Externa API:er och tjänster}

## Business Model
{Hur tjänar vi pengar?}

## Legal/Compliance
{GDPR, PCI-DSS, andra krav}

## Open Questions
{MÅSTE VARA TOM för att vara klar}
```

---

**NÄR KLAR**

Skriv:
```
DISCOVERY_COMPLETE

PRD sparad till: docs/PRD.md

Nästa steg:
1. Kör /ralph:preflight för att verifiera requirements
2. Kör /ralph:plan för att skapa implementation plan
```
