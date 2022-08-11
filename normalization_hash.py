##code <tab> concept IRI <tab> parents code <tab> synonyms <tab> definition <tab> display name <tab> concept status <tab> semantic type <EOL>

import os
import json

class record:

    def __init__(self):
        self.concept_id = ''
        self.parent_names = []
        self.generic_name = ''

    def setID(self, id):
        self.concept_id = id

    def setParentName(self, name):
        self.parent_names = name

    def setGenericName(self, gname):
        self.generic_name = gname

    def getID(self):
        return self.concept_id

    def getParentName(self):
        return self.parent_names

    def getGenericName(self):
        return self.generic_name


class processing:

    def __init__(self):
        self.concept_code_name_hash = {}
        self.concept_record_hash = {}
        self.contents = []

    def concept_id_hash_map_creator(self):

        for content in self.contents:
            elements = content.split('\t')
            concept_name = elements[5]

            concept_id = elements[0]
            self.concept_code_name_hash[concept_id] = concept_name

        with open('../data/Thesaurus NCI/code_to_name.json', 'w') as f:
            json.dump(self.concept_code_name_hash, f)

    def preprocessing(self, location):

        with open(location, mode='r', encoding='utf8') as f:
            self.contents = f.readlines()


        if os.path.exists('../data/Thesaurus NCI/code_to_name.json'):
            with open('../data/Thesaurus NCI/code_to_name.json') as f:
                self.concept_code_name_hash = json.load(f)

        else:
            self.concept_id_hash_map_creator()

    def record_curation(self):
        for content in self.contents:
            elements = content.split('\t')
            concept_name = elements[5]

            if concept_name!='':
                record_obj = record()
                id = elements[0]
                parent = elements[2]
                synonyms = elements[3]

                parent_ids = parent.split('|')
                synonyms_list = synonyms.split('|')

                record_obj.setID(id)
                record_obj.setGenericName(concept_name)
                parent_names = []
                for id in parent_ids:
                    try:
                        parent_names.append(self.concept_code_name_hash[id])
                    except:
                        parent_names.append(None)
                        print('No parent id found so appending None to parent names list')


                record_obj.setParentName(parent_names)

                for name in synonyms_list:
                    name = name.lower()
                    self.concept_record_hash[name] = record_obj

    def main(self):
        self.preprocessing('../data/Thesaurus NCI/Thesaurus.txt')
        self.record_curation()
        #print(self.concept_code_name_hash)
        #print(self.concept_record_hash)


if __name__=='__main__':
    processing_obj = processing()
    processing_obj.main()
    print(processing_obj.concept_record_hash)








