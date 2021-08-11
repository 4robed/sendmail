import gevent
from gevent.pool import Pool


class Service(object):
    pass


class Crawler(object):
    def __init__(self,
                 bulk_size=None,
                 max_workers=None):
        if not bulk_size:
            bulk_size = 500
        if not max_workers:
            max_workers = 10
        self.bulk_size = bulk_size
        self.max_workers = max_workers

        self.worker_pool = Pool(self.max_workers)

    @staticmethod
    def _prepare_update_payload(obj,
                                exclude_keys=None):
        if not exclude_keys:
            exclude_keys = []

        translatable_keys = getattr(obj, '_translatable_fields', [])

        add_to_set = {}
        object_data = obj.to_dict()
        for tk in translatable_keys:
            tl_value = object_data.pop(tk, None)
            if not tl_value:
                continue
            add_to_set[tk] = tl_value[0]

        for ek in exclude_keys:
            object_data.pop(ek, None)

        result = {
            '$set': object_data
        }
        if add_to_set:
            result['$addToSet'] = add_to_set

        return result

    def _bulk_write(self, ops):
        mapped_ops = {}
        workers = []
        for op in ops:
            model = op['model']
            coll_name = model._get_collection_name()
            if coll_name not in mapped_ops:
                mapped_ops[coll_name] = {
                    'model': model,
                    'ops': []
                }
            mapped_ops[coll_name]['ops'].append(op['operation'])

        worker_pool = Pool(self.max_workers)

        for coll_name, coll_data in mapped_ops.items():
            coll = coll_data['model']._get_collection()
            workers.append(worker_pool.spawn(
                coll.bulk_write,
                coll_data['ops']
            ))
        gevent.joinall(workers)
        print(f'_bulk_write {len(ops)} records')

    def _wait_for_workers(self):
        self.worker_pool.join()

    def run(self):
        raise NotImplementedError
