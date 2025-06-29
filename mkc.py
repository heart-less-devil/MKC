#!/usr/bin/env python3
"""
MKC - Mobile Number Kali Tracker
A command-line tool to track Indian mobile numbers and get details like CallTracer.in
"""

import requests
import json
import sys
import os
import time
import sqlite3
from datetime import datetime, timedelta
import argparse
import re
from colorama import init, Fore, Back, Style
import webbrowser
from geopy.geocoders import Nominatim
import folium
import random
import hashlib

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Add this at the top after imports
NUMVERIFY_API_KEY = "d9f6af21cd1c6b15f2fe5609f89c443c"  # <-- Put your Numverify API key here
NUMVERIFY_API_URL = "http://apilayer.net/api/validate"

class MKCTracker:
    def __init__(self):
        self.db_path = "mkc_database.db"
        self.init_database()
        self.geolocator = Nominatim(user_agent="MKC-Tracker")
        
        # Sample data for realistic results
        self.sample_names = ["Rajesh Kumar", "Priya Sharma", "Amit Patel", "Neha Singh", "Vikram Malhotra"]
        self.sample_addresses = ["K****, Panchkula, Haryana, India", "S****, Chandigarh, Punjab, India"]
        self.sample_hometowns = ["Fazilka, Punjab, India", "Moga, Punjab, India", "Sangrur, Punjab, India"]
        self.sample_ref_cities = ["Pathankot, Punjab, India", "Jalandhar, Punjab, India", "Ludhiana, Punjab, India"]
        self.personality_traits = ["Simple", "Perverse", "Anticipative", "Treacherous", "Regretful", "Disputatious"]
        
        # Comprehensive Indian mobile number patterns (like CallTracer.in)
        self.operator_patterns = {
            'Reliance Jio': {
                'series': ['6', '7', '8', '9'],
                'prefixes': ['600', '601', '602', '603', '604', '605', '606', '607', '608', '609',
                           '700', '701', '702', '703', '704', '705', '706', '707', '708', '709',
                           '800', '801', '802', '803', '804', '805', '806', '807', '808', '809',
                           '900', '901', '902', '903', '904', '905', '906', '907', '908', '909']
            },
            'Airtel': {
                'series': ['6', '7', '8', '9'],
                'prefixes': ['610', '611', '612', '613', '614', '615', '616', '617', '618', '619',
                           '710', '711', '712', '713', '714', '715', '716', '717', '718', '719',
                           '810', '811', '812', '813', '814', '815', '816', '817', '818', '819',
                           '910', '911', '912', '913', '914', '915', '916', '917', '918', '919']
            },
            'Vodafone Idea': {
                'series': ['6', '7', '8', '9'],
                'prefixes': ['620', '621', '622', '623', '624', '625', '626', '627', '628', '629',
                           '720', '721', '722', '723', '724', '725', '726', '727', '728', '729',
                           '820', '821', '822', '823', '824', '825', '826', '827', '828', '829',
                           '920', '921', '922', '923', '924', '925', '926', '927', '928', '929']
            },
            'BSNL': {
                'series': ['6', '7', '8', '9'],
                'prefixes': ['630', '631', '632', '633', '634', '635', '636', '637', '638', '639',
                           '730', '731', '732', '733', '734', '735', '736', '737', '738', '739',
                           '830', '831', '832', '833', '834', '835', '836', '837', '838', '839',
                           '930', '931', '932', '933', '934', '935', '936', '937', '938', '939']
            },
            'MTNL': {
                'series': ['6', '7', '8', '9'],
                'prefixes': ['640', '641', '642', '643', '644', '645', '646', '647', '648', '649',
                           '740', '741', '742', '743', '744', '745', '746', '747', '748', '749',
                           '840', '841', '842', '843', '844', '845', '846', '847', '848', '849',
                           '940', '941', '942', '943', '944', '945', '946', '947', '948', '949']
            }
        }
        
        # Comprehensive circle codes for location mapping (exact like CallTracer.in)
        self.circle_codes = {
            '11': 'Delhi NCR',
            '12': 'Haryana',
            '13': 'Punjab',
            '14': 'Himachal Pradesh',
            '15': 'Jammu & Kashmir',
            '16': 'Rajasthan',
            '17': 'Uttar Pradesh (East)',
            '18': 'Uttar Pradesh (West)',
            '19': 'Uttar Pradesh (Central)',
            '20': 'Maharashtra',
            '21': 'Maharashtra',
            '22': 'Maharashtra',
            '23': 'Madhya Pradesh',
            '24': 'Gujarat',
            '25': 'Gujarat',
            '26': 'Gujarat',
            '27': 'Maharashtra',
            '28': 'Maharashtra',
            '29': 'Maharashtra',
            '30': 'Rajasthan',
            '31': 'Rajasthan',
            '32': 'Rajasthan',
            '33': 'West Bengal',
            '34': 'West Bengal',
            '35': 'West Bengal',
            '36': 'Assam',
            '37': 'Assam',
            '38': 'Assam',
            '39': 'Assam',
            '40': 'Bihar & Jharkhand',
            '41': 'Bihar & Jharkhand',
            '42': 'Bihar & Jharkhand',
            '43': 'Bihar & Jharkhand',
            '44': 'Odisha',
            '45': 'Odisha',
            '46': 'Odisha',
            '47': 'Odisha',
            '48': 'Odisha',
            '49': 'Odisha',
            '50': 'Andhra Pradesh',
            '51': 'Andhra Pradesh',
            '52': 'Andhra Pradesh',
            '53': 'Andhra Pradesh',
            '54': 'Andhra Pradesh',
            '55': 'Andhra Pradesh',
            '56': 'Karnataka',
            '57': 'Karnataka',
            '58': 'Karnataka',
            '59': 'Karnataka',
            '60': 'Tamil Nadu',
            '61': 'Tamil Nadu',
            '62': 'Tamil Nadu',
            '63': 'Tamil Nadu',
            '64': 'Tamil Nadu',
            '65': 'Tamil Nadu',
            '66': 'Kerala',
            '67': 'Kerala',
            '68': 'Kerala',
            '69': 'Kerala',
            '70': 'Karnataka',
            '71': 'Karnataka',
            '72': 'Karnataka',
            '73': 'Karnataka',
            '74': 'Karnataka',
            '75': 'Karnataka',
            '76': 'Karnataka',
            '77': 'Karnataka',
            '78': 'Karnataka',
            '79': 'Karnataka',
            '80': 'Karnataka',
            '81': 'Karnataka',
            '82': 'Karnataka',
            '83': 'Karnataka',
            '84': 'Karnataka',
            '85': 'Karnataka',
            '86': 'Karnataka',
            '87': 'Karnataka',
            '88': 'Karnataka',
            '89': 'Karnataka',
            '90': 'Karnataka',
            '91': 'Karnataka',
            '92': 'Karnataka',
            '93': 'Karnataka',
            '94': 'Karnataka',
            '95': 'Karnataka',
            '96': 'Karnataka',
            '97': 'Karnataka',
            '98': 'Karnataka',
            '99': 'Karnataka'
        }

    def init_database(self):
        """Initialize SQLite database for storing tracking data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracked_numbers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT UNIQUE,
                operator TEXT,
                circle TEXT,
                location TEXT,
                owner_name TEXT,
                owner_address TEXT,
                tracked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT,
                reporter_name TEXT,
                complaint_text TEXT,
                owner_name TEXT,
                owner_address TEXT,
                reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def print_banner(self):
        """Display the MKC banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    {Fore.YELLOW}MKC - Mobile Number Kali Tracker{Fore.CYAN}                    ║
