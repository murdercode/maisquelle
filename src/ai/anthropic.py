# src/ai/anthropic.py

from anthropic import Anthropic
from typing import Dict, List, Optional
import json
from colorama import Fore, Style


class AnthropicHandler:
    def __init__(self, api_key: str):
        """Initialize Anthropic client with API key."""
        self.client = Anthropic(api_key=api_key)
        self.system_prompt = """
Analizza i seguenti log e metriche di monitoraggio MySQL e genera una risposta in formato JSON contenente i comandi da eseguire. 
Considera attentamente:
- Performance metrics
- Query cache statistics
- System resources
- InnoDB metrics
- MySQL processes and status
- Slow queries
- Table statistics (if available)

OUTPUT RICHIESTO:
Genera un oggetto JSON che contenga:
1. Una lista di comandi da eseguire per ottimizzare il sistema
2. La priorità di ogni comando (alta, media, bassa)
3. Il servizio target per ogni comando
4. Eventuali parametri necessari per l'esecuzione
5. Una breve descrizione della motivazione del comando
"""

    def _format_monitoring_data(self, data: Dict) -> str:
        """Format monitoring data for the prompt."""
        return json.dumps(data, indent=2)

    def analyze_report(self, monitoring_data: Dict) -> Optional[List[Dict]]:
        """
        Send monitoring data to Anthropic for analysis and return optimization commands.
        """
        try:
            formatted_data = self._format_monitoring_data(monitoring_data)

            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                temperature=0,
                system=self.system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"Analizza questi dati di monitoraggio MySQL e suggerisci comandi di ottimizzazione:\n{formatted_data}"
                }]
            )

            # Parse the JSON response
            try:
                response = json.loads(message.content[0].text)
                return response.get("commands", [])
            except json.JSONDecodeError as e:
                print(f"{Fore.RED}[✗] Errore nel parsing della risposta JSON: {str(e)}{Style.RESET_ALL}")
                return None

        except Exception as e:
            print(f"{Fore.RED}[✗] Errore nella comunicazione con Anthropic: {str(e)}{Style.RESET_ALL}")
            return None

    def process_commands_interactively(self, commands: List[Dict]) -> List[Dict]:
        """
        Process commands interactively, asking user confirmation for each.
        Returns list of approved commands.
        """
        if not commands:
            print(f"{Fore.YELLOW}[!] Nessun comando di ottimizzazione suggerito.{Style.RESET_ALL}")
            return []

        approved_commands = []

        print(f"\n{Fore.CYAN}[*] Comandi di ottimizzazione suggeriti:{Style.RESET_ALL}")

        for cmd in commands:
            print("\n" + "=" * 50)
            print(f"{Fore.WHITE}Comando ID: {cmd['id']}{Style.RESET_ALL}")
            print(f"Azione: {cmd['action']}")
            print(
                f"Priorità: {Fore.RED if cmd['priority'] == 'high' else Fore.YELLOW if cmd['priority'] == 'medium' else Fore.GREEN}{cmd['priority']}{Style.RESET_ALL}")
            print(f"Servizio Target: {cmd['target_service']}")
            print(f"Parametri: {json.dumps(cmd['parameters'], indent=2)}")
            print(f"Motivazione: {cmd['rationale']}")

            while True:
                choice = input(f"\n{Fore.CYAN}Eseguire questo comando? (Y/N): {Style.RESET_ALL}").strip().upper()
                if choice in ['Y', 'N']:
                    break
                print(f"{Fore.YELLOW}Per favore, inserisci Y o N.{Style.RESET_ALL}")

            if choice == 'Y':
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
                print(f"\n{Fore.WHITE}Esecuzione comando {cmd['id']}: {cmd['action']}{Style.RESET_ALL}")
                # Qui implementare la logica di esecuzione effettiva dei comandi
                # Per esempio:
                # if cmd['action'] == 'optimize_table':
                #     optimize_table(cmd['parameters']['table_name'])
                # elif cmd['action'] == 'adjust_buffer_pool':
                #     adjust_buffer_pool(cmd['parameters']['size'])
                # ...
                print(f"{Fore.GREEN}[✓] Comando eseguito con successo{Style.RESET_ALL}")

            except Exception as e:
                print(f"{Fore.RED}[✗] Errore nell'esecuzione del comando {cmd['id']}: {str(e)}{Style.RESET_ALL}")