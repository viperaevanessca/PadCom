import subprocess

cmd = "gcc coba.c -o coba"
proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
proc.wait()
out, err = proc.communicate()
if(err == b'' and out == b''):
	prog = subprocess.Popen(["./coba"], stdout=subprocess.PIPE)
	out, err = prog.communicate()
	print(out.decode('utf-8'))