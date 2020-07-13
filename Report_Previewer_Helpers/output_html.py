from __future__ import annotations  # for type annotations
from copy import deepcopy
import os
from pathlib import Path
from typing import Optional, Tuple, Union
import webbrowser
from distutils import dir_util

# Import third-party modules
from lxml import html  # type: ignore
from lxml.etree import _Element, Element, ElementTree  # type: ignore

# Local imports
from . import feedback
import Report_Previewer_Helpers.settings as st
from .settings import REQUIRED as Required


OutputPaths = {'report_web': Path(st.REPORT),
               'summary_web': Path(st.SUMMARY),
               'report_print': Path(st.REPORT_PRINT),
               'summary_print': Path(st.SUMMARY_PRINT)}

def set_up(input_htmp_Path: Path):

    output_folder_Path = input_htmp_Path.parent.parent

    for key, value in OutputPaths.items():
        OutputPaths[key] = output_folder_Path / value

    # copy css etc
    # try:
    Required['templates_dir']
    dir_util.copy_tree(Required['templates_dir'], str(output_folder_Path))
    # except:
    #     pass


class ReportHTML:

    # print(Required.get('templates_dir'))
    def __init__(self, html_: Union[Path, _Element], meta: dict):
        self.metadata = meta

        if isinstance(html_, _Element):
            self.root = html_
            self.html_tree = ElementTree(self.root)
        else:
            self.html_tree = html.parse(str(html_))
            self.root = self.html_tree.getroot()


    def write(self, output_file_path: Union[Path, str], open_in_browser=True, verbose=True):

        # lxml requires paths to be strings
        output_file_path = str(output_file_path)

        # use lxml.ElementTree's write method to write out
        self.html_tree.write(output_file_path, method="html",
                             encoding='UTF-8', doctype='<!DOCTYPE html>')

        if verbose: print(output_file_path)

        # try to open in a web browser
        try:
            if open_in_browser:
                if os.name == 'posix':
                    webbrowser.open('file://' + output_file_path)
                else:
                    webbrowser.open(output_file_path)
        except:
            pass


class OutputHTML(ReportHTML):
    def __init__(self, meta: dict, shell=''):
        if not shell:
            path_to_shell = str(Path(Required['shell']).resolve())
        else:
            path_to_shell = shell
        super().__init__(path_to_shell, meta)

        # the path where we will save this file...
        # self.output_Path = ''

        # where elements will be appended
        self.entryPoint = self.root.find('.//*[@id="report-body"]')

    def make_print_version(self) -> Optional[OutputHTML]:

        meta = self.metadata

        # read in the print report shell
        shell = OutputHTML(meta, shell=Required['print_shell'])

        # add meta-data
        shell.root.find(
            './/h1[@id="report-title"]').text = meta.get('report_title', '')
        shell.root.find(
            './/h2[@id="report-published-date"]').text = meta.get('publication_date', '')
        shell.root.find(
            './/h2[@id="committee-name"]').text = meta.get('committee_name', '')
        shell.root.find(
            './/head/title').text = meta.get('report_title', '') + ' - Report Summary'

        # we only want the report-body (theoretically there could be more than one)
        report_body = deepcopy(self.root.xpath('//div[@id="report-body"]'))

        if len(report_body) == 0:
            feedback.warning('Can\'t find the report body in the html so '
                             'no print version could be produced')
            return None

        body = shell.root.find('body')
        body.extend(report_body)  # will work even if there is more that one report-body

        # look through report-body for elements that should be in an `recommendations-container`
        recomendations_headings = body.xpath('.//h3[contains(text(),"ecommendations")]')

        for heading in recomendations_headings:
            container_div = Element('div')
            container_div.set('class', 'recommendations_container')
            heading.addprevious(container_div)

            elements_for_div = [heading]

            for sibling in heading.itersiblings(preceding=False):
                if sibling.tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                    break
                elements_for_div.append(sibling)

            container_div.extend(elements_for_div)

        return shell


