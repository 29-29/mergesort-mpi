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

def mpi(N, args, hostfile)->float:
	mpirun = ['mpirun','--mca','btl_tcp_if_include','br0','--hostfile',hostfile,'python3','src/main.py']
	time = subprocess.run([*mpirun,*args,N], stdout=subprocess.PIPE)
	# return float(time.stdout.decode().strip())
	print(time.stdout.decode().strip())
	return 0

if __name__ == '__main__':
	times = []
	for hostfile in hostfiles:
		for n in Ns:
			# sequential
			time = mpi(str(n),modes[0],hostfile)
			times.append({
				'N':n,'Mode':'sequential','Time':time
			})

			# parallel
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
	df.to_csv('results/runtimes.csv',index=False)