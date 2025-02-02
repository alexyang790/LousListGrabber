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
docker-compose up --build
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
| GET `/search/<query>/<format>` | Search courses |
| GET `/dashboard` | Interactive web interface |

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