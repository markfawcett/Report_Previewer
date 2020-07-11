from lxml import html  # type: ignore
from lxml.etree import Element  # type: ignore
import re


def drop_most_divs(htmlRoot):
    # remove divs not belonging to footnotes
    divs = htmlRoot.iter('div')
    for div in divs:
        try:
            if div.attrib['id'][0:3] != 'ftn':
                div.drop_tag()
        except:
            try:
                div.drop_tag()
            except:
                pass

    return(htmlRoot)


# changed by mark
def chage_class_names(htmlRoot, classes):
    for class_tupple in classes:

        for paras in htmlRoot.xpath(f'//p[@class="{class_tupple[0]}"]'):
            paras.set('class', class_tupple[1])

    return htmlRoot


def format_footnotes(htmlRoot):
    footnotes = htmlRoot.xpath('//div//p[@class="MsoFootnoteText"]')

    for footnote in footnotes:
        parent = footnote.getparent()
        parent.tag = 'p'
        parent.set('class', 'FootnoteText')
        footnote.drop_tag()

        try:
            # footnote_reference = parent.cssselect("span[class=MsoFootnoteReference] span[class=MsoFootnoteReference] span")[0]
            epath = './/span[@class="MsoFootnoteReference"]//span[@class="MsoFootnoteReference"]//span'
            footnote_reference = parent.find(epath)
            footnote_reference.text = footnote_reference.text.strip('[]')
            # if footnote_reference.text[0] == '[':
            #     footnote_reference.text = footnote_reference.text[1:]
            # if footnote_reference.text[-1] == ']':
            #     footnote_reference.text = footnote_reference.text[:-1]
        except:
            pass

        spans = parent.iter('span')
        for span in spans:
            try:
                if span.attrib['class'] == 'MsoFootnoteReference' or span.attrib['class'] == "MsoHyperlink":
                    span.attrib.pop('class')
            except:
                pass
            try:
                if len(span.attrib) == 0:
                    span.drop_tag()
            except:
                pass

    return (htmlRoot)

def format_footnote_refs(htmlRoot):
    # This must come after the footnotes have been formatted or else it might catch them accidentally
    # foot_refs = htmlRoot.cssselect('a span[class=MsoFootnoteReference] span[class=MsoFootnoteReference] span')
    xpath = '//a//span[@class="MsoFootnoteReference"]/span[@class="MsoFootnoteReference"]/span'
    foot_refs = htmlRoot.xpath(xpath)
    for foot_ref in foot_refs:
        try:
            if foot_ref.text[0] == '[':
                foot_ref.text = foot_ref.text[1:]
            if foot_ref.text[-1] == ']':
                foot_ref.text = foot_ref.text[:-1]
        except:
            pass

        try:
            foot_ref.getparent().getparent().drop_tag()
            foot_ref.getparent().drop_tag()
            foot_ref.tag = 'a'
        except:
            pass

        foot_ref.attrib['href'] = "#" + foot_ref.getparent().attrib['href'][2:]
        foot_ref.getparent().attrib.pop('href')

        try:
            foot_ref.getparent().tag = 'sup'
            foot_ref.getparent().attrib['id'] = foot_ref.getparent().attrib['name']
            foot_ref.getparent().attrib.pop('name')
        except:
            pass

        try:
            if foot_ref.getparent().attrib['title'] == "":
                foot_ref.getparent().attrib.pop('title')
        except:
            pass

    return(htmlRoot)


def fix_ordered_lists(htmlRoot):

    for ordered_class in ['Para1', 'Para2', 'Para3', 'Para4', 'OrderedList1',
                          'CRPara1', 'ChapterHeading1', 'AppendixHeading1']:

        elements = htmlRoot.xpath(f'//*[@class="{ordered_class}"]')

        for element in elements:
            try:
                if (re.fullmatch(r'\({0,1}\d+[\.\)]{0,1}', str(element.text)) is not None
                    or re.fullmatch(r'\({0,1}[a-zA-Z]{1,5}[\.\)]{0,1}', str(element.text)) is not None):
                    span = element.getchildren()[0]
                    if re.fullmatch(r'\s+', span.text) is not None:
                        span.text = ' '
                        try:
                            span.drop_tag()
                        except:
                            pass
            except:
                pass
    return (htmlRoot)


def fix_bullet_points(htmlRoot, bullet_classes):
    # Remove bad Windows bullet points and spacing
    for bullet_class in bullet_classes:

        elements = htmlRoot.xpath(f'//p[@class="{bullet_class}"]')
        for element in elements:
            while True:
                if element.text:
                    if element.text[0] == '·':
                        element.text = element.text[1:]
                    elif element.text[0] == ' ':
                        element.text = element.text[1:]
                    else:
                        break
                else:
                    break
    return htmlRoot


def wrap_uls(htmlRoot, bullet_classes):
    # it seams html is returned with <li>'s  that are not children of an <ul> element.
    # This is after triplets has run. Lets try and fix that
    for bullet_class in bullet_classes:
        elements = htmlRoot.xpath(f'//li[@class="{bullet_class}"]')
        for element in elements:
            if (element.getprevious() is not None and
               element.getprevious().tag == 'li' and
               element.getprevious().get('class', None) == bullet_class):
                continue
            ul_container = Element('ul')
            element.addprevious(ul_container)

            elements_for_ul = [element]

            for sibling in element.itersiblings(preceding=False):
                if sibling.tag != 'li':
                    break
                elements_for_ul.append(sibling)

            ul_container.extend(elements_for_ul)

    return htmlRoot


def separate_summary(htmlRoot):
    firstIndicator = None
    secondIndicator = None


    def drop_sibs(element, backwards=False):
        siblingIterator = element.itersiblings(preceding=backwards)
        for sibling in siblingIterator:
            sibling.drop_tree()

    def move_sibs(start, stop, destination):
        siblingIterator = start.itersiblings()
        destination.append(start)
        for sibling in siblingIterator:
            if sibling != stop:
                destination.append(sibling)
            else:
                break

    elements = htmlRoot.iter('h2')
    for element in elements:
        if str(element.text_content()).count('***'):
            if firstIndicator == None:
                firstIndicator = element
            elif secondIndicator == None:
                secondIndicator = element
            else:
                pass

    if firstIndicator == None:
        pass
        # more code needed - probably change html tag to div id="report" tag

    elif secondIndicator == None:
        summary = None
        report = html.Element('div', attrib={'id': 'report'})
        report.tail = '\n'

        drop_sibs(firstIndicator, backwards=True)
        move_sibs(firstIndicator, None, report)

    else:
        summary = html.Element('div', attrib={'id': 'summary'})
        summary.tail = '\n'
        report = html.Element('div', attrib={'id': 'report'})
        report.tail = '\n'

        drop_sibs(firstIndicator, backwards=True)
        move_sibs(firstIndicator, secondIndicator, summary)
        move_sibs(secondIndicator, None, report)

    return([summary, report])
