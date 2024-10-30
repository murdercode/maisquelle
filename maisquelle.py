import argparse
from datetime import datetime
from pathlib import Path

from colorama import init, Fore, Style

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

from src.utils.banner import print_header
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
        mysql_settings = self.settings.get("mysql", {})
        monitoring_settings = self.settings.get("monitoring", {})

        self.monitoring_level = monitoring_settings.get("level", 2)

        self.mysql_config = {
            "host": host or mysql_settings.get("host", "localhost"),
            "user": user or mysql_settings.get("user", "root"),
            "password": password or mysql_settings.get("password", ""),
            "port": port or mysql_settings.get("port", 3306),
        }

        # Initialize AI handler early
        if self.api_key:
            try:
                from src.ai.anthropic import AnthropicHandler

                self.ai_handler = AnthropicHandler(api_key=self.api_key)
            except Exception as e:
                print(
                    f"{Fore.YELLOW}[!] Warning: Could not initialize AI handler: {str(e)}{Style.RESET_ALL}"
                )
                self.ai_handler = None
        else:
            print(
                f"{Fore.YELLOW}[!] Warning: No Anthropic API key found in settings.{Style.RESET_ALL}"
            )
            self.ai_handler = None

        # Initialize monitors based on level
        self.system_monitor = SystemMonitor()
        self.mysql_monitor = MySQLMonitor(**self.mysql_config)
        self.query_analyzer = QueryAnalyzer(**self.mysql_config)
        self.performance_monitor = PerformanceMonitor(**self.mysql_config)
        self.table_statistics = TableStatistics(**self.mysql_config)
        self.report_handler = ReportHandler()

    def _load_settings(self):
        """Load settings from settings.yaml file"""
        if not YAML_AVAILABLE:
            return {}

        try:
            settings_path = Path("settings.yaml")
            example_settings_path = Path("settings.example.yaml")

            # If settings.yaml doesn't exist but example does
            if not settings_path.exists() and example_settings_path.exists():
                print(
                    f"{Fore.YELLOW}[!] settings.yaml not found, copying from settings.example.yaml{Style.RESET_ALL}"
                )
                settings_path.write_text(example_settings_path.read_text())

            if not settings_path.exists():
                return {}

            with open(settings_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"{Fore.RED}[✗] Error loading settings: {str(e)}{Style.RESET_ALL}")
            return {}

    def _get_api_key(self):
        """Get Anthropic API key from settings"""
        return self.settings.get("anthropic", {}).get("api_key", "")

    def collect_monitoring_data(self):
        """Collect monitoring data based on the configured level"""
        print(
            f"\n{Fore.CYAN}[*] Starting Level {self.monitoring_level} monitoring...{Style.RESET_ALL}"
        )

        try:
            monitoring_data = {
                "timestamp": datetime.now(),
                "monitoring_level": self.monitoring_level,
                "ai_enabled": bool(self.ai_handler),
            }

            # Level 1: Basic Health Check
            basic_data = self._collect_level_1()
            monitoring_data.update(basic_data)

            # Get AI insights for Level 1
            if self.ai_handler:
                monitoring_data["ai_analysis_basic"] = self._get_ai_insights(
                    basic_data, "basic"
                )

            # Level 2: Standard Analysis
            if self.monitoring_level >= 2:
                standard_data = self._collect_level_2()
                monitoring_data.update(standard_data)

                if self.ai_handler:
                    monitoring_data["ai_analysis_performance"] = self._get_ai_insights(
                        standard_data, "performance"
                    )

            # Level 3: Deep Inspection
            if self.monitoring_level == 3:
                deep_data = self._collect_level_3()
                monitoring_data.update(deep_data)

                if self.ai_handler:
                    monitoring_data["ai_analysis_deep"] = self._get_ai_insights(
                        deep_data, "deep"
                    )

            return monitoring_data

        except Exception as e:
            print(
                f"{Fore.RED}[✗] Error collecting monitoring data: {str(e)}{Style.RESET_ALL}"
            )
            raise

    def _get_ai_insights(self, data, analysis_type):
        """Get AI insights based on the type of data being analyzed"""
        try:
            print(
                f"{Fore.WHITE}[*] Getting AI insights for {analysis_type} analysis...{Style.RESET_ALL}"
            )

            if analysis_type == "basic":
                return self.ai_handler.analyze_basic_health(data)
            elif analysis_type == "performance":
                return self.ai_handler.analyze_performance(data)
            elif analysis_type == "deep":
                return self.ai_handler.analyze_deep_metrics(data)

        except Exception as e:
            print(f"{Fore.RED}[✗] Error getting AI insights: {str(e)}{Style.RESET_ALL}")
            return {"error": str(e)}

    def _collect_level_1(self):
        """Collect basic health metrics"""
        return {
            "system_basic": self.system_monitor.get_system_resources(),
            "mysql_status": self.mysql_monitor.get_mysql_status(),
        }

    def _collect_level_2(self):
        """Collect standard performance metrics"""
        return {
            "query_cache": self.query_analyzer.analyze_query_cache(),
            "innodb_metrics": self.performance_monitor.get_innodb_metrics(),
            "slow_queries": self.performance_monitor.get_slow_queries(),
        }

    def _collect_level_3(self):
        """Collect deep inspection metrics"""
        return {
            "table_stats": self.table_statistics.get_table_statistics(),
            "performance_schema": self.performance_monitor.get_performance_schema_metrics(),
        }

    def generate_report(self, enable_tables=False):
        """Generate monitoring report with AI insights"""
        print(
            f"\n{Fore.WHITE}[*] Generating Level {self.monitoring_level} Report with AI Analysis...{Style.RESET_ALL}"
        )

        try:
            monitoring_data = self.collect_monitoring_data()

            # Process and execute AI recommendations if available
            if self.ai_handler and any(
                key.startswith("ai_analysis_") for key in monitoring_data
            ):
                print(
                    f"\n{Fore.CYAN}[*] Processing AI recommendations...{Style.RESET_ALL}"
                )
                self._process_ai_recommendations(monitoring_data)

            filename = self.report_handler.save_report(monitoring_data)

            print(
                f"{Fore.GREEN}[✓] Report generated successfully: {filename}{Style.RESET_ALL}"
            )
            return filename

        except Exception as e:
            print(
                f"{Fore.RED}[✗] Error during report generation: {str(e)}{Style.RESET_ALL}"
            )

    def _process_ai_recommendations(self, monitoring_data):
        """Process and potentially execute AI recommendations"""
        try:
            all_recommendations = []
            for key in monitoring_data:
                if key.startswith("ai_analysis_"):
                    if (
                        isinstance(monitoring_data[key], dict)
                        and "recommendations" in monitoring_data[key]
                    ):
                        all_recommendations.extend(
                            monitoring_data[key]["recommendations"]
                        )

            if all_recommendations:
                approved_commands = self.ai_handler.process_commands_interactively(
                    all_recommendations
                )
                if approved_commands:
                    self.ai_handler.execute_approved_commands(approved_commands)
                return approved_commands

            return []

        except Exception as e:
            print(
                f"{Fore.RED}[✗] Error processing AI recommendations: {str(e)}{Style.RESET_ALL}"
            )
            return []


