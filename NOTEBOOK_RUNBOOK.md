# OpenEnv Notebooks Runbook (WSL)

Single source of truth to run `notebook.ipynb` → `notebook5.ipynb` with local servers.

## 0) One-time setup

```bash
cd /mnt/d/test

python3 -m venv .venv-reinf
source .venv-reinf/bin/activate

python -m pip install --upgrade pip setuptools wheel

python -m pip install \
  openenv-core>=0.2.2 \
  fastapi>=0.104.0 \
  uvicorn>=0.24.0 \
  fastmcp>=3.0.0 \
  pydantic>=2.0.0 \
  trl>=0.17.0 \
  transformers>=4.40.0 \
  datasets>=2.18.0 \
  accelerate>=0.28.0 \
  trackio \
  huggingface-hub>=0.22.0

python -m pip install -e ./OpenEnv
python -m pip install -e ./OpenEnv/envs/echo_env -e ./OpenEnv/envs/openspiel_env -e ./OpenEnv/envs/textarena_env

python -m pip install ipykernel
python -m ipykernel install --user --name reinf-hackathon --display-name "Python (reinf-hackathon)"
```

## 1) Every new terminal/session

```bash
cd /mnt/d/test
source .venv-reinf/bin/activate
export PYTHONPATH="/mnt/d/test/OpenEnv/src:/mnt/d/test/OpenEnv/envs:$PYTHONPATH"
```

In VS Code/Jupyter, select kernel: **Python (reinf-hackathon)**.

---

## 2) Server command quick map

- Echo (`localhost:8000`)
```bash
cd /mnt/d/test/OpenEnv
uvicorn envs.echo_env.server.app:app --host 127.0.0.1 --port 8000
```

- OpenSpiel Catch (`localhost:8000`)
```bash
cd /mnt/d/test/OpenEnv
unset OPENSPIEL_GAME
uvicorn envs.openspiel_env.server.app:app --host 127.0.0.1 --port 8000
```

- OpenSpiel Tic-Tac-Toe (`localhost:8000`)
```bash
cd /mnt/d/test/OpenEnv
export OPENSPIEL_GAME=tic_tac_toe
uvicorn envs.openspiel_env.server.app:app --host 127.0.0.1 --port 8000
```

- Modified Echo for Notebook 3 (`localhost:8001`)
```bash
cd /mnt/d/test
uvicorn server.app:app --host 127.0.0.1 --port 8001 --app-dir /mnt/d/test/echo-env-modified
```

- TextArena Wordle for Notebook 5 (`localhost:8001`)
```bash
cd /mnt/d/test/OpenEnv
export TEXTARENA_ENV_ID=Wordle-v0
export TEXTARENA_NUM_PLAYERS=1
uvicorn envs.textarena_env.server.app:app --host 127.0.0.1 --port 8001
```

Use one server per port. Stop with `Ctrl+C` before starting another on same port.

---

## 3) Notebook-by-notebook run steps

## Notebook 1 (`notebook.ipynb`)

1. Start Echo server (port 8000) using the command above.
2. Run notebook cells in order until Echo section completes.
3. Stop Echo server.
4. Start OpenSpiel Catch server (port 8000).
5. Continue running cells in order for OpenSpiel section.
6. TextArena section uses hosted URL by default in this notebook; run if endpoint is available.

## Notebook 2 (`notebook2.ipynb`)

1. Start OpenSpiel Catch server on port 8000.
2. Run notebook cells top-to-bottom.
3. If switching to Tic-Tac-Toe, stop server and restart with `OPENSPIEL_GAME=tic_tac_toe`.
4. Re-run the cells that create/use the OpenSpiel client.

## Notebook 3 (`notebook3.ipynb`)

1. Start modified Echo server on port 8001.
2. Run notebook cells top-to-bottom (clone/modify/test sections).
3. Keep Step 6 (HF deploy) optional unless you want to publish.
4. Stop server after validation.

## Notebook 4 (`notebook4.ipynb`)

1. Run all cells in order to generate `word_game` package files.
2. Optional local verification server:

```bash
cd /mnt/d/test
uvicorn word_game.server.app:app --host 127.0.0.1 --port 8002 --reload
```

3. If running verification cells against local server, keep server alive during those cells.

## Notebook 5 (`notebook5.ipynb`)

1. Start local TextArena Wordle server on port 8001 (command above).
2. Run cells in order.
3. This notebook now checks local server first and fails fast if server is not up.
4. `GRPOConfig` args are version-guarded in the notebook (unsupported args auto-skipped).
5. For quick validation (without long training), run through config + trainer init cells and skip long training execution.

---

## 4) Validation commands

Run these after notebook updates:

```bash
cd /mnt/d/test
source .venv-reinf/bin/activate
python validate_notebooks.py
python validate_snippets.py
```

---

## 5) Troubleshooting

- `ModuleNotFoundError`
```bash
cd /mnt/d/test
source .venv-reinf/bin/activate
export PYTHONPATH="/mnt/d/test/OpenEnv/src:/mnt/d/test/OpenEnv/envs:$PYTHONPATH"
```

- Wrong kernel in notebook
  - Switch to **Python (reinf-hackathon)**.

- Port already in use
```bash
ss -ltnp | grep ':8000\|:8001\|:8002'
kill <pid>
```

- HF hosted endpoint issues (`404`, websocket issues)
  - Use local server commands from this runbook.
