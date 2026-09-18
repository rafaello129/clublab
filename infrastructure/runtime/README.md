# Runtime contract

Runtime data does **not** live in Git.

Expected server location:

```text
/home/tulum/infra/clublab/runtime/
├── gateway.env
├── teams/
│   ├── team01.env
│   ├── team02.env
│   └── ...
├── secrets/
│   ├── team01-recovery.token
│   └── ...
├── state/
│   ├── team01.json
│   └── spare.json
└── audit/
    └── clublabctl.jsonl
```

Permissions:

```text
runtime/          0700
teams/            0700
secrets/          0700
*.env             0600
*.token           0600
state/*.json      0600
audit/*.jsonl     0600
```

Templates are stored in `infrastructure/templates/`.

## Generation ID

Every class deployment should use a non-secret generation identifier such as:

```text
2026-09-CLUBLAB01-A
```

It can be recorded in audit/state without exposing credentials.

## Important

`clublabctl deploy` does not generate secrets automatically in v1.

Runtime files must already exist and pass preflight. This avoids silently creating weak defaults or changing class credentials during a deployment.
