from typing import Optional, TypedDict
from log_parser_worker.app import celery_app
import os
import glob
import subprocess as sp
import shutil

class ParserConfig(TypedDict):
    parser: str
    delete_log_after_parsing: bool
    output_format_to_mongoresql: bool

def remove_entry(filepath):
    if os.path.isdir(filepath):
        shutil.rmtree(filepath)
    else:
        os.remove(filepath)


@celery_app.task(name='log_parser_worker.parse_log')
def parse_log(self, submission_id: str, config: ParserConfig):
    print(f'log_parser parse_log_task: submission_id: {submission_id}')
    postprocessor_path = os.path.join('/app/post-processors', 'vv8-post-processor')
    if not os.path.isfile(postprocessor_path):
        raise Exception(f'Postprocessor script cannot be found or does not exist. Expected path: {postprocessor_path}')
    logsdir = os.path.join( '/app/raw_logs', submission_id)
    outputdir = os.path.join('/app/parsed_logs', submission_id)
    if os.path.exists(outputdir):
        # Remove all files from working directory
        for entry in glob.glob(os.path.join(outputdir, '*')):
            remove_entry(entry)
    else:
        os.mkdir(outputdir)
    tempfile = os.path.join(logsdir, 'idldata.json')
    temp_fd = open(tempfile, 'w+')
    temp_fd.write('{}')
    temp_fd.close()
    if not os.path.isdir(logsdir):
        raise Exception(f'No logs found in workdir: {logsdir}')
    arguments = [postprocessor_path, '-aggs', config['parser']]
    filelist = glob.glob(os.path.join(logsdir, 'vv8*.log'))
    if len(filelist) == 0:
        return
    if config['output_format_to_mongoresql']:
        arguments.append( '-output' )
        arguments.append( 'mongresql' )
    for entry in filelist:
        arguments.append(entry)
    # Run postprocessor
    if not config['output_format_to_mongoresql']:
        outputfile = os.path.join(outputdir, 'parsed_log.output')
        f = open(outputfile, 'w+')
        postprocessor_proc = sp.Popen(arguments, cwd=logsdir, stdout=f)
        postprocessor_proc.wait()
        f.close()
    else:
        postprocessor_proc = sp.Popen(arguments, cwd=logsdir)
        postprocessor_proc.wait()
    if config['delete_log_after_parsing']:
        shutil.rmtree(logsdir)