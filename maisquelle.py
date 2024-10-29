import argparse
from pathlib import Path

from colorama import init, Fore, Style

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from src.monitor.mysql_monitor import MySQLMonitor
from src.monitor.performance_monitor import PerformanceMonitor
from src.monitor.query_analyzer import QueryAnalyzer
from src.monitor.system_monitor import SystemMonitor
from src.monitor.table_statistics import TableStatistics
from src.utils.report_handler import ReportHandler

# Initialize colorama for Windows color support
init()


class SystemMySQLMonitor:
    def __init__(self, host=None, user=None, password=None, port=None):
        self.settings = self._load_settings()
        self.api_key = self._get_api_key()

        # Get MySQL settings from yaml with defaults
        mysql_settings = self.settings.get('mysql', {})

        self.mysql_config = {
            "host": host or mysql_settings.get('host', 'localhost'),
            "user": user or mysql_settings.get('user', 'root'),
            "password": password or mysql_settings.get('password', ''),
            "port": port or mysql_settings.get('port', 3306)
        }

        self.system_monitor = SystemMonitor()
        self.mysql_monitor = MySQLMonitor(**self.mysql_config)
        self.query_analyzer = QueryAnalyzer(**self.mysql_config)
        self.table_statistics = TableStatistics(**self.mysql_config)
        self.performance_monitor = PerformanceMonitor(**self.mysql_config)
        self.report_handler = ReportHandler()

    def _load_settings(self):
        """Load settings from settings.yaml file"""
        if not YAML_AVAILABLE:
            return {}

        try:
            settings_path = Path("settings.yaml")
            example_settings_path = Path("settings.example.yaml")

            # Se settings.yaml non esiste ma esiste l'example
            if not settings_path.exists() and example_settings_path.exists():
                print(f"{Fore.YELLOW}[!] settings.yaml non trovato, copio da settings.example.yaml{Style.RESET_ALL}")
                # Copia il file example in settings.yaml
                settings_path.write_text(example_settings_path.read_text())

            if not settings_path.exists():
                return {}

            with open(settings_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"{Fore.RED}[✗] Errore nel caricamento delle impostazioni: {str(e)}{Style.RESET_ALL}")
            return {}

    def _get_api_key(self):
        """Get Anthropic API key from settings"""
        return self.settings.get("anthropic", {}).get("api_key", "")

    def get_ai_optimization_tips(self, monitoring_data):
        """Get AI-powered optimization tips based on monitoring data"""
        if not self.api_key:
            print(
                f"{Fore.YELLOW}[!] AI optimization tips not available - Anthropic API key not configured{Style.RESET_ALL}"
            )
            print(
                f"{Fore.YELLOW}[!] Add your API key to settings.yaml to enable AI-powered recommendations{Style.RESET_ALL}"
            )
            return None

        try:
            # This is where you would implement the AI analysis
            # Example structure for future implementation:
            """
            anthropic_client = AnthropicClient(api_key=self.api_key)

            prompt = {
                "system_metrics": monitoring_data["system_resources"],
                "mysql_stats": monitoring_data["mysql_stats"],
                "performance_metrics": monitoring_data["performance_schema_metrics"],
                "query_stats": monitoring_data["query_cache_report"]
            }

            optimization_tips = anthropic_client.analyze_metrics(prompt)
            return optimization_tips
            """
            pass
        except Exception as e:
            print(
                f"{Fore.RED}[✗] Cannot get an AI report, please check your API key: {str(e)}{Style.RESET_ALL}"
            )
            return None

    def collect_monitoring_data(self, enable_tables=False):
        """Collect all monitoring data and return as a structured dictionary"""
        try:
            monitoring_data = {
                "mysql_config": self.mysql_config,
                "system_resources": self.system_monitor.get_system_resources(),
                "mysql_processes": self.mysql_monitor.check_mysql_service(),
                "mysql_stats": self.mysql_monitor.get_mysql_status(),
                "query_cache_report": self.query_analyzer.analyze_query_cache(),
                "innodb_metrics": self.performance_monitor.get_innodb_metrics(),
                "slow_queries": self.performance_monitor.get_slow_queries(),
                "performance_schema_metrics": self.performance_monitor.get_performance_schema_metrics(),
            }

            if enable_tables:
                table_stats = self.table_statistics.get_table_statistics()
                monitoring_data["table_stats"] = table_stats

            return monitoring_data

        except Exception as e:
            print(
                f"{Fore.RED}[✗] Error collecting monitoring data: {str(e)}{Style.RESET_ALL}"
            )
            raise

    def generate_report(self, enable_tables=False):
        """Generate and save monitoring report"""
        print(f"\n{Fore.WHITE}[*] Generating report...{Style.RESET_ALL}")

        try:
            # Collect all monitoring data
            monitoring_data = self.collect_monitoring_data(enable_tables)

            # Get AI optimization tips if available
            optimization_tips = self.get_ai_optimization_tips(monitoring_data)
            if optimization_tips:
                monitoring_data["optimization_tips"] = optimization_tips

            # Save report using ReportHandler
            filename = self.report_handler.save_report(monitoring_data)

            print(f"{Fore.GREEN}[✓] Report generated successfully{Style.RESET_ALL}")
            return filename

        except Exception as e:
            print(
                f"{Fore.RED}[✗] Error during report generation: {str(e)}{Style.RESET_ALL}"
            )


def get_size(bytes):
    """Convert bytes to readable format"""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024


def parse_arguments(settings=None):
    """Handle command line arguments with fallback to settings.yaml"""
    parser = argparse.ArgumentParser(description="System and MySQL Monitor")

    # Get MySQL settings from yaml with defaults
    mysql_settings = settings.get('mysql', {}) if settings else {}

    parser.add_argument(
        "--host",
        default=mysql_settings.get('host', 'localhost'),
        help=f"MySQL Host (default: {mysql_settings.get('host', 'localhost')})"
    )
    parser.add_argument(
        "-u", "--user",
        default=mysql_settings.get('user', 'root'),
        help=f"MySQL Username (default: {mysql_settings.get('user', 'root')})"
    )
    parser.add_argument(
        "-p", "--password",
        default=mysql_settings.get('password', ''),
        help="MySQL Password (default: from settings.yaml or empty)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=mysql_settings.get('port', 3306),
        help=f"MySQL Port (default: {mysql_settings.get('port', 3306)})"
    )
    parser.add_argument(
        "--enable-tables",
        action="store_true",
        help="Enable collection of table statistics"
    )

    return parser.parse_args()


def main():
    try:
        # Prima carica le impostazioni
        monitor = SystemMySQLMonitor()

        # Passa le impostazioni al parser degli argomenti
        args = parse_arguments(monitor.settings)

        print(f"\n{Fore.CYAN}[*] Starting System and MySQL monitoring...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] MySQL Connection: {args.host}:{args.port} with user {args.user}{Style.RESET_ALL}\n")

        # Aggiorna il monitor con i parametri finali (combinazione di settings.yaml e argomenti CLI)
        monitor.mysql_config.update({
            "host": args.host,
            "user": args.user,
            "password": args.password,
            "port": args.port,
        })

        filename = monitor.generate_report(enable_tables=args.enable_tables)
        print(f"\n{Fore.GREEN}[✓] Report saved to: {filename}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Monitoring completed.{Style.RESET_ALL}\n")

    except Exception as e:
        print(f"\n{Fore.RED}[✗] Execution error: {str(e)}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
