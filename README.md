# Charts Skill Test Runner

Diese Dateien ermöglichen das Testen des Charts-Skills ohne Installation in AnythingLLM.

## Voraussetzungen

- Node.js installiert
- Alle benötigten npm-Pakete installiert (`axios`)

## Installation

```bash
npm install axios
```

## Verwendung

1. Bearbeiten Sie die Testdaten in `test-data.json` nach Ihren Wünschen oder erstellen Sie neue Test-Fälle.

2. Führen Sie den Test-Runner aus:
```bash
node test-runner.js
```

## Test-Daten Format

Die Test-Daten sollten folgendes Format haben:
```json
{
    "type": "line",     // Diagramm-Typ (z.B. "line", "bar", "scatter")
    "dataset": {        // Dataset als Objekt mit Arrays
        "x": [1, 2, 3], // Numerische Arrays
        "y": [10, 20, 30]
    },
    "x": "x",          // X-Achsen-Bezeichner
    "y": "y",          // Y-Achsen-Bezeichner
    "title": "Test Chart" // Titel des Diagramms
}
```

## Anpassung der Tests

Sie können die Test-Daten entweder:
1. Direkt in `test-data.json` bearbeiten
2. Die `testData` Variable in `test-runner.js` ändern
3. Den Test-Runner importieren und mit eigenen Daten aufrufen:

```javascript
const { runTest } = require('./test-runner');
runTest({
    type: "bar",
    dataset: {
        "values": [1, 2, 3],
        "labels": [10, 20, 30]
    },
    x: "labels",
    y: "values",
    title: "Mein Test"
});
```