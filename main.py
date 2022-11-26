from tkinter import filedialog
from os import system, remove

path = filedialog.askopenfilename()
filename = path[:path.find('.ipynb')]
local_path = filename + '-local.tmp'
remote_path = filename + '-remote.tmp'


def separate_versions(base, local, remote):
    notebook_file = open(base, 'rt')
    local_file = open(local, 'wt')
    remote_file = open(remote, 'wt')

    conflict_state = 'none'

    for line in notebook_file.readlines():
        if conflict_state == 'none':
            if '<<<<<<< local' in line:
                conflict_state = 'local'
            else:
                local_file.write(line)
                remote_file.write(line)
        else:
            if '=======' in line:
                conflict_state = 'remote'
            elif '>>>>>>> remote' in line:
                conflict_state = 'none'
            elif conflict_state == 'local':
                local_file.write(line)
            elif conflict_state == 'remote':
                remote_file.write(line)


separate_versions(path, local_path, remote_path)
system(f'nbdime merge {path} {local_path} {remote_path}')

remove(local_path)
remove(remote_path)
