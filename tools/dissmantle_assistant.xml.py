import xml.etree.ElementTree as XmlTree

tree = XmlTree.parse('/home/sztylet/MagicAssistantWorkspace/magiccards/MagicDB/Zendikar_Rising.xml')
root = tree.getroot()
print(root.find("name").text)
for magic_card in root.iter("mc"):
    for props in magic_card:
        print(props.tag, props.text)
    print()
