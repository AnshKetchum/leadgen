import requests
company = "openai"
response = requests.get(
    f'https://autocomplete.clearbit.com/v1/companies/suggest?query={company}')
data = response.json()
if len(data) > 0:
    domain = data[0]['domain']
    print(domain)
else:
    print(f'No domain found for {company}')