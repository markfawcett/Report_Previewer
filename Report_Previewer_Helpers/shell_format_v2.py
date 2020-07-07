from pathlib import Path

from lxml import html  # type: ignore

# local imports
from . import feedback_v2 as feedback
from .settings import REQUIRED as Required


def insert_html_into_new_shell(injection):
    path_to_shell = str(Path(Required['shell']).resolve())
    # print('Path to shell:')
    # print(path_to_shell)
    new_shell = html.parse(path_to_shell).getroot()
    entryPoint = new_shell.cssselect('[id=report-body]')[0]
    entryPoint.append(injection)
    entryPoint.getchildren()[0].drop_tag()
    return(new_shell)


def add_col_row_divs(htmlRoot):
    # Add 'row' and 'col-md-9' divs to h2 sections
    h2s = htmlRoot.cssselect("h2")
    for h2 in h2s:
        row_div = h2.makeelement('div', {'class': 'row'})
        col_div = h2.makeelement('div', {'class': 'col-md-9'})
        row_div.append(col_div)
        h2.addprevious(row_div)

        currentTarget = h2

        while True:
            nextTarget = currentTarget.getnext()
            col_div.append(currentTarget)
            if nextTarget is None:
                break
            elif nextTarget.tag == 'h2':
                break
            else:
                currentTarget = nextTarget
    return (htmlRoot)


def add_ids_for_headings(htmlRoot):
    # Add ids for headings in contents
    h2s = htmlRoot.cssselect('h2')
    for h2 in h2s:
        if 'id' in h2.attrib:
            pass
        else:
            h2.attrib['id'] = "heading-" + str(h2s.index(h2))
    return(htmlRoot)


def add_meta(file, page, meta):

    file = add_col_row_divs(file)
    file = add_ids_for_headings(file)
    file = insert_html_into_new_shell(file)

    try:
        if page == 'summary':
            file.cssselect('#report-title')[0].text = meta['report_title'] + ' – Report Summary'
        elif page == 'report':
            file.cssselect('#report-title')[0].text = meta['report_title']
    except:
        pass


    try:
        if page == 'summary':
            file.cssselect('#full-report-link-container p')[0].text   = 'This is the report summary, '
            file.cssselect('#full-report-link-container p a')[0].text = 'read the full report'
            file.cssselect('#full-report-link-container p a')[0].set('href', 'full-report.html')

        elif page == 'report':
            file.cssselect('#full-report-link-container p')[0].text   = 'This is the full report, '
            file.cssselect('#full-report-link-container p a')[0].text = 'read the report summary'
            file.cssselect('#full-report-link-container p a')[0].set('href', 'report-summary.html')
    except:
        pass


    try:
        if page == 'summary':
            file.cssselect('#report-number')[0].drop_tree()
        elif page == 'report':
            file.cssselect('#report-number')[0].text = meta['report_number'] + ' ' + meta['report_type'] + ' of Session 2017-19'
    except:
        feedback.warning('Report Number and Type not added to the output.')
    try:
        file.cssselect('#report-author')[0].getnext().text = meta['committee_name']
        file.cssselect('#report-author')[0].getnext().attrib['title'] = meta['committee_name'] + ' website'
        file.cssselect('#report-author')[0].getnext().attrib['href'] = meta['committee_address']

    except:
        feedback.warning('Committee name not added to author line in output.')
    try:
        file.cssselect('#report-publication-date')[0].tail = ' ' + meta['publication_date']
    except:
        feedback.warning('Publication Date not added to the output.')

    try:
        file.cssselect('#witness-heading-link')[0].attrib['href'] = meta['inquiry_publications']
        file.cssselect('#writEv-heading-link')[0].attrib['href'] = meta['inquiry_publications']
    except:
        feedback.warning('Inquiry Publications not added to the output.')

    try:
        file.cssselect('#pastRep-heading-link')[0].attrib['href'] = meta['committee_publications']
    except:
        feedback.warning('Committee publications not added to the output.')


    return (file)
