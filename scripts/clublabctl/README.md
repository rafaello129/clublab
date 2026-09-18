# clublabctl

Instructor-side control plane.

## Block A

Functional now:

```bash
python3 scripts/clublabctl/clublabctl.py version
python3 scripts/clublabctl/clublabctl.py inventory list
python3 scripts/clublabctl/clublabctl.py inventory show team01
python3 scripts/clublabctl/clublabctl.py inventory validate
```

The remaining subcommands are intentionally reserved but return exit code 10 until Phase 5 Blocks B/C implement their behavior.

No command in this tool should use `shell=True` or unvalidated target names.
