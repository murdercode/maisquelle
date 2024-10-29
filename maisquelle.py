import psutil
import mysql.connector
from datetime import datetime
import subprocess
import os
import argparse
from colorama import init, Fore, Style

# Initialize colorama for Windows color support
init()

class SystemMySQLMonitor:
    def __init__(self, host='localhost', user='root', password='', port=3307):
        self.mysql_config = {
            'host': host,
            'user': user,
            'password': password,
            'port': port
        }
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)

    def get_system_resources(self):
        """Monitor system resources"""
        try:
            print(f"{Fore.WHITE}[*] Collecting system data...")
            
            # CPU
            print(f"{Fore.WHITE}  └─ Collecting CPU data...", end='')
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")
            
            # RAM
            print(f"{Fore.WHITE}  └─ Collecting RAM data...", end='')
            ram = psutil.virtual_memory()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")
            
            # SWAP
            print(f"{Fore.WHITE}  └─ Collecting SWAP data...", end='')
            swap = psutil.swap_memory()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")
            
            # Disk
            print(f"{Fore.WHITE}  └─ Collecting DISK data...", end='')
            disk = psutil.disk_usage('/')
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")
            
            return {
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count,
                    'freq': cpu_freq
                },
                'ram': ram,
                'swap': swap,
                'disk': disk
            }
        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            raise

    def check_mysql_service(self):
        """Verify MySQL service status"""
        try:
            print(f"{Fore.WHITE}[*] Checking MySQL processes...", end='')
            mysql_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                if 'mysql' in proc.info['name'].lower():
                    mysql_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_percent': proc.info['memory_percent']
                    })
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")
            return mysql_processes
        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            raise

    def get_mysql_status(self):
        """Collect MySQL statistics"""
        print(f"{Fore.WHITE}[*] Collecting MySQL statistics...")
        try:
            print(f"{Fore.WHITE}  └─ Connecting to database...", end='')
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            print(f"{Fore.WHITE}  └─ Collecting status variables...", end='')
            cursor.execute("SHOW GLOBAL STATUS")
            status_vars = {row['Variable_name']: row['Value'] for row in cursor.fetchall()}
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            print(f"{Fore.WHITE}  └─ Collecting system variables...", end='')
            cursor.execute("SHOW GLOBAL VARIABLES")
            system_vars = {row['Variable_name']: row['Value'] for row in cursor.fetchall()}
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            print(f"{Fore.WHITE}  └─ Collecting process information...", end='')
            cursor.execute("SHOW FULL PROCESSLIST")
            processes = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            print(f"{Fore.WHITE}  └─ Collecting InnoDB status...", end='')
            cursor.execute("SHOW ENGINE INNODB STATUS")
            innodb_status = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            cursor.close()
            conn.close()

            return {
                'status_vars': status_vars,
                'system_vars': system_vars,
                'processes': processes,
                'innodb_status': innodb_status
            }
        except mysql.connector.Error as err:
            print(f"{Fore.RED} MySQL Connection Error: {err}{Style.RESET_ALL}")
            return f"MySQL Connection Error: {err}"
        except Exception as e:
            print(f"{Fore.RED} Generic Error: {e}{Style.RESET_ALL}")
            return f"Generic Error: {e}"
        
    def analyze_query_cache(self):
        """Analyze Query Cache efficiency and performance"""
        try:
            print(f"{Fore.WHITE}[*] Analyzing Query Cache metrics...")
            
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)

            # Get Query Cache configuration
            print(f"{Fore.WHITE}  └─ Collecting cache configuration...", end='')
            cursor.execute("SHOW GLOBAL VARIABLES LIKE 'query_cache%'")
            cache_config = {row['Variable_name']: row['Value'] for row in cursor.fetchall()}
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Get Query Cache statistics
            print(f"{Fore.WHITE}  └─ Collecting cache statistics...", end='')
            cursor.execute("SHOW GLOBAL STATUS LIKE 'Qcache%'")
            cache_status = {row['Variable_name']: row['Value'] for row in cursor.fetchall()}
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Calculate important metrics
            try:
                hits = float(cache_status.get('Qcache_hits', 0))
                inserts = float(cache_status.get('Qcache_inserts', 0))
                queries = hits + inserts
                hit_ratio = (hits / queries * 100) if queries > 0 else 0
                
                total_blocks = float(cache_status.get('Qcache_total_blocks', 1))
                free_blocks = float(cache_status.get('Qcache_free_blocks', 0))
                fragmentation_ratio = (free_blocks / total_blocks * 100)
                
                memory_usage = float(cache_status.get('Qcache_free_memory', 0))
                total_memory = float(cache_config.get('query_cache_size', 1))
                memory_usage_ratio = ((total_memory - memory_usage) / total_memory * 100)
            except (ValueError, ZeroDivisionError) as e:
                print(f"{Fore.RED}  └─ Error calculating metrics: {str(e)}{Style.RESET_ALL}")
                return None

            # Analyze and provide recommendations
            recommendations = []
            warnings = []

            # Check if Query Cache is enabled
            if cache_config.get('query_cache_type') == 'OFF':
                warnings.append("Query Cache is currently disabled")
            else:
                # Analyze hit ratio
                if hit_ratio < 30:
                    warnings.append("Low Query Cache hit ratio (<30%)")
                    if queries > 10000:
                        recommendations.append("Consider increasing query_cache_size as there's significant query traffic")
                elif hit_ratio > 80:
                    recommendations.append("Query Cache hit ratio is good (>80%)")

                # Analyze memory usage
                if memory_usage_ratio > 95:
                    warnings.append("Query Cache memory usage is very high (>95%)")
                    recommendations.append("Consider increasing query_cache_size")
                elif memory_usage_ratio < 20:
                    warnings.append("Query Cache memory usage is very low (<20%)")
                    recommendations.append("Consider decreasing query_cache_size to free up memory")

                # Analyze fragmentation
                if fragmentation_ratio > 20:
                    warnings.append("High Query Cache fragmentation (>20%)")
                    recommendations.append("Consider running FLUSH QUERY CACHE")

                # Analyze low memory conditions
                if int(cache_status.get('Qcache_lowmem_prunes', 0)) > int(cache_status.get('Qcache_inserts', 0)) / 3:
                    warnings.append("High number of queries removed due to low memory")
                    recommendations.append("Consider increasing query_cache_size or reducing query_cache_limit")

            cursor.close()
            conn.close()

            # Prepare detailed report
            report = f"""
    [QUERY CACHE ANALYSIS]
    cache_enabled: {cache_config.get('query_cache_type', 'N/A')}
    cache_size_bytes: {cache_config.get('query_cache_size', 'N/A')}
    cache_limit_bytes: {cache_config.get('query_cache_limit', 'N/A')}
    cache_min_res_unit_bytes: {cache_config.get('query_cache_min_res_unit', 'N/A')}

    [QUERY CACHE METRICS]
    total_queries_cached: {cache_status.get('Qcache_queries_in_cache', 'N/A')}
    cache_hits: {cache_status.get('Qcache_hits', 'N/A')}
    cache_inserts: {cache_status.get('Qcache_inserts', 'N/A')}
    cache_hit_ratio_percent: {hit_ratio:.2f}
    cache_memory_usage_percent: {memory_usage_ratio:.2f}
    cache_fragmentation_percent: {fragmentation_ratio:.2f}
    cache_free_memory_bytes: {cache_status.get('Qcache_free_memory', 'N/A')}
    cache_total_blocks: {cache_status.get('Qcache_total_blocks', 'N/A')}
    cache_free_blocks: {cache_status.get('Qcache_free_blocks', 'N/A')}
    cache_lowmem_prunes: {cache_status.get('Qcache_lowmem_prunes', 'N/A')}
    cache_not_cached: {cache_status.get('Qcache_not_cached', 'N/A')}

    [QUERY CACHE HEALTH]
    warnings:
    {chr(10).join(f"- {warning}" for warning in warnings)}

    recommendations:
    {chr(10).join(f"- {rec}" for rec in recommendations)}
    """
            print(f"{Fore.GREEN}[✓] Query Cache analysis completed{Style.RESET_ALL}")
            return report

        except mysql.connector.Error as err:
            print(f"{Fore.RED}  └─ MySQL Error: {str(err)}{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}  └─ Error: {str(e)}{Style.RESET_ALL}")
            return None
        
    def get_table_statistics(self):
        """Raccoglie statistiche dettagliate sulle tabelle"""
        try:
            print(f"{Fore.WHITE}[*] Collecting table statistics...")
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)

            # Statistiche generali delle tabelle
            print(f"{Fore.WHITE}  └─ Analyzing table sizes...", end='')
            query = """
            SELECT 
                table_schema AS 'Database',
                table_name AS 'Table',
                engine AS 'Engine',
                row_format AS 'Row_Format',
                table_rows AS 'Rows',
                avg_row_length AS 'Avg_Row_Length',
                data_length AS 'Data_Size',
                index_length AS 'Index_Size',
                data_free AS 'Free_Space'
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema')
            """
            cursor.execute(query)
            table_stats = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Analisi degli indici
            print(f"{Fore.WHITE}  └─ Analyzing indexes...", end='')
            query = """
            SELECT 
                table_schema AS 'Database',
                table_name AS 'Table',
                index_name AS 'Index_Name',
                column_name AS 'Column',
                cardinality AS 'Cardinality',
                nullable AS 'Is_Nullable'
            FROM information_schema.statistics 
            WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema')
            """
            cursor.execute(query)
            index_stats = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            return {
                'table_stats': table_stats,
                'index_stats': index_stats
            }

        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            return None

    def get_innodb_metrics(self):
        """Raccoglie metriche dettagliate di InnoDB"""
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

            return {
                'buffer_stats': buffer_stats,
                'io_stats': io_stats,
                'trx_stats': trx_stats
            }

        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            return None

    def get_slow_queries(self):
        """Analizza le query lente se il slow query log è attivo"""
        try:
            print(f"{Fore.WHITE}[*] Analyzing slow queries...")
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)

            # Verifica se il slow query log è attivo
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
                return slow_queries
            else:
                print(f"{Fore.YELLOW}  └─ Slow query log is not enabled{Style.RESET_ALL}")
                return None

        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            return None

    def get_performance_schema_metrics(self):
        """Raccoglie metriche dal Performance Schema"""
        try:
            print(f"{Fore.WHITE}[*] Collecting Performance Schema metrics...")
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)

            # Top query per tempo di esecuzione
            print(f"{Fore.WHITE}  └─ Analyzing top queries...", end='')
            cursor.execute("""
                SELECT 
                    digest_text AS query,
                    count_star AS executions,
                    avg_timer_wait/1000000000 AS avg_latency_ms,
                    sum_timer_wait/1000000000 AS total_latency_ms
                FROM performance_schema.events_statements_summary_by_digest
                ORDER BY sum_timer_wait DESC
                LIMIT 10
            """)
            top_queries = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Statistiche di lock
            print(f"{Fore.WHITE}  └─ Analyzing locks...", end='')
            cursor.execute("""
                SELECT * FROM performance_schema.metadata_locks
                WHERE OWNER_THREAD_ID IS NOT NULL
            """)
            locks = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            return {
                'top_queries': top_queries,
                'locks': locks
            }

        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            return None

    def generate_report(self, enable_tables=False):
        """Generate comprehensive system and MySQL status report"""
        print(f"\n{Fore.WHITE}[*] Generating report...{Style.RESET_ALL}")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Raccolta dati
            system_resources = self.get_system_resources()
            mysql_processes = self.check_mysql_service()
            mysql_stats = self.get_mysql_status()
            query_cache_report = self.analyze_query_cache()
            table_stats = self.get_table_statistics() if enable_tables else None
            innodb_metrics = self.get_innodb_metrics()
            slow_queries = self.get_slow_queries()
            perf_schema_metrics = self.get_performance_schema_metrics()
    
            def safe_get(dictionary, key, default='N/A'):
                """Recupera in modo sicuro i valori dal dizionario"""
                if dictionary is None:
                    return default
                return dictionary.get(key, default)
    
            def safe_size(value):
                """Converte in modo sicuro i bytes in formato leggibile"""
                try:
                    if value is None or value == 'N/A':
                        return 'N/A'
                    return get_size(float(value))
                except (ValueError, TypeError):
                    return 'N/A'
    
            def format_cpu_freq(freq_obj, attr):
                """Formatta in modo sicuro i valori della frequenza CPU"""
                try:
                    if hasattr(freq_obj, attr):
                        value = getattr(freq_obj, attr)
                        if value is not None:
                            return f"{value:.2f}"
                    return 'N/A'
                except (AttributeError, TypeError):
                    return 'N/A'
    
            # Inizio Report
            report = f"""
    === SYSTEM AND MYSQL STATUS REPORT ===
    Timestamp: {current_time}
    
    === MYSQL CONFIGURATION ===
    host: {self.mysql_config['host']}
    port: {self.mysql_config['port']}
    user: {self.mysql_config['user']}"""
    
            # System Resources Section
            if system_resources:
                current_freq = format_cpu_freq(system_resources['cpu']['freq'], 'current')
                max_freq = format_cpu_freq(system_resources['cpu']['freq'], 'max')
                
                report += f"""
    
    === SYSTEM METRICS ===
    [CPU]
    total_usage_percent: {system_resources['cpu']['percent']}
    core_count: {system_resources['cpu']['count']}
    current_frequency_mhz: {current_freq}
    max_frequency_mhz: {max_freq}
    
    [MEMORY]
    total_ram_bytes: {system_resources['ram'].total if system_resources['ram'] else 'N/A'}
    used_ram_bytes: {system_resources['ram'].used if system_resources['ram'] else 'N/A'}
    available_ram_bytes: {system_resources['ram'].available if system_resources['ram'] else 'N/A'}
    ram_usage_percent: {system_resources['ram'].percent if system_resources['ram'] else 'N/A'}
    total_swap_bytes: {system_resources['swap'].total if system_resources['swap'] else 'N/A'}
    used_swap_bytes: {system_resources['swap'].used if system_resources['swap'] else 'N/A'}
    swap_usage_percent: {system_resources['swap'].percent if system_resources['swap'] else 'N/A'}
    
    [DISK]
    total_disk_bytes: {system_resources['disk'].total if system_resources['disk'] else 'N/A'}
    used_disk_bytes: {system_resources['disk'].used if system_resources['disk'] else 'N/A'}
    free_disk_bytes: {system_resources['disk'].free if system_resources['disk'] else 'N/A'}
    disk_usage_percent: {system_resources['disk'].percent if system_resources['disk'] else 'N/A'}"""
    
            # MySQL Metrics Section
            report += "\n\n=== MYSQL METRICS ==="
    
            if isinstance(mysql_stats, str):
                report += f"""
    [ERROR]
    mysql_error: {mysql_stats}"""
            elif mysql_stats:
                stats = mysql_stats.get('status_vars', {})
                vars = mysql_stats.get('system_vars', {})
    
                # MySQL Processes
                if mysql_processes:
                    report += "\n[MYSQL PROCESSES]"
                    for proc in mysql_processes:
                        report += f"""
    process_pid: {proc.get('pid', 'N/A')}
    process_name: {proc.get('name', 'N/A')}
    process_cpu_percent: {proc.get('cpu_percent', 'N/A')}
    process_memory_percent: {proc.get('memory_percent', 'N/A')}"""
    
                # Connection Metrics
                report += f"""
    
    [CONNECTION METRICS]
    max_connections: {safe_get(vars, 'max_connections')}
    current_connections: {safe_get(stats, 'Threads_connected')}
    max_used_connections: {safe_get(stats, 'Max_used_connections')}
    aborted_connects: {safe_get(stats, 'Aborted_connects')}
    total_received_bytes: {safe_get(stats, 'Bytes_received')}
    total_sent_bytes: {safe_get(stats, 'Bytes_sent')}
    
    [QUERY METRICS]
    queries_per_second: {safe_get(stats, 'Queries')}
    slow_queries: {safe_get(stats, 'Slow_queries')}
    select_count: {safe_get(stats, 'Com_select')}
    insert_count: {safe_get(stats, 'Com_insert')}
    update_count: {safe_get(stats, 'Com_update')}
    delete_count: {safe_get(stats, 'Com_delete')}
    total_questions: {safe_get(stats, 'Questions')}
    
    [BUFFER AND CACHE]
    innodb_buffer_pool_size_bytes: {safe_get(vars, 'innodb_buffer_pool_size', 0)}
    key_buffer_size_bytes: {safe_get(vars, 'key_buffer_size', 0)}
    query_cache_size_bytes: {safe_get(vars, 'query_cache_size', 0)}
    innodb_buffer_pool_pages_total: {safe_get(stats, 'Innodb_buffer_pool_pages_total')}
    innodb_buffer_pool_pages_free: {safe_get(stats, 'Innodb_buffer_pool_pages_free')}
    key_blocks_unused: {safe_get(stats, 'Key_blocks_unused')}
    
    [INNODB METRICS]
    innodb_data_reads: {safe_get(stats, 'Innodb_data_reads')}
    innodb_data_writes: {safe_get(stats, 'Innodb_data_writes')}
    innodb_row_lock_current_waits: {safe_get(stats, 'Innodb_row_lock_current_waits')}
    innodb_buffer_pool_read_requests: {safe_get(stats, 'Innodb_buffer_pool_read_requests')}
    innodb_buffer_pool_write_requests: {safe_get(stats, 'Innodb_buffer_pool_write_requests')}
    
    [ACTIVE PROCESSES]"""
                
                if mysql_stats.get('processes'):
                    for process in mysql_stats['processes']:
                        if process.get('Command') != 'Sleep':
                            report += f"""
    process_id: {safe_get(process, 'Id')}
    process_user: {safe_get(process, 'User')}
    process_host: {safe_get(process, 'Host')}
    process_db: {safe_get(process, 'db', 'None')}
    process_command: {safe_get(process, 'Command')}
    process_time: {safe_get(process, 'Time')}
    process_state: {safe_get(process, 'State')}"""
    
            # Query Cache Analysis
            if query_cache_report:
                report += f"\n\n=== QUERY CACHE ANALYSIS ===\n{query_cache_report}"
    
            # Table Statistics Section
            if enable_tables and table_stats and table_stats.get('table_stats'):
                report += "\n[TABLE STATISTICS]"
                for stat in table_stats['table_stats']:
                    report += f"""
    Database: {safe_get(stat, 'Database')}
    Table: {safe_get(stat, 'Table')}
    Engine: {safe_get(stat, 'Engine')}
    Rows: {safe_get(stat, 'Rows')}
    Data Size: {safe_size(safe_get(stat, 'Data_Size'))}
    Index Size: {safe_size(safe_get(stat, 'Index_Size'))}
    Free Space: {safe_size(safe_get(stat, 'Free_Space'))}"""
    
            # InnoDB Detailed Metrics
            if innodb_metrics:
                report += "\n[INNODB DETAILED METRICS]"
                if innodb_metrics.get('buffer_stats'):
                    report += "\nBuffer Pool Stats:\n"
                    for k, v in innodb_metrics['buffer_stats'].items():
                        report += f"- {k}: {v}\n"
                
                if innodb_metrics.get('io_stats'):
                    report += "\nI/O Stats:\n"
                    for k, v in innodb_metrics['io_stats'].items():
                        report += f"- {k}: {v}\n"
                
                if innodb_metrics.get('trx_stats'):
                    report += "\nTransaction Stats:\n"
                    for k, v in innodb_metrics['trx_stats'].items():
                        report += f"- {k}: {v}\n"
    
            # Slow Queries Section
            if slow_queries:
                report += "\n[TOP 10 SLOW QUERIES]"
                for query in slow_queries:
                    report += f"""
    Query: {safe_get(query, 'sql_text', '')[:200]}...
    Execution Time: {safe_get(query, 'query_time')} sec
    Lock Time: {safe_get(query, 'lock_time')} sec
    Rows Examined: {safe_get(query, 'rows_examined')}"""
    
            # Performance Schema Metrics
            if perf_schema_metrics and perf_schema_metrics.get('top_queries'):
                report += "\n[PERFORMANCE SCHEMA METRICS]\nTop Queries by Execution Time:"
                for query in perf_schema_metrics['top_queries']:
                    report += f"""
    Query: {safe_get(query, 'query', '')[:200]}...
    Executions: {safe_get(query, 'executions')}
    Avg Latency: {safe_get(query, 'avg_latency_ms')} ms
    Total Latency: {safe_get(query, 'total_latency_ms')} ms"""
    
            # Save report
            filename = f"logs/status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"{Fore.GREEN}[✓] Report generated successfully{Style.RESET_ALL}")
            return filename
            
        except Exception as e:
            print(f"{Fore.RED}[✗] Error during report generation: {str(e)}{Style.RESET_ALL}")
            raise

