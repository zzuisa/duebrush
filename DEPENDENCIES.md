# Dependencies Documentation

## Core Dependencies

### Required Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.3 | Web framework for building the API |
| Flask-CORS | 4.0.0 | Cross-Origin Resource Sharing support |
| Werkzeug | 3.0.3 | WSGI utilities (required by Flask) |
| python-dotenv | 1.0.0 | Environment variable management |

### Standard Library Dependencies

The following modules are part of Python's standard library and don't need separate installation:

- `json` - JSON data handling
- `os` - Operating system interface
- `secrets` - Cryptographically strong random numbers
- `re` - Regular expressions
- `datetime` - Date and time handling
- `smtplib` - SMTP protocol client
- `email.mime.text` - Email message handling
- `email.mime.multipart` - Multipart email support
- `pathlib` - Object-oriented filesystem paths
- `functools` - Higher-order functions

## Installation

### Basic Installation

```bash
# Install required dependencies
pip install -r server/requirements.txt
```

### Development Installation

```bash
# Install with development dependencies
pip install -r server/requirements.txt

# Optional: Install development tools
pip install pytest==7.4.3  # For testing
pip install black==23.11.0  # For code formatting
pip install flake8==6.1.0   # For linting
```

### Production Installation

```bash
# Install production dependencies
pip install -r server/requirements.txt

# Uncomment and install production server
# pip install gunicorn==21.2.0
# pip install uwsgi==2.0.24
```

## Optional Dependencies

### For Production Deployment

Uncomment these lines in `requirements.txt` for production use:

```txt
# gunicorn==21.2.0      # Production WSGI server
# uwsgi==2.0.24         # Alternative WSGI server
```

### For Enhanced Security

```txt
# cryptography==41.0.7  # Enhanced security features
```

### For Better Performance

```txt
# ujson==5.8.0          # Faster JSON handling
```

## Environment Variables

The following environment variables can be configured:

```bash
# Admin authentication
ADMIN_PASSWORD=your-admin-password

# Email configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=admin@example.com
```

## System Requirements

### Python Version
- Python 3.8 or higher
- Recommended: Python 3.9+

### Operating System
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 18.04+, CentOS 7+)

### Memory Requirements
- Minimum: 512MB RAM
- Recommended: 1GB+ RAM

### Disk Space
- Minimum: 100MB
- Recommended: 500MB+ for file uploads

## Troubleshooting

### Common Issues

1. **Import Error: No module named 'flask'**
   ```bash
   pip install Flask==3.0.3
   ```

2. **CORS Issues**
   ```bash
   pip install Flask-CORS==4.0.0
   ```

3. **Email Sending Fails**
   - Check SMTP credentials
   - Ensure 2FA is enabled for Gmail
   - Use App Password instead of regular password

4. **Permission Errors**
   ```bash
   # On Linux/macOS
   chmod +x server/app.py
   ```

### Version Conflicts

If you encounter version conflicts:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r server/requirements.txt
```

## Development Setup

### Local Development

1. Clone the repository
2. Create virtual environment
3. Install dependencies
4. Set environment variables
5. Run the application

```bash
git clone <repository-url>
cd duebrush
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r server/requirements.txt
python server/app.py
```

### Docker Development

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY server/requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "server/app.py"]
```

## Security Considerations

1. **Never commit sensitive data** (passwords, API keys)
2. **Use environment variables** for configuration
3. **Enable HTTPS** in production
4. **Regular security updates** for dependencies
5. **Input validation** on all user inputs
6. **Rate limiting** for API endpoints

## Performance Optimization

1. **Use production WSGI server** (Gunicorn/uWSGI)
2. **Enable caching** for static files
3. **Optimize database queries** (if using database)
4. **Compress responses** (gzip)
5. **Use CDN** for static assets

## Monitoring and Logging

Consider adding these packages for production monitoring:

```txt
# logging==0.4.9.6        # Enhanced logging
# prometheus-client==0.19.0  # Metrics collection
# sentry-sdk==1.38.0      # Error tracking
```


