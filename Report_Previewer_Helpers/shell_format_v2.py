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
    entryPoint = new_shell.find('.//*[@id="report-body"]')
    entryPoint.append(injection)
    entryPoint[0].drop_tag()
    return(new_shell)


def add_col_row_divs(htmlRoot):
    """Add 'row' and 'col-md-9' divs to h2 sections"""
    h2s = htmlRoot.xpath('//h2')
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
    h2s = htmlRoot.xpath('//h2')
    for h2 in h2s:
        if 'id' in h2.attrib:
            pass
        else:
            h2.attrib['id'] = "heading-" + str(h2s.index(h2))
    return(htmlRoot)


def add_meta(file, page, meta):

    file = add_col_row_divs(file)  # what is the point of this?
    file = add_ids_for_headings(file)
    file = insert_html_into_new_shell(file)

    try:
        report_title_ele = file.find('.//*[@id="report-title"]')
        if page == 'summary':
            report_title_ele.text = meta['report_title'] + ' – Report Summary'
        elif page == 'report':
            report_title_ele.text = meta['report_title']
    except:
        pass


    try:
        p_ele  = file.find('.//*[@id="full-report-link-container"]//p')
        pa_ele = file.find('.//*[@id="full-report-link-container"]//p//a')
        if page == 'summary':
            p_ele.text  = 'This is the report summary, '
            pa_ele.text = 'read the full report'
            # TODO: make full report and report summary link to each other
            pa_ele.set('href', 'full-report.html')

        elif page == 'report':
            p_ele.text   = 'This is the full report, '
            pa_ele.text = 'read the report summary'
            pa_ele.set('href', 'report-summary.html')
    except:
        pass


    try:
        report_number_ele = file.find('.//*[@id="report-number"]')
        if page == 'summary':
            report_number_ele.drop_tree()
        elif page == 'report':
            report_number_ele.text = f"{meta['report_number']} {meta['report_type']} of Session 2017-19"
    except:
        feedback.warning('Report Number and Type not added to the output.')
    try:
        report_author_ele = file.find('.//*[@id="report-author"]')
        report_author_ele.getnext().text = meta['committee_name']
        report_author_ele.getnext().set('title',  meta['committee_name'] + ' website')
        report_author_ele.getnext().set('href',  meta['committee_address'])
    except:
        feedback.warning('Committee name not added to author line in output.')

    try:
        file.find('.//*[@id="report-publication-date"]').tail = ' ' + meta['publication_date']
    except:
        feedback.warning('Publication Date not added to the output.')

    try:
        file.find('.//*[@id="witness-heading-link"]').set('href', meta['inquiry_publications'])
        file.find('.//*[@id="writEv-heading-link"]').set('href', meta['inquiry_publications'])
    except:
        feedback.warning('Inquiry Publications not added to the output.')

    try:
        file.find('.//*[@id="pastRep-heading-link"]').set('href', meta['committee_publications'])
    except:
        feedback.warning('Committee publications not added to the output.')


    return file
