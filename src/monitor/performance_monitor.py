import mysql.connector
from colorama import Fore, Style


class PerformanceMonitor:
    """Class for monitoring MySQL performance metrics including InnoDB, slow queries, and Performance Schema"""

    def __init__(self, host='localhost', user='root', password='', port=3307):
        """
        Initialize Performance Monitor with MySQL connection parameters

        Args:
            host (str): MySQL host address
            user (str): MySQL username
            password (str): MySQL password
            port (int): MySQL port number
        """
        self.mysql_config = {
            'host': host,
            'user': user,
            'password': password,
            'port': port
        }

    def safe_int(self, value, default=0):
        """
        Safely convert a value to integer

        Args:
            value: Value to convert
            default: Default value if conversion fails

        Returns:
            int: Converted value or default
        """
        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def safe_float(self, value, default=0.0):
        """
        Safely convert a value to float

        Args:
            value: Value to convert
            default: Default value if conversion fails

        Returns:
            float: Converted value or default
        """
        try:
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def get_innodb_metrics(self):
        """
        Collect detailed InnoDB metrics including buffer pool, I/O, and transaction statistics

        Returns:
            dict: Dictionary containing metrics or empty dict if error occurs
        """
        try:
            print(f"{Fore.WHITE}[*] Collecting InnoDB metrics...")
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)

            # Buffer Pool Stats
            print(f"{Fore.WHITE}  └─ Analyzing buffer pool...", end='')
            cursor.execute("SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool%'")
            buffer_stats = {row['Variable_name']: row['Value'] for row in cursor.fetchall()}
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # File I/O Stats
            print(f"{Fore.WHITE}  └─ Analyzing I/O operations...", end='')
            cursor.execute("SHOW GLOBAL STATUS LIKE 'Innodb_data%'")
            io_stats = {row['Variable_name']: row['Value'] for row in cursor.fetchall()}
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Transaction Stats
            print(f"{Fore.WHITE}  └─ Analyzing transactions...", end='')
            cursor.execute("SHOW GLOBAL STATUS LIKE 'Innodb_trx%'")
            trx_stats = {row['Variable_name']: row['Value'] for row in cursor.fetchall()}
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            cursor.close()
            conn.close()

            return {
                'buffer_stats': buffer_stats,
                'io_stats': io_stats,
                'trx_stats': trx_stats
            }

        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            return {'buffer_stats': {}, 'io_stats': {}, 'trx_stats': {}}

    def get_slow_queries(self):
        """
        Analyze slow queries if slow query log is enabled

        Returns:
            list: List of slow queries or empty list if not available
        """
        try:
            print(f"{Fore.WHITE}[*] Analyzing slow queries...")
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SHOW VARIABLES LIKE 'slow_query_log'")
            slow_log_status = cursor.fetchone()

            if slow_log_status and slow_log_status['Value'] == 'ON':
                print(f"{Fore.WHITE}  └─ Fetching slow query log...", end='')
                cursor.execute("""
                    SELECT * FROM mysql.slow_log 
                    ORDER BY start_time DESC 
                    LIMIT 10
                """)
                slow_queries = cursor.fetchall()
                print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")
                return slow_queries or []
            else:
                print(f"{Fore.YELLOW}  └─ Slow query log is not enabled{Style.RESET_ALL}")
                return []

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            return []

    def get_performance_schema_metrics(self):
        """
        Collect metrics from Performance Schema

        Returns:
            dict: Dictionary containing metrics or empty dict if error occurs
        """
        try:
            print(f"{Fore.WHITE}[*] Collecting Performance Schema metrics...")
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)

            # Top queries by execution time
            print(f"{Fore.WHITE}  └─ Analyzing top queries...", end='')
            cursor.execute("""
                SELECT 
                    COALESCE(digest_text, 'Unknown') as query,
                    count_star AS executions,
                    COALESCE(avg_timer_wait/1000000000, 0) AS avg_latency_ms,
                    COALESCE(sum_timer_wait/1000000000, 0) AS total_latency_ms
                FROM performance_schema.events_statements_summary_by_digest
                ORDER BY sum_timer_wait DESC
                LIMIT 10
            """)
            top_queries = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Lock statistics
            print(f"{Fore.WHITE}  └─ Analyzing locks...", end='')
            cursor.execute("""
                SELECT * FROM performance_schema.metadata_locks
                WHERE OWNER_THREAD_ID IS NOT NULL
            """)
            locks = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            cursor.close()
            conn.close()

            return {
                'top_queries': top_queries or [],
                'locks': locks or []
            }

        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            return {'top_queries': [], 'locks': []}


def analyze_performance_metrics(self):
    """
    Analyze collected performance metrics and provide recommendations

    Returns:
        dict: Dictionary containing warnings and recommendations
    """
    warnings = []
    recommendations = []

    # Collect all metrics
    innodb_metrics = self.get_innodb_metrics()
    slow_queries = self.get_slow_queries()
    perf_schema = self.get_performance_schema_metrics()

    # Analyze InnoDB metrics
    if innodb_metrics and innodb_metrics['buffer_stats']:
        buffer_stats = innodb_metrics['buffer_stats']

        reads = self.safe_int(buffer_stats.get('Innodb_buffer_pool_reads', 0))
        read_requests = self.safe_int(buffer_stats.get('Innodb_buffer_pool_read_requests', 1))

        if read_requests > 0:
            hit_ratio = ((read_requests - reads) / read_requests) * 100
            if hit_ratio < 95:
                warnings.append(f"Low buffer pool hit ratio: {hit_ratio:.2f}%")
                recommendations.append("Consider increasing innodb_buffer_pool_size")

    # Analyze slow queries
    if slow_queries:
        if len(slow_queries) > 5:
            warnings.append(f"High number of slow queries detected: {len(slow_queries)}")
            recommendations.append("Review and optimize slow queries")
            recommendations.append("Consider increasing long_query_time if queries are acceptable")

    # Analyze performance schema metrics
    if perf_schema and perf_schema['top_queries']:
        high_latency_queries = [
            q for q in perf_schema['top_queries']
            if self.safe_float(q.get('avg_latency_ms', 0)) > 1000  # queries taking > 1 second
        ]
        if high_latency_queries:
            warnings.append(f"Found {len(high_latency_queries)} queries with high latency")
            recommendations.append("Review and optimize high latency queries")

    return {
        'warnings': warnings,
        'recommendations': recommendations
    }
