# process.py
import sys
import json
import time

def send_message(status, message, progress=None, **data):
    """Sendet eine JSON-formatierte Nachricht an Node.js"""
    output = {
        'status': status,
        'message': message,
        'progress': progress,
        **data
    }
    print(json.dumps(output))  # Eine Nachricht pro Zeile
    sys.stdout.flush()  # Sofortiges Flushen
    time.sleep(0.2)  # Kurze Pause zwischen Nachrichten

def calculate(value):
    """Beispiel-Berechnung"""
    return value * 2

def main():
    try:
        # Input verarbeiten
        input_value = float(sys.argv[1])
        
        # Start-Status
        send_message('started', 'Starting calculation', 0)
        
        # Erste Phase
        send_message('processing', 'Validating input...', 25)
        
        # Zweite Phase
        send_message('processing', 'Performing calculation...', 50)
        result = calculate(input_value)
        
        # Dritte Phase
        send_message('processing', 'Preparing results...', 75)
        
        # Ergebnis
        send_message('completed', 'Calculation finished', 100, 
                    results={'input': input_value, 'output': result})
        
    except Exception as e:
        send_message('error', str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()