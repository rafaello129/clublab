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

### Preflight and observation

```bash
python3 scripts/clublabctl/clublabctl.py preflight
python3 scripts/clublabctl/clublabctl.py preflight team01

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

## Still reserved for Block D

```text
deploy
```

Block D will connect deployment, smoke tests and the final operational validation matrix.

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
├── teams/
│   └── teamXX.env
├── secrets/
├── state/
│   ├── teamXX.json
│   └── spare.json
└── audit/
    └── clublabctl.jsonl
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
```

It never uses:

```text
shell=True
docker system prune
docker volume prune
docker network prune
```

Recovery does not perform an automatic reset.

## Current infrastructure status

The operation code exists before the real `team.compose.yml`, gateway and application images.

Therefore a real `preflight` is expected to fail until those implementation artifacts are added. This is intentional fail-closed behavior.
