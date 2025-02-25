# Python Agent Skill Base Project

This is a base project that demonstrates how to execute Python code within AnythingLLM agent skills. It provides a basic structure for running Python scripts and handling communication between Node.js and Python.

## Project Structure

- `handler.js` - The main Node.js handler that executes Python code
- `process.py` - Example Python script showing the basic structure
- `plugin.json` - Plugin configuration for AnythingLLM

## How to Use This Template

1. **Setup**
   - Copy this project folder to your AnythingLLM agent skills directory
   - Rename the folder to your desired skill name
   - Update `plugin.json` with your skill's details

2. **Modifying the Python Script**
   - Open `process.py`
   - The script uses a simple communication protocol with Node.js:
   ```python
   def send_message_to_agent(status, message, progress=None, **data):
       output = {
           'status': status,
           'message': message,
           'progress': progress,
           **data
       }
       print(json.dumps(output))
       sys.stdout.flush()
   ```
   - Use this function to send updates and data back to Node.js
   - Implement your Python logic in the `main()` function

3. **Handler Configuration**
   - The `handler.js` file manages Python process execution
   - It captures Python output and parses JSON messages
   - Progress updates are shown through `this.introspect()`
   - Results are returned via the promise resolution

4. **Input/Output**
   - Input is passed as command line argument to Python
   - Output should be JSON-formatted strings
   - Use the `send_message_to_agent` function for all communication

## Example Usage

1. **Basic Progress Updates**
   ```python
   send_message_to_agent('status', 'Processing started', 0)
   # Your code here
   send_message_to_agent('status', 'Step 1 complete', 50)
   # More code
   send_message_to_agent('completed', 'All done', 100, results={'data': 'your_result'})
   ```

2. **Error Handling**
   ```python
   try:
       # Your code
   except Exception as e:
       send_message_to_agent('error', f'Error occurred: {str(e)}')
       sys.exit(1)
   ```

## Plugin Configuration

Update the `plugin.json` with your skill's details:
```json
{
  "name": "Your Skill Name",
  "description": "Your skill description",
  "schema": "skill-1.0.0",
  "version": "1.0.0",
  "entrypoint": {
    "file": "handler.js",
    "params": {
      "input": {
        "description": "Input description",
        "type": "string"
      }
    }
  }
}
```

## Testing

To test your skill:
1. Place it in the AnythingLLM agent skills directory
2. Restart the agent to reload it completly
3. Use the skill through the AnythingLLM interface

## Notes

- Make sure Python 3.x is installed on your system
- Keep the communication protocol (JSON messages) intact
- Handle all exceptions appropriately
- Use progress updates to show status
- Clean up resources in your Python script

- If you are using any pip packages for python, you need to add them to the Dockerfile (if you are using Docker), else AnythingLLM cant access those packages. In case of requests, bs4 and googlesearch-python, use this:
```json
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install requests bs4 googlesearch-python && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

```
This template provides a foundation for building Python-based agent skills. You can extend it by adding more functionality while maintaining the basic communication structure between Node.js and Python.