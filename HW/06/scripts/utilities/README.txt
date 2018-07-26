If modify python files in Windows and want to run them as scripts (with #!) in Unix, there are some options to convert the files (e.g. new lines):
* dos2unix <file>
* vim <file> -> Esc -> :set fileformat=unix -> :wq!

For more info see
* https://stackoverflow.com/questions/9975011/pycharm-usr-bin-pythonm-bad-interpreter
* https://stackoverflow.com/questions/2920416/configure-bin-shm-bad-interpreter