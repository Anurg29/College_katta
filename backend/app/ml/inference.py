import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import pickle
import os


class CollaborativeFilter:
    """Collaborative filtering for user-user recommendations"""
    
    def __init__(self):
        self.user_item_matrix = None
        self.user_similarity = None
        self.user_ids = []
        
    def fit(self, interactions: List[Dict]):
        """
        Build user-item interaction matrix
        
        Args:
            interactions: List of dicts with keys: user_id, target_id, interaction_type, created_at
        """
        if not interactions:
            return
        
        # Create DataFrame
        df = pd.DataFrame(interactions)
        
        # Weight different interaction types
        interaction_weights = {
            'view': 1,
            'like': 3,
            'bookmark': 4,
            'share': 5,
            'comment': 6,
            'join': 7
        }
        
        df['weight'] = df['interaction_type'].map(interaction_weights)
        
        # Create user-item matrix
        self.user_item_matrix = df.pivot_table(
            index='user_id',
            columns='target_id',
            values='weight',
            aggfunc='sum',
            fill_value=0
        )
        
        self.user_ids = self.user_item_matrix.index.tolist()
        
        # Calculate user similarity matrix
        self.user_similarity = cosine_similarity(self.user_item_matrix)
        
    def get_similar_users(self, user_id: str, n: int = 10) -> List[Tuple[str, float]]:
        """Get N most similar users"""
        if user_id not in self.user_ids:
            return []
        
        user_idx = self.user_ids.index(user_id)
        similarities = self.user_similarity[user_idx]
        
        # Get indices of most similar users (excluding self)
        similar_indices = np.argsort(similarities)[::-1][1:n+1]
        
        return [(self.user_ids[idx], similarities[idx]) for idx in similar_indices]
    
    def recommend_items(self, user_id: str, n: int = 10) -> List[str]:
        """Recommend items based on similar users"""
        if user_id not in self.user_ids:
            return []
        
        similar_users = self.get_similar_users(user_id, n=20)
        
        # Get items interacted by similar users but not by target user
        user_idx = self.user_ids.index(user_id)
        user_items = set(self.user_item_matrix.iloc[user_idx][self.user_item_matrix.iloc[user_idx] > 0].index)
        
        recommendations = {}
        for similar_user_id, similarity in similar_users:
            similar_user_idx = self.user_ids.index(similar_user_id)
            similar_user_items = self.user_item_matrix.iloc[similar_user_idx]
            
            for item_id, score in similar_user_items[similar_user_items > 0].items():
                if item_id not in user_items:
                    recommendations[item_id] = recommendations.get(item_id, 0) + (score * similarity)
        
        # Sort by score and return top N
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [item_id for item_id, _ in sorted_recommendations[:n]]


class ContentBasedFilter:
    """Content-based filtering using user profiles and item features"""
    
    def __init__(self):
        self.user_profiles = {}
        self.item_features = {}
        
    def build_user_profile(self, user_id: str, skills: List[str], interests: List[str]):
        """Build user profile vector"""
        self.user_profiles[user_id] = {
            'skills': set(skills),
            'interests': set(interests)
        }
    
    def add_item_features(self, item_id: str, tags: List[str], category: str):
        """Add item features"""
        self.item_features[item_id] = {
            'tags': set(tags),
            'category': category
        }
    
    def calculate_similarity(self, user_id: str, item_id: str) -> float:
        """Calculate similarity between user and item"""
        if user_id not in self.user_profiles or item_id not in self.item_features:
            return 0.0
        
        user_profile = self.user_profiles[user_id]
        item_features = self.item_features[item_id]
        
        # Calculate Jaccard similarity for skills/tags
        skills_tags_union = user_profile['skills'] | item_features['tags']
        skills_tags_intersection = user_profile['skills'] & item_features['tags']
        
        if len(skills_tags_union) == 0:
            skill_similarity = 0
        else:
            skill_similarity = len(skills_tags_intersection) / len(skills_tags_union)
        
        # Check interest-category match
        category_match = 1.0 if item_features['category'] in user_profile['interests'] else 0.0
        
        # Weighted combination
        return 0.7 * skill_similarity + 0.3 * category_match
    
    def recommend_items(self, user_id: str, candidate_items: List[str], n: int = 10) -> List[str]:
        """Recommend items based on content similarity"""
        scores = [(item_id, self.calculate_similarity(user_id, item_id)) for item_id in candidate_items]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [item_id for item_id, _ in scores[:n]]


