from lxml import html
from lxml.etree import Element

from . import feedback_v2 as feedback
from .settings import REQUIRED as Required


def print_html(summary_html, **kwargs):
    # read in the print report shell
    print_shell = html.parse(Required['print_shell']).getroot()

    # add meta
    try:
        print_shell.xpath('//h1[@id="report-title"]')[0].text = kwargs['report_title']
    except:
        pass

    try:
        print_shell.xpath('//h2[@id="report-published-date"]')[0].text = kwargs['publication_date']
    except:
        pass

    try:
        print_shell.xpath('//h2[@id="committee-name"]')[0].text = kwargs['committee_name']
    except:
        pass

    try:
        print_shell.xpath('//head/title')[0].text = kwargs['report_title'] + ' - Report Summary'
    except:
        pass


    # we only want the report-body
    report_body = summary_html.xpath('//div[@id="report-body"]')

    if len(report_body) == 0:
        feedback.warning('Can\'t find the report body in the html so '
                         'no print version of the summary could be produced')
        return None

    body = print_shell.find('body')
    body.extend(report_body)  # will work even if there is more that one report-body

    # look through report-body for elements that should be in an `recommendations-container`
    recomendations_headings = body.xpath('.//h3[contains(text(),"ecommendations")]')

    for recomendations_heading in recomendations_headings:
        recommendations_container = Element('div')
        recommendations_container.set('class', 'recommendations_container')
        recomendations_heading.addprevious(recommendations_container)

        elements_for_div = [recomendations_heading]

        for sibling in recomendations_heading.itersiblings(preceding=False):
            if sibling.tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                break
            elements_for_div.append(sibling)

        recommendations_container.extend(elements_for_div)

    return(print_shell)








