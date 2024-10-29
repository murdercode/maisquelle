# src/monitor/system_monitor.py

from datetime import datetime
from typing import Dict, Any

import psutil
from colorama import Fore, Style


class SystemMonitor:
    """
    System resource monitoring class.
    Handles collection of CPU, RAM, SWAP, and Disk metrics.
    """

    def __init__(self, disk_path: str = "/"):
        """
        Initialize SystemMonitor

        Args:
            disk_path: Path to monitor for disk metrics
        """
        self.disk_path = disk_path

    def get_system_resources(self) -> Dict[str, Any]:
        """
        Monitor and collect all system resources

        Returns:
            Dictionary containing all system metrics

        Raises:
            Exception: If error occurs during data collection
        """
        try:
            print(f"{Fore.WHITE}[*] Collecting system data...")

            # CPU metrics
            print(f"{Fore.WHITE}  └─ Collecting CPU data...", end='')
            cpu_data = self._get_cpu_metrics()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # RAM metrics
            print(f"{Fore.WHITE}  └─ Collecting RAM data...", end='')
            ram_data = self._get_ram_metrics()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # SWAP metrics
            print(f"{Fore.WHITE}  └─ Collecting SWAP data...", end='')
            swap_data = self._get_swap_metrics()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            # Disk metrics
            print(f"{Fore.WHITE}  └─ Collecting DISK data...", end='')
            disk_data = self._get_disk_metrics()
            print(f"{Fore.GREEN} Completed{Style.RESET_ALL}")

            return {
                'cpu': cpu_data,
                'ram': ram_data,
                'swap': swap_data,
                'disk': disk_data,
                'timestamp': datetime.now()
            }

        except Exception as e:
            print(f"{Fore.RED} Error: {str(e)}{Style.RESET_ALL}")
            raise

    def _get_cpu_metrics(self) -> Dict[str, Any]:
        """Get CPU specific metrics"""
        return {
            'percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(),
            'freq': psutil.cpu_freq()
        }

    def _get_ram_metrics(self) -> Any:
        """Get RAM specific metrics"""
        return psutil.virtual_memory()

    def _get_swap_metrics(self) -> Any:
        """Get SWAP specific metrics"""
        return psutil.swap_memory()

    def _get_disk_metrics(self) -> Any:
        """Get Disk specific metrics"""
        return psutil.disk_usage(self.disk_path)
