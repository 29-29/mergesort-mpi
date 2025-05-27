import os
import pandas as pd
import subprocess
import csv

# PARAMETERS
Ns 						= [10**i for i in range(1, 7)] # up to a million bc 10^7 takes 100s
modes 				= ['seq','par']
merge 				= ['g','h']
sort 					= ['s','t']
thread_counts = [1, 2, 4]
hostfiles 		= ['hostfile_all','hostfile_servers']
slots					= [i for i in range(1, 32)]

def mpi(N, args, hostfile, slots=None)->float:
	mpirun = ['mpirun','--mca','btl_tcp_if_include','br0','--hostfile',hostfile,'--np' if slots else '',str(slots) if slots else '','python3','src/main.py']
	time = subprocess.run([*mpirun,*args,N], stdout=subprocess.PIPE)
	time = time.stdout.decode().strip() or 0
	return float(time)

def incN():
	times = []
	for hostfile in hostfiles:
		print(hostfile)
		for n in Ns:
			print('\t',n)
			# sequential
			print('\t\tsequential')
			time = mpi(str(n),['seq'],hostfile)
			times.append({
				'N':n,'Mode':'sequential','Time':time
			})

			# parallel
			print('\t\tparallel')
			for m_method in merge:
				for s_method in sort:
					# threaded sort
					if s_method == 't':
						for threads in thread_counts:
							time = mpi(str(n),[modes[1],m_method,s_method,str(threads)],hostfile)
							times.append({
								'N':n,'Mode':'parallel',
								'MergeMethod':('gather' if m_method == 'g' else 'hierarchical'),
								'SortMethod':'threaded','Threads':threads,
								'Time':time
							})
					# sequential sort
					else:
						time = mpi(str(n),[modes[1],m_method,s_method],hostfile)
						times.append({
							'N':n,'Mode':'parallel',
							'MergeMethod':('gather' if m_method == 'g' else 'hierarchical'),
							'SortMethod':'sequential',
							'Time':time
						})
	df = pd.DataFrame(times)
	os.makedirs('results',exist_ok=True)
	df.to_csv('results/runtimes.csv',index=False)

def incSlots():
	times = []
	for n in slots:
		print(n)
		for m_method in merge:
			print('\t%s'%('gather' if m_method == 'g' else 'hierarchical'))
			for s_method in sort:
				print('\t\t%s'%('threaded' if s_method == 't' else 'sequential'))
				if s_method == 't':
					for threads in thread_counts:
						time = mpi(str(Ns[-1]),[modes[1],m_method,s_method,threads],'hostfile_all',slots=n)
						times.append({
							'N':Ns[-1],'Mode':'parallel',
							'MergeMethod':('gather' if m_method == 'g' else 'hierarchical'),
							'SortMethod':'threaded','Threads':threads, 'Slots':n,
							'Time':time
						})
				else:
					time = mpi(str(Ns[-1]),[modes[1],m_method,s_method],'hostfile_all',slots=n)
					times.append({
						'N':Ns[-1],'Mode':'parallel',
						'MergeMethod':('gather' if m_method == 'g' else 'hierarchical'),
						'SortMethod':'sequential','Slots':n,
						'Time':time
					})

	df = pd.DataFrame(times)
	os.makedirs('results',exist_ok=True)
	df.to_csv('results/incSlots.csv',index=False)

if __name__ == '__main__':
	# incN()
	incSlots()
	pass