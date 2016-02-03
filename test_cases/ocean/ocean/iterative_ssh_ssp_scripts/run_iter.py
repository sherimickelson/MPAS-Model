#!/usr/bin/env python
import sys, os, subprocess
import xml.etree.ElementTree as ET
import argparse

## This script was generated by setup_testcases.py as part of a driver_script file.
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--iteration_count", dest="iteration_count", default=1, type=int, help="The number of iterations between init and forward mode for computing a balanced sea-surface pressure.")
parser.add_argument("--plot_ssh_ssp", dest="plot_ssh_ssp", action='store_true', help="If present, plot Cartesian ssh, ssp and deltaSSH fields for debugging.")
parser.add_argument("--plot_globalStats", dest="plot_globalStats", action='store_true', help="If present, plot mean and max KE, min layer thickness and mean temperature for debugging.")

args = parser.parse_args()
base_path = os.getcwd()
dev_null = open('/dev/null', 'w')
error = False

subprocess.check_call(['ln', '-sfn', '../init_step2/', 'forward_iter/ic'], stdout=dev_null, stderr=dev_null, env=os.environ.copy())
subprocess.check_call(['ln', '-sfn', '../init_step2/', 'forward/ic'], stdout=dev_null, stderr=dev_null, env=os.environ.copy())
subprocess.check_call(['mkdir', '-p', 'forward_iter/statsPlots'], stdout=dev_null, stderr=dev_null, env=os.environ.copy())

for iterIndex in range(args.iteration_count):
	print " * Iteration %i/%i"%(iterIndex+1,args.iteration_count)
	os.chdir(base_path)
	os.chdir('forward_iter')

	print "   * Running forward_iter"
	# ./run.py 
	subprocess.check_call(['./run.py'], stdout=dev_null, stderr=dev_null, env=os.environ.copy())
	print "       Complete"

        if args.plot_ssh_ssp:
	  print "   * Plotting stats"
	  subprocess.check_call(['../plot_globalStats.py', '%i'%iterIndex], stdout=dev_null, stderr=dev_null, env=os.environ.copy())
	  print "       Complete"

	os.chdir(base_path)
	os.chdir('init_iter')

	print "   * Running init_iter"
	# ./run.py 
	subprocess.check_call(['./run.py'], stdout=dev_null, stderr=dev_null, env=os.environ.copy())
	print "     Complete"

        if args.plot_ssh_ssp:
	  print "   * Plotting fields"
	  subprocess.check_call(['../plot_cart_ssh_ssp.py', '--iterIndex=%i'%iterIndex], stdout=dev_null, stderr=dev_null, env=os.environ.copy())
	  print "       Complete"

	os.chdir(base_path)
	subprocess.check_call(['ln', '-sfn', '../init_iter/', 'forward_iter/ic'], stdout=dev_null, stderr=dev_null, env=os.environ.copy())

os.chdir(base_path)
subprocess.check_call(['ln', '-sfn', '../init_iter/', 'forward/ic'], stdout=dev_null, stderr=dev_null, env=os.environ.copy())

if error:
	sys.exit(1)
else:
	sys.exit(0)