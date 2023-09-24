import json
import xml.etree.ElementTree as ET
from typing import Final
from zipfile import ZipFile


def extract_all_text(nodes):
    return " ".join([at.text.strip() for at in nodes])


TEXT_SELECTOR: Final = ".//a:t"
extract = {}

with ZipFile("input.pptx") as dzip:
    # with dzip.open("[Content_Types].xml") as dfile:
    #     print(dfile.read())
    #     tree = ET.parse(dfile)
    #     print(tree)
    #     root = tree.getroot()
    #     ET.indent(root)
    #     print(ET.tostring(root, encoding='unicode'))

    # <ns0:Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml" />
    # <ns0:Override PartName="/ppt/slides/slide2.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml" />
    # <ns0:Override PartName="/ppt/slides/slide3.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml" />
    # <ns0:Override PartName="/ppt/slides/slide4.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml" />

    ns = {
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    }

    extract.update({"slide_2": {}})
    with dzip.open("ppt/slides/slide2.xml") as slide2:
        # print(slide2.read())
        tree = ET.parse(slide2)
        # print(tree)
        root = tree.getroot()
        # print(root.attrib)
        # ET.indent(root)
        # print(ET.tostring(root, encoding='unicode'))

        # for tx_body in root.findall(".//p:txBody", ns):
        #     print(tx_body, tx_body.tag, tx_body.attrib)a

        tx_body = root.find(".//p:sp[2]//p:txBody", ns)
        # tx_body = root.find("./p:cSld/p:spTree/p:sp[2]//p:txBody", ns)
        # print(tx_body)
        # print(tx_body, tx_body.tag, tx_body.attrib)
        a_ts = tx_body.findall(TEXT_SELECTOR, ns)

        # print(a_ts[0].text.translate(str.maketrans("", "", string.punctuation)).lower())
        #  s.strip(": ").lower().replace(" ", "_")
        # print(a_ts[0].text, a_ts[1].text)
        extract["slide_2"].update({a_ts[0].text.strip(": "): a_ts[1].text})

        # print(a_ts[2].text, a_ts[3].text)
        extract["slide_2"].update({a_ts[2].text.strip(": "): a_ts[3].text})

        # print(a_ts[4].text, a_ts[5].text)
        extract["slide_2"].update({a_ts[4].text.strip(": "): a_ts[5].text})

        # s = a_ts[6].text + a_ts[7].text
        # print(s, a_ts[8].text)
        extract["slide_2"].update({a_ts[6].text.strip(": "): a_ts[7].text})

        # print(a_ts[9].text, a_ts[10].text)
        extract["slide_2"].update({a_ts[8].text.strip(": "): a_ts[9].text})

        # <a:graphic>
        #     <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">
        #         <a:tbl>
        trs = root.findall(".//a:tbl/a:tr", ns)
        # print(trs[0].find(TEXT_SELECTOR, ns).text)
        tr1 = trs.pop(0).findall(TEXT_SELECTOR, ns)
        table_name = tr1.pop(0).text
        # print(table_name)
        extract["slide_2"].update({table_name: {}})

        column_names = [at.text for at in tr1]
        # print(column_names)
        for tr in trs:
            # print(tr)
            tcs = tr.findall(".//a:tc", ns)
            # row_name = " ".join([at.text.strip() for at in tcs.pop(0).findall(TEXT_SELECTOR, ns)])
            row_name = extract_all_text(tcs.pop(0).findall(TEXT_SELECTOR, ns))
            # print(row_name)
            extract["slide_2"][table_name].update({row_name: {}})
            for x, tc in enumerate(tcs):
                # print(x)
                # print(column_names[x])
                # print("\t" + str(tc))
                # for at in tc.findall(TEXT_SELECTOR, ns):
                #     print("\t\t" + str(at))
                #     print("\t\t" + str(at.text))
                # column_value = " ".join([at.text.strip() for at in tc.findall(TEXT_SELECTOR, ns)])
                column_value = extract_all_text(tc.findall(TEXT_SELECTOR, ns))
                # print(column_value)
                extract["slide_2"][table_name][row_name].update(
                    {column_names[x]: column_value}
                )

    extract.update({"slide_3": {}})
    with dzip.open("ppt/slides/slide3.xml") as slide3:
        tree = ET.parse(slide3)
        root = tree.getroot()

        tx_body = root.find(".//p:sp[2]//p:txBody", ns)

        a_ts = tx_body.findall(TEXT_SELECTOR, ns)
        extract["slide_3"].update({a_ts[0].text.strip(": "): a_ts[1].text})
        extract["slide_3"].update({a_ts[2].text.strip(": "): a_ts[3].text})

        trs = root.findall(".//a:tbl/a:tr", ns)

        tr1 = trs.pop(0).findall(TEXT_SELECTOR, ns)

        table_name = tr1.pop(0).text
        extract["slide_3"].update({table_name: {}})

        column_names = [at.text for at in tr1]

        for tr in trs:
            tcs = tr.findall(".//a:tc", ns)

            row_name = extract_all_text(tcs.pop(0).findall(TEXT_SELECTOR, ns))
            extract["slide_3"][table_name].update({row_name: {}})
            for x, tc in enumerate(tcs):
                column_value = extract_all_text(tc.findall(TEXT_SELECTOR, ns))
                extract["slide_3"][table_name][row_name].update(
                    {column_names[x]: column_value}
                )

                solid_fill = tc.find(".//a:tcPr/a:solidFill", ns)
                if solid_fill:
                    color_value = None
                    status_color = column_names[x] + " Color"
                    if solid_fill.find(".//a:schemeClr", ns) is not None:
                        color = solid_fill.find(".//a:schemeClr", ns)
                        color_value = {status_color: {"schemeClr": color.get("val")}}
                        for child in color:
                            tag_name = child.tag.split("}")[1][0:]
                            attributes = child.attrib
                            color_value[status_color].update(
                                {tag_name: attributes["val"]}
                            )
                    elif solid_fill.find(".//a:srgbClr", ns) is not None:
                        color_value = {
                            status_color: {
                                "srgbClr": solid_fill.find(".//a:srgbClr", ns).get(
                                    "val"
                                )
                            }
                        }

                    extract["slide_3"][table_name][row_name].update(color_value)

    extract.update({"slide_4": {}})
    with dzip.open("ppt/slides/slide4.xml") as slide3:
        tree = ET.parse(slide3)
        root = tree.getroot()

        a_ts = root.findall(".//p:sp[2]//p:txBody/a:p/a:r/a:t", ns)

        extract["slide_4"].update({a_ts[0].text.strip(": "): a_ts[1].text})

        section = a_ts[2].text.strip(": ")
        d1 = {"deliverable": a_ts[3].text, "impact": a_ts[5].text}
        d2 = {"deliverable": a_ts[6].text, "impact": a_ts[8].text}
        d3 = {"deliverable": a_ts[9].text, "impact": a_ts[11].text}
        extract["slide_4"].update({section: [d1, d2, d3]})

        section = a_ts[12].text.strip(": ")
        d1 = {"deliverable": a_ts[13].text, "impact": a_ts[15].text}
        d2 = {"deliverable": a_ts[16].text, "impact": a_ts[18].text}
        d3 = {"deliverable": a_ts[19].text, "impact": a_ts[21].text}
        extract["slide_4"].update({section: [d1, d2, d3]})

    # print(str(extract))
    # print(json.dumps(extract, indent=4, ensure_ascii=False))

    with open("output.json", "w") as outfile:
        json.dump(extract, outfile, indent=4, ensure_ascii=False)
