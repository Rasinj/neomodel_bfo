# Documentation Hosting

The neomodel_bfo documentation is automatically built and hosted online for easy access.

## 📚 View Documentation Online

### Primary: ReadTheDocs

**URL**: **https://neomodel-bfo.readthedocs.io**

- ✅ Automatic builds on every commit
- ✅ Multiple versions (latest, stable, releases)
- ✅ Full-text search
- ✅ PDF and EPUB downloads
- ✅ Pull request previews

### Backup: GitHub Pages

**URL**: **https://rasinj.github.io/neomodel_bfo** (after setup)

- ✅ Fast CDN hosting
- ✅ Automatic deployment via GitHub Actions
- ✅ Always shows latest master/main

## 🚀 Quick Setup

### Enable ReadTheDocs (Maintainer)

1. Go to https://readthedocs.org/dashboard/import/
2. Click "Import a Project"
3. Select `rasinj/neomodel_bfo` from GitHub
4. ReadTheDocs detects `.readthedocs.yaml` automatically
5. Click "Build Version" to start first build

Done! Documentation will be available at https://neomodel-bfo.readthedocs.io

### Enable GitHub Pages (Maintainer)

1. Go to repository **Settings** → **Pages**
2. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **gh-pages** / **root**
3. Click **Save**
4. Push to master/main to trigger first build

The GitHub Actions workflow (`.github/workflows/docs.yml`) will:
- Build Sphinx documentation on every push
- Deploy to `gh-pages` branch
- Serve at https://rasinj.github.io/neomodel_bfo

## 🛠️ How It Works

### Automatic Building

```
┌─────────────────┐
│  Push to GitHub │
└────────┬────────┘
         │
    ┌────▼────┐
    │Triggers │
    └────┬────┘
         │
    ┌────▼─────────────────────────────┐
    │                                   │
┌───▼─────────────┐       ┌───▼──────────────┐
│ ReadTheDocs     │       │ GitHub Actions   │
│                 │       │                  │
│ 1. Clone repo   │       │ 1. Checkout code │
│ 2. Install deps │       │ 2. Install deps  │
│ 3. Build Sphinx │       │ 3. Build Sphinx  │
│ 4. Deploy       │       │ 4. Deploy Pages  │
└─────────────────┘       └──────────────────┘
         │                        │
         │                        │
         ▼                        ▼
┌─────────────────┐       ┌──────────────────┐
│  readthedocs.io │       │   github.io      │
└─────────────────┘       └──────────────────┘
```

### Configuration Files

| File | Purpose |
|------|---------|
| `.readthedocs.yaml` | ReadTheDocs build configuration |
| `.github/workflows/docs.yml` | GitHub Pages deployment workflow |
| `docs/conf.py` | Sphinx configuration |
| `requirements_dev.txt` | Documentation dependencies |

## 📖 Documentation Stack

**Technologies Used:**

- **Sphinx** - Documentation generator
- **MyST Parser** - Markdown support with rich directives
- **Furo** - Modern, beautiful theme
- **sphinx-design** - Cards, grids, tabs, dropdowns
- **sphinx-copybutton** - Copy buttons on code blocks

**Features:**

- 🎨 Beautiful MyST-MD formatting
- 📱 Mobile-responsive design
- 🌓 Dark/light mode
- 🔍 Full-text search
- 📥 PDF/EPUB downloads (ReadTheDocs)
- 🔗 Automatic cross-references
- 💻 Syntax highlighting
- ⌨️ Keyboard navigation

## 🔄 Updating Documentation

### Process

1. **Edit** documentation files in `docs/`
   - Prefer `.md` files (MyST-MD)
   - Use `.rst` for compatibility if needed

2. **Test locally**:
   ```bash
   cd docs
   make html
   open _build/html/index.html
   ```

3. **Commit and push**:
   ```bash
   git add docs/
   git commit -m "Update documentation"
   git push
   ```

4. **Automatic deployment**:
   - ReadTheDocs builds automatically
   - GitHub Pages builds via Actions
   - Both update within minutes

### Live Preview

For live editing with auto-reload:

```bash
pip install sphinx-autobuild
cd docs
sphinx-autobuild . _build/html --open-browser
```

Visit http://localhost:8000 and see changes instantly!

## 🐛 Troubleshooting

### Documentation Not Updating

**ReadTheDocs:**
1. Check https://readthedocs.org/projects/neomodel-bfo/builds/
2. Look for build errors
3. Verify webhook is active in GitHub settings

**GitHub Pages:**
1. Go to repository **Actions** tab
2. Check latest "Build and Deploy Documentation" workflow
3. Look for errors in build logs

### Build Failing

**Common issues:**

1. **Missing dependencies**:
   ```bash
   pip install -r requirements_dev.txt
   ```

2. **MyST syntax errors**:
   - Check MyST directive syntax
   - Ensure proper indentation
   - Validate with local build

3. **Theme not found**:
   ```bash
   pip install furo sphinx-design sphinx-copybutton myst-parser
   ```

## 📚 Resources

- **Full Deployment Guide**: `docs/DEPLOYMENT.md`
- **ReadTheDocs Docs**: https://docs.readthedocs.io
- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **MyST Parser**: https://myst-parser.readthedocs.io
- **Furo Theme**: https://pradyunsg.me/furo/

## ✅ Checklist for Maintainers

After setting up:

- [ ] ReadTheDocs import completed
- [ ] First build successful on ReadTheDocs
- [ ] GitHub Pages enabled in repository settings
- [ ] First GitHub Pages deployment successful
- [ ] Both URLs accessible:
  - [ ] https://neomodel-bfo.readthedocs.io
  - [ ] https://rasinj.github.io/neomodel_bfo
- [ ] ReadTheDocs webhook active in GitHub
- [ ] Default version set to "latest" on ReadTheDocs
- [ ] Update README badge if needed

---

**Questions?** See `docs/DEPLOYMENT.md` for detailed information.
