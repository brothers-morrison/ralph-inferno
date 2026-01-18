# /ralph:review - Review Ralph's work

Check if Ralph is done and review the results.

## Usage
```
/ralph:review
/ralph:review --tunnel   # Also open SSH tunnel for testing
```

## Instructions

**STEG 1: KOLLA OM RALPH KÖR**

```bash
ssh ralph@$(cat ~/.ralph-vm | grep VM_IP | cut -d= -f2) 'pgrep -f "ralph.sh|claude" && echo "RUNNING" || echo "NOT_RUNNING"'
```

Om RUNNING:
```
⏳ Ralph kör fortfarande på VM!

Följ progress:
  ssh ralph@VM_IP 'tail -f ~/projects/REPO/ralph-deploy.log'

Kom tillbaka när Ralph är klar.
```
STOPPA HÄR - ge inte fler alternativ.

Om NOT_RUNNING → fortsätt till steg 2.

**STEG 2: KOLLA RESULTAT**

```bash
# Hämta senaste från VM
source ~/.ralph-vm
ssh $VM_USER@$VM_IP "cd ~/projects/$(basename $(git remote get-url origin) .git) && git log --oneline -10"
```

Visa:
- Antal commits Ralph gjorde
- Vilka specs som kördes

**STEG 3: PULL CHANGES**

```bash
git pull origin main
```

**STEG 4: LISTA PRs (om några)**

```bash
gh pr list
```

**STEG 5: ÖPPNA TUNNEL (om --tunnel)**

```bash
# Öppna SSH tunnel för att testa appen
ssh -L 5173:localhost:5173 -L 54321:localhost:54321 $VM_USER@$VM_IP
```

Visa:
```
🔗 Tunnlar öppna!
- App: http://localhost:5173
- Supabase: http://localhost:54321

Tryck Ctrl+C för att stänga tunnlarna.
```
