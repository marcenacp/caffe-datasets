from pycaffe.plot.accuracy import print_learning_curve
from pycaffe.train.train_test import train_test_net_python
from pycaffe.utils.custom_log import make_time_stamp

# nets to train in net_prefixs
net_prefixs = ["twoears_classification"]

for net_prefix in net_prefixs:
    models_path = "models/" + net_prefix + "/"

    # process name with time stamp
    time_stamp = make_time_stamp('%Y%m%d_%H%M%S')
    process_name = net_prefix + "_" + time_stamp
    print "Training process:", process_name

    # log name
    log_name = "caffe_" + process_name + ".log"
    log_path = models_path + "logs/" + log_name

    # fig name
    fig_path = models_path + "figs/"

    # solver
    solver_name = "solver.prototxt"
    solver_path = models_path + solver_name

    # solve and plot
    train_test_net_python(solver_path, log_path, accuracy=True, key_score='sigmoid', accuracy_metrics='macro_recall', debug=True)
    print_learning_curve(net_prefix, log_path, fig_path, accuracy=True, format_x_axis=False)

    print "Logged to:", log_path
    print "Plotted to:", fig_path
