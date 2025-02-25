# process.py
import sys
import json
import requests
from googlesearch import search
from bs4 import BeautifulSoup

def new_search_texts_prompt(user_input):
    # """Erstelle Variationssuchen für Google Suche"""
    examples = """
        {
        "original_question": "Was sind die Auswirkungen von Klimawandel auf die Biodiversität?",
        "optimized_queries": [
            "Klimawandel Biodiversität Auswirkungen wissenschaftliche Studien",
            "Einfluss des Klimawandels auf die Artenvielfalt Forschung",
            "Wissenschaftliche Erkenntnisse zu Klimawandel und Biodiversität"
        ]
        },
        {
        "original_question": "Wie beeinflusst Stress die menschliche Gesundheit?",
        "optimized_queries": [
            "Einfluss von Stress auf die Gesundheit wissenschaftliche Analysen",
            "Stress und Gesundheit: Auswirkungen auf den menschlichen Körper",
            "Wissenschaftliche Studien zu Stress und Gesundheitsrisiken"
        ]
        },
        {
        "original_question": "Was sind die Vorteile der Meditation für das Gehirn?",
        "optimized_queries": [
            "Wissenschaftliche Vorteile von Meditation für das Gehirn",
            "Meditation und neuronale Veränderungen: Forschungsergebnisse",
            "Einfluss von Meditation auf die Gehirnfunktion Studien"
        ]
        },
        {
        "original_question": "Wie wirkt sich Ernährung auf psychische Gesundheit aus?",
        "optimized_queries": [
            "Ernährung und psychische Gesundheit: Wissenschaftliche Erkenntnisse",
            "Einfluss der Ernährung auf die psychische Gesundheit Forschung",
            "Zusammenhang zwischen Ernährung und psychischer Gesundheit Studien"
        ]
        },
        {
        "original_question": "Welche Rolle spielt Genetik bei der Krankheitsentwicklung?",
        "optimized_queries": [
            "Genetik und Krankheitsentwicklung: Wissenschaftliche Perspektiven",
            "Einfluss genetischer Faktoren auf die Krankheitsentwicklung Forschung",
            "Genetik und Erbkrankheiten: Aktuelle wissenschaftliche Studien"
        ]
        }
    """

    form = """{
        "original_question": "Gefrage Frage",
        "optimized_queries": [
            "Variation 1",
            "Variation 2",
            "Variation 3"
        ]
        }"""

    prompt = f"""
        Vergiss alle vorherhigen prompts und chat Historien.
        Du bist spezialist für die Google Suche und SEO. Du weißt genau, wie man mit welchen Anfragen auf sein Ziel kommt. Du kannst die normalste
        Information, die nach jemand sucht, in perfekt optimierte Google Suchbegriffe verarbeiten.
        Deine Aufgabe ist es, eine Frage unter anderem so umzustellen, dass sie in Google die besten Ergebnisse liefert.
        
        
        Hier hast du einige Beispiele für die erwartete Ausgabe: 
        {examples}

        wie du sehen kannst, will ich einzig und allein eine json Ausgabe haben. Du sollst sonst keine Texte erstellen. Nur eine json in diesem Format soll ausgegeben werden:
        {form}

        Erstelle, nachdem du nun tief luft genommen hast, Variationen für die nachfolgende Frage:
        {user_input}
    """

    return prompt


def is_good_source_prompt(results_array, question):
    examples = """[
    {
        "url": "https://www.lv1871.de/magazin/gesundheit/muell-vermeiden/",
        "title": "Müll vermeiden im Haushalt: 25 effektive Tipps - LV 1871",
        "description": "25 Tipps zur Müllvermeidung im Haushalt",
        "goodSource": true
    },
    {
        "url": "https://www.duh.de/aktuell/nachrichten/aktuelle-meldung/recycling-leichtgemacht-6-tipps-und-tricks-zur-muelltrennung/",
        "title": "Recycling leichtgemacht: 6 Tipps und Tricks zur Mülltrennung",
        "description": "18.03.2019  ·  Für ein optimales Recyclingergebnis sollten Deckel und Verpackung getrennt im Gelben Sack entsorgt werden. Dasselbe gilt für Papierbandrollen...",
        "goodSource": false
    },
    {
        "url": "https://utopia.de/ratgeber/muelltrennung-recycling_37038/",
        "title": "Mülltrennung: So geht richtiges Recyceln - Utopia",
        "description": "19.06.2024  ·  Gelbe Tonne und gelber Sack sollen helfen, Abfallmengen langfristig zu verringern, die Mülldeponierung abzuschaffen und Wertstoffe angemessen...",
        "goodSource": true
    }
    ]"""
    
    prompt = f"""
    Du vergisst alle vorherigen Chats und Nachrichtenprompts. 
    Du bist langjähriger wissenschaftler und hast eine Menge Erfahrung bei der Suche nach richtigen Quellen. Du hast einige
    Suchergebnisse gefunden, hast deren Webseite, URL und BEschreibungen. Du kannst die Qualität der Quellen anhand dieser Informationen bewerten und suchst
    daher aus, welche Quellen zu der Frage passen. 

    Deine Aufgabe ist es, diese Quellen nun zu bewerten, ob die für eine Recherche zu der jeweiligen Frage passt.
    Die Frage ist folgende: {question} 
    
    Hier sind die möglichen Quellen: {results_array}

    Deine Aufgabe ist es nun, eine solche Liste zu bewerten und die Quellen zu markieren. Du musst hierfür in der Liste der Quellen den Wert "goodSource" umwandeln in true oder false.
    Wenn die Quelle gut ist, danns setze es auf true. Wenn nicht, dann auch false. 
    Du musst die Liste der Quellen ansonsten genau so wieder zurück geben.  Hier ist ein kleines Beispiel, wie das aussehen kann:
    {examples}


"""
    return prompt

