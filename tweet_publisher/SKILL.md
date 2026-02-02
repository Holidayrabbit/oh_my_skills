---
name: twitter-publisher
description: Publish tweets and Twitter threads using Tweepy. Use when the user wants to post content to Twitter, including short tweets or long-form text that needs to be split into threaded replies. Handles automatic text splitting at natural boundaries (paragraphs, sentences) and thread creation. Trigger when user mentions "tweet", "post to Twitter", "publish to Twitter", "Twitter thread", or similar requests.
---

# Twitter Publisher

Automate Twitter posting with intelligent thread creation for long-form content.

## Quick Start

Install Tweepy first:
```bash
pip install tweepy --break-system-packages
```

### Simple Tweet

```bash
python scripts/publish_tweet.py \
  --text "Your tweet content here"
```

### Long Text (Automatic Thread)

```bash
python scripts/publish_tweet.py \
  --text "Your very long text that will be automatically split..." \
  --thread
```

Or read from file:
```bash
python scripts/publish_tweet.py \
  --text "@/path/to/article.txt" \
  --thread
```

### Preview Before Publishing

```bash
python scripts/publish_tweet.py \
  --text "Long text..." \
  --preview
```

Shows how text will be split without actually posting.

## Credentials Setup

Twitter API credentials are required. Run the setup script for interactive configuration:

```bash
python scripts/setup_credentials.py
```

Or set environment variables directly:
```bash
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

Get credentials from [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard). App must have "Read and Write" permissions.

## Text Splitting Strategy

The skill intelligently splits long text:

1. **Paragraph boundaries** (preferred): Splits at double newlines
2. **Sentence boundaries** (fallback): Splits at sentence endings
3. **Hard split** (last resort): If single sentence exceeds 274 chars

Each tweet in thread is numbered (e.g., "1/5") and replies to the previous tweet.

## Workflow

### Publishing a Simple Tweet

Use `scripts/publish_tweet.py` with text under 280 characters:

```python
# Example command
bash_tool: python scripts/publish_tweet.py --text "Check out this new feature!"
```

### Publishing a Thread

For long-form content:

1. Prepare text (from user input or file)
2. Preview split (optional but recommended)
3. Publish with `--thread` flag

```python
# Preview
bash_tool: python scripts/publish_tweet.py --text "@article.txt" --preview

# Publish after review
bash_tool: python scripts/publish_tweet.py --text "@article.txt" --thread
```

### Handling User Files

When user provides content in uploaded files:

1. Copy file from `/mnt/user-data/uploads/` to working directory
2. Use `@filepath` syntax to read content
3. Publish thread

```python
# If user uploaded "blog_post.txt"
bash_tool: python scripts/publish_tweet.py \
  --text "@/mnt/user-data/uploads/blog_post.txt" \
  --thread
```

## Programmatic Usage

For custom workflows, use `TwitterPublisher` class directly:

```python
from scripts.publish_tweet import TwitterPublisher

publisher = TwitterPublisher(
    api_key="...",
    api_secret="...",
    access_token="...",
    access_token_secret="..."
)

# Simple tweet
result = publisher.publish_single_tweet("Hello Twitter!")

# Thread
result = publisher.publish_thread("Long text that will be split...")
```

## Error Handling

Common issues:

- **401 Unauthorized**: Check credentials
- **403 Forbidden**: Verify app has write permissions in developer portal
- **429 Rate Limited**: Twitter limits to 300 tweets per 3 hours
- **Duplicate Tweet**: Same text posted recently, modify slightly

## Best Practices

1. **Always preview** long threads before publishing
2. **Check credentials** before running scripts
3. **Natural breaks**: Write with paragraphs for better splitting
4. **Rate limits**: Avoid publishing many threads in quick succession
5. **Review output**: Check returned tweet IDs for verification

## Additional Resources

- `references/twitter_api.md`: Detailed API documentation and rate limits
- `scripts/setup_credentials.py`: Interactive credential configuration
- `scripts/publish_tweet.py`: Main publishing script with all features