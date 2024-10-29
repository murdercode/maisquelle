import mysql.connector
from colorama import Fore, Style


class TableStatistics:
    """Class for collecting and analyzing MySQL table statistics"""

    def __init__(self, host='localhost', user='root', password='', port=3307):
        """
        Initialize TableStatistics analyzer with MySQL connection parameters

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

    def get_table_statistics(self):
        """
        Collect detailed statistics about MySQL tables and their indexes

        Returns:
            dict: Dictionary containing two main sections:
                - table_stats: List of dictionaries with table information including:
                    * Database name
                    * Table name
                    * Engine type
                    * Row format
                    * Number of rows
                    * Average row length
                    * Data size
                    * Index size
                    * Free space
                - index_stats: List of dictionaries with index information including:
                    * Database name
                    * Table name
                    * Index name
                    * Column name
                    * Cardinality
                    * Nullable status

        Raises:
            mysql.connector.Error: If there's an error connecting to MySQL
            Exception: For other generic errors
        """
        try:
            print(f"{Fore.WHITE}[*] Collecting table statistics...")
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)

            # General table statistics
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
            WHERE table_schema NOT IN 
                ('information_schema', 'mysql', 'performance_schema')
            """
            cursor.execute(query)
            table_stats = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Index analysis
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
            WHERE table_schema NOT IN 
                ('information_schema', 'mysql', 'performance_schema')
            """
            cursor.execute(query)
            index_stats = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            cursor.close()
            conn.close()

            return {
                'table_stats': table_stats,
                'index_stats': index_stats
            }

        except mysql.connector.Error as err:
            print(f"{Fore.RED} MySQL Error: {str(err)}{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            return None

    def analyze_table_health(self, stats):
        """
        Analyze table statistics and provide recommendations

        Args:
            stats (dict): Dictionary containing table and index statistics
                         as returned by get_table_statistics()

        Returns:
            dict: Dictionary containing:
                - warnings: List of potential issues
                - recommendations: List of suggested actions
        """
        warnings = []
        recommendations = []

        if not stats or 'table_stats' not in stats:
            return {'warnings': ['No table statistics available'], 'recommendations': []}

        for table in stats['table_stats']:
            # Check for tables without indexes
            if table['Index_Size'] == 0:
                warnings.append(f"Table {table['Database']}.{table['Table']} has no indexes")
                recommendations.append(
                    f"Consider adding appropriate indexes to {table['Database']}.{table['Table']}"
                )

            # Check for large tables
            if table['Data_Size'] > 1073741824:  # 1GB
                warnings.append(
                    f"Table {table['Database']}.{table['Table']} is larger than 1GB"
                )
                recommendations.append(
                    f"Consider partitioning {table['Database']}.{table['Table']}"
                )

            # Check for significant free space
            if table['Free_Space'] > table['Data_Size'] * 0.2:  # More than 20% fragmentation
                warnings.append(
                    f"Table {table['Database']}.{table['Table']} has significant free space"
                )
                recommendations.append(
                    f"Consider running OPTIMIZE TABLE on {table['Database']}.{table['Table']}"
                )

        return {
            'warnings': warnings,
            'recommendations': recommendations
        }
