import keyword
from urlopener.utils import ListInstance


class XMLRecord(ListInstance):

    def __init__(self, xml_list, name_space=None):
        self.name_space = name_space
        data = self.__build(xml_list)
        self.__dict__.update(data)

    def __build(self, xml_list):
        data ={}
        for child in xml_list:
            # Проверка на совпадение с ключевыми словами
            key = child.tag.lower()
            if self.name_space is not None:
                key = key.split(self.name_space)[1]

            if keyword.iskeyword(key):
                key += '_'

            if not len(child) and child.text is not None:
                data[key] = child.text.strip()
            elif self.__testelem(child) == 1:
                data[key] = tuple(str(item.text).strip() for item in child)
            elif len(child):
                data[key] = XMLRecord(child)
            else:
                data[key] = None
        return data

    def __testelem(self, mapping):
        a = {repr(obj).split()[1] for obj in mapping}
        return len(a)