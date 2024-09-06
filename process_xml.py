import os
import xml.etree.ElementTree as ET

# Directories
dir1 = "/Users/edgargonzalezblanco/Documents/dvs/xml_source"
dir2 = "/Users/edgargonzalezblanco/Documents/dvs/xml_result"
tags_replace = [
    "UebgID",
    "PreAdrID",
    "ProdVar",
    "VersProd",
    "ProdID",
    "FrkArt",
    "FrkDat",
    "SdgS",
    "AdrMerk",
    "AbrKontrakt",
    "Kd_Na1",
    "Kd_Na2",
    "Kd_Na3",
    "Kd_Str",
    "Kd_HNr",
    "Kd_PLZ",
    "Kd_Ort",
    "NSA_Na1",
    "NSA_Na2",
    "NSA_Na3",
    "NSA_Na4",
    "NSA_Str",
    "NSA_HNr",
    "NSA_PLZ",
    "NSA_Ort",
    "NSA_Land",
    "NSA_Postf",
    "NSA_PLZPostf",
    "NSA_OrtPostfach",
    "NSA_LandPostfach",
    "KdInfoDMC_Ascii"
]

# Create dir2 if it doesn't exist
os.makedirs(dir2, exist_ok=True)

# Iterate through each XML file in dir1
print("PROCESSING...")

def replace_self_closing_tags(xml_str, tag_names):
    for tag in tag_names:
        xml_str = xml_str.replace(f'<{tag} />', f'<{tag}></{tag}>')
    return xml_str

cont = 0;
for filename in os.listdir(dir1):
    if filename.endswith(".xml"):
        filepath = os.path.join(dir1, filename)
        cont += 1

        try:
            # Parse the XML file
            tree = ET.parse(filepath)
            root = tree.getroot()

            # Get the CreationTime from the Envelope tag
            envelope = root.find(".//Envelope")
            creation_time = envelope.attrib.get("CreationDate").replace("-", "")
            print(str(cont) + ":" + filename + " - " + str(envelope.attrib.get("CreationDate")))

            # Generate the new filename
            new_filename = f"Redressenexport_26996_{creation_time}_070814_0{cont}.xml"
            new_filepath = os.path.join(dir2, new_filename)

            # Process each Pos tag
            for pos in root.findall(".//Pos"):
                # Get NSA_Str, NSA_PLZ, NSA_Ort
                nsa_str = pos.find("NSA_Str").text.strip() if pos.find("NSA_Str").text else ""
                nsa_plz = pos.find("NSA_PLZ").text.strip() if pos.find("NSA_PLZ").text else ""
                nsa_ort = pos.find("NSA_Ort").text.strip() if pos.find("NSA_Ort").text else ""

                # Determine the value for SdgS
                if nsa_str and nsa_plz and nsa_ort:
                    pos.find("SdgS").text = "20"
                else:
                    pos.find("SdgS").text = "10"

                # Reformat empty tags to <TagEmpty></TagEmpty>
                for elem in pos.iter():
                    if len(elem) == 0 and elem.text is None:
                        elem.text = ""

            # Convert the ElementTree to a string
            xml_str = ET.tostring(root, encoding='unicode')

            # Replace self-closing tags with <TagEmpty></TagEmpty>
            xml_str = replace_self_closing_tags(xml_str, tags_replace)

            # Save the XML string directly to a file
            with open(new_filepath, 'w', encoding='utf-8') as file:
                file.write(xml_str)

        except ET.ParseError as e:
            print(f"Error parsing {filename}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {filename}: {e}")

print("Processing complete.")
