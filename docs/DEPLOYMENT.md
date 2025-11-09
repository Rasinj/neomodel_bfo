# Documentation Deployment Guide

This guide explains how the neomodel_bfo documentation is built and deployed.

## Hosting Options

neomodel_bfo documentation is available through two platforms:

### 1. ReadTheDocs (Primary) 📚

**URL**: https://neomodel-bfo.readthedocs.io

**Features:**
- ✅ Automatic builds on every commit
- ✅ Version management (latest, stable, tags)
- ✅ Full-text search
- ✅ PDF/EPUB downloads
- ✅ Pull request previews

**Configuration**: `.readthedocs.yaml`

**How it works:**
1. Push to GitHub triggers webhook to ReadTheDocs
2. ReadTheDocs pulls latest code
3. Installs dependencies from `requirements_dev.txt`
4. Builds Sphinx documentation
5. Deploys to https://neomodel-bfo.readthedocs.io

**Setup (One-time):**
1. Import project at https://readthedocs.org/dashboard/import/
2. Connect GitHub repository: `rasinj/neomodel_bfo`
3. ReadTheDocs auto-detects `.readthedocs.yaml`
4. Build starts automatically

### 2. GitHub Pages (Backup) 🌐

**URL**: https://rasinj.github.io/neomodel_bfo

**Features:**
- ✅ Fast, CDN-backed hosting
- ✅ Automatic deployment via GitHub Actions
- ✅ Always shows latest master/main branch

**Configuration**: `.github/workflows/docs.yml`

**How it works:**
1. Push to master/main triggers GitHub Action
2. Action builds Sphinx documentation
3. Deploys HTML to `gh-pages` branch
4. GitHub serves from `gh-pages` branch

**Setup (One-time):**
1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` / `root`
4. Save

## Building Locally

### Quick Build

```bash
cd docs
make html
open _build/html/index.html  # macOS
# or
xdg-open _build/html/index.html  # Linux
# or
start _build/html/index.html  # Windows
```

### Clean Build

```bash
cd docs
make clean
make html
```

### Live Reload (Development)

For live reloading while editing:

```bash
pip install sphinx-autobuild
cd docs
sphinx-autobuild . _build/html --open-browser
```

This opens a browser with live reload at http://localhost:8000

### Build All Formats

```bash
cd docs

# HTML
make html

# PDF (requires LaTeX)
make latexpdf

# EPUB
make epub

# Check for broken links
make linkcheck
```

## Documentation Structure

```
docs/
├── conf.py              # Sphinx configuration
├── index.md             # Landing page (MyST-MD)
├── installation.md      # Installation guide (MyST-MD)
├── usage.md             # Usage guide (MyST-MD)
├── development_old.rst  # Development guide (RST - to be converted)
├── contributing.rst     # Contributing guide (RST)
├── Makefile             # Build automation
├── make.bat             # Windows build script
├── _static/             # Custom CSS, images, etc.
├── _templates/          # Custom Sphinx templates
└── _build/              # Build output (gitignored)
```

## MyST-MD Features

Our documentation uses MyST (Markedly Structured Text) for beautiful, modern docs:

### Enabled Extensions

- `colon_fence` - Use `:::` for directives
- `deflist` - Definition lists
- `fieldlist` - Field lists
- `tasklist` - Task lists with checkboxes
- `attrs_inline` - Inline attributes
- `attrs_block` - Block attributes

### Sphinx Extensions

- `myst_parser` - MyST Markdown support
- `sphinx_design` - Cards, grids, tabs, dropdowns
- `sphinx_copybutton` - Copy buttons on code blocks
- `sphinx.ext.autodoc` - Auto-generate API docs
- `sphinx.ext.napoleon` - Google/NumPy docstrings
- `sphinx.ext.viewcode` - Add links to source code

### Theme

**Furo** - Modern, clean theme with:
- Beautiful light/dark mode
- Mobile-responsive design
- Keyboard navigation
- Custom blue color scheme

## Troubleshooting

### Build Errors

**Problem:** `Extension error: Could not import extension myst_parser`

```bash
pip install -r requirements_dev.txt
```

**Problem:** `WARNING: html_static_path entry '_static' does not exist`

```bash
mkdir -p docs/_static
```

**Problem:** Build succeeds but styling is broken

```bash
cd docs
make clean
make html
```

### ReadTheDocs Issues

**Build failing on ReadTheDocs:**

1. Check build logs at https://readthedocs.org/projects/neomodel-bfo/builds/
2. Verify `.readthedocs.yaml` is valid
3. Ensure all dependencies in `requirements_dev.txt`
4. Check Python version matches (3.9)

**PDF build failing:**

- This is often due to LaTeX issues
- Can disable PDF in `.readthedocs.yaml` if not needed
- Or add specific LaTeX packages to build config

### GitHub Pages Issues

**Pages not deploying:**

1. Check GitHub Actions tab for workflow status
2. Verify Pages is enabled in Settings
3. Ensure branch is set to `gh-pages`
4. Check workflow has Pages permissions

**404 on deployed site:**

- Wait a few minutes after deployment
- Clear browser cache
- Check that `gh-pages` branch has content

## Updating Documentation

### Adding New Pages

1. Create new `.md` file in `docs/`
2. Add to `toctree` in `index.md`:

```markdown
```{toctree}
:hidden:

newpage
```
```

3. Build and test locally
4. Commit and push

### Converting RST to MyST

For remaining `.rst` files:

```bash
# Install rst2myst
pip install rst-to-myst

# Convert file
rst2myst convert docs/oldfile.rst docs/newfile.md

# Review and edit converted file
# Update toctree references
# Delete old .rst file
```

## Best Practices

### Writing MyST Documentation

✅ **Use MyST directives for rich content:**

```markdown
:::{admonition} Title
:class: tip
Content here
:::
```

✅ **Use grids for visual layout:**

```markdown
::::{grid} 1 1 2 2
:::{grid-item-card} Card 1
Content
:::
:::{grid-item-card} Card 2
Content
:::
::::
```

✅ **Use tabs for alternatives:**

```markdown
::::{tab-set}
:::{tab-item} Option 1
Content
:::
:::{tab-item} Option 2
Content
:::
::::
```

### Content Guidelines

- Keep paragraphs short and scannable
- Use visual elements (cards, grids, admonitions)
- Include code examples with syntax highlighting
- Add cross-references with `{doc}` and `{ref}`
- Test all links with `make linkcheck`

## Maintenance

### Regular Updates

- **Dependencies**: Update Sphinx extensions annually
- **Theme**: Update Furo theme for latest features
- **Content**: Review docs for accuracy after major changes
- **Links**: Run `make linkcheck` quarterly

### Version Management (ReadTheDocs)

To create versioned documentation:

1. Tag release: `git tag v0.2.0`
2. Push tag: `git push --tags`
3. ReadTheDocs auto-creates version
4. Mark stable versions as "active"

## Resources

- **MyST Parser**: https://myst-parser.readthedocs.io
- **Sphinx Design**: https://sphinx-design.readthedocs.io
- **Furo Theme**: https://pradyunsg.me/furo/
- **ReadTheDocs**: https://docs.readthedocs.io
- **GitHub Pages**: https://docs.github.com/en/pages
