import os
import matplotlib.pyplot as plt
import pandas as pd

graphs_dir = './graph/jpg/'
results_dir = './results/'
inc_N_file = 'incN.csv'
inc_slots_file = 'incSlots.csv'

hostfiles = [
	('all',23,'-.'),
	('servers',16,'-')
]
modes = ['sequential','parallel']
merge_method = ['gather','hierarchical']
sort_method = ['sequential','threaded']
thread_counts = [1,2,4]

def plot_init(title=None, log=False):
	plt.clf()
	if title:
		plt.title(title)
	plt.xlabel('N (Number of Elements)')
	plt.ylabel('Time (seconds)')
	if log:
		plt.xscale('log')
	plt.grid(True)
	plt.tight_layout()

def row_label_N(row):
	label = f"{'all' if row['Slots']==23 else 'servers'}_{row['Mode']}"
	if row['MergeMethod'] != 'none':
		label += f"_{row['MergeMethod']}_{row['SortMethod']}"
		if row['SortMethod'] == 'threaded':
			label += f"_{int(row['Threads'])}"
	return label

def row_label_slots(row):
	label = f"{row['Mode']}"
	if row['MergeMethod'] != 'none':
		label += f"_{row['MergeMethod']}_{row['SortMethod']}"
		if row['SortMethod'] == 'threaded':
			label += f"_{int(row['Threads'])}"
	return label

def subset_df(df:pd.DataFrame,row_func,index='N') -> pd.DataFrame:
	_df = df.copy()
	_df['Label'] = df.apply(
		row_func,
		axis=1
	)
	return _df.pivot_table(index=index, columns='Label',values='Time').reset_index()

def plot_p(m_methods:list[str], df:pd.DataFrame):
	legends = []
	for hostfile in hostfiles:
		for mode in modes:
			if mode == 'parallel':
				for m_method in m_methods:
					for s_method in sort_method:
						if s_method == 'threaded':
							for threads in thread_counts:
								_df = df[
									(df['Mode']=='parallel') &
									(df['MergeMethod']==m_method) &
									(df['SortMethod']==s_method) &
									(df['Threads']==threads) &
									(df['Slots']==hostfile[1])
								].sort_values(by='N')
								# print(f'{hostfile[0].capitalize()} {mode.capitalize()} {m_method.capitalize()} {s_method.capitalize()} {threads}')
								plt.plot(
									_df['N'],
									_df['Time'],
									lw=2.5,
									linestyle=hostfile[2]
								)
								legends.append(f'{hostfile[0].capitalize()} {mode.capitalize()} {m_method.capitalize()} {s_method.capitalize()} {threads}')
						elif s_method == 'sequential':
							_df = df[
								(df['Mode']=='parallel')&
								(df['MergeMethod']=='gather')&
								(df['SortMethod']==s_method)&
								(df['Slots']==hostfile[1])
							].sort_values(by='N')
							# print(f'{hostfile[0].capitalize()} {mode.capitalize()} {m_method.capitalize()} {s_method.capitalize()}')
							plt.plot(
								_df['N'],
								_df['Time'],
								lw=2.5,
								linestyle=hostfile[2]
							)
							legends.append(f'{hostfile[0].capitalize()} {mode.capitalize()} {m_method.capitalize()} {s_method.capitalize()}')
			else: # sequential
				_df = df[
					(df['Mode']=='sequential')&
					(df['Slots']==hostfile[1])
				].sort_values(by='N')
				# print(f'{hostfile[0].capitalize()} {mode.capitalize()}')
				plt.plot(
					_df['N'],
					_df['Time'],
					lw=2.5,
					linestyle=hostfile[2]
				)
				legends.append(f'{hostfile[0].capitalize()} {mode.capitalize()}')
	plt.legend(legends)

