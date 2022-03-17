import re

from lxml import html  # type: ignore

from .settings import REQUIRED as Required
# ### Constants
PARAGRAPH_TAGS = ['p', 'h1', 'h2', 'h3', 'h4']
INLINE_TAGS = ['em', 'strong', 'span', 'a']


def drop_head(htmlRoot):
    htmlRoot.find("head").drop_tree()
    htmlRoot.find("body").drop_tag()
    return (htmlRoot)

def drop_cover(htmlRoot):
    xpath = '//*[@class="Heading1"] | //*[@class="ChapterHeading1"] | //*[@class="SummaryHeading"]'
    elements = htmlRoot.xpath(xpath)
    for element in elements:
        if str(element.text_content()).strip() == 'Summary':
            siblingIterator = element.itersiblings(preceding=True)
            for sibling in siblingIterator:
                sibling.drop_tree()
            break
    return htmlRoot

def drop_unwanted_attributes(htmlRoot, attribute_list):
    # remove unwanted attributes added by Word
    for attribute in attribute_list:
        # elements = htmlRoot.cssselect("[" + attribute + "]")
        elements = htmlRoot.xpath(f'//*[@{attribute}]')
        for element in elements:
            element.attrib.pop(attribute)
    return htmlRoot

def drop_pointless_tags(htmlRoot, pointlessTags):
    # all_elements = htmlRoot.cssselect("*")
    all_elements = htmlRoot.iter()  # should be a bit faster
    for element in all_elements:
        if element.tag in pointlessTags:
            if len(element.attrib) == 0:
                element.drop_tag()
    return htmlRoot

def size_images(htmlRoot):
    # images = htmlRoot.cssselect('img')
    images = htmlRoot.xpath('//img')
    for image in images:
        image.set('width', "100%")
    return htmlRoot


def free_img(htmlRoot):
    image_containers = htmlRoot.xpath('//p[img]')
    for image_container in image_containers:
        # drop the p tag if it has no text

        # get the text content (could be whitespace)
        text = image_container.text_content()
        if text:
            text = text.strip()  # remove whitespace
        if not text:
            image_container.drop_tag()

    return htmlRoot


def add_rules(htmlRoot):
    captions = htmlRoot.xpath('//p[@class="figure-caption"]')
    tags_of_interest = ('img', 'table', 'div')

    for caption in captions:
        try:
            next_ = caption.getnext()
            # print('Next element:\t', html.tostring(next_), '\n')
            # print('This elemebnt:\t', html.tostring(caption), '\n')
            previous = caption.getprevious()
            # print('Previous element:\t', html.tostring(previous), '\n')

            if next_ is not None:

                # also add rule before captions
                if next_.tag in tags_of_interest and previous not in captions:
                    caption.addprevious(html.Element('hr'))

            if previous is not None:

                if previous.tag in tags_of_interest and next_ not in captions:
                    caption.addnext(html.Element('hr'))

                if (len(previous) > 0 and previous[0].tag in tags_of_interest
                        and next_ not in captions):
                    caption.addnext(html.Element('hr'))
        except Exception:
            pass

    return htmlRoot


def fix_blockquotes(htmlRoot):

    # Change p-quote to blockquote
    # quotes = htmlRoot.cssselect('p[class=Quote]') + htmlRoot.cssselect('p[class=MsoQuote]')
    xpath = '//p[@class="Quote"] | //p[@class="MsoQuote"]'
    quotes = htmlRoot.xpath(xpath)
    for quote in quotes:
        if quote.getparent().tag == 'td':
            pass
        else:
            quote.tag = 'blockquote'

    elements = htmlRoot.xpath('//blockquote')
    for element in elements:
        try:
            if element.getprevious().tag == 'blockquote' or element.getprevious().tag == 'blockquote-subsequent':
                element.tag = 'blockquote-subsequent'
        except Exception:
            pass

    elements = htmlRoot.xpath('//blockquote')
    for element in elements:
        group = [element]
        element.tag = 'p'
        currentElement = element
        nextElement = element.getnext()

        while True:
            try:
                if nextElement.tag == 'blockquote-subsequent':
                    nextElement.tag = 'p'
                    group.append(nextElement)
                    nextElement = nextElement.getnext()
                else:
                    break
            except Exception:
                break
        myBlock = element.makeelement('blockquote')
        element.addprevious(myBlock)
        for listItem in group:
            myBlock.append(listItem)

    return htmlRoot


# use sets instead.
# def keep_only_accepted_classes(htmlRoot, accepted_classes):
#     elements_with_class = htmlRoot.cssselect('*[class]')
#     for element in elements_with_class:

#         if not set(element.get('class', default='').split(' ')
#                    ).issubset(accepted_classes):
#             element.attrib.pop('class')

#     return htmlRoot


