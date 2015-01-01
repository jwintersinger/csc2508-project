import math
import matplotlib
# Force matplotlib not to use X11 backend, which produces exception when run
# over SSH.
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns
from collections import defaultdict

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def load_results():
  results = {}

  for res in ['mongo_queries', 'postgres_json_queries', 'postgres_relational_queries']:
    with open('results.%s.csv' % res) as resf:
      results[res] = defaultdict(list)
      for line in resf:
        query, time = line.strip().split(',')
        results[res][query].append(float(time))

  return results

def organize_by_query(results):
  new_results = defaultdict(dict)

  for set_name, set_results in results.items():
    for query, times in set_results.items():
      new_results[query][set_name] = times

  return new_results

def plot(results):
  color = ('#1b9e77', '#de9f02', '#7570b3')
  width = 0.85
  name_mapper = {
    'mongo_queries': 'MongoDB',
    'postgres_json_queries': 'PostgreSQL\nJSON',
    'postgres_relational_queries': 'PostgreSQL\nrelational'
  }

  for query in sorted(results.keys()):
    f, ax = plt.subplots(1, 1, figsize=(6, 5))
    highest_y = 0

    set_results = results[query]
    x_vals = []
    stdev = []
    y_vals = []

    for set_name in sorted(set_results.keys()):
      times = set_results[set_name]
      mean_time = np.mean(times)
      x_vals.append(set_name)
      y_vals.append(mean_time)
      stdev.append(np.std(times))

    ind = np.arange(len(x_vals))
    rects = ax.bar(ind + width, y_vals, width, yerr=stdev, color=color, ecolor='black', capsize=100, edgecolor='none')

    ax.set_xticks(ind + width + width/2)
    xlabels = [name_mapper[xval] for xval in x_vals]
    ax.set_xticklabels(xlabels, rotation=0)

    highest_y = max(y_vals)
    lower, upper = 0, math.ceil(highest_y)
    tick_dist = math.ceil((upper - lower + 1) / 5)
    upper = (math.ceil(upper / tick_dist)) * tick_dist
    ax.get_yaxis().set_major_locator(matplotlib.ticker.MaxNLocator(nbins=9))

    #plt.title(result_set_name)
    plt.ylabel('Time (seconds)')
    plt.savefig(query + '.png')

def main():
  results = load_results()
  results = organize_by_query(results)
  plot(results)
  return
  for result_set_name, res in results.items():
    plot(result_set_name, res)

main()
