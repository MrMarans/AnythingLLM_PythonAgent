# process.py
import sys
import json
import requests
from googlesearch import search
from bs4 import BeautifulSoup
from prompts import *

Workspace_URL = 'http://192.XXX.XXX.XXX:3001/api/v1/workspace/deine-haupt-ki/chat'
AnythingLLM_api = ""


def send_message_to_agent(status, message, progress=None, **data):
    """Sendet eine JSON-formatierte Nachricht an Node.js"""
    output = {
        'status': status,
        'message': message,
        'progress': progress,
        **data
    }
    print(json.dumps(output))
    sys.stdout.flush()

def ask_llm(user_input):
    """Führt die API-Anfrage durch"""
    
    
    payload = {
        "message": user_input,
        "mode": "chat",
        "sessionId": "identifier-to-partition-chats-by-external-id"
    }
    
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {AnythingLLM_api}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(Workspace_URL, json=payload, headers=headers)
    response.raise_for_status()  # Fehler bei nicht-200 Status
    return response.json()

def main():
    try:
        # debug_file = "debug_results.json"
        user_input = sys.argv[1]
        # 
        
        # # try to load the json here. If there is none:
        # try:
        #     with open(debug_file, 'r', encoding='utf-8') as f:
        #         list_from_good_source = json.load(f)
        #         send_message_to_agent('Loading cached results from file', '', 25)
        # except FileNotFoundError:
            # do all this code:
        send_message_to_agent('Erstelle Variationen der Frage', '', 00)
        prompt = new_search_texts_prompt(user_input)

        response_data = ask_llm(prompt)

        send_message_to_agent('Entpacke mögliche Suchanfragen', '', 25)
        
        json_from_llm = response_data["textResponse"]
        json_from_llm = json.loads(json_from_llm)
        optimized_queries = json_from_llm["optimized_queries"]


        search_results = []
        seen_urls = []
        for search_querie in optimized_queries:

            searchResults = search(search_querie, advanced = True, num_results=15, unique=True, lang="de")
            for result in searchResults:
                if result.url not in seen_urls: 
                    search_results.append({"url": result.url, "title": result.title, "description": result.description, "goodSource": None})
                    seen_urls.append(result.url)
        
        send_message_to_agent(f'Die Qualität der {len(seen_urls)} Quellen wird geprüft. Das dauert etwas.', '', 30)

        is_good_source = ask_llm(is_good_source_prompt(search_results , user_input))

    
        send_message_to_agent('Webseiten werden aufgerufen und der Inhalt wird entnommen', '', 65)
        list_from_good_source = is_good_source["textResponse"] 
        list_from_good_source = json.loads(list_from_good_source)

        # Berechne den Fortschritt zwischen 65% und 80%
        progress_start = 65
        progress_end = 80
        progress_range = progress_end - progress_start
        
        # good_sources = [s for s in list_from_good_source if s["goodSource"] == True]
        progress_per_source = progress_range / len(list_from_good_source) if list_from_good_source else 0
        
        allText = []
        current_progress = progress_start
        
        for source in list_from_good_source:
            if source["goodSource"] == True:
                try:
                    url = source["url"]
                    send_message_to_agent(url, '', current_progress)
                    current_progress += progress_per_source
                    
                    response = requests.get(url)

                    if response.status_code == 200:
    
                        soup = BeautifulSoup(response.text, "html.parser")
        
                        text = soup.get_text(separator="\n", strip=True)
                        source_with_text = {"text": text, "url": url}

                        allText.append(source_with_text)
                except Exception as e:
                    send_message_to_agent('error', f'Fehler bei Webaufruf: {str(e)}')



        send_message_to_agent('Prüfe Token-Anzahl und kürze bei Bedarf', '', 80)
        # Zähle ungefähre Token-Anzahl (ca. 4 Zeichen pro Token)
        total_chars = sum(len(source['text']) for source in allText)
        approx_tokens = total_chars // 4

        if approx_tokens > 80000:
            send_message_to_agent(f'Zu viele Tokens: {approx_tokens}. Entferne überschüssige Quellen.', '', 82)
            # Sortiere Sources nach Länge (kürzeste zuerst)
            allText.sort(key=lambda x: len(x['text']))
            
            filtered_sources = []
            current_tokens = 0
            
            # Füge Sources hinzu, solange wir unter dem Token-Limit bleiben
            for source in allText:
                source_tokens = len(source['text']) // 4
                if current_tokens + source_tokens <= 80000:
                    filtered_sources.append(source)
                    current_tokens += source_tokens
                else:
                    break
            
            send_message_to_agent(f'Reduzierte Anzahl der Quellen von {len(allText)} auf {len(filtered_sources)}', '', 83)
            allText = filtered_sources

        send_message_to_agent('Fasse Webseitendaten zusammen', '', 85)
        output = summarize_webtexts_prompt(allText, user_input)
        # output = ask_llm(sum)

        


        # Ergebnis zurückgeben
        send_message_to_agent('completed', 'Request completed', 100, 
                    results={'input': user_input, 'output': output })
        
    except requests.exceptions.RequestException as e:
        send_message_to_agent('error', f'API request failed: {str(e)}')
        sys.exit(1)
    except Exception as e:
        send_message_to_agent('error', f'Error occurred: {str(e)}')
        sys.exit(1)

if __name__ == "__main__":
    main()