#!/usr/bin/env python3
"""
Test text splitting without requiring Tweepy
"""

import sys


def split_text(text: str, max_length: int = 280):
    """Split long text into multiple tweets"""
    reserve_chars = 6
    effective_max = max_length - reserve_chars
    
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    paragraphs = text.split('\n\n')
    current_chunk = ""
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        
        if current_chunk and len(current_chunk) + len(paragraph) + 2 > effective_max:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
        elif len(paragraph) > effective_max:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            
            sentences = paragraph.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').replace('。', '。|').split('|')
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                if current_chunk and len(current_chunk) + len(sentence) + 1 > effective_max:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                elif len(sentence) > effective_max:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = ""
                    
                    while len(sentence) > effective_max:
                        chunks.append(sentence[:effective_max].strip())
                        sentence = sentence[effective_max:]
                    if sentence:
                        current_chunk = sentence
                else:
                    current_chunk = (current_chunk + " " + sentence).strip() if current_chunk else sentence
        else:
            current_chunk = (current_chunk + "\n\n" + paragraph).strip() if current_chunk else paragraph
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    if len(chunks) > 1:
        total = len(chunks)
        chunks = [f"{chunk}\n\n{i+1}/{total}" for i, chunk in enumerate(chunks)]
    
    return chunks


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_split.py <text_or_@file>")
        sys.exit(1)
    
    text = sys.argv[1]
    if text.startswith('@'):
        with open(text[1:], 'r', encoding='utf-8') as f:
            text = f.read()
    
    chunks = split_text(text)
    
    print(f"Text will be split into {len(chunks)} tweet(s):")
    print("=" * 60)
    for i, chunk in enumerate(chunks, 1):
        print(f"\nTweet {i}:")
        print(chunk)
        print(f"Characters: {len(chunk)}")
        print("=" * 60)