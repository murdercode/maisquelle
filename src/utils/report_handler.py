# src/monitor/report_handler.py

import json
import os
from datetime import datetime, date
from typing import Dict, Any


class ReportHandler:
    """Class for handling system and MySQL monitoring reports"""

    def __init__(self, output_dir: str = 'logs'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _convert_to_serializable(self, data: Any) -> Any:
        """Convert non-serializable objects to serializable format"""
        if hasattr(data, '_asdict'):  # Handle namedtuples
            return dict(data._asdict())
        elif hasattr(data, '__dict__'):  # Handle custom objects
            return dict(data.__dict__)
        elif isinstance(data, (datetime, date)):  # Handle datetime objects
            return data.isoformat()
        elif isinstance(data, bytes):  # Handle bytes
            return data.decode('utf-8')
        elif isinstance(data, (int, float, str, bool, type(None))):
            return data
        elif isinstance(data, (list, tuple)):
            return [self._convert_to_serializable(item) for item in data]
        elif isinstance(data, dict):
            return {str(k): self._convert_to_serializable(v) for k, v in data.items()}
        else:
            return str(data)

    def prepare_report_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare and structure the report data"""
        timestamp = datetime.now()

        report_data = {
            "metadata": {
                "timestamp": timestamp.isoformat(),
                "report_version": "1.0"
            },
            "data": self._convert_to_serializable(data)
        }

        return report_data

    def save_report(self, report_data: Dict[str, Any], report_type: str = 'status') -> str:
        """
        Save the report in JSON format

        Args:
            report_data: Dictionary containing the report data
            report_type: Type of report (default: 'status')

        Returns:
            str: Path to the saved report file
        """
        structured_data = self.prepare_report_data(report_data)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_type}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        # Save as JSON with proper formatting
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=2, ensure_ascii=False)

        return filepath

    def load_report(self, filepath: str) -> Dict[str, Any]:
        """
        Load a report from a JSON file

        Args:
            filepath: Path to the report file

        Returns:
            dict: The report data
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
