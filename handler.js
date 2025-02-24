// handler.js
const { spawn } = require('child_process');
const path = require('path');

module.exports.runtime = {
    handler: async function ({ input }) {
        // Standardwert, falls kein Input
        if (!input) {
            input = "5";
            this.introspect("Using default value: 5");
        }

        let finalResults = null;

        return new Promise((resolve) => {
            try {
                // Python-Prozess starten
                const pythonScript = path.join(__dirname, 'process.py');
                const pythonProcess = spawn('python3', ['-u', pythonScript, input]);

                // Buffer für eingehende Daten
                let dataBuffer = '';

                // Ausgaben von Python verarbeiten
                pythonProcess.stdout.on('data', (data) => {
                    try {
                        // Daten zum Buffer hinzufügen und nach Zeilenumbrüchen splitten
                        dataBuffer += data.toString();
                        const lines = dataBuffer.split('\n');
                        
                        // Alle vollständigen Zeilen verarbeiten
                        for (let i = 0; i < lines.length - 1; i++) {
                            const line = lines[i].trim();
                            if (line) {
                                const jsonData = JSON.parse(line);
                                
                                // Status-Updates anzeigen
                                let message = `[${jsonData.status.toUpperCase()}] ${jsonData.message}`;
                                if (jsonData.progress !== null) {
                                    message += ` (${jsonData.progress}%)`;
                                }
                                
                                // Ergebnisse speichern
                                if (jsonData.results) {
                                    finalResults = jsonData.results;
                                }
                                
                                this.introspect(message);
                            }
                        }
                        
                        // Unvollständige Daten im Buffer behalten
                        dataBuffer = lines[lines.length - 1];
                        
                    } catch (e) {
                        this.introspect(`Parse error: ${e.message}`);
                    }
                });

                // Fehler behandeln
                pythonProcess.stderr.on('data', (data) => {
                    this.introspect(`Error: ${data}`);
                });

                // Prozess-Ende behandeln
                pythonProcess.on('close', (code) => {
                    if (code === 0 && finalResults) {
                        resolve(`Calculation completed: Input=${finalResults.input}, Result=${finalResults.output}`);
                    } else {
                        resolve("Process failed or no results returned");
                    }
                });

            } catch (error) {
                this.introspect(`Error: ${error.message}`);
                resolve(`Failed: ${error.message}`);
            }
        });
    }
};