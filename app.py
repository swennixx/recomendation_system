"""
Flask веб-приложение для рекомендательной системы.
Предоставляет веб-интерфейс для получения рекомендаций и просмотра аналитики.
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from recommendation_engine import RecommendationSystem
from data_analyzer import DataAnalyzer

app = Flask(__name__)

recommendation_system = RecommendationSystem()
analyzer = None


def initialize_system():
    """
    Инициализирует систему и загружает данные.
    Вызывается при запуске приложения.
    """
    global recommendation_system, analyzer
    
    if not os.path.exists('data/products.csv') or not os.path.exists('data/purchases.csv'):
        print("Данные не найдены. Генерируем тестовые данные...")
        from data_generator import generate_sample_data, save_data_to_csv
        
        os.makedirs('data', exist_ok=True)
        products, purchases = generate_sample_data()
        save_data_to_csv(products, purchases)
    
    print("Загрузка данных...")
    recommendation_system.load_data()
    
    analyzer = DataAnalyzer(
        recommendation_system.products_df,
        recommendation_system.purchases_df
    )
    
    print("Система готова к работе!")


@app.route('/')
def index():
    """
    Главная страница приложения.
    Показывает форму для выбора пользователя.
    """
    users = recommendation_system.purchases_df['user_id'].unique().tolist()
    users.sort()
    
    return render_template('index.html', users=users)


@app.route('/recommendations/<int:user_id>')
def recommendations(user_id):
    """
    Страница с рекомендациями для конкретного пользователя.
    
    Args:
        user_id: ID пользователя
    """
    user_purchases = recommendation_system.get_user_purchases(user_id)
    
    recommendations_df = recommendation_system.get_recommendations(user_id, num_recommendations=10)
    
    purchases_list = user_purchases.to_dict('records')
    recommendations_list = recommendations_df.to_dict('records')
    
    return render_template(
        'recommendations.html',
        user_id=user_id,
        purchases=purchases_list,
        recommendations=recommendations_list
    )


@app.route('/analytics')
def analytics():
    """
    Страница с аналитикой и визуализацией данных.
    Показывает различные графики и статистику.
    """
    stats = analyzer.get_summary_statistics()
    
    category_stats = analyzer.get_category_statistics()
    category_stats_dict = category_stats.to_dict('index')
    
    dashboard = analyzer.create_dashboard()
    
    return render_template(
        'analytics.html',
        stats=stats,
        category_stats=category_stats_dict,
        dashboard=dashboard
    )


@app.route('/api/recommendations/<int:user_id>')
def api_recommendations(user_id):
    """
    API endpoint для получения рекомендаций в формате JSON.
    
    Args:
        user_id: ID пользователя
        
    Returns:
        JSON с рекомендациями
    """
    num_recommendations = request.args.get('num', default=5, type=int)
    recommendations_df = recommendation_system.get_recommendations(user_id, num_recommendations)
    
    return jsonify(recommendations_df.to_dict('records'))


@app.route('/api/popular')
def api_popular():
    """
    API endpoint для получения популярных товаров в формате JSON.
    
    Returns:
        JSON с популярными товарами
    """
    num_products = request.args.get('num', default=5, type=int)
    popular_df = recommendation_system.get_popular_products(num_products)
    
    return jsonify(popular_df.to_dict('records'))


@app.route('/api/stats')
def api_stats():
    """
    API endpoint для получения общей статистики в формате JSON.
    
    Returns:
        JSON со статистикой
    """
    stats = analyzer.get_summary_statistics()
    return jsonify(stats)


if __name__ == '__main__':
    initialize_system()
    
    print("\nЗапуск веб-сервера...")
    print("Откройте браузер и перейдите по адресу: http://127.0.0.1:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
