from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()
app = Flask(__name__)

def get_property_data():
    """Fetch geocoded property data from database"""
    try:
        db_params = {
            'host': os.getenv('LOCAL_PG_HOST'),
            'database': os.getenv('LOCAL_PG_DBNAME'), 
            'user': os.getenv('LOCAL_PG_USER'),
            'password': os.getenv('LOCAL_PG_PASSWORD'),
            'port': os.getenv('LOCAL_PG_PORT')
        }
        
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT owner_name, owner_address, city, state, zip, county,
                   property_description, operator, well_name, longitude, latitude
            FROM addresses_with_coords 
            WHERE geocoded = TRUE 
            AND longitude IS NOT NULL 
            AND latitude IS NOT NULL
            ORDER BY owner_name
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return results
        
    except Exception as e:
        print(f"Database error: {e}")
        return []

@app.route("/")
def index():
    access_token = os.getenv("MAPBOX_ACCESS_TOKEN")
    return render_template("index.html", access_token=access_token)

@app.route("/api/properties")
def get_properties():
    """API endpoint to get property data as JSON"""
    properties = get_property_data()
    return jsonify(properties)

if __name__ == "__main__":
    app.run(debug=True)