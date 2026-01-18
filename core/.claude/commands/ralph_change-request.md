# /ralph:change-request - Create Change Request from Testing

Document bugs and issues found during testing, generate new specs for Ralph to fix.

## Usage
```
/ralph:change-request
```

## Prerequisites
- App has been built by Ralph (`/ralph:deploy` completed)
- Testing has been done (`/ralph:review` completed)
- Issues/bugs have been identified

## Output
- `docs/CHANGE_REQUEST.md` - Dokumentation av problem
- `specs/CR-*.md` - Nya spec-filer för fixes

## Instructions

**FAS 1: SAMLA IN PROBLEM**

Fråga användaren:
```
🔍 Change Request

Beskriv problemen du hittade under testning:
1. Vad fungerade inte som förväntat?
2. Vilka features saknas eller är ofullständiga?
3. Några UI/UX-problem?

Klistra in dina observationer:
```

Vänta på användarens input.

**FAS 2: KATEGORISERA PROBLEM**

Analysera input och kategorisera:

1. **BUGS** - Saker som är trasiga/fel
2. **INCOMPLETE** - Påbörjat men inte klart
3. **MISSING** - Saknas helt trots att det var i spec
4. **ENHANCEMENT** - Förbättringar utöver original-spec

**FAS 3: SKAPA CHANGE_REQUEST.md**

Skapa `docs/CHANGE_REQUEST.md`:

```markdown
# Change Request - [DATUM]

## Sammanfattning
{1-2 meningar om vad som hittades}

## Kategorier

### 🐛 Bugs
| # | Problem | Påverkar | Prioritet |
|---|---------|----------|-----------|
| B1 | {beskrivning} | {feature} | HIGH/MED/LOW |

### ⚠️ Incomplete
| # | Feature | Status | Saknas |
|---|---------|--------|--------|
| I1 | {feature} | {%} | {vad} |

### ❌ Missing
| # | Feature | Spec-referens |
|---|---------|---------------|
| M1 | {feature} | {original-spec} |

### 💡 Enhancements (Optional)
| # | Förslag | Värde |
|---|---------|-------|
| E1 | {förslag} | {värde} |

---

## Ursprungliga Specs
{Lista vilka specs som kördes}

## Testing Done
{Sammanfattning av testning}
```

**FAS 4: GENERERA NYA SPECS**

Skapa nya spec-filer för varje problem:

```
specs/
├── CR-01-fix-{bug}.md
├── CR-02-complete-{feature}.md
└── CR-03-add-{missing}.md
```

**Spec-format för fixes:**
```markdown
# CR-XX: {Kortfattad beskrivning}

{Problem}: {Vad som är fel}
{Fix}: {Vad som ska göras}

## Krav
- {Konkret krav 1}
- {Konkret krav 2}

## Klart när
- [ ] `npm run build` passerar
- [ ] {Specifik verifiering av fix}
- [ ] Regression: {existerande funktionalitet fungerar}
```

**VIKTIGT:**
- Håll specs MINIMALA (max 15 rader)
- En spec = ett problem
- Inkludera regression-test i "Klart när"
- CR-specs körs EFTER original-specs

**FAS 5: UPPDATERA IMPLEMENTATION_PLAN.md**

Lägg till CR-tasks i `docs/IMPLEMENTATION_PLAN.md`:

```markdown
## Change Request Tasks

### CR-Fixes (Prioritet: Kritisk)
- [ ] CR-01: {fix}
- [ ] CR-02: {fix}
- [ ] **HARD STOP** - Verifiera alla CR-fixes

### CR-Enhancements (Prioritet: Låg)
- [ ] CR-03: {enhancement}
```

**NÄR KLAR:**
```
CHANGE_REQUEST_DONE

Skapade:
- docs/CHANGE_REQUEST.md
- X nya specs i specs/CR-*.md

Nästa: Kör /ralph:deploy för att skicka CR-specs till VM
```
