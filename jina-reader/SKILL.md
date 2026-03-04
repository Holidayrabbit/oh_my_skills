---
name: jina-reader
description: "Web content extraction via Jina AI Reader API. Three modes: read (URL to markdown), search (web search + full content), ground (fact-checking). Extracts clean content without exposing server IP."
homepage: https://jina.ai/reader
---

# Jina Reader

Extract clean web content via Jina AI — without exposing your server IP.

## When to use
- when you need to extract content from a web page
- when you need to perform a web search
- when you need to fact-check a statement

## Read a URL

```bash
{baseDir}/scripts/reader.sh "https://example.com/article"
```

## Search the web (top 5 results with full content)

```bash
{baseDir}/scripts/reader.sh --mode search "latest AI news 2025"
```

## Fact-check a statement

```bash
{baseDir}/scripts/reader.sh --mode ground "OpenAI was founded in 2015"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--mode` | `read`, `search`, `ground` | `read` |
| `--selector` | CSS selector to extract specific region | — |
| `--wait` | CSS selector to wait for before extraction | — |
| `--remove` | CSS selectors to remove (comma-separated) | — |
| `--proxy` | Country code for geo-proxy (`br`, `us`, etc.) | — |
| `--nocache` | Force fresh content (skip cache) | off |
| `--format` | `markdown`, `html`, `text`, `screenshot` | `markdown` |
| `--json` | Raw JSON output | off |

## Examples

```bash
# Extract article content
{baseDir}/scripts/reader.sh "https://blog.example.com/post"

# Extract specific section via CSS selector
{baseDir}/scripts/reader.sh --selector "article.main" "https://example.com"

# Remove nav and ads before extraction
{baseDir}/scripts/reader.sh --remove "nav,footer,.ads" "https://example.com"

# Search with JSON output
{baseDir}/scripts/reader.sh --mode search --json "AI enterprise trends"

# Read via Brazil proxy
{baseDir}/scripts/reader.sh --proxy br "https://example.com.br"

# Fact-check a claim
{baseDir}/scripts/reader.sh --mode ground "Tesla is the most valuable car company"
```

## API Key

API Key is not essential.

```bash
export JINA_API_KEY="jina_..."
```