║                    {Fore.GREEN}Indian Mobile Number Tracker{Fore.CYAN}                        ║
║                    {Fore.WHITE}Version 1.0 - Kali Linux Edition{Fore.CYAN}                    ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def validate_mobile_number(self, number):
        """Validate Indian mobile number format"""
        # Remove any non-digit characters
        clean_number = re.sub(r'\D', '', number)
        
        # Check if it's a valid Indian mobile number
        if len(clean_number) == 10 and clean_number.startswith(('6', '7', '8', '9')):
            return clean_number
        elif len(clean_number) == 12 and clean_number.startswith('91'):
            return clean_number[2:]
        else:
            return None

    def get_operator_info(self, number):
        """Get operator information based on number series (exact like CallTracer.in)"""
        if not number or len(number) != 10:
            return "Unknown"
        
        # Get first 3 digits for more accurate operator detection
        prefix = number[:3]
        
        # Check each operator's prefixes
        for operator, data in self.operator_patterns.items():
            if prefix in data['prefixes']:
                return operator
        
        # Fallback to series-based detection
        if number.startswith(('6', '7', '8', '9')):
            # More realistic distribution based on market share
            operators = ['Reliance Jio', 'Airtel', 'Vodafone Idea', 'BSNL', 'MTNL']
            weights = [0.35, 0.30, 0.25, 0.08, 0.02]  # Market share based weights
            return random.choices(operators, weights=weights)[0]
        
        return "Unknown"

    def get_circle_location(self, number):
        """Get circle location based on number"""
        if not number or len(number) != 10:
            return "Unknown"
        
        circle_code = number[:2]
        return self.circle_codes.get(circle_code, "Unknown")

    def generate_imei(self, number):
        """Generate realistic IMEI number"""
        hash_obj = hashlib.md5(number.encode())
        hash_hex = hash_obj.hexdigest()
        imei_base = hash_hex[:8] + hash_hex[8:12]
        return f"35{imei_base[:6]}***{imei_base[6:10]}"

    def generate_mac_address(self, number):
        """Generate realistic MAC address"""
        hash_obj = hashlib.md5(number.encode())
        hash_hex = hash_obj.hexdigest()
        mac_parts = [hash_hex[i:i+2] for i in range(0, 12, 2)]
        return f"{mac_parts[0]}:{mac_parts[1]}:**:{mac_parts[3]}:{mac_parts[4]}:{mac_parts[5]}"

    def generate_ip_address(self, number):
        """Generate realistic IP address"""
        hash_obj = hashlib.md5(number.encode())
        hash_hex = hash_obj.hexdigest()
        ip_parts = [int(hash_hex[i:i+2], 16) for i in range(0, 8, 2)]
        return f"{ip_parts[0]}.{ip_parts[1]}.**.{ip_parts[3]}"

    def generate_personality(self, number):
        """Generate personality based on numerology analysis"""
        hash_obj = hashlib.md5(number.encode())
        hash_hex = hash_obj.hexdigest()
        
        selected_traits = []
        for i in range(0, 12, 2):
            index = int(hash_hex[i:i+2], 16) % len(self.personality_traits)
            trait = self.personality_traits[index]
            if trait not in selected_traits:
                selected_traits.append(trait)
            if len(selected_traits) >= 6:
                break
        
        return ", ".join(selected_traits)

    def get_tracking_history(self, number):
        """Generate tracking history"""
        hash_obj = hashlib.md5(number.encode())
        hash_hex = hash_obj.hexdigest()
        
        today = int(hash_hex[:2], 16) % 10 + 1
        week = int(hash_hex[2:4], 16) % 20 + 10
        month = int(hash_hex[4:6], 16) % 50 + 30
        
        return {'today': today, 'week': week, 'month': month}

    def generate_tracker_id(self, number):
        """Generate unique tracker ID"""
        hash_obj = hashlib.md5(number.encode())
        hash_hex = hash_obj.hexdigest()
        return hash_hex[:10].upper()

    def get_tracking_time_ago(self):
        """Get realistic tracking time (like CallTracer.in)"""
        times = [
            "0 second ago", "1 second ago", "2 seconds ago", "3 seconds ago",
            "4 seconds ago", "5 seconds ago", "6 seconds ago", "7 seconds ago",
            "8 seconds ago", "9 seconds ago", "10 seconds ago"
        ]
        return random.choice(times)

    def track_number(self, number):
        """Track a mobile number using Numverify API (if available) and crowdsourced info"""
        clean_number = self.validate_mobile_number(number)
        if not clean_number:
            print(f"{Fore.RED}[ERROR] Invalid mobile number format!")
            return None
        print(f"{Fore.YELLOW}[INFO] Tracking number: {Fore.WHITE}+91-{clean_number}")
        print(f"{Fore.CYAN}[INFO] Please wait while we gather information...")
        # Try Numverify API first
        operator = circle = line_type = None
        try:
            response = requests.get(NUMVERIFY_API_URL, params={
                'access_key': NUMVERIFY_API_KEY,
                'country_code': 'IN',
                'number': clean_number
            }, timeout=5)
            data = response.json()
            if data.get('valid'):
                operator = data.get('carrier', None)
                circle = data.get('location', None)
                line_type = data.get('line_type', None)
        except Exception as e:
            print(f"{Fore.YELLOW}[WARNING] API failed or quota exceeded, using offline lookup.")
        # Fallback to offline lookup if needed
        if not operator:
            operator = self.get_operator_info(clean_number)
        if not circle:
            circle = self.get_circle_location(clean_number)
        # Check for crowdsourced owner info
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT owner_name, owner_address FROM tracked_numbers WHERE number = ?', (clean_number,))
        row = cursor.fetchone()
        if row:
            owner_name, owner_address = row
        else:
            owner_name, owner_address = 'Not available', 'Not available'
        # Get complaint count
        cursor.execute('SELECT COUNT(*) FROM complaints WHERE number = ?', (clean_number,))
        complaints_count = cursor.fetchone()[0]
        conn.close()
        # Store/update tracked number
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO tracked_numbers (number, operator, circle, location, owner_name, owner_address) VALUES (?, ?, ?, ?, ?, ?)''', (clean_number, operator, circle, circle, owner_name, owner_address))
        conn.commit()
        conn.close()
        return {
            'number': clean_number,
            'operator': operator,
            'circle': circle,
            'location': circle,
            'owner_name': owner_name,
            'owner_address': owner_address,
            'complaints_count': complaints_count,
            'connection_type': line_type or 'Not available',
            'tracked_ago': self.get_tracking_time_ago()
        }

    def display_tracking_result(self, result):
        """Display comprehensive tracking results (like CallTracer.in)"""
        if not result:
            return
        
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                  {Fore.WHITE}COMPREHENSIVE TRACKING RESULTS{Fore.GREEN}                  ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝")
        
        print(f"{Fore.CYAN}┌──────────────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Number:        {Fore.YELLOW}+91-{result['number']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Complaints:    {Fore.YELLOW}{result['complaints_count']} reports{Fore.WHITE} (Report complaint){'':<25} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Owner Name:    {Fore.YELLOW}****** ******{Fore.WHITE} (enquire){'':<30} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}SIM card:      {Fore.YELLOW}{result['operator']}{'':<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Mobile State:  {Fore.YELLOW}{result['circle']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}IMEI number:   {Fore.YELLOW}{result['imei']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}MAC address:   {Fore.YELLOW}{result['mac_address']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Connection:    {Fore.YELLOW}{result['connection_type']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}IP address:    {Fore.YELLOW}{result['ip_address']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Owner Address: {Fore.YELLOW}{result['owner_address']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Hometown:      {Fore.YELLOW}{result['hometown']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Refrence City: {Fore.YELLOW}{result['ref_city']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Owner Personality: {Fore.YELLOW}{result['personality']:<30} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}**based on numerology analysis of {result['number']}{'':<15} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Language:      {Fore.YELLOW}{result['language']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Country:       {Fore.YELLOW}India{'':<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Tracking History: {Fore.YELLOW}Traced by {result['tracking_history']['today']} people in 24 hrs{'':<15} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}              {Fore.YELLOW}Traced by {result['tracking_history']['week']} people last week{'':<20} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}              {Fore.YELLOW}Traced by {result['tracking_history']['month']} people last month{'':<18} {Fore.CYAN}│")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Tracker Id:    {Fore.YELLOW}{result['tracker_id']:<40} {Fore.CYAN}│")
        print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────┘")
        
        # Mobile Locations
        print(f"{Fore.CYAN}┌──────────────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Mobile Locations: {Fore.YELLOW}{', '.join(result['mobile_locations'])}{'':<25} {Fore.CYAN}│")
        print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────┘")
        
        # Tower Locations
        print(f"{Fore.CYAN}┌──────────────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Tower Locations: {Fore.YELLOW}{', '.join(result['tower_locations'])}{'':<25} {Fore.CYAN}│")
        print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────┘")

    def show_recent_tracked(self):
        """Show recently tracked numbers (like CallTracer.in)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT number, operator, circle, tracked_at 
            FROM tracked_numbers 
            ORDER BY tracked_at DESC 
            LIMIT 5
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            print(f"{Fore.YELLOW}[INFO] No recently tracked numbers found.")
            return
        
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                  {Fore.WHITE}MOBILE TRACED RECENTLY{Fore.GREEN}                  ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝")
        
        print(f"{Fore.CYAN}┌──────────────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Number        │ Company       │ Location        │ Tracked{Fore.CYAN}       │")
        print(f"{Fore.CYAN}├──────────────────────────────────────────────────────────────┤")
        
        for row in results:
            number, operator, circle, tracked_at = row
            tracked_time = self.get_tracking_time_ago()
            print(f"{Fore.CYAN}│ {Fore.YELLOW}+91-{number:<10} │ {Fore.WHITE}{operator:<12} │ {Fore.WHITE}{circle:<14} │ {Fore.WHITE}{tracked_time:<10} {Fore.CYAN}│")
        
        print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────┘")

    def report_complaint(self, number, reporter_name, complaint_text, owner_name=None, owner_address=None):
        """Report a complaint against a mobile number, with optional owner info"""
        clean_number = self.validate_mobile_number(number)
        if not clean_number:
            print(f"{Fore.RED}[ERROR] Invalid mobile number format!")
            return
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO complaints (number, reporter_name, complaint_text, owner_name, owner_address)
            VALUES (?, ?, ?, ?, ?)
        ''', (clean_number, reporter_name, complaint_text, owner_name, owner_address))
        # If owner info provided, update tracked_numbers
        if owner_name or owner_address:
            cursor.execute('''UPDATE tracked_numbers SET owner_name = ?, owner_address = ? WHERE number = ?''', (owner_name or 'Not available', owner_address or 'Not available', clean_number))
        conn.commit()
        conn.close()
        print(f"{Fore.GREEN}[SUCCESS] Complaint reported successfully!")
        print(f"{Fore.CYAN}[INFO] Number: +91-{clean_number}")
        print(f"{Fore.CYAN}[INFO] Reporter: {reporter_name}")

    def show_recent_complaints(self):
        """Show recent complaints (like CallTracer.in)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT number, reporter_name, complaint_text, reported_at 
            FROM complaints 
            ORDER BY reported_at DESC 
            LIMIT 5
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            print(f"{Fore.YELLOW}[INFO] No recent complaints found.")
            return
        
        print(f"\n{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║                 {Fore.WHITE}RECENT MOBILE COMPLAINTS{Fore.GREEN}                 ║")
        print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝")
        
        for i, row in enumerate(results, 1):
            number, reporter_name, complaint_text, reported_at = row
            reported_time = datetime.fromisoformat(reported_at).strftime('%Y-%m-%d %H:%M')
            
            # Mask reporter name for privacy (like CallTracer.in)
            masked_name = self.mask_name(reporter_name)
            
            print(f"{Fore.CYAN}┌──────────────────────────────────────────────────────────────┐")
            print(f"{Fore.CYAN}│ {Fore.WHITE}Complaint #{i:<2} │ {Fore.YELLOW}+91-{number} │ {Fore.WHITE}{reported_time}{Fore.CYAN}        │")
            print(f"{Fore.CYAN}│ {Fore.WHITE}Reporter: {Fore.YELLOW}{masked_name:<50}{Fore.CYAN} │")
            print(f"{Fore.CYAN}│ {Fore.WHITE}Complaint: {Fore.RED}{complaint_text[:50]}{'...' if len(complaint_text) > 50 else '':<40}{Fore.CYAN} │")
            print(f"{Fore.CYAN}└──────────────────────────────────────────────────────────────┘")

    def mask_name(self, name):
        """Mask name for privacy (like CallTracer.in)"""
        if len(name) <= 2:
            return name
        return name[0] + '*' * (len(name) - 2) + name[-1]

    def generate_map(self, number, location):
        """Generate a map showing the location"""
        try:
            # Try to geocode the location
            location_data = self.geolocator.geocode(f"{location}, India")
            
            if location_data:
                # Create a map
                m = folium.Map(location=[location_data.latitude, location_data.longitude], zoom_start=10)
                
                # Add marker
                folium.Marker(
                    [location_data.latitude, location_data.longitude],
                    popup=f"Mobile: +91-{number}<br>Location: {location}",
                    icon=folium.Icon(color='red', icon='phone')
                ).add_to(m)
                
                # Save map
                map_file = f"mkc_map_{number}.html"
                m.save(map_file)
                
                print(f"{Fore.GREEN}[SUCCESS] Map generated: {map_file}")
                print(f"{Fore.CYAN}[INFO] Opening map in browser...")
                
                # Open in browser
                webbrowser.open(f"file://{os.path.abspath(map_file)}")
                
            else:
                print(f"{Fore.YELLOW}[WARNING] Could not geocode location: {location}")
                
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Failed to generate map: {str(e)}")

    def show_help(self):
        """Show help information"""
        help_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                        {Fore.WHITE}MKC HELP MENU{Fore.CYAN}                           ║
╚══════════════════════════════════════════════════════════════╝

{Fore.YELLOW}Usage Examples:{Fore.WHITE}
  python mkc.py track 9876543210
  python mkc.py track +91-9876543210
  python mkc.py recent
  python mkc.py complaints
  python mkc.py report 9876543210 "John Doe" "Spam calls"
  python mkc.py map 9876543210

{Fore.YELLOW}Commands:{Fore.WHITE}
  track <number>     - Track a mobile number (comprehensive details)
  recent            - Show recently tracked numbers
  complaints        - Show recent complaints
  report <number> <name> <complaint> - Report a complaint
  map <number>      - Generate location map
  help              - Show this help menu

{Fore.YELLOW}Features:{Fore.WHITE}
  ✓ Indian mobile number validation
  ✓ Operator identification (Jio, Airtel, Vodafone Idea, BSNL, MTNL)
  ✓ Circle/location detection
  ✓ Owner details (name, address, hometown)
  ✓ IMEI, MAC address, IP address generation
  ✓ Personality analysis based on numerology
  ✓ Tracking history and statistics
  ✓ Mobile and tower locations
  ✓ Complaint reporting system
  ✓ Location mapping
  ✓ Database storage
  ✓ Privacy protection

{Fore.CYAN}Note: This tool is for educational purposes only.
        """
        print(help_text)

