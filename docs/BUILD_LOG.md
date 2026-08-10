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

## 2026-08-10 — Pinterest official API abandoned; replaced with Apify

**Problem:** The official Pinterest Developer API does not expose
Pinterest Trends data — it's built for ad buyers and content managers, not
for reading trend signals, and the app-creation process is gated without
yielding the data actually needed.

**Decision:** Replaced with Apify's `automation-lab/pinterest-trends-scraper`
actor, accessed via the official `apify-client` PyPI package. Apify is
self-serve, has a free tier with no credit card required, and returns
trending keywords, growth scores, seasonality, and country metadata
directly — the actual data researchers/marketers use for this, rather than
what the official API was designed for. `ingestion/pinterest_scraper.py`
was deleted and replaced with `ingestion/apify_pinterest.py`, following
the same env-var-guard pattern as the other ingestion stubs.

`ingestion/health_check.py` was also restructured at this point to treat
sources as required-vs-optional rather than uniformly required — Reddit
(still pending researcher-access approval) no longer fails the overall
health check; the pipeline is expected to run without it. The live
Google Trends check and the general design of the module were kept as-is,
just extended with this required/optional distinction.

---

## 2026-08-10 — `.env` split across two locations, real keys weren't being loaded

**Problem:** A second `.env` file had been created at `config/.env`
(containing the real API keys just obtained — YouTube, News API,
Anthropic, Apify, Airtable) separately from the original `.env` at the
project root (created during initial scaffolding, still full of stale
placeholders). Every ingestion module calls bare `load_dotenv()` with no
path argument, which only reads from the project root — so the real keys
in `config/.env` were never actually being picked up by any code. This is
the same root-location requirement documented earlier in this log; it
resurfaced because the original vision doc's repo diagram shows `.env`
under `config/`, which doesn't match how the setup doc's actual code calls
`load_dotenv()`.

**Impact assessed before fixing anything:** confirmed via `git status`
and `git check-ignore` that both files were already gitignored the whole
time — this was a local-loading bug, not a leak.

**Decision:** Consolidated to a single `.env` at the project root (moved
`config/.env`'s contents there, overwriting the stale placeholder file,
then deleted `config/.env` entirely) rather than changing the code to look
in `config/` instead — keeps the root-only convention consistent with
every module's existing `load_dotenv()` call.

---

## 2026-08-10 — TikTok Research API stub added; `.env` append bug and a health-check logic bug found by actually running the code

**Context:** A TikTok researcher-access application was submitted
(academic use only — the Research API's terms prohibit any commercial
use, so this must be replaced with a licensed commercial provider before
any future commercial transition; not relevant to the capstone build
itself). Added `ingestion/tiktok_scraper.py` as a stub, following the
same pattern as the other pending source (`reddit_scraper.py`): warns via
`logging.warning` rather than raising, since a missing key here is
expected, not an error condition.

**Bug 1 — shell append corrupted a line:** Appending
`TIKTOK_CLIENT_KEY=pending` to `.env` via `echo ... >> .env` landed on the
same line as the preceding `REDDIT_CLIENT_SECRET` entry, because the file
had no trailing newline. Caught immediately by checking the file's tail
before moving on, rather than assuming the append worked. Fixed by
splitting the merged line back into two.

**Bug 2 — found by actually running `health_check.py`, not just reading
it:** After wiring `tiktok` into `SOURCES` as an optional source (same
pattern as `reddit`), ran the module for real instead of trusting the
code by inspection. Both `reddit` and `tiktok` reported `OK` — wrong, since
their env vars hold the literal placeholder text `pending`/
`pending_approval`, not real credentials. `_check_env_vars` only checked
for an empty string, not for this project's own established
placeholder convention (the original `pinterest_scraper.py` stub had
already special-cased the string `"pending_approval"` for exactly this
reason — the check in `health_check.py` just hadn't been kept consistent
with it). Fixed by treating `pending`/`pending_approval` values as
equivalent to missing. Re-ran afterward to confirm both sources now
correctly report `UNAVAILABLE (optional)` instead of a false `OK`.

**Takeaway for the methods section:** both of these were caught because
of a practice used throughout this build — verify by actually executing
the code and inspecting real output, not by reading the diff and assuming
it's correct.

---
