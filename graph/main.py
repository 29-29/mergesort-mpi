import matplotlib.pyplot as plt
import pandas as pd

hostfiles = [('all',23,'-.'),('servers',16,'-')]
modes = ['sequential','parallel']
merge_method = ['gather','hierarchical']
sort_method = ['threaded','sequential']
thread_counts = [1,2,4]

def plot_init(title=None):
	if title:
		plt.title(title)
	plt.xlabel('N (Number of Elements)')
	plt.ylabel('Time (seconds)')
	plt.xscale('log')
	plt.grid(True)
	plt.tight_layout()

def plot_p(m_method:str, df:pd.DataFrame):
	legends = []
	for hostfile in hostfiles:
		for s_method in sort_method:
			if s_method == 'threaded':
				for threads in [1,2,4]:
					_df = df[
						(df['Mode']=='parallel')&
						(df['MergeMethod']==m_method)&
						(df['SortMethod']==s_method)&
						(df['Threads']==threads)&
						(df['Slots']==hostfile[1])
					].sort_values(by='N')
					legends.append(f'{hostfile[0].capitalize()} Parallel {m_method.capitalize()} {s_method.capitalize()} {threads}')
					plt.plot(
						_df['N'],
						_df['Time'],
						lw=2.5,
						linestyle=hostfile[2]
					)
			elif s_method == 'sequential':
				_df = df[
					(df['Mode']=='parallel')&
					(df['MergeMethod']=='gather')&
					(df['SortMethod']==s_method)&
					(df['Slots']==hostfile[1])
				].sort_values(by='N')
				legends.append(f'{hostfile[0].capitalize()} Parallel {m_method.capitalize()} {s_method.capitalize()}')
				plt.plot(
					_df['N'],
					_df['Time'],
					lw=2.5,
					linestyle=hostfile[2]
				)
	plt.legend(legends)

def loadDf(df):
	df['MergeMethod'] = df['MergeMethod'].fillna('none')
	df['SortMethod'] = df['SortMethod'].fillna('none')
	df['Threads'] = df['Threads'].fillna(0)

	return df


if __name__ == '__main__':
	comparisonDf = pd.read_csv('./results/runtimes.csv')
	slotsDf = pd.read_csv('./results/incSlots.csv')

	df = loadDf(comparisonDf)

	plot_init(title='All & Server Nodes Gather Merge')
	plot_p('gather',df)
	plt.show()

	plot_init(title='All & Server Nodes Hierarchical Merge')
	plot_p('hierarchical',df)
	plt.show()