def summarize_webtexts_prompt(texts, question):
    prompt = f"""
    Vergiss alle vorherigen Anweisungen. Du bist experte für die Zusammenfassung von Texten. Du hast eine Menge Texte und wirst die Inhalte nun so zusammen fassen, damit die 
    gestellte Frage so gut wie möglich beantwortet werden kann. 

    Deine Antwort ist immer in Markdown und du stellt, soweit du eine Information wiedergibst, diese mit der Quelle dar.
    Wenn du also etwas aus einem Text zusammen fasst, dann machst du das mit Markdown folgendermaßen:

    **[Dein zusammengefasster Text](https://www.der-link-woher-du-die-Information-hast.de)**

    Dadurch sind die jeweiligen Texte immer mit der Quelle verlinkt. 

    Die Frage, die der Nutzer gestellt hat:
    {question}
    Nun folgen die Texte mit Quellen: 
    {texts}

    """


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
    url = 'http://192.168.80.35:3001/api/v1/workspace/deine-haupt-ki/chat'
    
    payload = {
        "message": user_input,
        "mode": "chat",
        "sessionId": "identifier-to-partition-chats-by-external-id"
    }
    
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer XHPMBWW-20VMQRB-NS2D1GQ-BE3246J',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Fehler bei nicht-200 Status
    return response.json()

def main():
    try:
        user_input = sys.argv[1]
        
        send_message_to_agent('Frage KI nach möglichen Variationen der Google Anfrage', '', 00)
        prompt = new_search_texts_prompt(user_input)

        response_data = ask_llm(prompt)

        
        
        send_message_to_agent('Entpacke mögliche Suchanfragen', '', 25)
        
        json_from_llm = response_data["textResponse"]
        json_from_llm = json.loads(json_from_llm)
        optimized_queries = json_from_llm["optimized_queries"]


        search_results = []
        for search_querie in optimized_queries:

            searchResults = search(search_querie, advanced = True, num_results=25, unique=True, lang="de")
            for result in searchResults:

                search_results.append({"url": result.url, "title": result.title, "description": result.description, "goodSource": None})

        send_message_to_agent('Entscheidung der Quellenauswahl anhand der Frage. Das kann eine Weile dauern.', '', 30)



        is_good_source =ask_llm(is_good_source_prompt(search_results , user_input))
        # is_good_source = search_results
        print(is_good_source)
        send_message_to_agent('Die Webseiten werden geladen', '', 65)
        allText = []
        debug = True
        list_from_good_source = is_good_source["textResponse"] 
        for source in  list_from_good_source:
            print(f"the source is: {source}")
            if source["goodSource"] == True or debug==True:
                # print(source["url"])
                url = source["url"]
                send_message_to_agent(url, '', 70)
                response = requests.get(url)
                print(url)
                if response.status_code == 200:
                    print(response)
                    # HTML-Inhalt parsen
                    soup = BeautifulSoup(response.text, "html.parser")
                    print(f"soup is {soup}")
                    # Nur den sichtbaren Text extrahieren
                    text = soup.get_text(separator="\n", strip=True)
                    source_with_text = {"text": text, "url": url}
                    print(f"texts of sources are: {source_with_text}")
                    allText.append(source_with_text)

        send_message_to_agent('Fasse Webseitendaten zusammen', '', 85)
        output = ask_llm(summarize_webtexts_prompt(allText, user_input))

        


        # Ergebnis zurückgeben
        send_message_to_agent('completed', 'Request completed', 100, 
                    results={'input': user_input, 'output': output})
        
    except requests.exceptions.RequestException as e:
        send_message_to_agent('error', f'API request failed: {str(e)}')
        sys.exit(1)
    except Exception as e:
        send_message_to_agent('error', f'Error occurred: {str(e)}')
        sys.exit(1)

if __name__ == "__main__":
    main()