class HybridRecommender:
    """Hybrid recommendation system combining collaborative and content-based filtering"""
    
    def __init__(self, collaborative_weight: float = 0.6, content_weight: float = 0.4):
        self.collaborative_filter = CollaborativeFilter()
        self.content_filter = ContentBasedFilter()
        self.collaborative_weight = collaborative_weight
        self.content_weight = content_weight
        
    def train_collaborative(self, interactions: List[Dict]):
        """Train collaborative filtering model"""
        self.collaborative_filter.fit(interactions)
    
    def add_user_profile(self, user_id: str, skills: List[str], interests: List[str]):
        """Add user profile for content-based filtering"""
        self.content_filter.build_user_profile(user_id, skills, interests)
    
    def add_item_features(self, item_id: str, tags: List[str], category: str):
        """Add item features for content-based filtering"""
        self.content_filter.add_item_features(item_id, tags, category)
    
    def recommend(self, user_id: str, candidate_items: List[str] = None, n: int = 10) -> List[str]:
        """Generate hybrid recommendations"""
        
        # Get collaborative recommendations
        collab_recs = self.collaborative_filter.recommend_items(user_id, n=n*2)
        
        # If no candidate items provided, use collaborative recommendations
        if candidate_items is None:
            candidate_items = collab_recs
        
        # Get content-based scores for candidates
        content_scores = {
            item_id: self.content_filter.calculate_similarity(user_id, item_id)
            for item_id in candidate_items
        }
        
        # Combine scores
        final_scores = {}
        for item_id in candidate_items:
            collab_score = 1.0 if item_id in collab_recs else 0.0
            content_score = content_scores.get(item_id, 0.0)
            
            final_scores[item_id] = (
                self.collaborative_weight * collab_score +
                self.content_weight * content_score
            )
        
        # Sort and return top N
        sorted_items = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        return [item_id for item_id, _ in sorted_items[:n]]
    
    def save_model(self, path: str):
        """Save model to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_model(path: str):
        """Load model from disk"""
        with open(path, 'rb') as f:
            return pickle.load(f)


class TeamMatcher:
    """Match users for hackathon teams based on skills and preferences"""
    
    def __init__(self):
        pass
    
    def calculate_skill_complementarity(
        self,
        team_required_skills: List[str],
        user_skills: List[str]
    ) -> float:
        """Calculate how well user's skills match team requirements"""
        if not team_required_skills:
            return 0.5  # Neutral score if no requirements
        
        required_set = set(team_required_skills)
        user_set = set(user_skills)
        
        matched_skills = required_set & user_set
        return len(matched_skills) / len(required_set)
    
    def match_users_to_team(
        self,
        team_required_skills: List[str],
        candidate_users: List[Dict],
        n: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Match users to a team based on skill requirements
        
        Args:
            team_required_skills: List of required skill names
            candidate_users: List of dicts with keys: user_id, skills (list of skill names)
            n: Number of recommendations
            
        Returns:
            List of (user_id, match_score) tuples
        """
        scores = []
        for user in candidate_users:
            score = self.calculate_skill_complementarity(
                team_required_skills,
                user.get('skills', [])
            )
            scores.append((user['user_id'], score))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]


# Global recommender instance
recommender = HybridRecommender()
team_matcher = TeamMatcher()
