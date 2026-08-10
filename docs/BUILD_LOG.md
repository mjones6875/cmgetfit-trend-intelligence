# Build Log — Engineering Decisions

Running record of non-obvious technical decisions, workarounds, and issues
encountered during the build, kept for the academic write-up (methods /
limitations sections) and capstone presentation. Business/commercial
context is intentionally excluded — see the separate local planning docs
for that.

Each entry: what happened, why it mattered, what was decided.

---

## 2026-08-10 — Python version pinned to 3.13, not the system default 3.14

**Context:** The dev machine has Python 3.14.4 installed as the default
`python` on PATH, alongside Python 3.13.7. The project spec
(`CAPSTONE_SETUP_TASKS.md`) requires Python 3.11+, which both satisfy.

**Problem:** Compiled ML dependencies (`torch`, `spaCy`, and transitively
`transformers`) publish prebuilt wheels for a given Python version only
after that version has been out long enough for the PyPy/CPython ABI to
stabilize and for maintainers to build against it. A brand-new Python
release (3.14) risks missing prebuilt wheels for one or more of these
packages, which forces a source build — slow, and prone to failing outright
if the required C/C++ toolchain isn't present.

**Decision:** Created the virtual environment against the Python 3.13.7
interpreter instead of the default 3.14.4, trading the newest language
version for wheel availability across the full ML stack. Reproducibility
note: `venv` was created via `C:\Users\famil\AppData\Local\Programs\Python\Python313\python.exe -m venv venv` rather than the bare `python -m venv venv` from the original setup doc, specifically to force this interpreter choice.

---

## 2026-08-10 — venv relocated outside the project tree (Windows MAX_PATH failure on torch)

**Problem:** `pip install -r requirements.txt` failed partway through with:

```
ERROR: Could not install packages due to an OSError: [WinError 206] The
filename or extension is too long: '...venv\Lib\site-packages\torch-2.13.0.dist-info\licenses\third_party\kineto\libkineto\third_party\dynolog\third_party\prometheus-cpp\3rdparty\civetweb\examples\rest\cJSON'
```

`torch` ships deeply nested third-party license directories (bundled
`kineto`/`dynolog`/`prometheus-cpp`/`civetweb` components). Combined with
this project's already-deep path
(`Desktop\Data_Science_Mastery\Capstone_Project\CMgetfit_Trend_Analysis\venv\...`),
the resulting absolute path (253 characters for the failing entry alone)
exceeds Windows' classic 260-character `MAX_PATH` limit.

**Root cause confirmed:** checked `HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled`
— it was `0` (disabled) on this machine. Enabling it is the "proper" fix
and would allow the venv to stay inside the project folder as the setup
doc originally specifies, but it requires an elevated (Administrator)
PowerShell session, which was not available in this environment.

**Decision:** Instead of requiring elevation, relocated the virtual
environment outside the project tree entirely, to a short path:
`C:\Users\famil\venvs\cmgetfit-trend-intelligence`. This cuts ~40
characters off the prefix, bringing the same failing path comfortably
under the 260-character limit with no registry/admin changes needed.

**Trade-off:** the venv is no longer colocated with the project, which
deviates from the setup doc's assumption of `venv\Scripts\activate` from
the project root — activation now requires the full external path (see
updated README). This is purely a local development convenience issue;
it has no effect on the repo itself, since `venv/` was always gitignored
regardless of where it physically lives.

---

## 2026-08-10 — Full dependency install succeeded; versions pinned

With the venv relocated (see above), `pip install -r requirements.txt`
completed cleanly: 100+ packages including `torch==2.13.0`,
`spacy==3.8.15`, `transformers==5.14.1`, `scikit-learn==1.9.0`. Followed
by `python -m spacy download en_core_web_lg` (400.7 MB model download).

Verified both with real smoke tests rather than just trusting exit codes:
- `import torch, spacy, transformers, sklearn, pandas, pytrends, praw, anthropic, dotenv, reportlab, apscheduler` — all succeeded.
- `spacy.load("en_core_web_lg")` on the sentence "air fryer chickpeas" — model loaded and tagged tokens correctly.

Ran `pip freeze > requirements.txt` to replace the unpinned dependency
list with the 116 exact versions actually installed and verified, so the
build is reproducible from this point forward.

No API keys were required for any of this — installation and model
download are independent of which API accounts are still pending.

---
