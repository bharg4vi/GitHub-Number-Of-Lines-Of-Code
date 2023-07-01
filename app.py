import requests

def get_user_languages(username, access_token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch repositories for user '{username}'. Status code: {response.status_code}")
        return {}

    try:
        repos = response.json()
        language_lines = {}

        for repo in repos:
            if "languages_url" not in repo:
                print(f"Invalid response for repository: {repo}")
                continue
                
            language_url = repo["languages_url"]
            language_response = requests.get(language_url, headers=headers)
            
            if language_response.status_code != 200:
                print(f"Failed to fetch languages for repository: {repo['name']}. Status code: {language_response.status_code}")
                continue
                
            languages_data = language_response.json()
            
            for language, lines_of_code in languages_data.items():
                if language in language_lines:
                    language_lines[language] += lines_of_code
                else:
                    language_lines[language] = lines_of_code

        return language_lines

    except ValueError:
        print("Error parsing response JSON.")
        return {}

username = "bhargaviiiii"
access_token = ""
language_lines = get_user_languages(username, access_token)
print(f"The user '{username}' has the following lines of code for each programming language: ")
for language, lines_of_code in language_lines.items():
    print(f"Language: {language} - Lines of Code: {lines_of_code}")