def plot_n(m_methods:list[str],df:pd.DataFrame):
	legends = []
	for mode in modes:
		if mode == 'parallel':
			for m_method in m_methods:
				for s_method in sort_method:
					# sorting with threads
					if s_method == 'threaded':
						for threads in thread_counts:
							_df = df[
								(df['Mode']=='parallel') &
								(df['MergeMethod']==m_method) &
								(df['SortMethod']==s_method) &
								(df['Threads']==threads)
							].sort_values(by='Slots')
							legends.append(f'{mode} {m_method} {s_method} {threads}')
							plt.plot(
								_df['Slots'],
								_df['Time'],
								lw=2.5,
							)
					elif s_method == 'sequential':
						_df = df[
							(df['Mode']=='sequential')
						].sort_values(by='Slots')
						legends.append(f'{mode} {m_method} {s_method} {threads}')
						plt.plot(
							_df['Slots'],
							_df['Time'],
							lw=2.5,
						)
	plt.legend(legends)

def loadDf(df):
	df['MergeMethod'] = df['MergeMethod'].fillna('none')
	df['SortMethod'] = df['SortMethod'].fillna('none')
	df['Threads'] = df['Threads'].fillna(0)

	return df

def plot_categories(df, x, categories):
	for cat in categories:
		plt.plot(df[x], df[cat])

def categories(
		_hostfiles:list[str]=[item[0] for item in hostfiles],
		_modes:list[str]=modes,
		_merge:list[str]=merge_method,
		_sort:list[str]=sort_method,
		_thread:list[int]=thread_counts
	):
	_categories = [
    f'{slot}_{mode}' if mode == 'sequential'
    else f'{slot}_{mode}_{m_method}_{s_method}{f"_{threads}" if s_method == "threaded" else ""}'
    for slot in _hostfiles
    for mode in _modes
    for m_method in (_merge if mode != 'sequential' else [None])
    for s_method in (_sort if mode != 'sequential' else [None])
    for threads in (_thread if s_method == 'threaded' else [None])
	]

	return _categories

def categories_s( # the _s means it's for increasing slots
		_modes:list[str]=modes,
		_merge:list[str]=merge_method,
		_sort:list[str]=sort_method,
		_thread:list[int]=thread_counts
	):
	_categories = [
    f'{mode}' if mode == 'sequential'
    else f'{mode}_{m_method}_{s_method}{f"_{threads}" if s_method == "threaded" else ""}'
    for mode in _modes
    for m_method in (_merge if mode != 'sequential' else [None])
    for s_method in (_sort if mode != 'sequential' else [None])
    for threads in (_thread if s_method == 'threaded' else [None])
	]

	return _categories

