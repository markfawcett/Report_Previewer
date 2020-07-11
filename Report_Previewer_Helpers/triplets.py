from lxml import html  # type: ignore


# Class and type changes
class triplet:
    def __init__(self, find, new_tag, new_class):
        self.find = find
        self.new_tag = new_tag
        self.new_class = new_class


WORD_TRIPLETS = [triplet('h4', 'h3', None),
                 triplet('h3', 'h3', None),
                 triplet('h2', 'h3', None),
                 triplet('h1', 'h2', 'contents-heading'),
                 triplet('p[@class="SummaryHeading"]',   'h2', 'contents-heading'),
                 triplet('p[@class="ChapterHeading1"]',  'h2', 'contents-heading'),
                 triplet('p[@class="CRHeading2"]',       'h3', None),
                 triplet('p[@class="AppendixHeading1"]', 'h2', 'contents-heading'),
                 triplet('p[@class="AppendixHeading2"]', 'h3', None),
                 triplet('p[@class="AppendixHeading3"]', 'h3', None),
                 triplet('p[@class="AppendixHeading4"]', 'h3', None),
                 triplet('p[@class="Source"]',           'p', 'figure-caption'),
                 triplet('p[@class="UnorderedList1"]',   'li', False),
                 triplet('p[@class="UnorderedList2"]',   'li', False),
                 triplet('p[@class="AppendixUnorderedList1"]', 'li', 'UnorderedList1'),
                 triplet('p[@class="AppendixUnorderedList2"]', 'li', 'UnorderedList2')]


# ID_TRIPLETS = [triplet('p[class=Source]', 'p', 'figure-caption'),
#                triplet('p[class=FMParaCentreAligned]', 'p', 'text-center'),
#                triplet('p[class=FMParaRightAligned]', 'p', 'text-right'),
#                triplet('h5', 'h3', None),
#                triplet('h4', 'h3', None),
#                triplet('h3', 'h3', None),
#                triplet('h2[FMTitle]', 'p', 'text-center'),
#                triplet('h2', 'h3', None),
#                triplet('h1', 'h2', 'contents-heading')]


def map_classes_and_tags(htmlRoot, source):

    if source[0] == 'Word':
        triplets = WORD_TRIPLETS

    # if source[0] == 'ID':
    #     triplets = ID_TRIPLETS

    for item in triplets:
        elementList = htmlRoot.xpath(item.find)

        for element in elementList:
            try:
                if item.new_tag is False:
                    pass
                else:
                    element.tag = item.new_tag

                if item.new_class is None:
                    try:
                        element.attrib.pop('class')
                    except:
                        pass

                elif item.new_class is False:
                    pass

                else:
                    element.attrib['class'] = item.new_class

            except:
                pass

##    set_of_classes_to_keep = set ()
##    set_of_classes_to_remove = set ()
##    set_of_unexpected_classes = set()
##
##    for triplet in triplets:
##        if type(triplet.new_class) == type(''):
##            set_of_classes_to_keep.add(triplet.new_class)
##
##    all_elements = htmlRoot.cssselect("*")
##    for element in all_elements:
##        try:
##            if element.attrib['class'] in set_of_classes_to_keep:
##                pass
##            elif element.attrib['class'] in set_of_classes_to_remove:
##                element.attrib.pop('class')
##            else:
##                set_of_unexpected_classes.add(element.attrib['class'])
##        except:
##            pass
##
##    print(set_of_classes_to_keep)
##    print(set_of_unexpected_classes)



    return htmlRoot
