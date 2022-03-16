#!/usr/bin/env python

# std library imports
from copy import deepcopy
import os
from pathlib import Path
import sys
import time
import traceback
from typing import Dict

# Import third-party modules
from lxml import html  # type: ignore
from watchdog.observers import Observer  # type: ignore
from watchdog.events import PatternMatchingEventHandler  # type: ignore

# Import local modules
try:
    import Report_Previewer_Helpers.feedback   as feedback
    import Report_Previewer_Helpers.settings   as st
    import Report_Previewer_Helpers.triplets   as triplets
    import Report_Previewer_Helpers.univ_html  as univ_html
    import Report_Previewer_Helpers.word_html  as word_html
    import Report_Previewer_Helpers.output_html as output_html
    import Report_Previewer_Helpers.cli_interface as cli
except ModuleNotFoundError as e:
    print('Error: The script requires the Report_Previewer_Helpers folder.\n', e)

ReportHTML = output_html.ReportHTML


def main():

    # - if the command receives command line arguments assume we want the cmd_line version
    if len(sys.argv) > 1:
        cli.run(process_html)
        return

    # - otherwise to the watching thing

    # feedback.writeln('Username:\t' + feedback.USERNAME)

    # create event handler for watched folder
    patterns = ["*.htm", '*.html']
    ignore_patterns = ['*.txt', '*$*']

    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns,
                                                ignore_directories=True,
                                                case_sensitive=True)
    event_handler.on_created = lambda x: on_created(x, watched_Path)

    # create cross platform path to folder to watch
    watched_Path = Path(Path.home(), 'committee_report_html/word_filtered_html')

    # create folder to watch if it does not already exist
    if not watched_Path.exists():
        watched_Path.mkdir(parents=True, exist_ok=True)

    my_observer = Observer()
    my_observer.schedule(event_handler, str(watched_Path),
                         recursive=False)  # not interested in sub-directories

    # print('\nWaiting for files to be added to:\n  {}\n'.format(watched_Path))
    wait_msg(watched_Path)
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


def wait_msg(watched_Path):
    print('\nWaiting for files to be added to:\n  {}\n'.format(watched_Path))

def roubust_execution(funcs, input_html):
    for func in funcs:
        # global input_html
        if not isinstance(func, list):
            # if(type(func) != type([])):
            print('\t', func.__name__)
            try:
                input_html = func(input_html)
            except Exception as e:
                feedback.writeln('\t\t' + str(e))
        else:
            print('\t', func[0].__name__)
            try:
                input_html = func[0](input_html, func[1])
            except Exception as e:
                feedback.writeln('\t\t' + str(e))


def on_created(event, watched_Path):

    def wait_for_file(file):
        """ wait for file to finish being created or copied"""
        historicalSize = -1
        while (historicalSize != os.path.getsize(file)):
            historicalSize = os.path.getsize(file)
            time.sleep(1)

    html_Path = Path(event.src_path)

    # wait for file to finish being created/copied
    wait_for_file(html_Path)
    print(f"New HTML file created:\n  {event.src_path}")

    parameters_file = html_Path.parent.joinpath('parameters.txt')
    print(f'Looking for required parameters file\n  {str(parameters_file)}')

    if not parameters_file.exists():
        feedback.error(
            f'there is no parameters file associated with  {html_Path.name}'
            '\nthe parameters file is required and is expected to be saved in the following folder:'
            f'\n{html_Path.parent}')

        return

    wait_for_file(parameters_file)

    input_params = {}

    with open(parameters_file, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines, start=1):
        line = line.strip()

        if not line: continue  # skip blank lines

        key_value = line.split('\t')
        if len(key_value) != 2:
            feedback.warning(f'The parameters file has an error in line {i}.\n  Line {i}:  {line}\n'
                             f'  Expected key followed by tab followed by value')
        else:
            input_params[key_value[0].strip()] = key_value[1].strip()


    # input_html = ReportHTML(html_Path, parameters)
    process_html(html_Path, input_params)

    # I wonder if we should now delete both parameters.txt and the html_Path
    html_Path.unlink(missing_ok=True)  # deletes the file
    parameters_file.unlink(missing_ok=True)

    # reprint wait message
    wait_msg(watched_Path)


def check_metadate(metadata: Dict[str, str]) -> Dict[str, str]:

    expected_parameters = deepcopy(st.EXPECTED_PARAMETERS)
    expected_parameters.update(metadata)

    for key, value in expected_parameters.items():
        if not value:
            feedback.warning(f'Expected parameter {key} is either not present or has no value.'
                              ' The outputted HTML will be incomplete without this.')

    return expected_parameters


