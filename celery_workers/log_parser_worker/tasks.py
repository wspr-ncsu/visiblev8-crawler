from typing import Optional, TypedDict
from log_parser_worker.app import celery_app
import os
import glob
import subprocess as sp
import shutil
import time

class ParserConfig(TypedDict):
    parser: str
    delete_log_after_parsing: bool
    output_format: Optional[str]
    mongo_id: Optional[str]

def remove_entry(filepath):
    if os.path.isdir(filepath):
        shutil.rmtree(filepath)
    else:
        os.remove(filepath)


@celery_app.task(name='log_parser_worker.parse_log', bind=True)
def parse_log(self, output_from_vv8_worker: str, submission_id: str, config: ParserConfig):
    start = time.perf_counter()
    print('Garbage from vv8_worker: {}'.format(output_from_vv8_worker))
    print(f'log_parser parse_log_task: submission_id: {submission_id}')
    self.update_state(state='PROGRESS', meta={'status': 'Postprocessor started'})
    postprocessor_path = os.path.join('/app/post-processors', 'vv8-post-processor')
    if not os.path.isfile(postprocessor_path):
        raise Exception(f'Postprocessor script cannot be found or does not exist. Expected path: {postprocessor_path}')
    logsdir = os.path.join( '/app/raw_logs', submission_id)
    outputdir = os.path.join('/app/parsed_logs', submission_id)
    if not os.path.isdir(logsdir):
        raise Exception(f'No logs found in workdir: {logsdir}')
        return
    arguments = [postprocessor_path, '-aggs', config['parser'], '-submissionid', submission_id]
    filelist = glob.glob(os.path.join(logsdir, 'vv8*.log'))
    if len(filelist) == 0:
        raise Exception(f'No logs found in workdir: {logsdir}')
        return
    if config['output_format']:
        arguments.append( '-output' )
        arguments.append( config['output_format'] )
    self.update_state(state='PROGRESS', meta={'status': 'Running postprocessor'})
    for entry in filelist:
        arguments.append(entry)
    # Run postprocessor
    postprocessor_proc = None
    if config['output_format'] == 'stdout' or not config['output_format']:
        if os.path.exists(outputdir):
            # Remove all files from working directory
            for entry in glob.glob(os.path.join(outputdir, '*')):
                remove_entry(entry)
        else:
            os.mkdir(outputdir)
        outputfile = os.path.join(outputdir, 'parsed_log.output')
        f = open(outputfile, 'w+')
        postprocessor_proc = sp.Popen(arguments, cwd=logsdir, stdout=f)
        postprocessor_proc.wait()
        f.close()
    else:
        print(arguments)
        postprocessor_proc = sp.Popen(arguments, cwd=logsdir)
        postprocessor_proc.wait()
    if config['delete_log_after_parsing']:
        shutil.rmtree(logsdir)
    if config['compress_after_parsing']:
        shutil.make_archive(outputdir, 'zip', outputdir)
        shutil.rmtree(outputdir)
    if postprocessor_proc.returncode != 0:
        raise Exception('Postprocessor did not a return a success code')
    end = time.perf_counter()
    self.update_state(state='SUCCESS', meta={'status': 'Postprocessor finished', 'time': end - start, 'end_time': time.time()})