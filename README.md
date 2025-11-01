# umamusume-model-replace
- replace umamusume models

# Installation (uv)
- Install the `uv` package manager for Python
- Install Python 3.12 & dependencies:

```shell
uv sync
```

- Run the `main` module through `uv`:

```shell
uv run -m main
```

# Installation (pip)
- Install Python 3.12. 3.13 will not work.
- Set up a virtual environment. For Windows:

```shell
python -m venv .venv
.venv\Scripts\activate
```

- Install the dependencies from `requirements.txt`:

```shell
pip install -r requirements.txt
```

- Run the `main` module:

```shell
python -m main
```

# Usage
- Follow the prompts within:

```
[1] replace head model
[2] replace body model
[3] replace tail model (deprecated)
[4] replace head and body model
[5] replace body materials
[6] replace gacha character
[7] replace skill character
[8] replace g1 victory character action (Experimental)
[9] unlock live dress
[10] disable live blur
[98] restore your changes
[99] exit
```