# def process_html(input_html: ReportHTML, input_Path: Path):
def process_html(input_html_Path: Path, metadata: Dict[str, str]):

    print('\nProcessing HTML....\n')


    # process the metadata
    metadata = check_metadate(metadata)
    # try adding data from settings.py to metadata
    c_name = metadata['committee_name']  # could still be ''
    committee_address = st.COMMITTEES_AND_ADDRESSES.get(c_name, ['', ''])
    # if committee_name is the empty string both the below will be the empty string too
    metadata['committee_address'], metadata['committee_publications'] = committee_address


    # if the report title has been passed in as we should add it to the output
    # output_html.set_up(input_html_Path, report_title=metadata['report_title'])
    ReportHTML.set_up(input_html_Path, metadata)

    input_html = ReportHTML(input_html_Path, metadata)

    # changed to set
    accepted_classes = {'contents-heading', 'UnorderedList1', 'UnorderedList2', 'FootnoteText',
                        'figure-caption', 'caption', 'callout', 'text-center', 'text-right',
                        'table', 'table-bordered',  'header-cell'}

    # remove the word vs indesign version
    # if source == "Word":
    funcs = (
        univ_html.drop_head,
        univ_html.add_footnote_heading,
        [univ_html.drop_unwanted_attributes, ['style']],
        word_html.drop_most_divs,
        univ_html.drop_cover,
        univ_html.size_images,
        word_html.format_footnotes,  # must run before footnote_refs function
        word_html.format_footnote_refs,  # must run after format_footnotes function
        [word_html.chage_class_names, [('MsoCaption', 'figure-caption')]],  # NEW
        [univ_html.drop_unwanted_attributes, [
            # --------------------------------------------- I am not sure about align
            'name', 'border', 'cellspacing', 'cellpadding', 'width', 'height', 'align']],
        [univ_html.drop_pointless_tags, ['a']],
        # name attribute must be cleared but pointless spans must still be there
        word_html.fix_ordered_lists,
        [univ_html.drop_pointless_tags, ['span', 'a']],
        [word_html.fix_bullet_points, ['UnorderedList1', 'BoxUnorderedList1']],
        univ_html.convert_box_tables,
        univ_html.add_classes_to_tables,
        univ_html.fix_blockquotes,
        univ_html.correct_internal_links,
        univ_html.conclusion_recommendation,  # must be before keep_only_accepted_classes
        # [triplets.map_classes_and_tags, [source]],
        [triplets.map_classes_and_tags, ['Word']],  # only use word version atm
        [word_html.wrap_uls, ['UnorderedList1', 'UnorderedList2', 'BoxUnorderedList1']],
    )
    roubust_execution(funcs, input_html.root)

    # final functions are the same regardless of source
    funcs = ([univ_html.keep_only_accepted_classes, accepted_classes],  # type: ignore
             univ_html.tidy_cycle,
             univ_html.generic_clean,
             univ_html.tidy_cycle,  # deliberately repeated
             univ_html.free_img,    # must be before add rules
             univ_html.add_rules,   # must be after the triplets
             # univ_html.add_back_to_top,
             univ_html.no_toc_footnote_heading,
             univ_html.replace_back_pages)
    roubust_execution(funcs, input_html.root)

    # fix images
    fix_images(input_html.root)

    summary, report = output_html.separate_summary(input_html)

    if summary:  # could be None
        print('\nCreating summary:')
        # summary.write(output_html.OutputPaths['summary_web'])
        summary.write(ReportHTML.summary_web, verbose=True)

        # lets also have a go at creating a print-summary
        print_summary = summary.make_print_version()
        if print_summary:
            # print_summary.write(output_html.OutputPaths['summary_print'], open_in_browser=False)
            print_summary.write(ReportHTML.summary_print, open_in_browser=False, verbose=True)
            # try running oxygen PDF chemistry if it exists
    else:
        feedback.warning('Summary not created')

    if report:
        print('\nCreating full report')
        # report.write(output_html.OutputPaths['report_web'])
        report.write(ReportHTML.report_web, verbose=True)

        print_report = report.make_print_version()
        if print_report:
            # print_report.write(output_html.OutputPaths['report_print'], open_in_browser=False)
            print_report.write(ReportHTML.report_print, open_in_browser=False, verbose=True)
    else:
        feedback.warning('Full report not created')

    feedback.writeln('\n  ' + 'All Done!\n')


def fix_images(root):
    # we need to move the
    word_folder_name = 'word_filtered_html_files'
    images = root.xpath(f'//*[@*[contains(., "{word_folder_name}")]]')
    for images in images:
        for key, value in images.attrib.items():
            images.attrib[key] = value.replace(word_folder_name, ReportHTML.img_folder)


if __name__ == "__main__":
    try:
        if os.name == 'nt':
            os.system('color')  # coloured text in windows cmd prompt
        main()
    except Exception:
        print("Exception in user code:\n")
        traceback.print_exc(file=sys.stdout)
        input()
        exit()
