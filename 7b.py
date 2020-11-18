from __future__ import print_function

import base64
import json

print('Loading function')


def lambda_handler(event, context):
    output = []

    for record in event['records']:
        print(record['recordId'])
        payload = base64.b64decode(record['data'])
        
        # Do custom processing on the payload here
        
        pythonPayload = json.loads(payload)
        if pythonPayload.get('total_amount', 0) < 5:
            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': base64.b64encode(payload)
            }
            output.append(output_record)
        
        

        

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}
