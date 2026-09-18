# clublabctl

Instructor-side control plane for ClubLab.

## Implemented

```bash
python3 scripts/clublabctl/clublabctl.py version

python3 scripts/clublabctl/clublabctl.py inventory list
python3 scripts/clublabctl/clublabctl.py inventory show team01
python3 scripts/clublabctl/clublabctl.py inventory validate

python3 scripts/clublabctl/clublabctl.py scenario status team01
python3 scripts/clublabctl/clublabctl.py scenario load team01 ranking-db-failure
python3 scripts/clublabctl/clublabctl.py scenario load team01 api-down
python3 scripts/clublabctl/clublabctl.py scenario clear team01

python3 scripts/clublabctl/clublabctl.py recover team01
python3 scripts/clublabctl/clublabctl.py reset team01 --yes
```

For all deployed teams:

```bash
python3 scripts/clublabctl/clublabctl.py scenario load all ranking-db-failure
python3 scripts/clublabctl/clublabctl.py scenario clear all
```

Destructive global reset additionally requires:

```bash
python3 scripts/clublabctl/clublabctl.py reset all --yes --confirm RESET-ALL
```

## Still reserved for Block C

```text
preflight
deploy
status
resources
logs
spare
audit
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

## Safety

The control plane validates team inventory, Docker labels, project prefixes and resettable volume names.

It never uses:

```text
shell=True
docker system prune
docker volume prune
docker network prune
```

Recovery does not perform an automatic reset.