# Some elements (like tales) take multiple, space separated, classes.
def keep_only_accepted_classes(htmlRoot, accepted_classes):
    elements_with_class = htmlRoot.xpath('//*[@class]')

    for element in elements_with_class:
        element_classes = element.get('class', default='').split(' ')
        good_classes = []

        for element_class in element_classes:
            if element_class in accepted_classes:
                good_classes.append(element_class)

        if good_classes:
            element.set('class', ' '.join(good_classes))
        else:
            element.attrib.pop('class')

    return htmlRoot

# def keep_only_accepted_classes (htmlRoot, accepted_classes):
#     elements_with_class = htmlRoot.cssselect('*[class]')
#     for element in elements_with_class:
#         try:
#             if element.attrib['class'] not in accepted_classes:
#                 element.attrib.pop('class')
#         except Exception:
#             pass
#     return htmlRoot

def tidy_cycle(htmlRoot):
    # Removes empty tags that have no function

    def attempt_drop_tree(element):
        try:
            element.drop_tree()
            nonlocal repeat
            repeat = True
        except Exception:
            pass


    def attempt_drop_tag(element):
        try:
            element.drop_tag()
            nonlocal repeat
            repeat = True
        except Exception:
            pass

    repeat = False

    while repeat == False:

        repeat = False

        # ### Part One
        # all_elements = htmlRoot.cssselect("*")
        all_elements = htmlRoot.iter()
        for element in all_elements:

            if element.getchildren() == []:

                # remove textless, childless inline tags
                if element.tag in INLINE_TAGS:
                    if str(element.text_content()) == "":
                        attempt_drop_tree(element)
                        repeat = True

                # remove textless, childless paragraph tags
                elif element.tag in PARAGRAPH_TAGS:
                    if re.fullmatch(r'\s*', str(element.text_content())) != None:
                        attempt_drop_tree(element)
                        repeat = True

                # remove childless div tags
                elif element.tag == 'div':
                    attempt_drop_tree(element)
                    repeat = True


        # ### Part Two
        # drop tags that have no attributes and that are pointless without attributes
        drop_pointless_tags(htmlRoot, ['span', 'a'])

        # ### Part Three - remove redundant immediate tag repetition
        # all_elements = htmlRoot.cssselect("*")
        all_elements = htmlRoot.iter()
        for element in all_elements:
            try:
                parent = element.getparent()
                if element.tag == parent.tag and element.text_content() == parent.text_content() and element.attrib == parent.attrib:
                    attempt_drop_tag(element)
                    repeat = True
            except Exception:
                pass

        # Remove empty attributes that have no purpose if empty
        for pointless_attribute in 'title', 'class', 'id':
            all_elements = htmlRoot.xpath(f'//*[@{pointless_attribute}]')
            for element in all_elements:
                if element.attrib[pointless_attribute] == "":
                    element.attrib.pop(pointless_attribute)
                    repeat = True

        # Remove whitespace at the end of paragraph tags
        for element in htmlRoot.iter():
            if element.tag in PARAGRAPH_TAGS:
                if element.getchildren() is None or element.getchildren() == []:
                    if element.text:
                        element.text = element.text.rstrip()
                        repeat = True
                else:
                    last_child = element.getchildren()[-1]
                    if last_child.tail:
                        last_child.tail = last_child.tail.rstrip()
                        repeat = True

        # #Tried to switch two non-breaking spaces for a horizontal tab but can't do it at this level. html.tostring is used later and doesn't interpret horizontal tab as we would want.
        try:
            for element in htmlRoot.iter():
                if element.text and element.text.find('\xa0\xa0') != -1:
                    element.text = str(element.text).replace('\xa0\xa0', '\xa0')
                    repeat = True
                if element.tail and element.tail.find('\xa0\xa0') != -1:
                    element.tail = str(element.tail).replace('\xa0\xa0', '\xa0')
                    repeat = True
        except Exception:
            pass


    return (htmlRoot)

