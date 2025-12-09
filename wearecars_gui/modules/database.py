"""
Database Module - SQLite Database Management
WeAreCars Car Rental System
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

class Database:
    def __init__(self, db_path='data/bookings.db'):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.insert_sample_data()
    
    def connect(self):
        """Connect to SQLite database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Create necessary database tables."""
        # Customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                surname TEXT NOT NULL,
                address TEXT NOT NULL,
                age INTEGER NOT NULL,
                license_valid INTEGER NOT NULL,
                created_date TEXT NOT NULL
            )
        ''')
        
        # Bookings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                car_type TEXT NOT NULL,
                fuel_type TEXT NOT NULL,
                days INTEGER NOT NULL,
                unlimited_mileage INTEGER DEFAULT 0,
                breakdown_cover INTEGER DEFAULT 0,
                base_cost REAL NOT NULL,
                car_surcharge REAL NOT NULL,
                fuel_surcharge REAL NOT NULL,
                extras_cost REAL NOT NULL,
                total_cost REAL NOT NULL,
                booking_date TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT DEFAULT 'Active',
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Cars inventory table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_type TEXT NOT NULL,
                daily_rate REAL NOT NULL,
                surcharge REAL NOT NULL,
                available INTEGER DEFAULT 1,
                description TEXT
            )
        ''')
        
        self.conn.commit()
    
    def insert_sample_data(self):
        """Insert sample data for testing."""
        # Check if cars already exist
        self.cursor.execute('SELECT COUNT(*) FROM cars')
        if self.cursor.fetchone()[0] == 0:
            cars = [
                ('City Car', 25.0, 0.0, 1, 'Perfect for urban driving'),
                ('Family Car', 25.0, 50.0, 1, 'Spacious and comfortable'),
                ('Sports Car', 25.0, 75.0, 1, 'High performance vehicle'),
                ('SUV', 25.0, 65.0, 1, 'All-terrain capability'),
            ]
            self.cursor.executemany(
                'INSERT INTO cars (car_type, daily_rate, surcharge, available, description) VALUES (?, ?, ?, ?, ?)',
                cars
            )
        
        # Check if sample bookings exist
        self.cursor.execute('SELECT COUNT(*) FROM bookings')
        if self.cursor.fetchone()[0] == 0:
            # Sample customers
            customers = [
                ('John', 'Smith', '123 Main St, London', 35, 1),
                ('Emma', 'Johnson', '456 Park Ave, Manchester', 28, 1),
                ('Michael', 'Brown', '789 Oak Rd, Birmingham', 42, 1),
            ]
            
            for first, last, addr, age, lic in customers:
                self.cursor.execute(
                    'INSERT INTO customers (first_name, surname, address, age, license_valid, created_date) VALUES (?, ?, ?, ?, ?, ?)',
                    (first, last, addr, age, lic, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                )
                customer_id = self.cursor.lastrowid
                
                # Create a booking for this customer
                car_types = ['City Car', 'Family Car', 'Sports Car', 'SUV']
                fuel_types = ['Petrol', 'Diesel', 'Hybrid', 'Electric']
                car_type = random.choice(car_types)
                fuel_type = random.choice(fuel_types)
                days = random.randint(3, 14)
                
                # Calculate costs
                base_cost = 25.0 * days
                car_surcharges = {'City Car': 0, 'Family Car': 50, 'Sports Car': 75, 'SUV': 65}
                fuel_surcharges = {'Petrol': 0, 'Diesel': 0, 'Hybrid': 30, 'Electric': 50}
                
                car_surcharge = car_surcharges[car_type]
                fuel_surcharge = fuel_surcharges[fuel_type]
                extras_cost = random.choice([0, 10 * days, 2 * days])
                total = base_cost + car_surcharge + fuel_surcharge + extras_cost
                
                start_date = datetime.now() - timedelta(days=random.randint(1, 10))
                end_date = start_date + timedelta(days=days)
                
                self.cursor.execute('''
                    INSERT INTO bookings (customer_id, customer_name, car_type, fuel_type, days,
                                        unlimited_mileage, breakdown_cover, base_cost, car_surcharge,
                                        fuel_surcharge, extras_cost, total_cost, booking_date,
                                        start_date, end_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    customer_id,
                    f"{first} {last}",
                    car_type,
                    fuel_type,
                    days,
                    1 if extras_cost == 10 * days else 0,
                    1 if extras_cost == 2 * days else 0,
                    base_cost,
                    car_surcharge,
                    fuel_surcharge,
                    extras_cost,
                    total,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    start_date.strftime('%Y-%m-%d'),
                    end_date.strftime('%Y-%m-%d'),
                    'Active'
                ))
        
        self.conn.commit()
    
    def add_customer(self, first_name, surname, address, age, license_valid):
        """Add a new customer to the database."""
        self.cursor.execute('''
            INSERT INTO customers (first_name, surname, address, age, license_valid, created_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, surname, address, age, license_valid, 
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def add_booking(self, customer_id, customer_name, car_type, fuel_type, days,
                   unlimited_mileage, breakdown_cover, base_cost, car_surcharge,
                   fuel_surcharge, extras_cost, total_cost, start_date):
        """Add a new booking to the database."""
        end_date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=days)
        
        self.cursor.execute('''
            INSERT INTO bookings (customer_id, customer_name, car_type, fuel_type, days,
                                unlimited_mileage, breakdown_cover, base_cost, car_surcharge,
                                fuel_surcharge, extras_cost, total_cost, booking_date,
                                start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            customer_id, customer_name, car_type, fuel_type, days,
            unlimited_mileage, breakdown_cover, base_cost, car_surcharge,
            fuel_surcharge, extras_cost, total_cost,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            start_date,
            end_date.strftime('%Y-%m-%d'),
            'Active'
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_all_bookings(self):
        """Retrieve all bookings from the database."""
        self.cursor.execute('''
            SELECT id, customer_name, car_type, fuel_type, days, total_cost,
                   booking_date, start_date, end_date, status
            FROM bookings
            ORDER BY id DESC
        ''')
        return self.cursor.fetchall()
    
    def search_bookings(self, search_term):
        """Search bookings by customer name or booking ID."""
        self.cursor.execute('''
            SELECT id, customer_name, car_type, fuel_type, days, total_cost,
                   booking_date, start_date, end_date, status
            FROM bookings
            WHERE customer_name LIKE ? OR CAST(id AS TEXT) LIKE ?
            ORDER BY id DESC
        ''', (f'%{search_term}%', f'%{search_term}%'))
        return self.cursor.fetchall()
    
    def get_booking_stats(self):
        """Get statistics for dashboard."""
        stats = {}
        
        # Total bookings
        self.cursor.execute('SELECT COUNT(*) FROM bookings')
        stats['total_bookings'] = self.cursor.fetchone()[0]
        
        # Total revenue
        self.cursor.execute('SELECT SUM(total_cost) FROM bookings')
        total = self.cursor.fetchone()[0]
        stats['total_revenue'] = total if total else 0.0
        
        # Active bookings
        self.cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'Active'")
        stats['active_bookings'] = self.cursor.fetchone()[0]
        
        # Most popular car type
        self.cursor.execute('''
            SELECT car_type, COUNT(*) as count
            FROM bookings
            GROUP BY car_type
            ORDER BY count DESC
            LIMIT 1
        ''')
        result = self.cursor.fetchone()
        stats['popular_car'] = result[0] if result else 'N/A'
        
        return stats
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