def separate_summary(html_: ReportHTML) -> Tuple[Optional[OutputHTML], Optional[OutputHTML]]:
    """Separates the HTML into a summary and a main report"""

    def move_sibs(start, stop, destination):
        siblingIterator = start.itersiblings()
        destination.append(start)
        for sibling in siblingIterator:
            if sibling == stop:
                break
            # do we want to move or copy the summary?
            destination.append(sibling)  # MOVE
            # COPY - perhaps it would be faster to copy the root rather than many small elements..?
            # destination.append(deepcopy(sibling))

    elements = html_.root.xpath('//h2 |  //*[@class="SummaryHeading"]')

    summary_start = None
    report_start = None
    for element in elements:
        if str(element.text_content()).strip() in ('Summary', '***Summary'):
            summary_start = element
            siblingIterator = element.itersiblings(preceding=False)
            for sibling in siblingIterator:
                if sibling.tag == 'h2' or sibling.get('class', None) == 'ChapterHeading1':
                    report_start = sibling
                    break

    summary_e = html.Element('div', attrib={'id': 'summary'})
    summary_e.tail = '\n'

    report_e = html.Element('div', attrib={'id': 'report'})
    report_e.tail = '\n'

    # print(report_start)
    summary: Optional[OutputHTML] = None
    report: Optional[OutputHTML] = None

    if summary_start is not None:
        move_sibs(summary_start, report_start, summary_e)
        summary = _web_html(summary_e, 'summary', html_.metadata)

    if summary_start is not None:
        move_sibs(report_start, None, report_e)
        report = _web_html(report_e, 'report', html_.metadata)

    # link the files together
    p_epath  = './/*[@id="full-report-link-container"]//p'
    pa_epath = './/*[@id="full-report-link-container"]//p//a'
    if summary:
        summary.root.find(p_epath).text  = 'This is the report summary, '
        pa_ele = summary.root.find(pa_epath)
        pa_ele.text = 'read the full report'
        pa_ele.set('href', str(OutputPaths['report_web'].name))
    if report:
        report.root.find(p_epath).text   = 'This is the full report, '
        pa_ele = report.root.find(pa_epath)
        pa_ele.text = 'read the report summary'
        pa_ele.set('href', str(OutputPaths['summary_web'].name))

    return summary, report


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


def add_ids_for_headings(htmlRoot):
    """Add ids for headings in contents"""
    h2s = htmlRoot.xpath('//h2')
    for h2 in h2s:
        if 'id' in h2.attrib:
            pass
        else:
            h2.attrib['id'] = "heading-" + str(h2s.index(h2))


def _web_html(element: _Element, page: str, meta: dict) -> OutputHTML:

    add_col_row_divs(element)  # what is the point of this?
    add_ids_for_headings(element)
    # root = insert_html_into_new_shell(root)

    output_html = OutputHTML(meta)
    shell_root = output_html.root

    try:
        report_title_ele = shell_root.find('.//*[@id="report-title"]')
        if page == 'summary':
            report_title_ele.text = meta['report_title'] + ' – Report Summary'
        elif page == 'report':
            report_title_ele.text = meta['report_title']
    except:
        pass

    try:
        report_number_ele = shell_root.find('.//*[@id="report-number"]')
        if page == 'summary':
            report_number_ele.drop_tree()
        elif page == 'report':
            report_number_ele.text = f"{meta['report_number']} {meta['report_type']} of Session 2017-19"
    except Exception as e:
        feedback.warning(f'Report Number and Type not added to the output. {e}')
    try:
        report_author_ele = shell_root.find('.//*[@id="report-author"]')
        report_author_ele.getnext().text = meta['committee_name']
        report_author_ele.getnext().set('title',  meta['committee_name'] + ' website')
        report_author_ele.getnext().set('href',  meta['committee_address'])
    except Exception as e:
        feedback.warning(f'Committee name not added to author line in output. {e}')

    try:
        shell_root.find('.//*[@id="report-publication-date"]').tail = ' ' + meta['publication_date']
    except Exception as e:
        feedback.warning(f'Publication Date not added to the output. {e}')

    try:
        shell_root.find('.//*[@id="witness-heading-link"]').set('href', meta['inquiry_publications'])
        shell_root.find('.//*[@id="writEv-heading-link"]').set('href', meta['inquiry_publications'])
    except Exception as e:
        feedback.warning(f'Inquiry Publications not added to the output. {e}')

    try:
        shell_root.find('.//*[@id="pastRep-heading-link"]').set('href', meta['committee_publications'])
    except Exception as e:
        feedback.warning(f'Committee publications not added to the output. {e}')


    output_html.entryPoint.append(element)
    # I think if we did extend instead of append we would not have, <div id="report"> in the output
    # output_html.entryPoint.extend(element)
    return output_html