def generic_clean(htmlRoot):

    paragraphTags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5']
    blocksWithoutInlines = ['html', 'head', 'body', 'title', 'meta', 'link', 'script', 'hr', 'col', 'colgroup', 'tr', 'svg', 'polygon', 'g', 'table', 'img', 'path', 'tbody']
    blocksWithInlines = ['div', 'blockquote', 'nav', 'footer', 'td', 'ul', 'ol', 'li', 'button']
    blockTags = paragraphTags + blocksWithoutInlines + blocksWithInlines
    inlineTags = ['em', 'strong', 'span', 'a', 'sup', 'i', 'br']
    allKnownTags = blockTags + inlineTags
    unknownTags = set()

    allElements = htmlRoot.xpath('//*')
    counter = 0
    for e in allElements:
        # Unknown tags record to error file for JB review
        if e.tag not in allKnownTags:
            unknownTags.add(e.tag)

    #    # Could potentially remove tail entirely in some cases but perhaps risky for no real benefit
    #    if e.tag in blockTags and e.tail != None:
    #        e.tail = None

        # remove unnecessary line breaks and tabbing from tail but replace with space so that web user doesn't lose space
        if e.tail != None:
            e.tail = e.tail.replace('\r', ' ')
            e.tail = e.tail.replace('\n', ' ')
            e.tail = e.tail.replace('\t', ' ')

            # reduce double spacing to single in tail - doesn't touch &nbsp; so only affects code view not web user view
            while True:
                if e.tail.count('  ') != 0:
                    e.tail = e.tail.replace('  ', ' ')
                else:
                    break

        # same as above but for text rather than tail
        if e.text != None:
            e.text = e.text.replace('\r', ' ')
            e.text = e.text.replace('\n', ' ')
            while True:
                if e.text.count('  ') != 0:
                    e.text = e.text.replace('  ', ' ')
                else:
                    break


    for element in reversed(allElements):
        # Consistency
        if element.tail == '':
            element.tail = None
        # resolve situation where inline tags unnecessarily close and then immediately reopen
        if element.tag in inlineTags and element.tail == None and element.getchildren() == []:
            if element.getnext() !=None and element.getnext().tag == element.tag and element.getnext().attrib == element.attrib:
                if element.text != None and element.getnext().text == None:
                    element.getnext().text = element.text
                elif element.text != None:
                    element.getnext().text = element.text + element.getnext().text
                element.drop_tree()
                counter += 1

    # sort newline and tabbing
    currentGen = [htmlRoot]
    nextGen = []
    genCounter = 0

    while len(currentGen) > 0:
        for item in currentGen:
            if item.tag in blockTags:
                if item.getprevious() != None:
                    item.getprevious().tail = '\n' + genCounter*'\t'
                elif item.getparent() != None:
                    if item.getparent().text == None:
                        item.getparent().text = '\n' + genCounter*'\t'
                    else:
                        item.getparent().text = item.getparent().text + '\n' + genCounter*'\t'
                    item.getparent().getchildren()[-1].tail = '\n' + (genCounter-1)*'\t'
            else:
                if item.getprevious() != None and item.getparent() != None and item.getparent().tag in blocksWithoutInlines:
                    item.getprevious().tail = '\n' + genCounter*'\t'
                elif item.getparent() != None and item.getparent().tag in blocksWithoutInlines:
                    if item.getparent().text == None:
                        item.getparent().text = '\n' + genCounter*'\t'
                    else:
                        item.getparent().text = item.getparent().text + '\n' + genCounter*'\t'
                    item.getparent().getchildren()[-1].tail = '\n' + (genCounter-1)*'\t'
            nextGen = nextGen + item.getchildren()

        currentGen = nextGen
        nextGen = []
        genCounter += 1

    return (htmlRoot)

def replace_back_pages(htmlRoot):
    # h2s = htmlRoot.cssselect('h2')

    def drop_and_replace(h2_to_drop, replacement_html):
        while True:
            next_element = h2_to_drop.getnext()
            try:
                if next_element.tag == 'h2':
                    break
                else:
                    next_element.drop_tree()
            except Exception:
                break
        try:
            h2_to_drop.addnext(replacement_html)
        except Exception:
            pass
        h2_to_drop.drop_tree()

    witnessText = html.parse(Required['witnessText']).getroot().getchildren()[0].getchildren()[0]
    writEvText = html.parse(Required['writEvText']).getroot().getchildren()[0].getchildren()[0]
    pastRepText = html.parse(Required['pastRepText']).getroot().getchildren()[0].getchildren()[0]

    # for h2 in h2s:
    for h2 in htmlRoot.iter('h2'):
        if h2.text_content().strip().lower() == 'witnesses' or h2.text_content().strip().lower() == 'witness':
            drop_and_replace(h2, witnessText)

        elif h2.text_content().strip().lower() == 'published written evidence':
            drop_and_replace(h2, writEvText)

        elif h2.text_content().strip().lower() == 'list of reports from the committee during the current parliament':
            drop_and_replace(h2, pastRepText)

    return (htmlRoot)


def separate_summary(htmlRoot):

    def move_sibs(start, stop, destination):
        siblingIterator = start.itersiblings()
        destination.append(start)
        for sibling in siblingIterator:
            if sibling == stop:
                break
            # do we want to move or copy the summary?
            # MOVE
            destination.append(sibling)

            # COPY
            # perhaps it would be faster to copy the root rarther than many small elements..?
            # destination.append(deepcopy(sibling))

    # elements = htmlRoot.cssselect('h2, .SummaryHeading')
    elements = htmlRoot.xpath('//h2 |  //*[@class="SummaryHeading"]')

    summary_start = None
    for element in elements:
        if str(element.text_content()).strip() in ('Summary', '***Summary'):
            summary_start = element
            siblingIterator = element.itersiblings(preceding=False)
            for sibling in siblingIterator:
                if sibling.tag == 'h2' or sibling.get('class', None) == 'ChapterHeading1':
                    report_start = sibling
                    break

    summary = html.Element('div', attrib={'id': 'summary'})
    summary.tail = '\n'
    report = html.Element('div', attrib={'id': 'report'})
    report.tail = '\n'

    # print(report_start)
    if summary_start is not None:
        move_sibs(summary_start, report_start, summary)
    move_sibs(report_start, None, report)

    return summary, report


