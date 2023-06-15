__author__ = 'https://github.com/password123456/'
__version__ = '1.0.0-20230615'

import os
import sys
import boto3
import datetime
import requests
import json
from tqdm import tqdm


class Bcolors:
    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36m'
    White = '\033[37m'
    Endc = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def start():
    backup_list = f'{os.getcwd()}/list.txt'

    try:
        if os.path.exists(backup_list):
            with open(backup_list, 'r') as f:
                for line in f:
                    if not line.startswith('#'):
                        _category = line.split(',')[0].strip()
                        _target_directory = line.split(',')[1].strip()

                        if _category and _target_directory:
                            find_target_files(_category, _target_directory)
                        else:
                            print(f'{Bcolors.Yellow}- List File is Invalid.! check {backup_list} {Bcolors.Endc}')
                            sys.exit(1)
            f.close()
        else:
            print(f'{Bcolors.Yellow}- List File not found.! check {backup_list} {Bcolors.Endc}')
    except Exception as e:
        print(f'{Bcolors.Yellow}- ::Exception:: Func:[{start.__name__}] '
              f'Line:[{sys.exc_info()[-1].tb_lineno}] [{type(e).__name__}] {e}{Bcolors.Endc}')


def find_target_files(_category, _target_directory):
    # Find the target file to back up.
    # In the case below, looking for files created on yesterday
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday_files = []

    for root, dirs, files in os.walk(_target_directory):
        for file in files:
            filepath = os.path.join(root, file)
            created_date = datetime.date.fromtimestamp(os.path.getctime(filepath))
            if created_date == yesterday:
                yesterday_files.append(filepath)

    upload_to_s3(_category, yesterday_files)


def upload_to_s3(_category, backup_files):

    print(f'>> Run time   : {datetime.datetime.now()}')
    print(f'>> Category   : {_category} ')
    print(f'>> File Count : {len(backup_files)} files')
    backup_list = f'\n'.join(backup_files)
    print(f'>> TargetFiles: \n\n{backup_list}')
    print(f'\n')

    # Configure S3 bucket name
    s3_bucket_name = f'##Your S3 Bucket to save logs##'
    s3_client = boto3.client('s3')


    # Variables to record after copying file that success/failure result
    success_files = []
    failure_files = []
    i = 0
    n = 0
    for file in backup_files:
        try:
            # do put the file into s3
            s3_key = file.replace('/data/logs/', '')   # define s3 main path to copying
            file_size = os.path.getsize(file)  # get the file size of the backup target

            # check If the backup target files in s3
            try:
                n += 1
                s3_client.head_object(Bucket=s3_bucket_name, Key=s3_key)
                failure_files.append(f'{n},[fail],File exists in s3,{file} | {file_size} bytes')
                continue
            except:
                pass
            i += 1

            # if not, processing backup
            print(f'{Bcolors.Yellow} putting the file into S3.....{Bcolors.Endc}')

            # progressbar of uploaded status.
            with tqdm(total=file_size, unit='B', unit_scale=True, postfix=os.path.basename(file)) as progress_bar:
                s3_client.upload_file(
                    file,
                    s3_bucket_name,
                    s3_key,
                    Callback=lambda bytes_uploaded: progress_bar.update(bytes_uploaded)
                )

            success_files.append(f'{i},[ok],success,{file} | {file_size} bytes')
        except Exception as e:
            failure_files.append(f'{n},[faill],Unknown Error,{file} | {file_size} bytes')


    # convert the list
    success_list = ''
    failure_list = ''

    for file in success_files:
        success_list += f'\n{file}'

    for file in failure_files:
        failure_list += f'\n{file}'


    print(f'\n>> Backup Result')
    if success_list:
        print(f'{success_list}\n')
    if failure_list:
        print(f'{failure_list}\n')

    print(f'{Bcolors.Green}------------------------------------->{Bcolors.Endc}')

    # Send the result to slack webhook
    message = f'>> py_s3_log_backup <<\n\n- {os.uname()[1]}\n- *{datetime.datetime.now()}*'
    message = f'*{message}\n\n*{_category}* :smile:\n```{success_list}{failure_list}```'
    send_to_slack(message)
    print(f'\n\n')



def send_to_slack(message):
    webhook_url = f'##Your SLACK_WEB_HOOKS##'

    header = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    }

    params = [
        {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': message
            }
        }
    ]

    try:
        r = requests.post(webhook_url, headers=header, data=json.dumps({'blocks': params}), verify=True)
        print(f'{Bcolors.Green}>> Send to Slack: {r.status_code} { Bcolors.Endc}')
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'{Bcolors.Yellow}>> Exception: Func:[{send_to_slack.__name__}] Line:[{sys.exc_info()[-1].tb_lineno}] [{type(e).__name__}] {e}{Bcolors.Endc}')
    else:
        r.close()


def main():
    banner = """
=======================================================
    python backup files uploader to s3
=======================================================
"""
    print(f'\n')
    print(f'{Bcolors.Cyan}{banner}{Bcolors.Endc}')

    start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'{Bcolors.Yellow}- ::Exception:: Func:[{__name__.__name__}] '
              f'Line:[{sys.exc_info()[-1].tb_lineno}] [{type(e).__name__}] {e}{Bcolors.Endc}')
