
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Read the new Excel file into a DataFrame
df = pd.read_excel('products.xlsx')

@app.route('/')
def index():
    grouped = df.groupby('Category')[['Inner', 'Productname', 'image_name']].apply(lambda x: x.to_dict('records')).to_dict()
    return render_template('index.html', grouped_products=grouped)

@app.route('/product/<int:product_id>')
def product(product_id):
    product_info = df[df['Inner'] == product_id].iloc[0].to_dict()
    # Calculate the minimum price among the wholesalers
    wholesaler_columns = ['BESTWAY', 'PARFETTS', 'S&W', 'BOOKER (LONDIS)', 'MUSGRAVE', 'BOOKER']
    min_price = min(product_info[col] for col in wholesaler_columns if product_info[col] is not None)
    return render_template('product.html', product=product_info, min_price=min_price)

if __name__ == '__main__':
    app.run(debug=True)


# Define the static folder for CSS and JS files
app.static_folder = 'static'