# MaisQuelle 🌽 Your AI-Powered MySQL companion

**MaisQuelle** (_**M**ySQL **A**rtificial **I**ntelligence **S**ystem for **Q**uerying, **U**nderstanding, **E**
valuating, **L**earning and **L**og **E**nhancement_) is a smart configurator and performance monitoring tool that
combines the power of artificial intelligence with traditional monitoring techniques to keep your MySQL servers happy
and healthy! 🎯

> ⚠️ WARNING: MaisQuelle is currently in an experimental phase and is NOT ready for production use!

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
   git clone https://github.com/murdercode/mais-quelle.git
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

anthropic:
  api_key: "your-api-key-here"
```

2. Using command-line arguments (these override settings.yaml):

```bash
python maisquelle.py --host localhost --user root --password mypassword --port 3306 --enable-tables
```

### Available Arguments

- `--host`: MySQL host address (default: localhost)
- `-u, --user`: MySQL username (default: root)
- `-p, --password`: MySQL password (default: empty)
- `--port`: MySQL port number (default: 3306)
- `--enable-tables`: Enable detailed table statistics collection

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

- Performance optimization recommendations
- Query analysis
- Interactive command suggestions
- Automated improvement execution

## Output

Reports are generated in the `logs` directory with timestamps:

```
logs/status_YYYYMMDD_HHMMSS.txt
```

### Report Sections

1. **MySQL Configuration**
    - Connection settings
    - Server configuration

2. **System Resources**
    - CPU metrics
    - Memory usage
    - Disk statistics

3. **MySQL Status**
    - Process information
    - Service status
    - Server variables

4. **Performance Metrics**
    - Query cache analysis
    - InnoDB metrics
    - Slow queries
    - Performance schema data
    - Table statistics (if enabled)

5. **AI Optimization** (when API key is configured)
    - Suggested improvements
    - Approved commands
    - Execution results

## Best Practices

1. **Configuration**
    - Use `settings.yaml` for persistent configuration
    - Set up a dedicated monitoring user
    - Configure appropriate permissions

2. **Monitoring**
    - Use `--enable-tables` sparingly on production servers
    - Monitor during various load conditions
    - Keep historical reports for trend analysis

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