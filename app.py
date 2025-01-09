from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dishes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库模型：Dish
class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredients = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Dish {self.name}>'

# 初始化数据库（首次运行时创建数据库和表）
with app.app_context():
    db.create_all()

# 首页路由：显示菜品和筛选功能
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filter_option = request.form.get('filter_option')

        if filter_option == 'all':
            # 显示所有菜品
            dishes = Dish.query.all()
            return render_template('index.html', dishes=dishes, ingredient=None, filter_option='all')

        elif filter_option == 'filter':
            selected_ingredient = request.form.get('ingredient')
            dishes = Dish.query.filter(Dish.ingredients.contains(selected_ingredient)).all()

            if dishes:
                return render_template('index.html', dishes=dishes, ingredient=selected_ingredient)
            else:
                return render_template('index.html', message='Sorry, no matching dishes found.', ingredient=selected_ingredient)

    return render_template('index.html', dishes=None, message=None, ingredient=None, filter_option=None)

# 添加新菜品的路由
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        image_filename = request.form['image_filename']

        # 创建新菜品并保存到数据库
        new_dish = Dish(name=name, ingredients=ingredients, image_filename=image_filename)
        db.session.add(new_dish)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add.html')

# 添加示例数据的路由
@app.route('/add_sample_data')
def add_sample_data():
    sample_dishes = [
        {'ingredients': 'chicken,pepper,onion', 'name': 'Black Pepper Chicken', 'image_filename': 'black_pepper_chicken.jpg'},
        {'ingredients': 'fish,ginger,scallion', 'name': 'Steamed Fish', 'image_filename': 'steamed_fish.jpg'},
        {'ingredients': 'potato,beef', 'name': 'Beef Potato Stew', 'image_filename': 'beef_potato_stew.jpg'},
        {'ingredients': 'shrimp,garlic', 'name': 'Garlic Shrimp', 'image_filename': 'garlic_shrimp.jpg'},
        {'ingredients': 'tofu,beef', 'name': 'Mapo Tofu', 'image_filename': 'mapo_tofu.jpg'},
        {'ingredients': 'tofu,mushroom,vegetable', 'name': 'Tofu Mushroom Pot', 'image_filename': 'tofu_mushroom_pot.jpg'},
        {'ingredients': 'egg,tomato', 'name': 'Tomato Egg Stir-Fry', 'image_filename': 'tomato_egg.jpg'},
        {'ingredients': 'pork,green pepper', 'name': 'Pepper Pork Stir-Fry', 'image_filename': 'pepper_pork.jpg'},
        {'ingredients': 'lamb,onion', 'name': 'Cumin Lamb', 'image_filename': 'cumin_lamb.jpg'},
        {'ingredients': 'fish,tofu', 'name': 'Fish Tofu Soup', 'image_filename': 'fish_tofu_soup.jpg'},
        {'ingredients': 'beef,onion', 'name': 'Onion Beef Stir-Fry', 'image_filename': 'onion_beef.jpg'},
        {'ingredients': 'chicken,chili,garlic', 'name': 'Spicy Chicken Wings', 'image_filename': 'spicy_chicken_wings.jpg'},
        {'ingredients': 'rice,peas,carrot,egg', 'name': 'Vegetable Fried Rice', 'image_filename': 'vegetable_fried_rice.jpg'},
        {'ingredients': 'fish,lemon,herb', 'name': 'Lemon Herb Fish', 'image_filename': 'lemon_herb_fish.jpg'},
        {'ingredients': 'beef,noodles,scallion', 'name': 'Beef Noodle Soup', 'image_filename': 'beef_noodle_soup.jpg'}
    ]
    

    for dish in sample_dishes:
        sorted_ingredients = ','.join(sorted(dish['ingredients'].split(',')))
        if not Dish.query.filter_by(ingredients=sorted_ingredients).first():
            new_dish = Dish(
                ingredients=sorted_ingredients,
                name=dish['name'],
                image_filename=dish['image_filename']
            )
            db.session.add(new_dish)

    db.session.commit()
    return 'Sample data has been added!'

if __name__ == '__main__':
    app.run(debug=True)
