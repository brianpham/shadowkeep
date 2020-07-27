import requests
import json
requests.packages.urllib3.disable_warnings()

loki_address = <loki_address>
# job = "hosted-california"
# instanceId = "i-014d62354ae91fb91"

customer_name = demisto.args().get('customer_name', None)
customer_serial_number = demisto.args().get('serial_number', None)
aws_region = demisto.args().get('aws_region', None).lower()
# job = f'hosted-{aws_region}'

def aws_region_translator(aws_region):
    choices = {
            'virginia': 'us-east-1',
            'ohio': 'us-east-2',
            'california': 'us-west-1',
            'oregon': 'us-west-2',
            'canada': 'ca-central-1',
            'frankfurt': 'eu-central-1',
            'ireland': 'eu-west-1',
            'london': 'eu-west-2',
            'paris': 'eu-west-3',
            'tokyo': 'ap-northeast-1',
            'seoul': 'ap-northeast-2',
            'singapore': 'ap-southeast-1',
            'sydney': 'ap-southeast-2',
            'mumbai': 'ap-south-1',
            'sao paulo': 'sa-east-1',
            }
    return choices.get(aws_region)

def checkCustomerLocation():

    if customer_name is not None:
        ## Customer has a name tag
        newHostedCustomer = False
        return newHostedCustomer
    else:
        ## Customer only has serialnumber tag
        newHostedCustomer = True
        return newHostedCustomer

def get_instance_details(getRegion, customerLocation):
    if customerLocation == False:
        instanceDetails = demisto.executeCommand("aws-ec2-describe-instances", { "region": getRegion, "filters": f'Name=tag:Customer,Values={customer_name}', 'using': 'demisto-hosted-customers-old' })
        instanceId = instanceDetails[0]['Contents']['AWS.EC2.Instances(val.InstanceId === obj.InstanceId)'][0]['InstanceId']
        return instanceId
    elif customerLocation == True:
        instanceDetails = demisto.executeCommand("aws-ec2-describe-instances", { "region": getRegion, "filters": f'Name=tag:Name,Values={customer_serial_number}-prod', 'using': 'demisto-hosted-customers' })
        instanceId = instanceDetails[0]['Contents']['AWS.EC2.Instances(val.InstanceId === obj.InstanceId)'][0]['InstanceId']
        return instanceId

def get_journal_logs(instanceId, jobId):
    payload = {
            'query': f'{{job="{jobId}"}} |= "{instanceId}" |= "journalctl" |= "error" |= "demisto.service"',
            'direction': 'BACKWARD',
            'start': '1594768247731911000',
            'end': '1595371138039857000',
            'limit': '100'}
    r = requests.get(f'{loki_address}/loki/api/v1/query_range', params=payload, verify=False)
    if r.status_code == 200:
        print(r.text)
    elif r.status_code == 504:
        print(f'{r.status_code} Timeout Error. Please try again in a few mins.')
        print(r.url)
    else:
        print(r.status_code)

def get_job(customerLocation):
    if customerLocation == False:
        jobId = f'hosted-{aws_region}'
        return jobId
    elif customerLocation == True:
        jobId = f'thanos-{aws_region}'
        return jobId

def main():
    customerLocation = checkCustomerLocation()
    jobId = get_job(customerLocation)
    getRegion = aws_region_translator(aws_region)
    instanceId = get_instance_details(getRegion, customerLocation)
    getJournal = get_journal_logs(instanceId, jobId)

if __name__ in __main__:
    main()