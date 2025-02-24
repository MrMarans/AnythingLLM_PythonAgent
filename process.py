# process.py
import sys
import time
import json
from datetime import datetime

def output_json(status, message, progress, **kwargs):
    """Helper function to output JSON in a consistent format"""
    output = {
        'status': status,
        'message': message,
        'progress': progress,
        **kwargs
    }
    print(json.dumps(output, ensure_ascii=False))
    sys.stdout.flush()  # Ensure output is sent immediately

def perform_calculation(number):
    """Beispielberechnung: Berechnet Quadrat und Kubik der Eingabezahl"""
    return {
        'square': number ** 2,
        'cube': number ** 3
    }

def main():
    try:
        # Überprüfe Version oder Hilfe-Anfrage
        if len(sys.argv) > 1 and sys.argv[1] in ['--version', '-v', '--help', '-h']:
            print('Python Calculation Process v1.0')
            sys.exit(0)

        # Check if we have input
        if len(sys.argv) < 2:
            raise ValueError("No input value provided")

        # Input als Zahl konvertieren
        try:
            input_value = float(sys.argv[1])
        except ValueError:
            raise ValueError(f"Could not convert input '{sys.argv[1]}' to number")
        
        # Initialisierung
        output_json(
            'started',
            f'Starting calculations with input value: {input_value}',
            0
        )
        time.sleep(0.2)  # Noch kürzere Sleep-Zeit
        
        # Erste Berechnung
        output_json(
            'processing',
            'Performing initial calculations...',
            33
        )
        time.sleep(0.2)
        
        # Zwischenberechnung
        interim_results = perform_calculation(input_value)
        output_json(
            'processing',
            'Intermediate results ready...',
            66,
            interim_results=interim_results
        )
        time.sleep(0.2)
        
        # Finale Berechnung und Ergebnisse
        final_results = {
            **interim_results,
            'input': input_value,
            'timestamp': datetime.now().isoformat()
        }
        
        # Finales Ergebnis
        output_json(
            'completed',
            'Calculations completed successfully!',
            100,
            results=final_results
        )
        
    except Exception as e:
        output_json(
            'error',
            f'Error: {str(e)}',
            -1
        )
        sys.exit(1)

if __name__ == "__main__":
    main()