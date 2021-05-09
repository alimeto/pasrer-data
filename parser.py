# Program to convert an xml
# file to json file

# import json module and xmltodict
# module provided by python
import json
import xmltodict
from benedict import benedict
from csv import DictReader
import sys


def load_data(file_name):
    file_data = None

    with open(file_name, encoding='utf-8') as file:
        if file_name.split(".")[-1] == "xml":
            file_data = xmltodict.parse(file.read())

        elif file_name.split(".")[-1] == "csv":
            json_array = []
            # load csv file data using csv library's dictionary reader
            csv_reader = DictReader(file)
            # convert each csv row into python dict
            for row in csv_reader:
                # add this python dict to json array
                json_array.append(dict(row))
            file_data = json_array

    file.close()
    return file_data


def wirte_json(data_dict):
    json_data = json.dumps(data_dict, indent=4)

    # Write the json data to output
    # json file
    with open("data.json", "w") as json_file:
        json_file.write(json_data)
        json_file.close()


def convert_xml_to_json(file_name):
    # open the input xml file and read
    # data in form of python dictionary
    # using xmltodict module
    data_dict = load_data(file_name)

    # generate the object using json.dumps()
    # corresponding to json data
    json_data = json.dumps(data_dict)

    # convert all string keys to snake_case (nested dict keys included)
    json_data = benedict(json_data)
    json_data.standardize()

    # processing on data for sample.json
    json_data_temp = json_data
    json_data = {"file_name": "xml/customer2.xml"}
    vehicle = json_data_temp["transaction"]['customer']["units"]["vehicle"]
    del json_data_temp["transaction"]['customer']["units"]
    json_data["transaction"] = json_data_temp["transaction"]
    json_data["transaction"]["vehicle"] = vehicle
    # Write the json data to output
    # json file
    wirte_json(json_data)


def convert_csv_to_json(file_name1, file_name2):
    # read two csv
    costomer = load_data(file_name1)
    vehicles = load_data(file_name2)

    # initialize data json
    data = {
        "file_name": [
            "csv/" + file_name1.split("/")[-1],
            "csv/" + file_name2.split("/")[-1]
        ],
        "transaction": {
            "customers": [],
            "vehicles": []
        }
    }

    # add customers and vehicles
    data['transaction']['customers'] = costomer
    data['transaction']['vehicles'] = vehicles
    wirte_json(data)


if __name__ == "__main__":
    '''Get argument values'''
    if len(sys.argv > 3):
        file_format = sys.argv[1]

        if file_format == "xml":
            file_name = sys.argv[2]
            if file_name.split(".")[-1] == "xml":
                convert_xml_to_json(file_name)
            else:
                print("the file type is not xml")

        elif file_format == "csv":
            if len(sys.argv > 3):
                file_name1, file_name2 = sys.argv[2], sys.argv[3]
                if file_name1.split(".")[-1] == "csv" and \
                        file_name2.split(".")[-1] == "csv":
                    convert_csv_to_json(file_name1, file_name2)
                else:
                    print("the file type is not csv")

            else:
                print("not enough argument")

    else:
        print("not enough argument")
