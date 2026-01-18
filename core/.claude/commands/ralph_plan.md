# /ralph:plan - Create Implementation Plan

Analyze PRD and create implementation plan with executable specs.

## Usage
```
/ralph:plan
```

## Prerequisites
- `docs/prd.md` must exist (run `/ralph:discover` first)

## Output
- `docs/IMPLEMENTATION_PLAN.md` - Översikt med epics och tasks
- `specs/*.md` - Körbara spec-filer för varje task (detta kör Ralph på VM)

## Instructions

Läs `docs/prd.md` och skapa en implementation plan.

**FAS 1: ANALYSERA PRD**
1. Läs `docs/prd.md` noggrant
2. Identifiera alla features och krav
3. Gruppera till logiska epics

**FAS 2: SKAPA IMPLEMENTATION_PLAN.md**

Skapa filen med denna struktur:

```markdown
# IMPLEMENTATION_PLAN.md

## Epics Overview

| Epic | Namn | Status |
|------|------|--------|
| E1 | {namn} | pending |
| E2 | {namn} | pending |

## Tasks

### Kritisk (E1: {epic-namn})
- [ ] T1: {Specifik task}
- [ ] T2: {Task}
- [ ] **HARD STOP** - Verifiera grundflöde fungerar

### Hög (E2: {epic-namn})
- [ ] T3: {Task}
- [ ] T4: {Task}

### Låg
- [ ] T5: {Task}

---

## Progress

| Datum | Task | Resultat |
|-------|------|----------|

---

## Learnings

| Problem | Lärdom |
|---------|--------|

---

## Blocked
```

**FAS 3: SKAPA SPEC-FILER (OBLIGATORISKT)**

Skapa ALLTID körbara spec-filer i `specs/`. Detta är vad Ralph kör på VM.

> **Templates:** Se `templates/SPEC-template.md` och `templates/specs/01-project-setup.md`

```
specs/
├── 01-project-setup.md   ← MÅSTE inkludera Playwright!
├── 02-database-schema.md
├── 03-auth-context.md
├── 04-login-page.md
└── ...
```

**KRITISKT - 01-project-setup MÅSTE innehålla:**
- Vite + React + TypeScript setup
- Tailwind med design tokens från PRD
- **Playwright installation** (`npx playwright install`)
- `playwright.config.ts`
- `e2e/smoke.spec.ts`

> ⚠️ Utan Playwright fungerar inte Ralph's test-loop!

**Spec-fil format (MINIMALT för liten context window):**
```markdown
# {Task-namn}

{1-2 meningar vad som ska byggas}

## Krav
- {Konkret krav 1}
- {Konkret krav 2}

## E2E Test
Skriv test i `e2e/{feature}.spec.ts` som verifierar:
- {vad testet ska kolla}

## Klart när
- [ ] `npm run build` passerar
- [ ] E2E-test passerar
- [ ] {Specifik verifiering}
```

**VIKTIGT - HÅLL SPECS MINIMALA:**
- MAX 20 rader per spec
- Ingen bakgrund/kontext - Claude läser koden
- Inga implementation-detaljer - Claude vet hur
- Bara VAD, inte HUR
- En spec = en fokuserad uppgift

**EXEMPEL PÅ BRA SPEC:**
```markdown
# Auth Context

Skapa React context för autentisering med Supabase.

## Krav
- AuthProvider wrappare
- useAuth hook (user, signIn, signOut)
- Automatisk session-refresh

## Klart när
- [ ] `npm run build` passerar
- [ ] Kan logga in/ut via hook
```

**EXEMPEL PÅ DÅLIG SPEC (för lång):**
```markdown
# Auth Context

## Bakgrund
Autentisering är viktigt för...
[10 rader kontext]

## Implementation
1. Skapa src/contexts/AuthContext.tsx
2. Importera createContext från react
3. ...
[20 rader implementation-detaljer]
```

**REGLER:**
- En task = en mening utan "och"
- HARD STOP mellan prioritetsnivåer
- Kritiska blockerare först
- Tasks grupperade under sin epic

**NÄR KLAR:**
Skriv:
```
PLANNING_DONE

Nästa: Kör /ralph:deploy för att skicka till VM och starta bygget
```
