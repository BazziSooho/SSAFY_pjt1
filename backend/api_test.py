import json
import requests


api_url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
api_key = '1c1cffc2a23cbe61a88b8ea749f7a10a'

params = {
    'auth': api_key,
    'topFinGrpNo': '020000',
    'pageNo': '1',
}

response = requests.get(api_url, params=params)
data = response.json()
print(data)

# # print(data['result']['baseList'])
savings = data['result']['baseList']
saving_list = []

for saving in savings:
    new_data = {"model": "savings.savingproduct"}
    new_data['fields'] = saving
    saving_list.append(new_data)
print(saving_list)

rate_list = []
rates = data['result']['optionList']
for rate in rates:
    rate_data = {"model": "savings.productinterest"}
    rate_data['fields'] = rate
    rate_list.append(rate_data)
print(rate_list)


# with open('saving_product.json', 'w', encoding='UTF-8') as m:
#     json.dump(new_list, m, ensure_ascii=False, indent=2)