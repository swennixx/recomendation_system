"""
Модуль рекомендательной системы на основе коллаборативной фильтрации.
Использует алгоритм k-ближайших соседей для поиска похожих пользователей.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationSystem:
    """
    Класс для создания рекомендаций товаров пользователям.
    Работает на основе истории покупок и оценок других пользователей.
    """
    
    def __init__(self):
        """
        Инициализация рекомендательной системы.
        Загружает данные о товарах и покупках.
        """
        self.products_df = None
        self.purchases_df = None
        self.user_item_matrix = None
        
    def load_data(self, products_path='data/products.csv', purchases_path='data/purchases.csv'):
        """
        Загружает данные из CSV файлов.
        
        Args:
            products_path: путь к файлу с товарами
            purchases_path: путь к файлу с покупками
        """
        self.products_df = pd.read_csv(products_path)
        self.purchases_df = pd.read_csv(purchases_path)
        
        self.user_item_matrix = self.purchases_df.pivot_table(
            index='user_id',
            columns='product_id',
            values='rating',
            fill_value=0
        )
        
    def find_similar_users(self, user_id, num_similar=5):
        """
        Находит похожих пользователей на основе их покупок.
        
        Args:
            user_id: ID пользователя
            num_similar: количество похожих пользователей для поиска
            
        Returns:
            list: список ID похожих пользователей
        """
        if user_id not in self.user_item_matrix.index:
            return []
        
        user_similarity = cosine_similarity(self.user_item_matrix)
        
        similarity_df = pd.DataFrame(
            user_similarity,
            index=self.user_item_matrix.index,
            columns=self.user_item_matrix.index
        )
        
        similar_users = similarity_df[user_id].sort_values(ascending=False)[1:num_similar+1]
        
        return similar_users.index.tolist()
    
    def get_recommendations(self, user_id, num_recommendations=5):
        """
        Генерирует рекомендации товаров для пользователя.
        
        Алгоритм:
        1. Находит похожих пользователей
        2. Смотрит, что они покупали
        3. Исключает товары, которые пользователь уже купил
        4. Возвращает топ товаров с лучшими оценками
        
        Args:
            user_id: ID пользователя
            num_recommendations: количество рекомендаций
            
        Returns:
            DataFrame: датафрейм с рекомендованными товарами
        """
        similar_users = self.find_similar_users(user_id)
        
        if not similar_users:
            return self.get_popular_products(num_recommendations)
        
        user_purchases = self.purchases_df[self.purchases_df['user_id'] == user_id]['product_id'].tolist()
        
        similar_purchases = self.purchases_df[
            (self.purchases_df['user_id'].isin(similar_users)) &
            (~self.purchases_df['product_id'].isin(user_purchases))
        ]
        
        # Группируем по товару и считаем средний рейтинг
        recommendations = similar_purchases.groupby('product_id').agg({
            'rating': 'mean',
            'user_id': 'count'
        }).rename(columns={'user_id': 'count'})
        
        recommendations = recommendations.sort_values(
            by=['rating', 'count'],
            ascending=False
        ).head(num_recommendations)
        
        recommendations = recommendations.merge(
            self.products_df,
            left_index=True,
            right_on='product_id'
        )
        
        return recommendations[['product_id', 'name', 'category', 'price', 'rating', 'count']]
    
    def get_popular_products(self, num_products=5):
        """
        Возвращает самые популярные товары.
        Используется как запасной вариант, если нет данных о пользователе.
        
        Args:
            num_products: количество товаров
            
        Returns:
            DataFrame: датафрейм с популярными товарами
        """
        popular = self.purchases_df.groupby('product_id').agg({
            'rating': 'mean',
            'user_id': 'count'
        }).rename(columns={'user_id': 'count'})
        
        popular = popular.sort_values(
            by=['rating', 'count'],
            ascending=False
        ).head(num_products)
        
        popular = popular.merge(
            self.products_df,
            left_index=True,
            right_on='product_id'
        )
        
        return popular[['product_id', 'name', 'category', 'price', 'rating', 'count']]
    
    def get_user_purchases(self, user_id):
        """
        Получает историю покупок пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            DataFrame: датафрейм с покупками пользователя
        """
        user_data = self.purchases_df[self.purchases_df['user_id'] == user_id]
        
        user_data = user_data.merge(
            self.products_df,
            on='product_id'
        )
        
        return user_data[['product_id', 'name', 'category', 'price', 'rating']]


if __name__ == '__main__':
    print("Инициализация рекомендательной системы...")
    rs = RecommendationSystem()
    
    print("Загрузка данных...")
    rs.load_data()
    
    test_user = 1
    print(f"\nИстория покупок пользователя {test_user}:")
    print(rs.get_user_purchases(test_user))
    
    print(f"\nРекомендации для пользователя {test_user}:")
    print(rs.get_recommendations(test_user))
    
    print("\nСамые популярные товары:")
    print(rs.get_popular_products())
