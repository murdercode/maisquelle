import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from anthropic import Anthropic
from colorama import Fore, Style


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling datetime objects."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class AnthropicHandler:
    def __init__(self, api_key: str):
        """Initialize Anthropic client with API key string."""
        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)
        self.system_prompt = """
Analizza i seguenti log e metriche di monitoraggio MySQL e genera una risposta in formato JSON contenente i comandi da eseguire.
Per ogni comando, specifica:
- action: l'azione da eseguire
- priority: priorità (high, medium, low)
- target_service: il servizio target
- parameters: parametri necessari per l'esecuzione
- rationale: motivazione del comando

Esempio di formato risposta:
{
    "commands": [
        {
            "action": "optimize_table",
            "priority": "high",
            "target_service": "mysql",
            "parameters": {
                "table_name": "users",
                "operation": "analyze"
            },
            "rationale": "La tabella mostra segni di frammentazione"
        }
    ]
}

Analizza attentamente:
- Performance metrics
- Query cache statistics
- System resources
- InnoDB metrics
- MySQL processes and status
- Slow queries
- Table statistics (if available)
"""

    def _format_monitoring_data(self, data: Dict) -> str:
        """Format monitoring data for the prompt using custom JSON encoder."""
        try:
            return json.dumps(data, indent=2, cls=DateTimeEncoder)
        except Exception as e:
            print(
                f"{Fore.YELLOW}[!] Errore nella formattazione dei dati: {str(e)}{Style.RESET_ALL}"
            )
            sanitized_data = self._sanitize_data(data)
            return json.dumps(sanitized_data, indent=2)

    def _sanitize_data(self, data):
        """Recursively sanitize data to ensure JSON serialization."""
        if isinstance(data, dict):
            return {key: self._sanitize_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        elif isinstance(data, (datetime,)):
            return data.isoformat()
        elif isinstance(data, (int, float, str, bool, type(None))):
            return data
        else:
            return str(data)

    def _process_ai_response(self, response_text: str) -> List[Dict]:
        """Process and validate AI response, ensuring all required fields are present."""
        try:
            # Parse the JSON response
            response_data = json.loads(response_text)

            # Extract commands from response
            if isinstance(response_data, dict):
                commands = response_data.get("commands", [])
            elif isinstance(response_data, list):
                commands = response_data
            else:
                commands = []

            # Validate and fix each command
            processed_commands = []
            for cmd in commands:
                if isinstance(cmd, dict):
                    # Ensure all required fields are present
                    processed_cmd = {
                        "id": cmd.get("id", str(uuid.uuid4())[:8]),
                        "action": cmd.get("action", "unknown_action"),
                        "priority": cmd.get("priority", "medium"),
                        "target_service": cmd.get("target_service", "mysql"),
                        "parameters": cmd.get("parameters", {}),
                        "rationale": cmd.get("rationale", "No rationale provided"),
                    }
                    processed_commands.append(processed_cmd)

            return processed_commands

        except json.JSONDecodeError as e:
            print(
                f"{Fore.RED}[✗] Errore nel parsing della risposta JSON: {str(e)}{Style.RESET_ALL}"
            )
            return []
        except Exception as e:
            print(
                f"{Fore.RED}[✗] Errore nell'elaborazione della risposta: {str(e)}{Style.RESET_ALL}"
            )
            return []

    def analyze_report(self, monitoring_data: Dict) -> Optional[List[Dict]]:
        """
        Send monitoring data to Anthropic for analysis and return optimization commands.
        """
        try:
            formatted_data = self._format_monitoring_data(monitoring_data)

            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                temperature=0,
                system=self.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Analizza questi dati di monitoraggio MySQL e suggerisci comandi di ottimizzazione:\n{formatted_data}",
                    }
                ],
            )

            # Process the response using the new handler
            commands = self._process_ai_response(response.content[0].text)
            return commands if commands else None

        except Exception as e:
            print(
                f"{Fore.RED}[✗] Errore nella comunicazione con Anthropic: {str(e)}{Style.RESET_ALL}"
            )
            return None

    def process_commands_interactively(self, commands: List[Dict]) -> List[Dict]:
        """
        Process commands interactively, asking user confirmation for each.
        Returns list of approved commands.
        """
        if not commands:
            print(
                f"{Fore.YELLOW}[!] Nessun comando di ottimizzazione suggerito.{Style.RESET_ALL}"
            )
            return []

        approved_commands = []

        print(f"\n{Fore.CYAN}[*] Comandi di ottimizzazione suggeriti:{Style.RESET_ALL}")

        for cmd in commands:
            print("\n" + "=" * 50)
            print(f"{Fore.WHITE}Comando ID: {cmd['id']}{Style.RESET_ALL}")
            print(f"Azione: {cmd['action']}")
            print(
                f"Priorità: {Fore.RED if cmd['priority'] == 'high' else Fore.YELLOW if cmd['priority'] == 'medium' else Fore.GREEN}{cmd['priority']}{Style.RESET_ALL}"
            )
            print(f"Servizio Target: {cmd['target_service']}")
            print(f"Parametri: {json.dumps(cmd['parameters'], indent=2)}")
            print(f"Motivazione: {cmd['rationale']}")

            while True:
                choice = (
                    input(
                        f"\n{Fore.CYAN}Eseguire questo comando? (Y/N): {Style.RESET_ALL}"
                    )
                    .strip()
                    .upper()
                )
                if choice in ["Y", "N"]:
                    break
                print(f"{Fore.YELLOW}Per favore, inserisci Y o N.{Style.RESET_ALL}")

            if choice == "Y":
                approved_commands.append(cmd)
                print(f"{Fore.GREEN}[✓] Comando approvato{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] Comando saltato{Style.RESET_ALL}")

        return approved_commands

    def execute_approved_commands(self, approved_commands: List[Dict]) -> None:
        """
        Execute the approved commands.
        This is a placeholder - implement actual command execution logic based on your needs.
        """
        if not approved_commands:
            return

        print(f"\n{Fore.CYAN}[*] Esecuzione dei comandi approvati...{Style.RESET_ALL}")

        for cmd in approved_commands:
            try:
                print(
                    f"\n{Fore.WHITE}Esecuzione comando {cmd['id']}: {cmd['action']}{Style.RESET_ALL}"
                )
                # Implement command execution logic here
                print(f"{Fore.GREEN}[✓] Comando eseguito con successo{Style.RESET_ALL}")

            except Exception as e:
                print(
                    f"{Fore.RED}[✗] Errore nell'esecuzione del comando {cmd['id']}: {str(e)}{Style.RESET_ALL}"
                )
