"""
Sentiment analysis module using VADER
"""

import logging
from typing import Dict
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import re


class SentimentAnalyzer:
    """Performs sentiment analysis on review text"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._download_nltk_resources()
        self.sia = SentimentIntensityAnalyzer()
        
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
    
    def _download_nltk_resources(self):
        """Download required NLTK resources"""
        resources = ['vader_lexicon', 'stopwords', 'punkt']
        
        for resource in resources:
            try:
                nltk.data.find(f'sentiment/{resource}' if resource == 'vader_lexicon' 
                             else f'corpora/{resource}' if resource == 'stopwords' 
                             else f'tokenizers/{resource}')
            except LookupError:
                try:
                    nltk.download(resource, quiet=True)
                except Exception as e:
                    self.logger.warning(f"Could not download {resource}: {str(e)}")
    
    def analyze_sentiment(self, text: str) -> float:
        """
        Analyze sentiment of text using VADER
        
        Args:
            text: Review text to analyze
            
        Returns:
            Compound sentiment score between -1 (negative) and 1 (positive)
        """
        if not text or not isinstance(text, str):
            return 0.0
        
        try:
            # Clean text
            cleaned_text = self._preprocess_text(text)
            
            # Get sentiment scores
            scores = self.sia.polarity_scores(cleaned_text)
            
            # Return compound score
            return scores['compound']
            
        except Exception as e:
            self.logger.warning(f"Error analyzing sentiment: {str(e)}")
            return 0.0
    
    def analyze_sentiment_detailed(self, text: str) -> Dict[str, float]:
        """
        Get detailed sentiment analysis
        
        Args:
            text: Review text to analyze
            
        Returns:
            Dictionary with positive, negative, neutral, and compound scores
        """
        if not text or not isinstance(text, str):
            return {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
        
        try:
            cleaned_text = self._preprocess_text(text)
            scores = self.sia.polarity_scores(cleaned_text)
            return scores
            
        except Exception as e:
            self.logger.warning(f"Error in detailed sentiment analysis: {str(e)}")
            return {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for sentiment analysis
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def get_sentiment_label(self, score: float) -> str:
        """
        Convert sentiment score to label
        
        Args:
            score: Compound sentiment score
            
        Returns:
            'Positive', 'Negative', or 'Neutral'
        """
        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    
    def batch_analyze(self, texts: list) -> list:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of text strings
            
        Returns:
            List of compound sentiment scores
        """
        return [self.analyze_sentiment(text) for text in texts]
    
    def extract_keywords(self, text: str, top_n: int = 10) -> list:
        """
        Extract top keywords from text
        
        Args:
            text: Review text
            top_n: Number of keywords to return
            
        Returns:
            List of keywords
        """
        try:
            # Tokenize and clean
            words = text.lower().split()
            
            # Remove stopwords and short words
            keywords = [word for word in words 
                       if word not in self.stop_words 
                       and len(word) > 3
                       and word.isalpha()]
            
            # Count frequency
            from collections import Counter
            word_freq = Counter(keywords)
            
            # Return top keywords
            return [word for word, _ in word_freq.most_common(top_n)]
            
        except Exception as e:
            self.logger.warning(f"Error extracting keywords: {str(e)}")
            return []