from app.models import Acquisition, AcquisitionItem
from app.views.base_views import BaseListView, BaseView, BaseNestedListView, BaseNestedModelView
from app.modules.example_data import ExampleAcquisitions, ExampleAcquisitionItems
from app.serializers import AcquisitionSerializer, AcquisitionDeserializer, AcquisitionItemSerializer, \
    AcquisitionItemDeserializer
from app.views.common import api_func


class AcquisitionListView(BaseListView):
    _model = Acquisition
    _serializer = AcquisitionSerializer()
    _deserializer = AcquisitionDeserializer()

    @api_func('List acquisitions', url_tail='/acquisitions',
              response=[ExampleAcquisitions.ACQUISITION1.get(), ExampleAcquisitions.ACQUISITION2.get()])
    def get(self):
        return self._get()

    @api_func('Create acquisition', url_tail='/acquisitions',
              request=ExampleAcquisitions.ACQUISITION1.set(),
              response=ExampleAcquisitions.ACQUISITION1.get())
    def post(self):
        return self._post()


class AcquisitionView(BaseView):
    _model = Acquisition
    _serializer = AcquisitionSerializer()
    _deserializer = AcquisitionDeserializer()

    @api_func('Get acquisition', item_name='acquisition', url_tail='/acquisitions/1',
              response=ExampleAcquisitions.ACQUISITION1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update acquisition', item_name='acquisition', url_tail='/acquisitions/1',
              request=ExampleAcquisitions.ACQUISITION1.set(change={'comment': 'A box has been damaged'}),
              response=ExampleAcquisitions.ACQUISITION1.get(change={'comment': 'A box has been damaged'}))
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete acquisition', item_name='acquisition', url_tail='/acquisitions/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)


class AcquisitionItemListView(BaseNestedListView):
    _model = AcquisitionItem
    _parent_model = Acquisition
    _serializer = AcquisitionItemSerializer()
    _deserializer = AcquisitionItemDeserializer()

    @api_func('List acquisition items', url_tail='/acquisitions/1/items',
              response=[ExampleAcquisitionItems.ITEM1.get(), ExampleAcquisitionItems.ITEM2.get()],
              queries={'id': 'ID of acquisition'})
    def get(self, id: int):
        self._initialize_parent_item(id)
        return self._get(acquisition_id=id)

    @api_func('Create acquisition item', url_tail='/acquisitions/1/items',
              request=ExampleAcquisitionItems.ITEM1.set(),
              response=ExampleAcquisitionItems.ITEM1.get(),
              status_codes={422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of acquisition'})
    def post(self, id: int):
        self._initialize_parent_item(id)
        item = self._post_populate(acquisition_id=id)
        return self._post_commit(item)


class AcquisitionItemView(BaseNestedModelView):
    _model = AcquisitionItem
    _parent_model = Acquisition
    _serializer = AcquisitionItemSerializer()
    _deserializer = AcquisitionItemDeserializer()

    @api_func('Get acquisition item', item_name='acquisition item', url_tail='/acquisitions/1/items/1',
              response=ExampleAcquisitionItems.ITEM1.get(),
              queries={'id': 'ID of acquisition',
                       'item_id': 'ID of selected acquisition item for get'})
    def get(self, id: int, item_id: int):
        self._initialize_parent_item(id)
        item = self._get(acquisition_id=id, id=item_id)
        return self._serialize(item)

    @api_func('Update acquisition item', item_name='acquisition item', url_tail='/acquisitions/1/items/1',
              request=ExampleAcquisitionItems.ITEM1.set(),
              response=ExampleAcquisitionItems.ITEM1.get(),
              status_codes={422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of acquisition',
                       'item_id': 'ID of selected acquisition item for get'})
    def put(self, id: int, item_id: int):
        self._initialize_parent_item(id)
        item = self._put_populate(acquisition_id=id, id=item_id)
        return self._put_commit(item)

    @api_func('Delete acquisition item', item_name='acquisition item', url_tail='/acquisitions/1/items/1',
              response=None,
              queries={'id': 'ID of acquisition',
                       'item_id': 'ID of selected acquisition item for get'})
    def delete(self, id: int, item_id: int):
        self._initialize_parent_item(id)
        item = self._delete_get_item(acquisition_id=id, id=item_id)
        return self._delete_commit(item)