def parse_arguments(settings=None):
    """Handle command line arguments with fallback to settings.yaml"""
    parser = argparse.ArgumentParser(description="MAISQUELLE - MySQL Monitoring System")

    # Get settings with defaults
    mysql_settings = settings.get("mysql", {}) if settings else {}
    monitoring_settings = settings.get("monitoring", {}) if settings else {}

    # MySQL connection arguments
    parser.add_argument(
        "--host",
        default=mysql_settings.get("host", "localhost"),
        help=f"MySQL Host (default: {mysql_settings.get('host', 'localhost')})",
    )
    parser.add_argument(
        "-u",
        "--user",
        default=mysql_settings.get("user", "root"),
        help=f"MySQL Username (default: {mysql_settings.get('user', 'root')})",
    )
    parser.add_argument(
        "-p",
        "--password",
        default=mysql_settings.get("password", ""),
        help="MySQL Password (default: from settings.yaml or empty)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=mysql_settings.get("port", 3306),
        help=f"MySQL Port (default: {mysql_settings.get('port', 3306)})",
    )

    # Monitoring level argument
    parser.add_argument(
        "--level",
        type=int,
        choices=[1, 2, 3],
        default=monitoring_settings.get("level", 2),
        help="Monitoring level: 1-Basic, 2-Advanced, 3-Expert (default: from settings.yaml or 2)",
    )

    parser.add_argument(
        "--enable-tables",
        action="store_true",
        help="Enable collection of table statistics",
    )

    return parser.parse_args()


def main():
    try:
        print_header()
        monitor = SystemMySQLMonitor()
        args = parse_arguments(monitor.settings)

        # Update monitoring level from command line argument
        monitor.monitoring_level = args.level

        # Print monitoring level description
        level_descriptions = {
            1: "Basic health check and essential metrics",
            2: "Advanced analysis with performance metrics",
            3: "Expert level deep inspection and detailed analytics",
        }

        print(
            f"\n{Fore.CYAN}[*] Starting System and MySQL monitoring (Level {args.level})...{Style.RESET_ALL}"
        )
        print(
            f"{Fore.CYAN}[*] MySQL Connection: {args.host}:{args.port} with user {args.user}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.CYAN}[*] Monitoring Level {args.level}: {level_descriptions[args.level]}{Style.RESET_ALL}\n"
        )

        monitor.mysql_config.update(
            {
                "host": args.host,
                "user": args.user,
                "password": args.password,
                "port": args.port,
            }
        )

        filename = monitor.generate_report(enable_tables=args.enable_tables)
        print(f"\n{Fore.GREEN}[✓] Report saved to: {filename}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Monitoring completed.{Style.RESET_ALL}\n")

    except Exception as e:
        print(f"\n{Fore.RED}[✗] Execution error: {str(e)}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
