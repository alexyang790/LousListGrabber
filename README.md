# Lou's List Grabber

A Flask-based web application that fetches and analyzes UVA course data from Lou's List, with emphasis on class scheduling and building efficiency optimization (built for UVA office for sustainability).

## Features

- 🔄 Real-time data fetching from Lou's List
- 🔍 Advanced search capabilities with multiple filters
- 📊 Interactive dashboard interface
- 📥 Export data in CSV and JSON formats
- 🎯 Specialized filters for OFS (Office of Facilities Services) and Enrollment data
- 🌐 RESTful API with Swagger documentation

## 🚀 Quick Start

### Using Docker (Recommended)
```bash
# Clone and run
git clone https://github.com/alexyang790/louslistgrabber.git
cd louslistgrabber
docker build -t louslistgrabber .
docker run -p 5002:5002 louslistgrabber
```

### Manual Setup
```bash
# Clone repository
git clone https://github.com/alexyang790/louslistgrabber.git
cd louslistgrabber

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python run.py
```

## 🌟 Features

- Real-time data fetching from Lou's List
- Advanced search with multiple filters
- Interactive dashboard
- CSV/JSON data export
- Specialized OFS and Enrollment filters
- Swagger API documentation

## 🛠 API Endpoints

| Endpoint | Description |
|----------|-------------|
| GET `/` | Welcome message |
| GET `/fetch` | Fetch latest Lou's List data |
| GET `/data` | View all course data (JSON) |
| GET `/getcsv` | Download complete dataset (CSV) |
| GET `/search/<query>/<format>` | Search courses with basic filtering |
| GET `/dashboard` | Interactive web interface |
| GET `/advanced_search/ofs/<query>/<format>` | Search OFS-specific columns (ClassNumber, Room1, Days1, Enrollment, MeetingDates1, Type) |
| GET `/advanced_search/enrollment/<query>/<format>` | Search enrollment-specific columns (ClassNumber, Days1, Enrollment, EnrollmentLimit, Status, Title) |

## Detailed Usage Examples

### Basic Data Operations
```bash
# Get welcome message
curl http://localhost:5002/
# Response: {"message": "Lou's List App is Running!"}

# Fetch fresh data
curl http://localhost:5002/fetch
# Response: {"message": "Data fetched successfully"}

# Get all data
curl http://localhost:5002/data
# Response: {"data": [{course1}, {course2}, ...]}

# Download CSV
curl http://localhost:5002/getcsv -O courses.csv
```

### Search Operations
```bash
# Basic search (JSON)
curl http://localhost:5002/search/CS1110/json
# Response: {"results": [{matched_courses}]}

# OFS search for specific building
curl http://localhost:5002/advanced_search/ofs/Rice%20Hall/json
# Response: {"results": [{building_specific_data}]}

# Find courses with open enrollment
curl http://localhost:5002/advanced_search/enrollment/OPEN/json
# Response: {"results": [{open_courses}]}
```

## Column Specifications

### OFS Search Columns
- ClassNumber
- Room1
- Days1
- Enrollment
- MeetingDates1
- Type

### Enrollment Search Columns
- ClassNumber
- Days1
- Enrollment
- EnrollmentLimit
- Status
- Title

## 💻 Tech Stack

- Flask (Python)
- Pandas for data processing
- Bootstrap UI
- Docker support
- GitHub Actions CI/CD

## 📝 Configuration

- Default port: `5002`
- Environment variables:
  - `FLASK_APP=run.py`
  - `FLASK_ENV=development/production`

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 👥 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Submit Pull Request

---
Created by [@alexyang790](https://github.com/alexyang790)