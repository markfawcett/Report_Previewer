from lxml import html
import re

def remove_nonfootnote_divs (htmlRoot):
    divs = htmlRoot.cssselect('div')
    for div in divs:
        try:
            if div.attrib['id'][0:8] != 'footnote':
                div.drop_tag()
        except:
            try:
                div.drop_tag()
            except:
                pass
    return(htmlRoot)



def fix_ordered_lists (htmlRoot):
    for ordered_class in ['Para1', 'Para2', 'Para3', 'Para4', 'OrderedList1', 'ChapterHeading1', 'AppendixHeading1']:
        
        elements = htmlRoot.cssselect('*[class=' + ordered_class + ']')

        for element in elements:
            try:
                span = element.getchildren()[0]
                if span.tag == 'span':                
                    if re.fullmatch(r'\({0,1}\d+[\.\)]{0,1}', str(span.text)) != None:
                        span.text = str(span.text) + ' '
                    elif re.fullmatch(r'\({0,1}[a-zA-Z][\.\)]{0,1}', str(span.text)) != None:
                        span.text = str(span.text) + ' '
            except:
                pass
    return (htmlRoot)

def fix_footnotes (htmlRoot):
    divs =  htmlRoot.cssselect('div')
    for div in divs:

        ## Test to see if it's a footnote div by checking the id
        try:
            if div.attrib['id'].index('footnote-') == 0:
                hasFootnoteId = True
            else:
                hasFootnoteId = False
        except:
            hasFootnoteId = False

        if hasFootnoteId == True:
            footnoteId =  div.attrib['id']
            footnotePara = div.cssselect('p')[0]
            footnotePara.attrib['class'] = 'FootnoteText'
            footnotePara.attrib['id'] = footnoteId
            footnotePara.cssselect('a')[0].tail = ' '
            div.drop_tag()
        else:
            pass
    return (htmlRoot)

def fix_footnote_refs (htmlRoot):
    ### Fix footnotes references
    footnoteRefs = htmlRoot.cssselect('span>span[id|=footnote]')
    for footnoteRef in footnoteRefs:
        footnoteRef.getparent().drop_tag()
        footnoteRef.tag = 'sup'
        footnoteRef.attrib['class'] = 'footnote-reference'

    return (htmlRoot)


            
