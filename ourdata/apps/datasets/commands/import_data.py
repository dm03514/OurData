from csv import DictReader
from mongoengine import connection
from optparse import OptionParser
from ourdata.apps.common.exceptions import DataConversionError
from ourdata.apps.datasets.models import DatasetSchema
from pyramid.paster import bootstrap


def main():
    """Entry Into Application"""
    usage = 'usage: %prog dataset_title path/to/csv [options]' 
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    env = bootstrap('development.ini')

    if len(args) != 2:
        raise Exception('Must provide 2 arguments')

    title = args[0]
    path_to_csv = args[1]

    # see if collection is defined in db schema
    schema = DatasetSchema.objects.get(title=title)

    # open file
    f = open(path_to_csv)

    # get the actual collection in pymongo sorry mongoengine
    db = connection.get_db()
    collection = db[title]

    # wrap this in dict reader and start reading!
    dict_reader = DictReader(f)

    # should we make sure that the input file has only the fields in
    # dataschema? 
    for line_dict in dict_reader:
        new_doc = {}
        for field_name, field_value in line_dict.items():
            converted_value = schema.convert_field_value(field_name,
                                                        field_value)
            new_doc[field_name] = converted_value
        # insert this new_doc? this should probably be done in
        # batches, also need to catch errors and prsent those lines
        # to user afterwardS???
        collection.insert(new_doc)


if __name__ == '__main__':
    main()
