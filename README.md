# MaisQuelle

MaisQuelle is a comprehensive Python-based monitoring tool for MySQL servers and system resources. The name combines "MySQL" with "Quelle", reflecting its purpose as a detailed source of MySQL and system performance insights.

## Features

- **System Resource Monitoring**
  - CPU usage and frequency
  - RAM and swap memory utilization
  - Disk space and usage statistics

- **MySQL Server Monitoring**
  - Connection metrics and statistics
  - Query performance analysis
  - Buffer and cache utilization
  - InnoDB metrics
  - Process list monitoring
  - Slow query analysis
  - Performance schema metrics

- **Query Cache Analysis**
  - Cache hit ratio
  - Memory usage analysis
  - Fragmentation detection
  - Performance recommendations

- **Table Statistics**
  - Size and row counts
  - Index analysis
  - Storage engine details
  - Space utilization

- **Advanced InnoDB Metrics**
  - Buffer pool statistics
  - I/O operations
  - Transaction monitoring

- **Performance Schema Integration**
  - Top queries by execution time
  - Lock analysis
  - Resource utilization patterns

## Requirements

- Python 3.6+
- MySQL Server 5.7+ or MariaDB 10.2+
- Required Python packages:
  ```
  psutil
  mysql-connector-python
  colorama
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/maisquelle.git
   cd maisquelle
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the script with default settings:

```bash
python monitor.py
```

### Advanced Usage

The script supports various command-line arguments:

```bash
python monitor.py --host localhost --user root --password mypassword --port 3307 --enable-tables
```

### Available Arguments

- `--host`: MySQL host address (default: localhost)
- `-u, --user`: MySQL username (default: root)
- `-p, --password`: MySQL password (default: empty)
- `--port`: MySQL port number (default: 3307)
- `--enable-tables`: Enable detailed table statistics collection

## Output

MaisQuelle generates comprehensive reports in the `logs` directory with the following naming convention:
```
logs/status_YYYYMMDD_HHMMSS.txt
```

### Report Sections

1. **System Metrics**
   - CPU utilization and specifications
   - Memory usage (RAM and swap)
   - Disk space statistics

2. **MySQL Configuration**
   - Current connection settings
   - Server variables
   - Process information

3. **Performance Metrics**
   - Query statistics
   - Cache performance
   - Buffer utilization
   - InnoDB metrics

4. **Query Analysis**
   - Slow query details
   - Query cache statistics
   - Performance recommendations

## Example Report Output

```
=== SYSTEM AND MYSQL STATUS REPORT ===
Timestamp: 2024-10-29 14:30:00

=== MYSQL CONFIGURATION ===
host: localhost
port: 3307
user: root

=== SYSTEM METRICS ===
[CPU]
total_usage_percent: 45.2
core_count: 8
current_frequency_mhz: 2800.00
...
```

## Configuration

MaisQuelle uses default MySQL configuration but can be customized using command-line arguments. For persistent configuration, you can modify the default values in the `SystemMySQLMonitor` class initialization.

## Best Practices

1. **Regular Monitoring**
   - Schedule regular monitoring intervals
   - Keep historical reports for trend analysis
   - Monitor during peak and off-peak hours

2. **Performance Impact**
   - Use `--enable-tables` sparingly on production servers
   - Monitor the monitoring tool's own resource usage
   - Consider network impact for remote monitoring

3. **Security**
   - Use dedicated monitoring user accounts
   - Implement proper password management
   - Restrict monitoring user privileges

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify MySQL server is running
   - Check credentials and permissions
   - Confirm correct port configuration

2. **Performance Impact**
   - Reduce monitoring frequency
   - Disable detailed table statistics
   - Optimize query cache analysis

3. **Report Generation Issues**
   - Check disk space for logs
   - Verify write permissions
   - Monitor log file growth

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python's psutil and mysql-connector libraries
- Inspired by various MySQL monitoring tools
- Thanks to all contributors and testers

## Author

Your Name
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com