"""
Модуль для анализа и визуализации данных покупок.
Создает графики и статистику для понимания поведения пользователей.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class DataAnalyzer:
    """
    Класс для анализа данных покупок и создания визуализаций.
    """
    
    def __init__(self, products_df, purchases_df):
        """
        Инициализация анализатора данных.
        
        Args:
            products_df: датафрейм с товарами
            purchases_df: датафрейм с покупками
        """
        self.products_df = products_df
        self.purchases_df = purchases_df
        
    def get_category_statistics(self):
        """
        Вычисляет статистику по категориям товаров.
        
        Returns:
            DataFrame: статистика по каждой категории
        """
        merged_data = self.purchases_df.merge(self.products_df, on='product_id')
        
        category_stats = merged_data.groupby('category').agg({
            'product_id': 'count',  # количество покупок
            'rating': 'mean',       # средний рейтинг
            'price': 'sum'          # общая сумма продаж
        }).rename(columns={
            'product_id': 'total_purchases',
            'rating': 'avg_rating',
            'price': 'total_revenue'
        })
        
        return category_stats.round(2)
    
    def plot_category_distribution(self):
        """
        Создает круговую диаграмму распределения покупок по категориям.
        
        Returns:
            str: HTML код графика
        """
        merged_data = self.purchases_df.merge(self.products_df, on='product_id')
        
        category_counts = merged_data['category'].value_counts()
        
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Распределение покупок по категориям'
        )
        
        return fig.to_html(full_html=False)
    
    def plot_rating_distribution(self):
        """
        Создает гистограмму распределения оценок.
        
        Returns:
            str: HTML код графика
        """
        rating_counts = self.purchases_df['rating'].value_counts().sort_index()
        
        fig = px.bar(
            x=rating_counts.index,
            y=rating_counts.values,
            labels={'x': 'Оценка', 'y': 'Количество'},
            title='Распределение оценок товаров'
        )
        
        return fig.to_html(full_html=False)
    
    def plot_top_products(self, top_n=10):
        """
        Создает график топ-N самых покупаемых товаров.
        
        Args:
            top_n: количество топ товаров
            
        Returns:
            str: HTML код графика
        """
        product_purchases = self.purchases_df['product_id'].value_counts().head(top_n)
        
        product_names = []
        for product_id in product_purchases.index:
            name = self.products_df[self.products_df['product_id'] == product_id]['name'].values[0]
            product_names.append(name)
        
        fig = px.bar(
            x=product_purchases.values,
            y=product_names,
            orientation='h',
            labels={'x': 'Количество покупок', 'y': 'Товар'},
            title=f'Топ-{top_n} самых популярных товаров'
        )
        
        return fig.to_html(full_html=False)
    
    def plot_user_activity(self):
        """
        Создает гистограмму активности пользователей.
        
        Returns:
            str: HTML код графика
        """
        user_purchases = self.purchases_df.groupby('user_id').size()
        
        fig = px.histogram(
            x=user_purchases.values,
            nbins=20,
            labels={'x': 'Количество покупок', 'y': 'Количество пользователей'},
            title='Распределение активности пользователей'
        )
        
        return fig.to_html(full_html=False)
    
    def plot_price_by_category(self):
        """
        Создает box plot цен по категориям.
        
        Returns:
            str: HTML код графика
        """
        merged_data = self.purchases_df.merge(self.products_df, on='product_id')
        
        fig = px.box(
            merged_data,
            x='category',
            y='price',
            labels={'category': 'Категория', 'price': 'Цена (руб)'},
            title='Распределение цен по категориям'
        )
        
        return fig.to_html(full_html=False)
    
    def create_dashboard(self):
        """
        Создает комплексный дашборд со всеми графиками.
        
        Returns:
            dict: словарь с HTML кодами всех графиков
        """
        dashboard = {
            'category_distribution': self.plot_category_distribution(),
            'rating_distribution': self.plot_rating_distribution(),
            'top_products': self.plot_top_products(),
            'user_activity': self.plot_user_activity(),
            'price_by_category': self.plot_price_by_category()
        }
        
        return dashboard
    
    def get_summary_statistics(self):
        """
        Возвращает общую статистику по данным.
        
        Returns:
            dict: словарь со статистикой
        """
        merged_data = self.purchases_df.merge(self.products_df, on='product_id')
        
        stats = {
            'total_users': self.purchases_df['user_id'].nunique(),
            'total_products': self.products_df.shape[0],
            'total_purchases': self.purchases_df.shape[0],
            'avg_rating': round(self.purchases_df['rating'].mean(), 2),
            'total_revenue': merged_data['price'].sum(),
            'avg_purchase_price': round(merged_data['price'].mean(), 2),
            'most_popular_category': merged_data['category'].mode()[0]
        }
        
        return stats


if __name__ == '__main__':
    print("Загрузка данных...")
    products_df = pd.read_csv('data/products.csv')
    purchases_df = pd.read_csv('data/purchases.csv')
    
    analyzer = DataAnalyzer(products_df, purchases_df)
    analyzer = DataAnalyzer(products_df, purchases_df)
    
    print("\nОбщая статистика:")
    stats = analyzer.get_summary_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\nСтатистика по категориям:")
    print(analyzer.get_category_statistics())
