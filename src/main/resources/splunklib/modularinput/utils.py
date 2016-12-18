#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

# File for utility functions

def xml_compare(expected, found):
    """Checks equality of two ``ElementTree`` objects.

    :param expected: An ``ElementTree`` object.
    :param found: An ``ElementTree`` object.
    :return: ``Boolean``, whether the two objects are equal.
    """

    # if comparing the same ET object
    if expected == found:
        return True

    # compare element attributes, ignoring order
    if set(expected.items()) != set(found.items()):
        return False

    # check for equal number of children
    expected_children = list(expected)
    found_children = list(found)
    if len(expected_children) != len(found_children):
        return False

    # compare children
    if not all([xml_compare(a, b) for a, b in zip(expected_children, found_children)]):
        return False

    # compare elements, if there is no text node, return True
    if (expected.text is None or expected.text.strip() == "") \
        and (found.text is None or found.text.strip() == ""):
        return True
    else:
        return expected.tag == found.tag and expected.text == found.text \
            and expected.attrib == found.attrib

def parse_parameters(param_node):
    if param_node.tag == "param":
        return param_node.text
    elif param_node.tag == "param_list":
        parameters = []
        for mvp in param_node:
            parameters.append(mvp.text)
        return parameters
    else:
        raise ValueError("Invalid configuration scheme, %s tag unexpected." % param_node.tag)

def parse_xml_data(parent_node, child_node_tag):
    data = {}
    for child in parent_node:
        if child.tag == child_node_tag:
            if child_node_tag == "stanza":
                data[child.get("name")] = {}
                for param in child:
                    data[child.get("name")][param.get("name")] = parse_parameters(param)
        elif "item" == parent_node.tag:
            data[child.get("name")] = parse_parameters(child)
    return data