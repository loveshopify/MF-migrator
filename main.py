import base64
import requests
import json

stagingUrl = 'https://beast-ea.myshopify.com'
stagingAPIKey = '53a07f86b7fa553127cbf94cfa20383f'
stagingAPIPwd = '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'

productionUrl = 'https://beast-health-llc.myshopify.com'
productionAPIKey = '29b511948916a4f65a4774b5fdebd7fa'
productionAPIPwd = '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'

migrationTypes = []

# Migrate products metafields? If not comment out the line below
migrationTypes.append('products')

# Migrate customers metafields? If not comment out the line below

# migrationTypes.append('collections')

# Migrate pages metafields? If not comment out the line below

# migrationTypes.append('pages')

# Migrate customers metafields? If not comment out the line below

# migrationTypes.append('customers')


stagingToken = stagingAPIKey + ':' + stagingAPIPwd
tokenBytes = stagingToken.encode('ascii')
base64_bytes = base64.b64encode(tokenBytes)
stagingToken = base64_bytes.decode('ascii')
stagingToken = 'Basic ' + stagingToken

productionToken = productionAPIKey + ':' + productionAPIPwd
tokenBytes = productionToken.encode('ascii')
base64_bytes = base64.b64encode(tokenBytes)
productionToken = base64_bytes.decode('ascii')
productionToken = 'Basic ' + productionToken

for migrationType in migrationTypes:
    print('Starting ' + migrationType + ' migration:')
    url = stagingUrl + '/admin/api/2020-07/' + migrationType + '.json?limit=250'
    head = {'Authorization': stagingToken}
    ret = requests.get(url, headers=head)
    itemsData = ret.json()
    count = 0
    try:
        for item in itemsData[migrationType]:
            count = count + 1
            itemId = item['id']
            itemHandle = item['handle']
            url = stagingUrl + '/admin/' + migrationType + '/' + str(itemId) + '/metafields.json'
            head = {'Authorization': stagingToken}
            ret = requests.get(url, headers=head)
            metafields = ret.json()
            url =  productionUrl + '/admin/api/2020-07/' + migrationType + '.json'
            head = {'Authorization': productionToken}
            data = {'handle': itemHandle}
            print(itemHandle)
            ret = requests.get(url, headers=head, params=data)
            data = ret.json()
            if(len(data[migrationType])):
                newItemId = data[migrationType][0]['id']
                for metafield in metafields['metafields']:
                    newfield = {"namespace": metafield['namespace'], "key": metafield['key'], "value": metafield['value'], "value_type": metafield['value_type']}
                    url = productionUrl + '/admin/api/2020-07/' + migrationType + '/' + str(newItemId) + '/metafields.json'
                    head = {'Authorization': productionToken, 'Content-Type': 'application/json'}
                    data = {"metafield": newfield}
                    json_str = json.dumps(data)
                    print(url)
                    print(json_str)
                    ret = requests.post(url, headers=head, data=json_str)
                    print(ret.status_code)
        print("\n")
        print("---------------------------------------------------\n")
    except:
        print(itemsData)
