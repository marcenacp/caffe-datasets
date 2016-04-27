# coding: utf8

import os
import nideep.iow.file_system_utils as fs

def is_wav(p):

    return os.path.splitext(p)[-1] == '.wav'

def list2cmdline(cmd):

    return ' '.join(cmd)

def lower_samplerate_cmds(dir_src, samplerate, dir_dst, fpath_exec_script):

    paths = fs.gen_paths(dir_src, is_wav)
    commands = []
    for fpath in paths:
        path_dst = os.path.join(dir_dst, os.path.basename(fpath))
        cmd = ['ffmpeg', '-i', fpath, '-ac', '2', '-ar', "%d" % (samplerate,), path_dst]
        commands.append(cmd)

    commands = [list2cmdline(cmd) for cmd in commands]

    with open(fpath_exec_script, 'w') as f:
        for cmd in commands:
            f.write('%s\n' % (cmd,))

if __name__=="__main__":
    lower_samplerate_cmds("/home/pierre/Téléchargements/data2/annotated_speech/Recorded",
                          16000,
                          "/home/pierre/Téléchargements/data2/annotated_speech/Recorded_16000/",
                          "lower_samplerate.sh")
