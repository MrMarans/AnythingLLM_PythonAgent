// handler.js
const { spawn } = require('child_process');
const path = require('path');

async function tryPythonCommand(command, script, input, introspectFn) {
    return new Promise((resolve, reject) => {
        try {
            const process = spawn(command, ['-u', script, input]);
            
            process.on('error', (error) => {
                reject(error);
            });

            // Kurzer Timeout um zu prüfen ob der Prozess startet
            setTimeout(() => {
                if (process.killed === false) {
                    resolve(process);
                }
            }, 100);

        } catch (error) {
            reject(error);
        }
    });
}

async function findPythonCommand() {
    const commands = ['python', 'python3', 'py'];
    const script = path.join(__dirname, 'process.py');
    
    for (const cmd of commands) {
        try {
            const process = await tryPythonCommand(cmd, script, '--version', () => {});
            process.kill();
            return cmd;
        } catch (error) {
            continue;
        }
    }
    throw new Error('No Python interpreter found. Please ensure Python is installed and in PATH');
}

module.exports.runtime = {
    handler: async function ({ input }) {
        // Wenn kein Input gegeben ist, setzen wir einen Standardwert
        if (!input) {
            input = "5";  // Standardwert
            this.introspect("No input provided, using default value: 5");
        }

        let finalResults = null;
        let processFinished = false;

        const result = await (async () => {
            return new Promise(async (resolve, reject) => {
                try {
                    this.introspect(`Starting calculation process with input: ${input}`);
                    
                    // Finde den korrekten Python-Befehl
                    const pythonCommand = await findPythonCommand();
                    this.introspect(`Using Python command: ${pythonCommand}`);
                    
                    const pythonScript = path.join(__dirname, 'process.py');
                    const pythonProcess = spawn(pythonCommand, ['-u', pythonScript, input]);
                    
                    // Timeout nach 30 Sekunden
                    const timeout = setTimeout(() => {
                        if (!processFinished) {
                            pythonProcess.kill();
                            reject(new Error('Process timed out after 30 seconds'));
                        }
                    }, 30000);

                    pythonProcess.stdout.on('data', (data) => {
                        try {
                            const jsonData = JSON.parse(data.toString().trim());
                            
                            // Formatierte Nachricht für introspect
                            let statusMessage = `[${jsonData.status.toUpperCase()}] ${jsonData.message}`;
                            if (jsonData.progress >= 0) {
                                statusMessage += ` (${jsonData.progress}%)`;
                            }
                            
                            // Wenn Zwischenergebnisse vorhanden sind, diese anzeigen
                            if (jsonData.interim_results) {
                                statusMessage += `\nInterim Results:\n`;
                                statusMessage += `Square: ${jsonData.interim_results.square}\n`;
                                statusMessage += `Cube: ${jsonData.interim_results.cube}`;
                            }
                            
                            // Wenn finale Ergebnisse vorhanden sind, diese speichern
                            if (jsonData.results) {
                                finalResults = jsonData.results;
                                statusMessage += `\nFinal Results:\n`;
                                statusMessage += `Input: ${finalResults.input}\n`;
                                statusMessage += `Square: ${finalResults.square}\n`;
                                statusMessage += `Cube: ${finalResults.cube}\n`;
                                statusMessage += `Timestamp: ${finalResults.timestamp}`;
                            }
                            
                            this.introspect(statusMessage);
                            
                        } catch (parseError) {
                            // Falls die Ausgabe kein JSON ist, zeige sie als normalen Text
                            this.introspect(`Output: ${data.toString().trim()}`);
                        }
                    });

                    pythonProcess.stderr.on('data', (data) => {
                        const error = data.toString().trim();
                        this.introspect(`Error: ${error}`);
                    });

                    pythonProcess.on('error', (error) => {
                        clearTimeout(timeout);
                        this.introspect(`Process error: ${error.message}`);
                        reject(error);
                    });

                    pythonProcess.on('close', (code) => {
                        clearTimeout(timeout);
                        processFinished = true;
                        
                        if (code === 0) {
                            if (finalResults) {
                                this.introspect("Process completed successfully!");
                                // Formatiere das Ergebnis als String
                                const resultString = `Calculation completed:\nInput: ${finalResults.input}\nSquare: ${finalResults.square}\nCube: ${finalResults.cube}`;
                                resolve(resultString);
                            } else {
                                this.introspect("Process completed but no results were returned");
                                resolve("Process completed but no results were calculated.");
                            }
                        } else {
                            const errorMsg = `Process exited with code ${code}`;
                            this.introspect(errorMsg);
                            resolve(`Error: ${errorMsg}`);
                        }
                    });

                } catch (error) {
                    this.introspect(`Failed to execute: ${error.message}`);
                    resolve(`Error: Failed to execute - ${error.message}`);
                }
            });
        })();

        return result;
    }
};