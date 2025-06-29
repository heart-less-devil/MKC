# MKC - Mobile Number Kali Tracker (Real Data Edition)

## Description
A command-line tool to track Indian mobile numbers and get real operator/location info using the Numverify API. For educational use only.

## Features
- Real operator, location, and line type lookup via Numverify
- Complaint reporting and history
- Works on Kali Linux

## Setup
1. Clone/download this repo.
2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Get a free API key from [Numverify](https://numverify.com/).
4. Open `mkc.py` and put your API key in the `NUMVERIFY_API_KEY` variable at the top.

## Usage
```bash
python3 mkc.py track <number>
python3 mkc.py recent
python3 mkc.py complaints
python3 mkc.py report <number> <name> <complaint>
python3 mkc.py map <number>
python3 mkc.py help
```

## Notes
- Owner name, address, IMEI, MAC, etc. are not available for privacy reasons.
- This tool is for educational purposes only.

## Features

- 🔍 **Mobile Number Tracking**: Track any Indian mobile number and get operator details
- 📍 **Location Detection**: Identify circle/location based on number series
- 🗺️ **Interactive Maps**: Generate location maps with GPS coordinates
- 📝 **Complaint System**: Report and track complaints against numbers
- 💾 **Database Storage**: SQLite database for tracking history
- 🎨 **Beautiful CLI**: Colored output with ASCII art banners
- 📊 **Recent History**: View recently tracked numbers and complaints

## Installation

### Prerequisites
- Python 3.7+
- Kali Linux (recommended) or any Linux distribution
- Internet connection for geocoding and mapping features

### Quick Install

1. **Clone or download the tool:**
```bash
git clone <repository-url>
cd MKC
```

2. **Install dependencies:**
```bash
pip3 install -r requirements.txt
```

3. **Make executable:**
```bash
chmod +x mkc.py
```

4. **Run the tool:**
```bash
python3 mkc.py
```

## Usage

### Basic Commands

```bash
# Track a mobile number
python3 mkc.py track 9876543210
python3 mkc.py track +91-9876543210

# Show recently tracked numbers
python3 mkc.py recent

# Show recent complaints
python3 mkc.py complaints

# Report a complaint
python3 mkc.py report 9876543210 "John Doe" "Harassment calls"

# Generate location map
python3 mkc.py map 9876543210

# Show help
python3 mkc.py help
```

### Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `track <number>` | Track a mobile number | `track 9876543210` |
| `recent` | Show recently tracked numbers | `recent` |
| `complaints` | Show recent complaints | `complaints` |
| `report <number> <name> <complaint>` | Report a complaint | `report 9876543210 "John" "Spam calls"` |
| `map <number>` | Generate location map | `map 9876543210` |
| `help` | Show help menu | `help` |

## Features Explained

### 1. Mobile Number Tracking
- Validates Indian mobile number format (10 digits starting with 6,7,8,9)
- Identifies telecom operator (Airtel, Jio, Vodafone Idea, BSNL, etc.)
- Determines circle/location based on number series
- Stores tracking history in SQLite database

### 2. Location Detection
- Maps circle codes to Indian states/circles
- Provides accurate location information
- Supports all major telecom circles in India

### 3. Interactive Maps
- Generates HTML maps using Folium
- Shows exact location with GPS coordinates
- Opens automatically in default browser
- Includes mobile number and location details

### 4. Complaint System
- Report complaints against any mobile number
- Anonymous reporting option
- Track complaint history
- Database storage for future reference

### 5. Database Features
- SQLite database for data persistence
- Tracks number history and complaints
- Fast query performance
- Automatic database initialization

## Sample Output

```
╔══════════════════════════════════════════════════════════════╗
║                    MKC - Mobile Number Kali Tracker                    ║
║                    Indian Mobile Number Tracker                        ║
║                    Version 1.0 - Kali Linux Edition                    ║
╚══════════════════════════════════════════════════════════════╝

[INFO] Tracking number: +91-9876543210
[INFO] Please wait while we gather information...

╔══════════════════════════════════════════════════════════════╗
║                    TRACKING RESULTS                    ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│ Mobile Number: +91-9876543210                               │
│ Operator:      Reliance Jio                                 │
│ Circle:        Delhi NCR                                    │
│ Location:      Delhi NCR                                    │
│ Tracked At:    2024-01-15 14:30:25                         │
└──────────────────────────────────────────────────────────────┘
```

## Database Schema

### tracked_numbers Table
- `id`: Primary key
- `number`: Mobile number (10 digits)
- `operator`: Telecom operator name
- `circle`: Circle/location
- `location`: Location details
- `tracked_at`: Timestamp

### complaints Table
- `id`: Primary key
- `number`: Mobile number
- `reporter_name`: Name of person reporting
- `complaint_text`: Complaint description
- `reported_at`: Timestamp

## Technical Details

### Dependencies
- `requests`: HTTP requests for API calls
- `colorama`: Cross-platform colored terminal output
- `geopy`: Geocoding and location services
- `folium`: Interactive map generation
- `sqlite3`: Database operations (built-in)

### File Structure
```
MKC/
├── mkc.py              # Main tool script
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── mkc_database.db    # SQLite database (auto-generated)
└── mkc_map_*.html     # Generated maps (auto-generated)
```

## Legal Disclaimer

⚠️ **IMPORTANT**: This tool is for educational and legitimate purposes only. 

- Use only for tracking your own numbers or numbers you have permission to track
- Respect privacy laws and regulations
- Do not use for harassment or illegal activities
- The tool does not provide real-time location tracking
- Operator information is based on number series patterns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## Version History

- **v1.0**: Initial release with basic tracking features
- Basic mobile number validation
- Operator identification
- Location detection
- Complaint system
- Interactive maps

---

**Made with ❤️ for the Kali Linux community** 