def get_size(bytes):
    """Convert bytes to readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024

def parse_arguments():
    """Handle command line arguments"""
    parser = argparse.ArgumentParser(description='System and MySQL Monitor')
    parser.add_argument('--host', default='localhost',
                      help='MySQL Host (default: localhost)')
    parser.add_argument('-u', '--user', default='root',
                      help='MySQL Username (default: root)')
    parser.add_argument('-p', '--password', default='',
                      help='MySQL Password (default: empty)')
    parser.add_argument('--port', type=int, default=3307,
                      help='MySQL Port (default: 3307)')
    parser.add_argument('--enable-tables', action='store_true',
                      help='Enable collection of table statistics')
    
    return parser.parse_args()

def main():
    try:
        args = parse_arguments()
        
        print(f"\n{Fore.CYAN}[*] Starting System and MySQL monitoring...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] MySQL Connection: {args.host}:{args.port} with user {args.user}{Style.RESET_ALL}\n")
        
        monitor = SystemMySQLMonitor(
            host=args.host,
            user=args.user,
            password=args.password,
            port=args.port
        )
        
        filename = monitor.generate_report(enable_tables=args.enable_tables)
        print(f"\n{Fore.GREEN}[✓] Report saved to: {filename}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Monitoring completed.{Style.RESET_ALL}\n")
            
    except Exception as e:
        print(f"\n{Fore.RED}[✗] Execution error: {str(e)}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()