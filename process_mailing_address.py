import usaddress, csv

def process_address_lib(address):
    attrs = {"Street": "", "City": "", "State": "", "Zip": ""}
    components = usaddress.parse(address)
    street = ""
    for name, tag in components:
        if tag=="PlaceName": 
            attrs["City"] = name.rstrip(", ")
            attrs["Street"] = street.rstrip(", ")
        elif tag=="StateName": attrs["State"] = name.rstrip(", ")
        elif tag=="ZipCode": attrs["Zip"] =  name
        else: street+=name+" "
    return attrs
def process_address_manual(address):
    attrs = {"Street": "", "City": "", "State": "", "Zip": ""}
    components = address.split(", ")
    street = []
    remainder = []
    end = components[-1].split(" ")
    if len(end)==2:
        street = components[:-2]
        components[-1] = end[0]
        components.append(end[1])
    else:
        street = components[:-3]
    remainder = components[-3:]
    street = ", ".join(street)
    attrs["Street"] = street
    attrs["City"] = remainder[0]
    attrs["State"] = remainder[1]
    attrs["Zip"] = remainder[2]
    return attrs
def process_csv(input, output):
    with open(input, 'r') as infile, open(output, 'w', newline='') as outfile: 
        reader = csv.reader(infile, skipinitialspace=True)
        writer = csv.writer(outfile)
        headers = next(reader)
        new_headers = headers + ["Street", "City", "State", "Zip"]
        writer.writerow(new_headers)
        for row in reader:
            processed_addr = process_address_lib(row[1])
            new_row = row + [processed_addr[field] for field in processed_addr]
            writer.writerow(new_row)
if __name__=="__main__":
    input = 'data/addresses.csv'
    output = "data/output.csv"
    process_csv(input, output)