if __name__ == '__main__':
	# comparisonDf = pd.read_csv('./results/runtimes.csv')
	# slotsDf = pd.read_csv('./results/incSlots.csv')

	df = subset_df(loadDf(pd.read_csv(results_dir + inc_N_file)), row_label_N)
	df.to_csv(results_dir + 'cat_' + inc_N_file, index=False)
	orig_df = df.copy()

	# All Nodes Gather Merge
	plot_init(title='All Nodes Gather Merge',log=True)
	_categories = categories(_hostfiles=['all'],_modes=['parallel'],_merge=['gather'])
	plot_categories(df,'N',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'comparison_all_gather.jpg')

	# All Nodes Hierarchical Merge
	plot_init(title='All Nodes Hierarchical Merge',log=True)
	_categories = categories(_hostfiles=['all'],_modes=['parallel'],_merge=['hierarchical'])
	plot_categories(df,'N',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'comparison_all_hierarchical.jpg')

	# All Nodes Gather vs Hierarchical Merge
	hierarchical_threaded_cols = [col for col in orig_df.columns if 'gather' in col and 'all' in col]
	df['all_gather'] = df[hierarchical_threaded_cols].mean(axis=1)
	hierarchical_cols = [col for col in orig_df.columns if 'hierarchical' in col and 'all' in col]
	df['all_hierarchical'] = df[hierarchical_cols].mean(axis=1)

	plot_init(title='All Nodes Gather vs Hierarchical Merge',log=True)
	_categories = ['all_gather','all_hierarchical']
	plot_categories(df,'N',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'comparison_all_parallel.jpg')

	# All Nodes Parallel vs Sequential
	plot_init(title='All Nodes Parallel vs Sequential',log=True)
	_categories += categories(_hostfiles=['all'],_modes=['sequential'])
	plot_categories(df,'N',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'comparison_all.jpg')

	# All vs Server Sequential
	plot_init(title='All vs Server Nodes Sequential',log=True)
	_categories = categories(_modes=['sequential'])
	plot_categories(df,'N',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'comparison_sequential.jpg')

	# All vs Server Parallel
	all_parallel_cols = [col for col in orig_df.columns if 'parallel' in col and 'all' in col]
	df['all_parallel'] = df[all_parallel_cols].mean(axis=1)
	servers_parallel_cols = [col for col in orig_df.columns if 'parallel' in col and 'servers' in col]
	df['servers_parallel'] = df[servers_parallel_cols].mean(axis=1)

	plot_init(title='All vs Server Nodes Parallel',log=True)
	_categories = ['all_parallel','servers_parallel']
	plot_categories(df,'N',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'comparison_parallel.jpg')

	# All vs Server Gather
	hierarchical_threaded_cols = [col for col in orig_df.columns if 'gather' in col and 'servers' in col]
	df['servers_gather'] = df[hierarchical_threaded_cols].mean(axis=1)
	hierarchical_cols = [col for col in orig_df.columns if 'hierarchical' in col and 'servers' in col]
	df['servers_hierarchical'] = df[hierarchical_cols].mean(axis=1)

	plot_init(title='All vs Server Nodes Gather',log=True)
	_categories = ['all_gather','servers_gather']
	plot_categories(df,'N',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'comparison_gather.jpg')

	# All vs Server Hierarchical
	plot_init(title='All vs Server Nodes Hierarchical',log=True)
	_categories = ['all_hierarchical','servers_hierarchical']
	plot_categories(df,'N',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'comparison_hierarchical.jpg')

	# INCREASING SLOTS
	df = subset_df(loadDf(pd.read_csv(results_dir + inc_slots_file)), row_label_slots,index='Slots')
	df.to_csv(results_dir + 'cat_' + inc_slots_file, index=False)
	orig_df = df.copy()

	# Gather as Slots Increases
	hierarchical_threaded_cols = [col for col in orig_df.columns if 'gather' in col and 'threaded' in col]
	df['parallel_gather_threaded'] = df[hierarchical_threaded_cols].mean(axis=1)

	plot_init(title='Gather Merge as Slots Increases')
	_categories = categories_s(_modes=['parallel'],_merge=['gather'])
	plot_categories(df,'Slots',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'slots_gather_expanded.jpg')

	plot_init(title='Gather Merge as Slots Increases')
	_categories = categories_s(_modes=['parallel'],_merge=['gather'],_sort=['sequential']) + ['parallel_gather_threaded']
	plot_categories(df,'Slots',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'slots_gather_avg.jpg')

	hierarchical_cols = [col for col in orig_df.columns if 'gather' in col]
	df['parallel_gather'] = df[hierarchical_cols].mean(axis=1)

	# Hierarchical
	hierarchical_threaded_cols = [col for col in orig_df.columns if 'hierarchical' in col and 'threaded' in col]
	df['parallel_hierarchical_threaded'] = df[hierarchical_threaded_cols].mean(axis=1)

	plot_init(title='Hierarchical Merge as Slots Increases')
	_categories = categories_s(_modes=['parallel'],_merge=['hierarchical'])
	plot_categories(df,'Slots',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'slots_hierarchical_expanded.jpg')

	plot_init(title='Hierarchical Merge as Slots Increases')
	_categories = categories_s(_modes=['parallel'],_merge=['hierarchical'],_sort=['sequential']) + ['parallel_hierarchical_threaded']
	plot_categories(df,'Slots',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'slots_hierarchical_avg.jpg')

	hierarchical_cols = [col for col in orig_df.columns if 'hierarchical' in col]
	df['parallel_hierarchical'] = df[hierarchical_cols].mean(axis=1)

	# Gather vs Hierarchical
	plot_init(title='Gather vs Hierarchical Merge as Slots Increases')
	_categories = ['parallel_gather','parallel_hierarchical']
	plot_categories(df,'Slots',_categories)
	plt.legend(_categories)
	# plt.show()
	plt.savefig(graphs_dir + 'slots_parallel.jpg')

	parallel_cols = [col for col in orig_df.columns if 'parallel' in col]
	df['parallel'] = df[parallel_cols].mean(axis=1)