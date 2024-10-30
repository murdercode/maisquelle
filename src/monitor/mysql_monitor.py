import mysql.connector
import psutil
from colorama import Fore, Style


class MySQLMonitor:
    """Class to monitor MySQL-specific processes and metrics"""

    def __init__(self, host="localhost", user="root", password="", port=3307):
        """
        Initialize MySQL monitor with connection parameters

        Args:
            host (str): MySQL host address
            user (str): MySQL username
            password (str): MySQL password
            port (int): MySQL port number
        """
        self.mysql_config = {
            "host": host,
            "user": user,
            "password": password,
            "port": port,
        }

    def get_mysql_version(self):
        """
        Get MySQL server version

        Returns:
            str: MySQL version string

        Raises:
            mysql.connector.Error: If there's an error connecting to MySQL
            Exception: For other generic errors
        """
        try:
            print(f"{Fore.WHITE}[*] Checking MySQL version...", end="")
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor()

            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")
            return version

        except mysql.connector.Error as err:
            print(f"{Fore.RED} MySQL Connection Error: {err}{Style.RESET_ALL}")
            return f"MySQL Connection Error: {err}"

        except Exception as e:
            print(f"{Fore.RED} Generic Error: {e}{Style.RESET_ALL}")
            return f"Generic Error: {e}"

    def check_mysql_service(self):
        """
        Verify MySQL service status by checking running processes

        Returns:
            list: List of dictionaries containing MySQL process information
                  Each dictionary contains: pid, name, cpu_percent, memory_percent

        Raises:
            Exception: If there's an error accessing process information
        """
        try:
            print(f"{Fore.WHITE}[*] Checking MySQL processes...", end="")
            mysql_processes = []

            for proc in psutil.process_iter(
                ["pid", "name", "cpu_percent", "memory_percent"]
            ):
                if "mysql" in proc.info["name"].lower():
                    mysql_processes.append(
                        {
                            "pid": proc.info["pid"],
                            "name": proc.info["name"],
                            "cpu_percent": proc.info["cpu_percent"],
                            "memory_percent": proc.info["memory_percent"],
                        }
                    )

            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")
            return mysql_processes

        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            raise

    def get_mysql_status(self):
        """
        Collect comprehensive MySQL statistics including status variables,
        system variables, process list, and InnoDB status.

        Returns:
            dict: Dictionary containing various MySQL statistics:
                - status_vars: Global status variables
                - system_vars: Global system variables
                - processes: List of current processes
                - innodb_status: InnoDB engine status

        Raises:
            mysql.connector.Error: If there's an error connecting to MySQL
            Exception: For other generic errors
        """
        print(f"{Fore.WHITE}[*] Collecting MySQL statistics...")
        try:
            print(f"{Fore.WHITE}  └─ Connecting to database...", end="")
            conn = mysql.connector.connect(**self.mysql_config)
            cursor = conn.cursor(dictionary=True)
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Collect status variables
            print(f"{Fore.WHITE}  └─ Collecting status variables...", end="")
            cursor.execute("SHOW GLOBAL STATUS")
            status_vars = {
                row["Variable_name"]: row["Value"] for row in cursor.fetchall()
            }
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Collect system variables
            print(f"{Fore.WHITE}  └─ Collecting system variables...", end="")
            cursor.execute("SHOW GLOBAL VARIABLES")
            system_vars = {
                row["Variable_name"]: row["Value"] for row in cursor.fetchall()
            }
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Collect process information
            print(f"{Fore.WHITE}  └─ Collecting process information...", end="")
            cursor.execute("SHOW FULL PROCESSLIST")
            processes = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Collect InnoDB status
            print(f"{Fore.WHITE}  └─ Collecting InnoDB status...", end="")
            cursor.execute("SHOW ENGINE INNODB STATUS")
            innodb_status = cursor.fetchall()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            cursor.close()
            conn.close()

            return {
                "status_vars": status_vars,
                "system_vars": system_vars,
                "processes": processes,
                "innodb_status": innodb_status,
            }

        except mysql.connector.Error as err:
            print(f"{Fore.RED} MySQL Connection Error: {err}{Style.RESET_ALL}")
            return f"MySQL Connection Error: {err}"

        except Exception as e:
            print(f"{Fore.RED} Generic Error: {e}{Style.RESET_ALL}")
            return f"Generic Error: {e}"
