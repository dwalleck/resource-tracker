import mock
import unittest

from resource_tracker import ResourceTracker, MockResourceProvider, ResourceTypeNotFoundException, ResourceNotFoundException

class TestResourceTracker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tracker = ResourceTracker()
        cls.mock_provider = mock.MagicMock(MockResourceProvider)
        cls.mock_provider.get_resources_by_type.return_value = [
                {'resource_name': 'ubuntu', 'uuid': '1', 'size': '1 GB', 'boot': 'slow', 'is_used': False},
                {'resource_name': 'ubuntu-lts', 'uuid': '4', 'size': '1 GB', 'boot': 'fast', 'is_used': False},
                {'resource_name': 'debian', 'uuid': '2', 'size': '600 MB', 'boot': 'slow', 'is_used': False},
                {'resource_name': 'windows', 'uuid': '3', 'size': '9 GB', 'boot': 'slow', 'is_used': False}
            ]
        cls.tracker.provider = cls.mock_provider
    
    def tearDown(self):
        self.mock_provider.get_resources_by_type.return_value = [
                {'resource_name': 'ubuntu', 'uuid': '1', 'size': '1 GB', 'boot': 'slow', 'is_used': False},
                {'resource_name': 'ubuntu-lts', 'uuid': '4', 'size': '1 GB', 'boot': 'fast', 'is_used': False},
                {'resource_name': 'debian', 'uuid': '2', 'size': '600 MB', 'boot': 'slow', 'is_used': False},
                {'resource_name': 'windows', 'uuid': '3', 'size': '9 GB', 'boot': 'slow', 'is_used': False}
            ]

    def test_requires_no_filter(self):
        image = self.tracker.requires('images')
        self.assertEquals(image.get('resource_name'), 'ubuntu')
        self.assertEquals(image.get('uuid'), '1')
        self.assertEquals(image.get('size'), '1 GB')
        self.assertEquals(image.get('boot'), 'slow')
   
    def test_requires_with_filter(self):
        image = self.tracker.requires('images', boot='fast')
        self.assertEquals(image.get('resource_name'), 'ubuntu-lts')
        self.assertEquals(image.get('uuid'), '4')
        self.assertEquals(image.get('size'), '1 GB')
        self.assertEquals(image.get('boot'), 'fast')
    
    def test_requires_with_multiple_filters(self):
        image = self.tracker.requires('images', boot='slow', size='9 GB')
        self.assertEquals(image.get('resource_name'), 'windows')
        self.assertEquals(image.get('uuid'), '3')
        self.assertEquals(image.get('size'), '9 GB')
        self.assertEquals(image.get('boot'), 'slow')

    def test_requires_with_multiple_filters(self):
        image = self.tracker.requires('images', boot='slow', size='9 GB')
        self.assertEquals(image.get('resource_name'), 'windows')
        self.assertEquals(image.get('uuid'), '3')
        self.assertEquals(image.get('size'), '9 GB')
        self.assertEquals(image.get('boot'), 'slow')
    
    def test_requires_filters_with_no_fallback(self):
        self.assertRaises(ResourceNotFoundException, self.tracker.requires, 'images', boot='fast', size='9 GB', fallback=False)
    
    def test_requires_filters_with_fallback(self):
        image = self.tracker.requires('images', boot='fast', size='9 GB', fallback=True)
        self.assertEquals(image.get('resource_name'), 'ubuntu')
    
    def test_requires_unexpected_resource_type(self):
        self.assertRaises(ResourceTypeNotFoundException, self.tracker.requires, 'servers')
        
