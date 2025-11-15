# Simple Streamlit Calculator — Code + GitHub + Streamlit Community Cloud (Streamlit Share) Guide

This document contains everything you need to create a **simple calculator** using **Streamlit**, push it to **GitHub**, and deploy it on **Streamlit Community Cloud** (a.k.a. Streamlit Share).

---

## What you'll get here

* `app.py` — complete Streamlit app (calculator with expression input, buttons, and session history)
* `requirements.txt` — dependencies for Streamlit Community Cloud
* `.gitignore` — recommended ignores
* Step‑by‑step Git commands to create the repo and push to GitHub
* Streamlit Community Cloud deployment steps

---

## File: `app.py`

```python
# app.py
import streamlit as st
from math import *

st.set_page_config(page_title="Simple Calculator", layout="centered")
st.title("🧮 Simple Calculator")
st.write("Type a Python arithmetic expression (e.g. `2+3*4`, `sin(pi/4)`, `round(2.718,2)`)")

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

if 'last' not in st.session_state:
    st.session_state.last = ''

expr = st.text_input("Expression", value=st.session_state.get('last', ''), key='expr_input')

col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("Evaluate"):
        do_eval = True
    else:
        do_eval = False
with col2:
    if st.button("Clear input"):
        st.session_state.expr_input = ''
        do_eval = False
with col3:
    if st.button("Clear history"):
        st.session_state.history = []

# Evaluate when user presses Enter in the text_input: Streamlit triggers rerun
# To also allow pressing Enter, we rely on the Evaluate button; users can press it.

if do_eval and expr.strip() != '':
    try:
        # Safe-ish eval: expose only math functions and a couple builtins
        safe_globals = {k: v for k, v in globals().items() if k in ('__name__',)}
        safe_locals = {name: obj for name, obj in globals().items() if name in globals()}
        # Better approach: provide a curated namespace
        allowed = {}
        from math import *
        allowed.update({name: obj for name, obj in globals().items() if name in dir()})
        # Build an explicit environment of safe math functions and a few builtins
        env = {
            'abs': abs, 'round': round, 'min': min, 'max': max,
        }
        # Add all math module names
        import math
        for name in dir(math):
            if not name.startswith('__'):
                env[name] = getattr(math, name)
        # Evaluate expression
        result = eval(expr, {"__builtins__": None}, env)
        st.success(f"Result: {result}")
        st.session_state.history.insert(0, (expr, result))
        st.session_state.last = expr
    except Exception as e:
        st.error(f"Error: {e}")

# Show history
if st.session_state.history:
    st.markdown("---")
    st.subheader("History")
    for i, (e, r) in enumerate(st.session_state.history[:20]):
        st.write(f"{i+1}. `{e}` = **{r}**")

st.info("Note: This app uses a restricted `eval` environment exposing math functions. Don't paste untrusted code you don't understand.")

# Footer
st.markdown("---")
st.caption("Built with Streamlit — push to GitHub & deploy on Streamlit Community Cloud")
```

> This `app.py` accepts Python arithmetic expressions. It exposes `math` module functions (sin, cos, pi, etc.) and a few safe builtins (`abs`, `round`, `min`, `max`). It intentionally uses a restricted `eval` environment, but **do not** paste arbitrary untrusted code.

---

## File: `requirements.txt`

```
streamlit
```

(You can pin a version like `streamlit==1.25.0` if you want reproducible builds.)

---

## File: `.gitignore`

```
__pycache__/
*.pyc
.env
.venv/
*.egg-info/
.DS_Store
```

---

## Quick Git + GitHub steps

1. Create a new GitHub repository on GitHub (e.g. `streamlit-simple-calculator`).
2. Locally, in your project folder (containing `app.py`, `requirements.txt`, `.gitignore`):

```bash
# initialize repo (if you haven't already)
git init
git add .
git commit -m "Initial commit: Streamlit calculator"
# replace URL with your repo
git remote add origin https://github.com/<your-username>/streamlit-simple-calculator.git
git branch -M main
git push -u origin main
```

If you prefer SSH: use `git remote add origin git@github.com:your-username/streamlit-simple-calculator.git`.

---

## Deploy to Streamlit Community Cloud (Streamlit Share)

1. Go to [https://share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
2. Click **New app** → choose the GitHub repo, branch (`main`) and the file path (`app.py`).
3. Click **Deploy**. Streamlit will install dependencies from `requirements.txt` and start the app.
4. After deploy you get a live URL you can share.

Notes:

* If you update code, commit & push to GitHub — Streamlit Community Cloud will automatically rebuild (or you can trigger a redeploy manually).
* If you need private dependencies or secrets (none are required here), you can set them in the app's Settings on Streamlit Cloud.

---

## Optional improvements you might want later

* Replace `eval` with a proper expression parser (e.g. `asteval`, `sympy` or a custom parser) for safety.
* Add a numeric keypad UI for mobile users.
* Add keyboard shortcuts (JS) or improved UX with columns, larger buttons.
* Add unit tests and CI workflow (GitHub Actions).

---

## Need help?

* If you want, I can:

  * generate the GitHub repo contents as a zip for you to download,
  * create a more feature-rich UI (keypad, parentheses button, memory slots), or
  * convert this to a multi-file Streamlit app with custom CSS.

Just tell me which one and I’ll add it right here.

---

*End of document.*
