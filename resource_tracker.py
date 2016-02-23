
 
class ResourceType(object):

    IMAGES = 'images'
    FLAVORS = 'flavors'
    SHARED_NETWORKS = 'shared_networks'
    
    resource_types = [IMAGES, FLAVORS, SHARED_NETWORKS]


class MockResourceProvider(object):
    
    def __init__(self):
        
        self.resources = {
            'images': [
                {'resource_name': 'ubuntu', 'uuid': '1', 'size': '1 GB', 'boot': 'slow', 'is_used': False},
                {'resource_name': 'ubuntu-lts', 'uuid': '4', 'size': '1 GB', 'boot': 'fast', 'is_used': False},
                {'resource_name': 'debian', 'uuid': '2', 'size': '600 MB', 'boot': 'slow', 'is_used': False},
                {'resource_name': 'windows', 'uuid': '3', 'size': '9 GB', 'boot': 'slow', 'is_used': False}
            ]
        }
    
    def get_resources_by_type(self, resource_type):
        return self.resources.get(resource_type)


class ResourceTracker(object):

    def __init__(self):
        self.provider = MockResourceProvider()
        
    def requires(self, resource_type, **kwargs):
        
        fallback_enabled = kwargs.pop('fallback', True)
        if resource_type not in ResourceType.resource_types:
            raise Exception(
                'Resource type of ' + resource_type + ' not found. '
                'Expected resource types are ' + str(ResourceType.resource_types))
        
        
        resources = self.provider.get_resources_by_type(resource_type)
        print resources
        available_resources = [
            resource for resource in resources
            if not resource.get('is_used')]

        if available_resources:
            # Apply all provided filters
            filtered_resources = available_resources
            for k, v in kwargs.iteritems():
                filtered_resources = [
                    resource for resource in filtered_resources
                    if resource.get(k) == v]
            
            # Pick a resource to use based on filtering
            selected_resource = None
            if filtered_resources:
                selected_resource = filtered_resources[0]
            elif fallback_enabled:
                # Unless fallback is disabled, return a resource of the correct type
                selected_resource = available_resources[0]
            if selected_resource:
                selected_resource['is_used'] = True
                return selected_resource
        
        # If no resources are found, raise an exception
        raise Exception('No resources of type ' + resource_type + ' remaining')
        

#r = ResourceTracker()
#r.requires('images', size='1 GB', boot='fast')
#print r.requires('images')
#print r.requires('images')
#print r.requires('images')