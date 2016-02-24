

class ResourceTypeNotFoundException(Exception):
    pass


class ResourceNotFoundException(Exception):
    pass


class ResourceRepository(object):

    def __init__(self):
        # Load the ResourceConfiguration
        
        self.resources = {
            'images': [
                {'resource_name': 'ubuntu', 'uuid': '1', 'size': '1 GB', 'boot': 'slow', 'is_used': False},
                {'resource_name': 'ubuntu-lts', 'uuid': '4', 'size': '1 GB', 'boot': 'fast', 'is_used': False},
                {'resource_name': 'debian', 'uuid': '2', 'size': '600 MB', 'boot': 'slow', 'is_used': False},
                {'resource_name': 'windows', 'uuid': '3', 'size': '9 GB', 'boot': 'slow', 'is_used': False}
            ]
        }
    
    def get_resource_types(self):
        return self.resources.keys()
    
    def get_available_resources_by_type(self, resource_type):
        resources = self.resources.get(resource_type)
        return filter(lambda x: not x.get('is_used'), resources)
    
    def get_all_resources_by_type(self, resource_type):
        return self.resources.get(resource_type)
            
    def claim_resource(self, resource_type, resource_name):
        resources = self.get_all_resources_by_type(resource_type)
        filtered_resources = [resource for resource in resources
                              if resource.get('resource_name') == resource_name]
        filtered_resources[0]['is_used'] = True
    

class ResourceProvider(object):

    def __init__(self):
        # Get an instance of the ResourceRepository
        self.repository = ResourceRepository()
    
    def requires(self, resource_type, **kwargs):
        
        resource_types = self.repository.get_resource_types()
        if resource_type not in resource_types:
            raise ResourceTypeNotFoundException(
                'Resource type of ' + resource_type + ' not found. '
                'Expected resource types are ' + str(resource_types))
        
        fallback_enabled = kwargs.pop('fallback', False)
        available_resources = self.repository.get_available_resources_by_type(resource_type)
        
        if available_resources:
            # Apply all provided filters
            filtered_resources = list(available_resources)
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
                self.repository.claim_resource(
                    resource_type, selected_resource.get('resource_name'))
                return selected_resource
        
        # If no resources are found, raise an exception
        raise ResourceNotFoundException('No resources of type {resource_type} remaining.'.format(resource_type=resource_type))
