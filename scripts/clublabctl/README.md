# clublabctl

Instructor-side control plane for ClubLab.

## Implemented

### Inventory

```bash
python3 scripts/clublabctl/clublabctl.py version
python3 scripts/clublabctl/clublabctl.py inventory list
python3 scripts/clublabctl/clublabctl.py inventory show team01
python3 scripts/clublabctl/clublabctl.py inventory validate
```

### Preflight, deploy and smoke

```bash
python3 scripts/clublabctl/clublabctl.py preflight
python3 scripts/clublabctl/clublabctl.py preflight team01

python3 scripts/clublabctl/clublabctl.py deploy
python3 scripts/clublabctl/clublabctl.py deploy team01

python3 scripts/clublabctl/clublabctl.py smoke
python3 scripts/clublabctl/clublabctl.py smoke team01
```

### Observation

```bash
python3 scripts/clublabctl/clublabctl.py status
python3 scripts/clublabctl/clublabctl.py status team01

python3 scripts/clublabctl/clublabctl.py resources
python3 scripts/clublabctl/clublabctl.py logs team01 api --lines 100
```

### Scenarios

```bash
python3 scripts/clublabctl/clublabctl.py scenario status team01
python3 scripts/clublabctl/clublabctl.py scenario load team01 ranking-db-failure
python3 scripts/clublabctl/clublabctl.py scenario load team01 api-down
python3 scripts/clublabctl/clublabctl.py scenario clear team01
```

For all deployed teams:

```bash
python3 scripts/clublabctl/clublabctl.py scenario load all ranking-db-failure
python3 scripts/clublabctl/clublabctl.py scenario clear all
```

### Recovery and reset

```bash
python3 scripts/clublabctl/clublabctl.py recover team01
python3 scripts/clublabctl/clublabctl.py reset team01 --yes
```

Global reset requires:

```bash
python3 scripts/clublabctl/clublabctl.py reset all --yes --confirm RESET-ALL
```

### Spare

```bash
python3 scripts/clublabctl/clublabctl.py spare status
python3 scripts/clublabctl/clublabctl.py spare assign team03
python3 scripts/clublabctl/clublabctl.py spare release
```

### Audit

```bash
python3 scripts/clublabctl/clublabctl.py audit tail --lines 30
```

## Runtime state

Default:

```text
/home/tulum/infra/clublab/runtime
```

Override for development/testing:

```bash
--runtime-dir /path/to/runtime
```

Runtime tree:

```text
runtime/
├── gateway.env
├── teams/
│   └── teamXX.env
├── secrets/
├── state/
│   ├── teamXX.json
│   └── spare.json
└── audit/
    └── clublabctl.jsonl
```

Templates live in:

```text
infrastructure/templates/
```

Expected permissions:

```text
runtime/teams       0700
runtime/secrets     0700
team env files      0600
state files         0600
audit file          0600
```

## Safety

The control plane validates:

```text
team inventory
Docker labels
project prefixes
published ports
IPAM
container hardening
resettable volume names
runtime secret permissions
APP network ownership
gateway ownership
```

It never uses:

```text
shell=True
docker system prune
docker volume prune
docker network prune
```

Recovery does not perform an automatic reset. Deploy does not reset existing data.

## Deployment contract

`deploy` expects real implementation artifacts:

```text
infrastructure/compose/team.compose.yml
infrastructure/compose/gateway.compose.yml
runtime/teams/teamXX.env
runtime/gateway.env
pinned application images
```

Until those exist, preflight/deploy intentionally fail closed.

## Tests

```bash
python -m unittest discover -s tests/operation -v
```

GitHub Actions runs the same operation suite on relevant changes.
