from __future__ import annotations  # for type annotations
from copy import deepcopy
import os
from pathlib import Path
import re
from typing import Dict, Optional, Tuple, Union
import webbrowser
from distutils import dir_util
from distutils.errors import DistutilsFileError

# Import third-party modules
from lxml import html  # type: ignore
from lxml.etree import _Element, Element, ElementTree  # type: ignore

# Local imports
from . import feedback
import Report_Previewer_Helpers.settings as st
from .settings import REQUIRED as Required


# # must be copied each time we run
# OutputPaths = {}

# def set_up(input_htmp_Path: Path, report_title: str = ''):

#     # copy all the output paths - must happen every time we run
#     global OutputPaths
#     OutputPaths = {'report_web': Path(st.REPORT),
#                    'summary_web': Path(st.SUMMARY),
#                    'report_print': Path(st.REPORT_PRINT),
#                    'summary_print': Path(st.SUMMARY_PRINT)}

#     # we don't want any stupidly long file names so lets tuncate them
#     report_title = report_title[:50]
#     # ascii only
#     report_title = report_title.encode('ascii', 'ignore').decode()
#     # make lowercase and remove space from ends
#     report_title = report_title.strip().lower()
#     # dont allow anything that is not a word, space or -
#     report_title = re.sub(r'[^\w\s-]', '', report_title)
#     # no spaces
#     report_title = re.sub(r'[-\s]+', '-', report_title)

#     output_folder_Path = input_htmp_Path.parent.parent

#     for key, value in OutputPaths.items():
#         file_name = f'{report_title}-{value}'
#         OutputPaths[key] = output_folder_Path / file_name

#     # copy css etc
#     # try:
#     Required['templates_dir']
#     dir_util.copy_tree(Required['templates_dir'], str(output_folder_Path))
#     # except:
#     #     pass


class ReportHTML:

    # temporary values
    report_web = Path(st.REPORT)
    summary_web = Path(st.SUMMARY)
    report_print = Path(st.REPORT_PRINT)
    summary_print = Path(st.SUMMARY_PRINT)

    img_folder = ''

    # _set_up_done = False

    @classmethod
    def set_up(cls, html_path: Union[Path, str], meta: dict):

        print('Copying files.')

        html_Path = Path(html_path)

        file_title = meta.get('report_title', '')
        # we don't want any stupidly long file names so lets truncate them
        file_title = file_title[:50]
        # ascii only
        file_title = file_title.encode('ascii', 'ignore').decode()
        # make lowercase and remove space from ends
        file_title = file_title.strip().lower()
        # don't allow anything that is not a word, space or -
        file_title = re.sub(r'[^\w\s-]', '', file_title)
        # no spaces
        file_title = re.sub(r'[-\s]+', '-', file_title)

        cls.img_folder = f'{file_title}-files'

        output_folder_Path = html_Path.parent.parent

        # affect the class attributes
        ReportHTML.report_web    = output_folder_Path / f'{file_title}-{st.REPORT}'
        ReportHTML.summary_web   = output_folder_Path / f'{file_title}-{st.SUMMARY}'
        ReportHTML.report_print  = output_folder_Path / f'{file_title}-{st.REPORT_PRINT}'
        ReportHTML.summary_print = output_folder_Path / f'{file_title}-{st.SUMMARY_PRINT}'

        # print(ReportHTML.report_web, ReportHTML.summary_web,
        #       ReportHTML.report_print, ReportHTML.summary_print, sep='\n')

        # copy css etc
        try:
            Required['templates_dir']
            dir_util.copy_tree(Required['templates_dir'], str(output_folder_Path))
        except Exception:
            feedback.error('Could not copy CSS etc. HTML file may not appear styled correctly.')

        # copy any images that may be in a word_filtered_html_files folder
        # remember to also change all the paths in the html
        try:
            dir_util.copy_tree(str(html_Path.parent / 'word_filtered_html_files'),
                               str(output_folder_Path / cls.img_folder))
        except DistutilsFileError:
            pass
        except Exception:
            feedback.error('Could not copy any Images etc.')

        # cls._set_up_done = True

    def __init__(self, html_path: Union[Path, str], meta: dict):
        self.metadata = meta

        # lxml requires a string (not Path)
        self.html_tree = html.parse(str(html_path))
        self.root = self.html_tree.getroot()

        # if not self._set_up_done:
        #     ReportHTML._set_up(html_path, meta)



    def write(self, output_file_path: Union[Path, str], open_in_browser=True, verbose=True):

        # lxml requires paths to be strings
        output_file_path = str(output_file_path)

        # use lxml.ElementTree's write method to write out
        self.html_tree.write(output_file_path, method="html",
                             encoding='UTF-8', doctype='<!DOCTYPE html>')

        if verbose:
            print(output_file_path)
            print('self is')
            print(f'{self.report_web=}', f'{self.summary_web=}',
                  f'{self.report_print=}', f'{self.summary_print}')



        # try to open in a web browser
        try:
            if open_in_browser:
                if os.name == 'posix':
                    webbrowser.open('file://' + str(Path(output_file_path).resolve()))
                else:
                    webbrowser.open(output_file_path)
        except Exception:
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

        # remove non-breaking spaces as oxygen PDF chemistry does not like them
        for ele in body.iter():
            if ele.text:
                ele.text = ele.text.replace('\u00A0', ' ')  # remove no break space
                ele.text = ele.text.replace('\u00AD', '')  # remove discretionary hyphens
            if ele.tail:
                ele.tail = ele.tail.replace('\u00A0', ' ')  # remove no break space
                ele.tail = ele.tail.replace('\u00AD', '')  # remove discretionary hyphens

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

    # sometimes there is no summary
    if not report_start:
        xpath = '//h2 |  //*[@class="SummaryHeading"] | //*[@class="ChapterHeading1"]'
        headings = html_.root.xpath(xpath)
        if headings:
            report_start = headings[0]

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

    if report_start is not None:
        move_sibs(report_start, None, report_e)
        report = _web_html(report_e, 'report', html_.metadata)

    # link the files together
    p_epath  = './/*[@id="full-report-link-container"]//p'
    pa_epath = './/*[@id="full-report-link-container"]//p//a'
    if summary:
        summary.root.find(p_epath).text  = 'This is the report summary, '
        pa_ele = summary.root.find(pa_epath)
        pa_ele.text = 'read the full report'
        # pa_ele.set('href', str(OutputPaths['report_web'].name))
        pa_ele.set('href', str(ReportHTML.report_web.name))
    if report:
        report.root.find(p_epath).text   = 'This is the full report, '
        pa_ele = report.root.find(pa_epath)
        pa_ele.text = 'read the report summary'
        # pa_ele.set('href', str(OutputPaths['summary_web'].name))
        pa_ele.set('href', str(ReportHTML.summary_web.name))

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
