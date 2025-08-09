import requests
import json
import re
from string import Template

promptTemplate = Template(
        """i would like you to return a json object with the following terrorist groups placed in this json template i have filled out one prop for you as an example, return nothing else:
        {
            "Al-Shabaab": [],
            "Boko Haram": [],
            "Hamas": [],
            "Hezbollah": [],
            "Islamic State (ISIS)": [],
            "Taliban": [],
            "Al-Qaeda and Affiliates": [
                "Al-Qaida",
                "Al-Qaida Kurdish Battalions (AQKB)",
                "Al-Qaida Network for Southwestern Khulna Division",
                "Al-Qaida Organization for Jihad in Sweden",
                "Al-Qaida in Iraq",
                "Al-Qaida in Lebanon",
                "Al-Qaida in Saudi Arabia",
                "Al-Qaida in Yemen",
                "Al-Qaida in the Arabian Peninsula (AQAP)",
                "Al-Qaida in the Indian Subcontinent",
                "Al-Qaida in the Islamic Maghreb (AQIM)"
            ],
            "Basque Separatists": [],
            "Corsican Separatists": [],
            "Irish Republican Groups": [],
            "Kurdish Groups": [],
            "Other Nationalist/Separatist Groups": [],
            "Communist/Left-Wing Groups": [],
            "Right-Wing/Neo-Nazi Groups": [],
            "Other Ideological Groups": [],
            "Gangs": [],
            "Guerrilla forces": [],
            "Miscellaneous": []
        }

        The groups to be placed in the template:
        $groups
        """)

def loadGroupNames(filePath):
    with open(filePath, 'r') as file:
        return json.load(file)

def genResponse(session, batch):
    prompt = promptTemplate.substitute(groups='\n'.join(batch))
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "dolphin3",
        "prompt": prompt,
        "keep_alive": "5m",
        "stream": False
    }

    response = session.post(url, json=data)
    if response.status_code == 200:
        # print(response.json()['response'])
        parsed = parseJson(response.json()['response'])
        return parsed

    else:
        return f"Error: {response.status_code}, {response.text}"
    
def parseJson(s):
    s_clean = s.strip()
    # mode often puts ```json at the start and end of the json blocks
    s_clean = re.sub(r'```(?:json)?\s*', '', s_clean)
    s_clean = s_clean.replace('```', '')
    start = s_clean.find('{')
    end = s_clean.rfind('}')
    jsonObject = s_clean[start:end+1]

    try:
        return json.loads(jsonObject)
    except json.JSONDecodeError:
        pass

def main():
    BATCH_SIZE = 10
    filePath = "../src/lib/data/groupNames.json"
    groupNames = loadGroupNames(filePath)
    session = requests.Session()

    categorised = {
            "Al-Shabaab": [],
            "Boko Haram": [],
            "Hamas": [],
            "Hezbollah": [],
            "Islamic State (ISIS)": [],
            "Taliban": [],
            "Al-Qaeda and Affiliates": [
                "Al-Qaida",
                "Al-Qaida Kurdish Battalions (AQKB)",
                "Al-Qaida Network for Southwestern Khulna Division",
                "Al-Qaida Organization for Jihad in Sweden",
                "Al-Qaida in Iraq",
                "Al-Qaida in Lebanon",
                "Al-Qaida in Saudi Arabia",
                "Al-Qaida in Yemen",
                "Al-Qaida in the Arabian Peninsula (AQAP)",
                "Al-Qaida in the Indian Subcontinent",
                "Al-Qaida in the Islamic Maghreb (AQIM)"
            ],
            "Basque Separatists": [],
            "Corsican Separatists": [],
            "Irish Republican Groups": [],
            "Kurdish Groups": [],
            "Other Nationalist/Separatist Groups": [],
            "Communist/Left-Wing Groups": [],
            "Right-Wing/Neo-Nazi Groups": [],
            "Other Ideological Groups": [],
            "Gangs": [],
            "Guerrilla forces": [],
            "Miscellaneous": []
        }

    response = genResponse(session, groupNames[0:BATCH_SIZE])
    for key in response:
        if response[key]:
            categorised[key].extend(response[key])

    print(categorised)
    # for i in range(0, len(groupNames), BATCH_SIZE):
    #     response = genResponse(groupNames[i:i + BATCH_SIZE])

main()