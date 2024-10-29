import mysql.connector
from colorama import Fore, Style


class QueryAnalyzer:
    """Class for analyzing MySQL query performance and cache metrics"""

    def __init__(self, host='localhost', user='root', password='', port=3307):
        """
        Initialize QueryAnalyzer with MySQL connection parameters

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

    def analyze_query_cache(self):
        """
        Analyze Query Cache efficiency and performance

        Returns:
            str: A detailed report containing:
                - Query Cache configuration
                - Cache performance metrics
                - Health analysis
                - Warnings and recommendations

        Raises:
            mysql.connector.Error: If there's an error connecting to MySQL
            Exception: For other generic errors
        """
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
                        recommendations.append(
                            "Consider increasing query_cache_size as there's significant query traffic")
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
