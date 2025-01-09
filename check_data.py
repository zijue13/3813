 from app import db, Dish

dishes = Dish.query.all()
for dish in dishes:
    print(f"Name: {dish.name}, Ingredients: {dish.ingredients}, Image: {dish.image_filename}")
