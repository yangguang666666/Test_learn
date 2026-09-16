# Harness v0

Harness v0 is a small, deterministic wrapper around pytest. It does four
things only:

1. Runs `python -m pytest` in a selected repository.
2. Captures standard output, standard error, exit code, and duration.
3. Applies a basic failure classification.
4. Saves the result as UTF-8 JSON.

Run it from the project root:

```powershell
python -m harness --repo . --result artifacts/harness_result.json
```

Pass additional pytest arguments after `--`:

```powershell
python -m harness --repo . --result artifacts/collect.json -- --collect-only -q
```

The command uses the same Python interpreter that starts Harness. Therefore,
run it with `.venv\Scripts\python.exe` after pytest has been installed into
that virtual environment.

The result file is the contract that later versions will extend with coverage,
generated-test metadata, mutation results, and repair history.
