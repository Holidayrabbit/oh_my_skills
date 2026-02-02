#!/usr/bin/env python3
"""
Twitter Publisher Script
Publishes tweets and threads using Tweepy
"""

import os
import sys
import tweepy
import argparse
import json
from typing import List, Optional


class TwitterPublisher:
    """Handle Twitter publishing operations"""
    
    def __init__(self, api_key: str, api_secret: str, 
                 access_token: str, access_token_secret: str):
        """
        Initialize Twitter API client
        
        Args:
            api_key: Twitter API key
            api_secret: Twitter API secret
            access_token: Twitter access token
            access_token_secret: Twitter access token secret
        """
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
    
    def split_text(self, text: str, max_length: int = 280) -> List[str]:
        """
        Split long text into multiple tweets, preserving sentence/paragraph boundaries
        
        Args:
            text: The text to split
            max_length: Maximum characters per tweet (default 280)
            
        Returns:
            List of text chunks suitable for tweets
        """
        # Reserve space for thread numbering like "1/5"
        # This gives us room for up to 99 tweets (takes 5 chars: " 1/99")
        reserve_chars = 6
        effective_max = max_length - reserve_chars
        
        # If text fits in one tweet, return as-is
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        paragraphs = text.split('\n\n')
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # If adding this paragraph would exceed limit
            if current_chunk and len(current_chunk) + len(paragraph) + 2 > effective_max:
                # Save current chunk and start new one
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            # If paragraph itself is too long, split by sentences
            elif len(paragraph) > effective_max:
                # Save current chunk if exists
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                # Split paragraph by sentences
                sentences = paragraph.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').split('|')
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    if current_chunk and len(current_chunk) + len(sentence) + 1 > effective_max:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence
                    # If single sentence is too long, hard split it
                    elif len(sentence) > effective_max:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = ""
                        
                        # Hard split long sentence
                        while len(sentence) > effective_max:
                            chunks.append(sentence[:effective_max].strip())
                            sentence = sentence[effective_max:]
                        if sentence:
                            current_chunk = sentence
                    else:
                        current_chunk = (current_chunk + " " + sentence).strip() if current_chunk else sentence
            else:
                current_chunk = (current_chunk + "\n\n" + paragraph).strip() if current_chunk else paragraph
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Add thread numbering if multiple chunks
        if len(chunks) > 1:
            total = len(chunks)
            chunks = [f"{chunk}\n\n{i+1}/{total}" for i, chunk in enumerate(chunks)]
        
        return chunks
    
    def publish_single_tweet(self, text: str) -> dict:
        """
        Publish a single tweet
        
        Args:
            text: Tweet content
            
        Returns:
            Response data from Twitter API
        """
        response = self.client.create_tweet(text=text)
        return {
            'success': True,
            'tweet_id': response.data['id'],
            'text': text
        }
    
    def publish_thread(self, text: str) -> dict:
        """
        Publish a thread of tweets
        
        Args:
            text: Long text to split into thread
            
        Returns:
            Response data with all tweet IDs
        """
        chunks = self.split_text(text)
        
        if len(chunks) == 1:
            return self.publish_single_tweet(chunks[0])
        
        tweet_ids = []
        previous_tweet_id = None
        
        for i, chunk in enumerate(chunks):
            if previous_tweet_id:
                # Reply to previous tweet to create thread
                response = self.client.create_tweet(
                    text=chunk,
                    in_reply_to_tweet_id=previous_tweet_id
                )
            else:
                # First tweet in thread
                response = self.client.create_tweet(text=chunk)
            
            tweet_id = response.data['id']
            tweet_ids.append(tweet_id)
            previous_tweet_id = tweet_id
        
        return {
            'success': True,
            'thread_length': len(chunks),
            'tweet_ids': tweet_ids,
            'first_tweet_id': tweet_ids[0]
        }


def main():
    parser = argparse.ArgumentParser(description='Publish tweets and threads to Twitter')
    parser.add_argument('--text', type=str, help='Tweet text (or path to file with @ prefix)')
    parser.add_argument('--thread', action='store_true', help='Publish as thread if text is long')
    parser.add_argument('--api-key', type=str, help='Twitter API key')
    parser.add_argument('--api-secret', type=str, help='Twitter API secret')
    parser.add_argument('--access-token', type=str, help='Twitter access token')
    parser.add_argument('--access-token-secret', type=str, help='Twitter access token secret')
    parser.add_argument('--preview', action='store_true', help='Preview split without publishing')
    
    args = parser.parse_args()
    
    # Get text from argument or file
    text = args.text
    if text.startswith('@'):
        # Read from file
        file_path = text[1:]
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    
    # Get credentials from args or environment
    api_key = args.api_key or os.environ.get('TWITTER_API_KEY')
    api_secret = args.api_secret or os.environ.get('TWITTER_API_SECRET')
    access_token = args.access_token or os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = args.access_token_secret or os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("Error: Missing Twitter credentials", file=sys.stderr)
        print("Provide via arguments or environment variables:", file=sys.stderr)
        print("  TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET", file=sys.stderr)
        sys.exit(1)
    
    publisher = TwitterPublisher(api_key, api_secret, access_token, access_token_secret)
    
    # Preview mode
    if args.preview:
        chunks = publisher.split_text(text)
        print(f"Text will be split into {len(chunks)} tweet(s):")
        print("=" * 50)
        for i, chunk in enumerate(chunks, 1):
            print(f"\nTweet {i}:")
            print(chunk)
            print(f"Characters: {len(chunk)}")
            print("=" * 50)
        sys.exit(0)
    
    # Publish
    try:
        if args.thread or len(text) > 280:
            result = publisher.publish_thread(text)
            print(json.dumps(result, indent=2))
        else:
            result = publisher.publish_single_tweet(text)
            print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error publishing tweet: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()