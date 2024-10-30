# MaisQuelle 🌽 Your AI-Powered MySQL companion

**MaisQuelle** (_**M**ySQL **A**rtificial **I**ntelligence **S**ystem for **Q**uerying, **U**nderstanding, **E**
valuating, **L**earning and **L**og **E**nhancement_) is a smart configurator and performance monitoring tool that
combines the power of artificial intelligence with traditional monitoring techniques to keep your MySQL servers happy
and healthy! 🎯

> ⚠️ WARNING: MaisQuelle is currently in an experimental phase and is NOT ready for production use!

Inspired by the versatility of [MySQLTuner](https://github.com/major/MySQLTuner-perl) and its essential role in MySQL
administration, MaisQuelle aims to bring that
same level of utility to performance monitoring and optimization, enhanced with AI capabilities.

<p align="center">
<img src="https://github.com/murdercode/maisquelle/raw/HEAD/art/demo.gif" width="100%" 
alt="MaisQuelle Animated Demo"></p>

## Why MaisQuelle? 🤔

- 🧠 AI-Enhanced Analysis: Uses machine learning algorithms to provide intelligent insights and recommendations for your
  MySQL performance
- 📊 Smart Reporting: Automatically generates human-readable reports with AI-driven explanations
- 🎯 Predictive Monitoring: Identifies potential issues before they become problems
- 🚀 Performance Optimization: Provides AI-powered suggestions for query optimization and system tuning
- 🤖 Self-Learning: Continuously improves its recommendations based on your system's specific patterns

## Requirements

- Python 3.6+
- MySQL Server 5.7+ or MariaDB 10.2+
- [Anthropic API Key](https://www.anthropic.com/) (for AI-enhanced features)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/murdercode/maisquelle.git
   cd maisquelle
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure settings:
    - Copy `settings.example.yaml` to `settings.yaml`
    - Add your Anthropic API key and MySQL configuration in `settings.yaml`

## Configuration

MaisQuelle can be configured in two ways:

1. Using `settings.yaml`:

```yaml
mysql:
  host: localhost
  user: root
  password: ""
  port: 3306

monitoring:
  level: 2  # 1-Basic, 2-Advanced (default), 3-Expert
  interval: 300

anthropic:
  api_key: "your-api-key-here"
```

2. Using command-line arguments (these override settings.yaml):

```bash
# Basic monitoring
python maisquelle.py --level 1 --host localhost --port 3306

# Advanced monitoring (default)
python maisquelle.py --level 2 -u root -p password

# Expert monitoring with all features
python maisquelle.py --level 3 --enable-tables
```

### Available Arguments

- `--level`: Monitoring detail level (1=Basic, 2=Advanced, 3=Expert)
- `--host`: MySQL host address (default: localhost)
- `-u, --user`: MySQL username (default: root)
- `-p, --password`: MySQL password (default: empty)
- `--port`: MySQL port number (default: 3306)
- `--enable-tables`: Enable detailed table statistics collection

## Monitoring Levels

### Level 1: Basic Health Check 🟢

- System resources (CPU, RAM, Disk)
- MySQL service status
- Basic MySQL metrics
- Essential health indicators
- Perfect for daily monitoring

### Level 2: Advanced Analysis 🟡

Everything in Level 1, plus:

- Query cache analysis
- InnoDB metrics
- Slow query detection
- Performance schema basics
- Ideal for weekly performance reviews

### Level 3: Expert Inspection 🔴

Everything in Level 2, plus:

- Detailed table statistics
- Index analysis
- Deep performance metrics
- Complete schema inspection
- Recommended for monthly deep analysis

## Features

### System Monitoring

- CPU utilization and specifications
- Memory usage (RAM and swap)
- Disk space statistics

### MySQL Monitoring

- Service status and processes
- Server variables and status
- Query cache analysis
- InnoDB metrics
- Slow query analysis
- Performance schema metrics
- Table statistics (optional)

### AI-Enhanced Features

- Performance optimization recommendations based on monitoring level
- Intelligent query analysis
- Interactive command suggestions
- Automated improvement execution
- Level-specific insights and recommendations

## Output

Reports are generated in the `logs` directory with timestamps:

```
logs/status_YYYYMMDD_HHMMSS.txt
```

### Report Sections

1. **Monitoring Level Information**
    - Current level details
    - Enabled features
    - AI analysis depth

2. **System Resources**
    - CPU metrics
    - Memory usage
    - Disk statistics

3. **MySQL Status**
    - Process information
    - Service status
    - Server variables

4. **Performance Metrics** (Level 2+)
    - Query cache analysis
    - InnoDB metrics
    - Slow queries
    - Performance schema data

5. **Detailed Analytics** (Level 3)
    - Table statistics
    - Index analysis
    - Deep performance metrics

6. **AI Optimization**
    - Level-specific recommendations
    - Suggested improvements
    - Execution results

## Best Practices

1. **Monitoring Level Selection**
    - Use Level 1 for daily health checks
    - Use Level 2 for weekly performance reviews
    - Use Level 3 for monthly deep analysis
    - Avoid Level 3 during peak hours

2. **Configuration**
    - Use `settings.yaml` for persistent configuration
    - Override with CLI arguments when needed
    - Configure appropriate permissions

3. **Security**
    - Store API keys securely
    - Use encrypted connections
    - Regularly rotate credentials

## Troubleshooting

### Common Issues

1. **Settings Loading**
    - Ensure `settings.yaml` exists
    - Check YAML syntax
    - Verify file permissions

2. **MySQL Connection**
    - Confirm MySQL server is running
    - Verify credentials
    - Check port availability

3. **AI Features**
    - Validate Anthropic API key
    - Check internet connectivity
    - Monitor API rate limits

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Your Name

- GitHub: [@murdercode](https://github.com/murdercode)
- Email: murdercode@gmail.com