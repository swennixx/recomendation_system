"""
Модуль для генерации тестовых данных покупок пользователей.
Создает данные о товарах и истории покупок для обучения рекомендательной системы.
"""

import pandas as pd
import numpy as np
import random


def generate_sample_data():
    """
    Генерирует тестовые данные о товарах и покупках пользователей.
    
    Создает данные о:
    - Товарах (название, категория, цена)
    - Истории покупок пользователей
    
    Returns:
        tuple: (products_df, purchases_df) - два датафрейма с товарами и покупками
    """
    
    categories = ['Электроника', 'Книги', 'Одежда', 'Спорт', 'Еда', 'Дом']
    
    products_by_category = {
        'Электроника': ['Ноутбук', 'Смартфон', 'Наушники', 'Клавиатура', 'Мышь', 'Монитор'],
        'Книги': ['Программирование', 'Фантастика', 'Детектив', 'История', 'Психология', 'Бизнес'],
        'Одежда': ['Футболка', 'Джинсы', 'Куртка', 'Кроссовки', 'Платье', 'Свитер'],
        'Спорт': ['Мяч', 'Гантели', 'Коврик для йоги', 'Скакалка', 'Бутылка для воды', 'Велосипед'],
        'Еда': ['Кофе', 'Чай', 'Шоколад', 'Печенье', 'Орехи', 'Сухофрукты'],
        'Дом': ['Подушка', 'Одеяло', 'Лампа', 'Ваза', 'Рамка для фото', 'Свечи']
    }
    
    products = []
    product_id = 1
    
    for category in categories:
        for product_name in products_by_category[category]:
            price = random.randint(100, 10000)
            products.append({
                'product_id': product_id,
                'name': product_name,
                'category': category,
                'price': price
            })
            product_id += 1
    
    products_df = pd.DataFrame(products)
    
    purchases = []
    num_users = 50
    
    for user_id in range(1, num_users + 1):
        num_purchases = random.randint(3, 15)
        
        purchased_products = random.sample(range(1, len(products) + 1), num_purchases)
        
        for prod_id in purchased_products:
            rating = random.randint(1, 5)
            purchases.append({
                'user_id': user_id,
                'product_id': prod_id,
                'rating': rating
            })
    
    purchases_df = pd.DataFrame(purchases)
    
    return products_df, purchases_df


def save_data_to_csv(products_df, purchases_df):
    """
    Сохраняет датафреймы в CSV файлы.
    
    Args:
        products_df: датафрейм с товарами
        purchases_df: датафрейм с покупками
    """
    products_df.to_csv('data/products.csv', index=False)
    purchases_df.to_csv('data/purchases.csv', index=False)
    print("Данные сохранены в папку data/")


if __name__ == '__main__':
    import os
    os.makedirs('data', exist_ok=True)
    
    print("Генерация тестовых данных...")
    products, purchases = generate_sample_data()
    
    save_data_to_csv(products, purchases)
    print(f"\nСоздано товаров: {len(products)}")
    print(f"Создано покупок: {len(purchases)}")
    print(f"\nПример товаров:")
    print(products.head())
    print(f"\nПример покупок:")
    print(purchases.head())
