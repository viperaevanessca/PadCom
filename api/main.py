from typing import Union

from fastapi import FastAPI, Request
from pydantic import BaseModel
import string
import random
import subprocess
import os, time, base64

def get_random_string(length):
	letters = string.ascii_lowercase
	result_str = ''.join(random.choice(letters) for i in range(length))
	return result_str

def create_file(name, code):
	path = '/home/linuz/Desktop/Semester7/MPPL/PadCom/api/code/'+name
	f = open(path,'w')
	f.write(code)
	f.close()

def run(name):
	path = '/home/linuz/Desktop/Semester7/MPPL/PadCom/api/code/'+name
	cmd = f"gcc {path}"
	proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	proc.wait()
	out, err = proc.communicate()
	if(err == b'' and out == b''):
		cmd = f"./a.out"
		prog = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
		out, err = prog.communicate()
		return out, err
	else:
		return out, err

class Item(BaseModel):
	name: str
	description: Union[str, None] = None
	price: float
	tax: Union[float, None] = None

class Program(BaseModel):
	code: str


app = FastAPI()



@app.post("/items/")
async def create_item(item: Item):
	return item

@app.post("/save/")
async def save(program: Program):
	res = program.dict()
	name = get_random_string(6)+'.c'
	path = '/home/linuz/Desktop/Semester7/MPPL/PadCom/api/code/'+name
	res.update({"name": name})
	create_file(res.name)
	return res

@app.post("/compile/")
async def compile(program: Program):
	res = program.dict()
	name = get_random_string(6)+'.c'
	path = '/home/linuz/Desktop/Semester7/MPPL/PadCom/api/code/'+name
	create_file(name, program.code)
	while not os.path.isfile(path):
		time.sleep(1)
	out, err = run(name)
	print("Out: ", out)
	res.update({"name": name})
	if(err != b''):
		res.update({"output": err.decode('utf-8')})
	else:
		res.update({"output": out.decode('utf-8')})
	# cmd = '/home/linuz/Desktop/Semester7/MPPL/PadCom/api/code/*.c'
	# os.system(f"rm {cmd}")
	return res