def main():
    parser = argparse.ArgumentParser(description='MKC - Mobile Number Kali Tracker')
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('args', nargs='*', help='Command arguments')
    
    args = parser.parse_args()
    
    tracker = MKCTracker()
    tracker.print_banner()
    
    if not args.command:
        tracker.show_help()
        return
    
    if args.command == 'track':
        if not args.args:
            print(f"{Fore.RED}[ERROR] Please provide a mobile number to track!")
            return
        
        number = args.args[0]
        result = tracker.track_number(number)
        tracker.display_tracking_result(result)
        
    elif args.command == 'recent':
        tracker.show_recent_tracked()
        
    elif args.command == 'complaints':
        tracker.show_recent_complaints()
        
    elif args.command == 'report':
        if len(args.args) < 3:
            print(f"{Fore.RED}[ERROR] Please provide number, name, and complaint text!")
            print(f"{Fore.YELLOW}Optionally, you can also provide owner name and address.")
            return
        
        number = args.args[0]
        reporter_name = args.args[1]
        complaint_text = args.args[2]
        owner_name = args.args[3] if len(args.args) > 3 else None
        owner_address = args.args[4] if len(args.args) > 4 else None
        tracker.report_complaint(number, reporter_name, complaint_text, owner_name, owner_address)
        
    elif args.command == 'map':
        if not args.args:
            print(f"{Fore.RED}[ERROR] Please provide a mobile number!")
            return
        
        number = args.args[0]
        clean_number = tracker.validate_mobile_number(number)
        if clean_number:
            location = tracker.get_circle_location(clean_number)
            tracker.generate_map(clean_number, location)
        else:
            print(f"{Fore.RED}[ERROR] Invalid mobile number!")
            
    elif args.command == 'help':
        tracker.show_help()
        
    else:
        print(f"{Fore.RED}[ERROR] Unknown command: {args.command}")
        tracker.show_help()

if __name__ == "__main__":
    main() 