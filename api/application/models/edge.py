class Mapper:

    @staticmethod
    def map_edge(source, target):
        return {
            'data':
                {
                    "source": source,
                    "target": target
                }
        }

    @staticmethod
    def map_node(id, name):
        return {
            'data':
                {
                    "id": id,
                    'name': name
                }

        }
