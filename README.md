# Hossain Md Asad – Personal Website

A personal portfolio website built with [Streamlit](https://streamlit.io).

## Edit your content

All text on the site comes from **`profile_data.py`**. Open it and replace every `TODO`
with your real details (headline, about, experience, education, skills, projects,
certifications). You don't need to touch `app.py`.

Optional extras:

- **Photo:** add a square image at `assets/profile.jpg` (or `.png`).
- **CV:** add `assets/resume.pdf` and a "Download CV" button appears.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501.

## Deploy free on Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app** → **Deploy a public app from GitHub**.
4. Pick your repository, branch `main`, and main file `app.py`.
5. Optionally set a custom subdomain (e.g. `asad-portfolio.streamlit.app`), then click **Deploy**.

Every time you push a change to `profile_data.py`, the live site updates automatically.

## Project structure

```
app.py               # page layout and styling
profile_data.py      # all your content (edit this)
assets/              # profile photo and CV go here
.streamlit/config.toml  # theme colour
requirements.txt
```
