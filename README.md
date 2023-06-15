# python file backup to s3
![made-with-python][made-with-python]
![Python Versions][pyversion-button]
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpassword123456%2Fpy_file_backup_to_s3&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

[pyversion-button]: https://img.shields.io/pypi/pyversions/Markdown.svg
[made-with-python]: https://img.shields.io/badge/Made%20with-Python-1f425f.svg


# Features
- Provides the functionality to upload a specified local file to Amazon S3.
- Requires configuration of the AWS S3 bucket name (s3_bucket_name), the destination path in S3 (s3_key), and the local file path (local_file_path) before running the script.
- Uploads the configured local file to the specified path in the S3 bucket and displays a successful upload message.
- Create a file named "list.txt" with the following format. Each line represents a log file name and the corresponding directory for S3 backup:
```python
# vim list.txt
ssh_logs,/data/logs/ssh_logs
system_logs,/var/log
```
  
- When specifying a directory for S3 backup, the script will search for files in the subdirectories as well. It will find the files created yesterday and include them in the backup list.
- The script also checks if the files are already backed up in S3. If a file has already been uploaded, it will not be uploaded again.
- The script separates the files into success and failure categories and outputs the corresponding lists.
- The tqdm library is used to provide a progress bar for the file uploads to S3. This is especially useful for large files, as it allows monitoring the backup progress.
- Once all the operations are completed, the script sends the job details to Slack.
- Feel free to modify and customize the code as per your requirements.

- Let me know if there are any changes required or additional features need it.
- and give the "stars" can be helpful for sharing scrub code snippets. then it will continue to improvement.

# preview
```bash
[root@buddy2:/]# python main.py
=======================================================
    python backup files uploader to s3
=======================================================

>> Run time   : 2023-06-15 17:51:12.269210
>> Category   : system_logs
>> File Count : 4 files
>> TargetFiles:

/var/log/2023-06-14/ssh_auth.tar.gz
/var/log/2023-06-14/ssh_xferlog.tar.gz
/var/log/2023-06-14/messages.tar.gz
/var/log/2023-06-14/cron.tar.gz



 putting the file into S3.....
100%|███████████████████████████████████| 326k/326k [00:12<00:00, 60.6MB/s, ssh_auth.tar.gz]
 putting the file into S3.....
100%|███████████████████████████████████| 326k/326k [00:00<00:00, 2.96MB/s, ssh_xferlog.tar.gz]
 putting the file into S3.....
100%|███████████████████████████████████| 100M/100M [00:00<00:00, 1.68kB/s, messages.tar.gz]
 putting the file into S3.....
100%|███████████████████████████████████| 64.0/64.0 [00:00<00:00, 1.63kB/s, cron.tar.gz]

>> Backup Result

1,[ok],success,/var/log/2023-06-14/ssh_auth.tar.gz | 326465 bytes
2,[ok],success,/var/log/2023-06-14/ssh_xferlog.tar.gz | 326465 bytes
3,[ok],success,/var/log/2023-06-14/messages.tar.gz | 102400 bytes
4,[ok],success,/var/log/2023-06-14/cron.tar.gz | 64 bytes

------------------------------------->
>> Send to Slack: 200

..
...
.....

```