def conclusion_recommendation(htmlRoot):
    spans = htmlRoot.xpath(
        '//span[@class="Recommendation"]|//span[@class="Conclusion"]')
    for span in spans:
        if span.get('class') == 'Conclusion':
            span.tag = 'strong'
        else:
            # recomendations are bold and italic
            span.tag = 'em'
            parent = span.getparent()
            if parent is not None and parent.tag != 'strong':
                # wrap the element in a strong
                strong = html.Element('Strong')
                span.addprevious(strong)
                strong.insert(0, span)

    return htmlRoot


def no_toc_footnote_heading(htmlRoot):
    heading_texts = htmlRoot.xpath('//h1/text()|//h2/text()|//h3/text()')
    # print(headings)
    # the footnotes heafing is usualy on of the last
    for heading_text in reversed(heading_texts):
        if heading_text.lower() == 'footnotes':
            heading_element = heading_text.getparent()
            heading_element.classes.discard('contents-heading')
            break
    return htmlRoot

# def add_back_to_top(htmlRoot):
#     report_body = htmlRoot.find('.//div[@id="report-body"]')
#     if report_body is not None:
#         report_body.append(html.fromstring(
#             '<a href="#" id="back-to-top-link">'
#             '<svg class="app-back-to-top__icon" height="17" viewBox="0 0 13 17" width="13" xmlns="http://www.w3.org/2000/svg">'
#             '<path d="M6.5 0L0 6.5 1.4 8l4-4v12.7h2V4l4.3 4L13 6.4z" fill="currentColor"></path>'
#             '</svg> Back to top'
#             '</a>'))
#     else:
#         print('cant find report body')
#     return htmlRoot


def convert_box_tables(htmlRoot):
    tables = htmlRoot.iter('table')
    for table in tables:
        cells = table.xpath('.//td')
        rows  = table.xpath('.//tr')

        if len(cells) == 1 and len(rows) == 1:
            cells[0].drop_tag()
            rows[0].drop_tag()
            # colgroups = table.cssselect('colgroup')
            # cols      = table.cssselect('col')
            # tbodies   = table.cssselect('tbody')
            # for item in colgroups + cols + tbodies:
            for item in table.xpath('.//colgroup | .//col | .//tbody'):
                item.drop_tag()
            table.attrib['class'] = 'callout'
            table.tag = 'div'
    return htmlRoot


def add_classes_to_tables(htmlRoot):
    tables = htmlRoot.xpath('//table')
    for table in tables:
        cells = table.xpath('.//td')
        rows  = table.xpath('.//tr')

        if len(cells) > 0 and len(rows) > 0:
            table.set('class', 'table table-bordered header-cell')

    return htmlRoot



def correct_internal_links(htmlRoot):
    # elements = htmlRoot.cssselect('[href*="IDExport.html"]')
    elements = htmlRoot.xpath('.//*[@href and contains(@href, "IDExport.html")]')
    for element in elements:
        element.attrib['href'] = element.attrib['href'][13:]
    return htmlRoot

def add_footnote_heading(htmlRoot):
    # target = htmlRoot.cssselect('#ftn1')[0]
    target = htmlRoot.find('.//*[@id="ftn1"]')

    # I think all the below is for InDesign stuff
    # if not iselement(iselement):
    #     # target = htmlRoot.cssselect('div[class=_idFootnotes]')[0]
    #     target = htmlRoot.find('.//div[@class="_idFootnotes"]')

    footnoteHeading = html.Element('h1')
    footnoteHeading.text = 'Footnotes'
    target.addprevious(footnoteHeading)
    return htmlRoot

def fix_fm_tables(htmlRoot):
    fmTables = list(htmlRoot.iter('table'))
    print('No. fmTables: ', len(fmTables))
    for tab in fmTables:
        tab.find('.//colgroup').drop_tree()
        ps = tab.iter('p')
        for p in ps:
            if not p.text:
                p.drop_tree()
            else:
                p.tag = 'td'
        # double_tds = tab.cssselect('td td')
        double_tds = tab.xpath('.//td/td')
        for double_td in double_tds:
            # why are we doing this?
            double_td.getparent().drop_tag()

        # rows = tab.cssselect('tr')

    return htmlRoot
