# Installation

```{contents} On this page
:local:
:depth: 2
```

## Requirements

:::::{grid} 1 1 2 2
:gutter: 3

::::{grid-item-card} Python
:class-header: sd-bg-primary sd-text-white

```text
Python 3.7+
```

neomodel_bfo is compatible with Python 3.7 and above.
::::

::::{grid-item-card} Neo4j
:class-header: sd-bg-primary sd-text-white

```text
Neo4j 4.0+
```

Requires a running Neo4j instance (local or remote).
::::

:::::

## Installation Methods

::::{tab-set}

:::{tab-item} pip (Recommended)

### Install from PyPI

The easiest way to install neomodel_bfo:

```bash
pip install neomodel-bfo
```

```{admonition} Virtual Environment Recommended
:class: tip

We recommend using a virtual environment:

\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install neomodel-bfo
\`\`\`
```

:::

:::{tab-item} Development Install

### Install from Source

For development or to get the latest changes:

```bash
git clone https://github.com/rasinj/neomodel_bfo.git
cd neomodel_bfo
pip install -r requirements_dev.txt
```

This installs:
- All runtime dependencies
- Development tools (pytest, flake8)
- Documentation tools (Sphinx, MyST)

:::

:::{tab-item} Docker

### Using Docker

Run Neo4j in a container:

```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

Then install neomodel_bfo:

```bash
pip install neomodel-bfo
```

:::

::::

## Setting Up Neo4j

### Option 1: Local Installation

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} 🍎 macOS
:class-header: sd-bg-info sd-text-white

```bash
brew install neo4j
neo4j start
```
:::

:::{grid-item-card} 🐧 Linux
:class-header: sd-bg-info sd-text-white

```bash
# Debian/Ubuntu
sudo apt-get install neo4j

# Start service
sudo systemctl start neo4j
```
:::

:::{grid-item-card} 🪟 Windows
:class-header: sd-bg-info sd-text-white

Download from [neo4j.com/download](https://neo4j.com/download/)

Run the installer and start Neo4j Desktop.
:::

:::{grid-item-card} 🐳 Docker
:class-header: sd-bg-info sd-text-white

```bash
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```
:::

::::

### Option 2: Cloud Service

```{admonition} Neo4j Aura (Free Tier)
:class: info

[Neo4j Aura](https://neo4j.com/cloud/aura/) offers a free tier perfect for development:

1. Sign up at [console.neo4j.io](https://console.neo4j.io)
2. Create a free instance
3. Save the connection URL and credentials
4. Use in your configuration
```

## Configuration

### Configure Database Connection

:::::{tab-set}

::::{tab-item} Basic Configuration

```python
from neomodel import config

# Local Neo4j
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'
```

::::

::::{tab-item} Environment Variables

```python
import os
from neomodel import config

# Load from environment
config.DATABASE_URL = os.getenv('NEO4J_URL', 'bolt://neo4j:password@localhost:7687')
```

Set in your shell:
```bash
export NEO4J_URL='bolt://neo4j:password@localhost:7687'
```

::::

::::{tab-item} Secure Connection

```python
from neomodel import config

# Neo4j Aura or SSL-enabled instance
config.DATABASE_URL = 'bolt+s://user:password@host:7687'

# Or with routing (Neo4j cluster)
config.DATABASE_URL = 'neo4j://user:password@host:7687'
```

::::

:::::

### Connection URL Format

```text
bolt://username:password@host:port
```

```{list-table}
:header-rows: 1

* - Scheme
  - Usage
* - `bolt://`
  - Standard unencrypted connection
* - `bolt+s://`
  - Encrypted connection (SSL/TLS)
* - `neo4j://`
  - Routing connection for clusters
* - `neo4j+s://`
  - Encrypted routing connection
```

## Verify Installation

### Test Your Setup

```python
from neomodel import config, db
from neomodel_bfo import Object

# Configure
config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

# Test connection
db.cypher_query("RETURN 1 as test")
print("✓ Database connection successful!")

# Test BFO classes
test_obj = Object(name="Test").save()
print(f"✓ Created object: {test_obj.name}")

# Cleanup
test_obj.delete()
print("✓ neomodel_bfo is working!")
```

```{admonition} Expected Output
:class: success

\`\`\`
✓ Database connection successful!
✓ Created object: Test
✓ neomodel_bfo is working!
\`\`\`
```

## Troubleshooting

::::{dropdown} Connection Refused
:color: warning

**Problem:** `ServiceUnavailable: Failed to establish connection`

**Solutions:**
- ✅ Verify Neo4j is running: Check [http://localhost:7474](http://localhost:7474)
- ✅ Check port: Default is 7687 for Bolt protocol
- ✅ Verify credentials: Default is `neo4j/neo4j` (change on first login)
- ✅ Check firewall: Ensure ports 7474 and 7687 are open

::::

::::{dropdown} Authentication Failed
:color: warning

**Problem:** `AuthError: The client is unauthorized`

**Solutions:**
- ✅ Use correct username and password
- ✅ Change default password on first Neo4j login
- ✅ For Neo4j Desktop, check connection details in the UI
- ✅ For Aura, use the generated password from the web console

::::

::::{dropdown} Import Error
:color: warning

**Problem:** `ImportError: No module named 'neomodel_bfo'`

**Solutions:**
- ✅ Ensure neomodel_bfo is installed: `pip list | grep neomodel`
- ✅ Check you're in the right virtual environment
- ✅ Try reinstalling: `pip install --upgrade neomodel-bfo`

::::

::::{dropdown} Version Compatibility
:color: warning

**Problem:** Errors related to neomodel or Neo4j versions

**Solutions:**
- ✅ neomodel_bfo requires neomodel ≥5.0.0
- ✅ Check installed version: `pip show neomodel`
- ✅ Update: `pip install --upgrade neomodel`
- ✅ Use Neo4j 4.0 or later

::::

## Next Steps

```{admonition} You're ready to go! 🎉
:class: success

Now that you have neomodel_bfo installed:

1. 📖 Read the {doc}`usage` guide to learn BFO concepts
2. 🧬 Explore the [examples](https://github.com/rasinj/neomodel_bfo/tree/master/examples) directory
3. 🏗️ Start building your domain ontology!
```

---

```{seealso}
**Additional Resources:**
- [Neo4j Documentation](https://neo4j.com/docs/)
- [neomodel Documentation](https://neomodel.readthedocs.io)
- [BFO Specification](https://basic-formal-ontology.org)
```
