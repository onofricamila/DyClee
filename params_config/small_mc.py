from params_config.base import path_template

prefix = "small"

params = {
    'relativeSize': 0.02,
    'speed' : 5000,
    'lambd' : 0.4 ,# if it has a value over 0, when a micro cluster is updated, tl will be checked and the diff with current time will matter
    'periodicUpdateAt' : 3, # float("inf")
    'timeWindow' : 3, # float("inf")
    'periodicRemovalAt' : 3,# float("inf") # 4 # 15
    'closenessThreshold' : 1, # 1 # cuanto mas grande, menos pintas
}

results_path = path_template.format(prefix)