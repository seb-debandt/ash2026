# Mantle cell lymphoma at ASH 2026

A password-protected briefing for the Mantle Cell Lymphoma Alliance (MCLA) board. It lists the 173 abstracts in the ASH 2026 Annual Meeting program (New Orleans, December 12–15, 2026) that cover or mention mantle cell lymphoma (MCL).

Live site: https://seb-debandt.github.io/ash2026/

## How the password works

`index.html` holds the abstract data encrypted with AES-256-GCM, using a key derived from the password with PBKDF2-SHA256 (310,000 iterations). The page decrypts it in the browser once someone enters the password. The repository holds no plain-text abstract data and no password.

## What the site contains

- **Key abstracts:** 13 editorial picks, each with a one-line reason.
- **Six topic groups:** frontline treatment; relapsed or refractory treatment; CAR-T and stem cell transplant; biology, biomarkers and prognosis; real-world outcomes and access; and safety, supportive care and quality of life.
- **Relevance labels:**
  - **MCL focus:** MCL is in the title (73 abstracts).
  - **Includes MCL data:** MCL is mentioned 3 or more times in the abstract (36).
  - **Mentions MCL:** MCL is mentioned once or twice (64).
- **Per abstract:** the full text, authors, affiliations, disclosures and a link to the ASH program.

## Rebuilding

Source: https://onlineprogram.hematology.org/

1. `scraper/search.js` (Playwright) runs keyword searches for "mantle", "MCL", "MIPI" and "Blastoid" and collects the paper IDs.
2. Download each `paper-details.aspx?pid=N` page, then run `scraper/parse.py` to extract the fields and classify how often MCL is mentioned. Matches on the MCL-1 gene, on "mast cell leukemia" and on session titles alone are excluded.
3. `build/build_data.py` cleans the authors, affiliations and abstract HTML.
4. `build/enrich.py` adds the topic and key-abstract notes.
5. `node build/encrypt.js <data.json> build/template.html index.html <password>` writes the encrypted page.

The scripts expect a local `dl/` working folder for downloaded pages and intermediate JSON. That folder is git-ignored.
