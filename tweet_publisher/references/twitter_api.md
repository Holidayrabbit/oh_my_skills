# Twitter API Reference

## Authentication

The skill uses OAuth 1.0a User Context authentication via Tweepy v4+.

### Required Credentials

- **API Key (Consumer Key)**: Identifies your app
- **API Secret (Consumer Secret)**: App secret key
- **Access Token**: User-specific token
- **Access Token Secret**: Token secret

### Getting Credentials

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a project and app (if you haven't)
3. Navigate to "Keys and Tokens" section
4. Generate/regenerate keys as needed
5. Set app permissions to "Read and Write" for posting

## Tweepy Client Methods

### create_tweet()

Publishes a single tweet.

**Parameters:**
- `text` (str): Tweet content (max 280 chars)
- `in_reply_to_tweet_id` (Optional[int]): Reply to a tweet (for threads)

**Returns:**
- Response object with `data['id']` containing the tweet ID

**Example:**
```python
response = client.create_tweet(text="Hello Twitter!")
tweet_id = response.data['id']
```

## Text Length Limits

- **Standard tweet**: 280 characters
- **Thread numbering**: Reserves ~6 characters (e.g., " 12/50")
- **Effective limit per tweet in thread**: 274 characters

## Thread Publishing Strategy

1. Split long text into chunks at paragraph boundaries
2. Fall back to sentence boundaries if paragraphs are too long
3. Hard split if single sentence exceeds limit
4. Add numbering to each tweet (e.g., "1/5")
5. Publish first tweet, then reply to it with subsequent tweets

## Error Handling

Common errors:
- **401 Unauthorized**: Invalid credentials
- **403 Forbidden**: App doesn't have write permissions
- **429 Too Many Requests**: Rate limit exceeded
- **DuplicateTweet**: Identical tweet posted recently

## Rate Limits

- **Tweets**: 300 tweets per 3-hour window (user context)
- **Recommended**: Add delays between thread tweets (not strictly required but good practice)

## Best Practices

1. **Preview before publishing**: Use `--preview` flag to see how text will be split
2. **Paragraph-aware splitting**: Text is split intelligently at natural breaks
3. **Thread numbering**: Automatically added for user clarity
4. **Error recovery**: Check credentials and permissions if publishing fails