from behave import *
from recordtype import recordtype
import sys
import random
import os
# parsert type
use_step_matcher("parse")

# ---------------------------------------
# Changin this value to 'True' will have 
# each step Dump what it did into whatever 
# file is denoted in {file}
DUMP = False;
file = ".output"
# ----------------------------------------

# Gloabal default Parameters for state of experiemnt
global_default_params = {}

# User default paramters for users inside experiment
user_default_params = {}

# Record of price jumps w/ time at index [i][0] and value at [i][1]
pricejumps = [[]]

# Struct defining the users attributes 
myStruct = {'subject': '', 'type': '', 'status': '', 'speed':'', 'bid0':'', 'offer0':''}

# List containing each subject's struct
subjects_list = []

# list of scenario
scenario_index = 0;

# Array that mirrors subject_list 
participant_type = []
# num of subejcts
subjects_num = 0
# session_length
session_length = 0
#time records
record_time = {}
# CSV target
target = open(file, 'w')
# Scenario prefix
target_prefix = "/home/leeps/redwood-test-harness/data/scenarios/"


#!--------------------------------------------------------------------->
# Below this line is production code and does not need further modifications
# or commenting
#!--------------------------------------------------------------------->

# Global default table parser
@given('global default parameters')
def step_impl(context):
	# Grab from the table and add to global_default_params
	for row in context.table:
		global_default_params[row['parameter']] = row['value']

	if(DUMP):
		target.write("---------------Reading Global Parameters----------------\n")
		for i in global_default_params:
			target.write(i +' : ' + global_default_params[i] + '\n')

# Reads in the global value of # of participants
@given('there are {num} participants')
def step_impl(context,num):
	global subjects_num
	subjects_num = int(num);
	
	global participant_type
	participant_type = [None] * subjects_num

	if(DUMP):
		target.write("----------------Reading Number of Users----------------\n")
		target.write("number of participants: " + num + '\n')

# Reads in default values for participants
@given('default parameters')
def step_impl(context):
	for row in context.table:
			user_default_params[row['parameter']] = row['value']

	if(DUMP):
		target.write("----------Reading in User Default Parameters----------\n")
		for i in user_default_params:
			target.write(i +' : ' + user_default_params[i] + '\n')

# vanialla python function to format print a Participant and its attrivutes
def dump_subject(subject_dict):
	target.write("Subject:  " + str(subject_dict['subject']) + '\n')
	target.write("	Status: " + subject_dict['status'] + '\n')
	target.write("	Speed:  " + subject_dict['speed'] + '\n')
	target.write("	Bid0:   " + subject_dict['bid0'] + '\n')
	target.write("	Offer0:	" + subject_dict['offer0'] + '\n')
	target.write("	Type:	" + subject_dict['type'] + '\n')


# Updates the length of the session
@given('session lasts {t} seconds')
def step_impl(context,t):
	global session_length
	session_length = t
	if(DUMP):
		target.write("----------------Updating Session Length----------------\n")
		target.write("Sessions lasts: " + session_length + ' seconds\n')

# Creates number of participants of participants using default participant values 
@given('default parameters for users')
def step_impl(context):
	
	global scenario_index
	scenario_index = scenario_index + 1;
	# Create direvtory
	dir_create = "mkdir " + target_prefix + "Scenario" + str(scenario_index)
	os.system(dir_create)
	out_create = "touch " + target_prefix + "Scenario" + str(scenario_index) + "/output.csv"
	os.system(out_create)

	if(scenario_index > 1):
		reset_users();

	 # Create a "struct" for a user and load the default values 
	# into it. 
	for i in range(0, subjects_num):

		temp = dict(myStruct)

		temp['subject'] = i
		temp['type'] = "null"
		temp['status'] = user_default_params['status']
		temp['speed'] = user_default_params['speed']
		temp['bid0'] = user_default_params['bid0']
		temp['offer0'] = user_default_params['offer0']

		if(DUMP):
			target.write("----------------Creating Participant----------------\n")
			dump_subject(temp)

		# add it subject_list 
		# !! subject list is the list that contains all users !!
		subjects_list.append(temp)


# Takes modified attributes of participants
@given('participant {p} has {key} updated to {value}')
def step_impl(context, p, key, value):
	
	# # Get index of subject list 
	# subj_i = subj_index(p)

	# # if dne add it
	# if(subj_i == -1):
	# 	global subjects_num
	# 	subj_i = random.randint(0, subjects_num-1)
	# 	while subjects_list[subj_i] == "null":
	# 		subj_i = random.randint(0, subjects_num-1)
	# 	subjects_list[subj_i]['type'] = p;
	# 	# adds to mirror list to make searching concievable
	# 	participant_type[subj_i] = p;
	# 	if(DUMP):
	# 		target.write("----------------------Updating Type----------------------\n")
	# 		dump_subject(subjects_list[subj_i])

	# update the value
	subjects_list[int(p)][key] = value

	if(DUMP):
		target.write("-------------------Updating Attribute-------------------\n")
		dump_subject(subjects_list[int(p)])


	pass

# Takes intital V jump and creates the jump.csv for the experiemnt
@when('V jumps to {value} at {time}')
def step_impl(context, value, time):
	global target
	if(DUMP):
		target.write("---------------Adding values to jump.csv---------------\n")

	global scenario_index
	jump_name = target_prefix + "Scenario" + str(scenario_index) + "/T1_jump.csv"
	jump_targ = open(jump_name, 'w')

	# initial header for the file
	jump_targ.write("jumpTime,jumpSizes\n")
	if(time != "-1"):
	# V0
		jump_targ.write("0," + global_default_params["V0"] +  "\n")
		jump_targ.write("0," + global_default_params["V0"] +  "\n")
		# trigger time
		jump_targ.write(global_default_params[time] + ',' + value + "\n")
	else:
		jump_targ.write("300000,-1\n")
	jump_targ.close();

	# global scenario_index

	inv_name = target_prefix + "Scenario" + str(scenario_index) + "/T1_investors.csv"
	inv_targ = open(inv_name, 'w')

	# initial header for the file
	inv_targ.write("investorTimes,investorDirections\n")

	inv_targ.close()



# I dont know why eric included this but its in it for now
# Temporary
@when('session runs to {time}')
def step_impl(context, time):
	global session_length
	if(time == "completion"):
		pass
	else:
		session_length = time;

@when('an investor arrives to {d} at {t}')
def step_impl(context, t, d):
	time = parse_times_str(t)
	target.write(str(time) + "\n")

	# global target
	if(DUMP):
		target.write("---------------Adding values to investor.csv---------------\n")

	global scenario_index
	inv_name = target_prefix + "Scenario" + str(scenario_index) + "/T1_investors.csv"
	inv_targ = open(inv_name, 'w')

	direction = -1

	if(d == "buy"):
		direction = 1
	else:
		direction = 0

	inv_targ.write(str(time) + "," + str(direction))

	inv_targ.close();


# Vanialla python function to reset n numebr of 
# participants to their default values
def reset_users():
	global participant_type
	participant_type = [None] * subjects_num
	for i in range(0, subjects_num):
		subjects_list[i]['subject'] = i
		subjects_list[i]['type'] = "null"
		subjects_list[i]['status'] = user_default_params['status']
		subjects_list[i]['speed'] = user_default_params['speed']
		subjects_list[i]['bid0'] = user_default_params['bid0']
		subjects_list[i]['offer0'] = user_default_params['offer0']

		if(DUMP):
			target.write("---------------Resetting Participants---------------\n")
			dump_subject(subjects_list[i])
		record_time = {}


# Function that returns the index of the 
# type_list
def subj_index(type_label):
	try:
		n = participant_type.index(type_label)
	except ValueError : 
		return -1;
	return n


# Function that takes equation and substitues global 
# values and evaluates
def parse_times(dictionary):
	# super ugly, just dont look at it please
	for key in dictionary:
		# target.write(key + " : " + dictionary[key] + "\n")
		temp = dictionary[key]
		replaced_var = ""
		tempword = ""
		i = 0;
		while i != len(temp):
			if(temp[i] != "+" and temp[i] != "-" and temp[i] != "*" and temp[i] != "/"):
				tempword = tempword + temp[i]
				# target.write(tempword + "\n")
			else:
				replaced_var = replaced_var + global_default_params[tempword] + temp[i]
				tempword = ""
			if(i == len(temp)-1):
				replaced_var = replaced_var + global_default_params[tempword]
			i= i + 1 
		dictionary[key] = eval(replaced_var)


# Function that takes equation and substitues global 
# values and evaluates
def parse_times_str(time):
	# super ugly, just dont look at it please
	temp = time
	replaced_var = ""
	tempword = ""
	i = 0;
	while i != len(temp):
		if(temp[i] != "+" and temp[i] != "-" and temp[i] != "*" and temp[i] != "/"):
			tempword = tempword + temp[i]
			# target.write(tempword + "\n")
		else:
			replaced_var = replaced_var + global_default_params[tempword] + temp[i]
			tempword = ""
		if(i == len(temp)-1):
			replaced_var = replaced_var + global_default_params[tempword]
		i= i + 1 
	return eval(replaced_var)

#!--------------------------------------------------------------------->
# Above this line is production code and does not need further modifications
# or commenting
#!--------------------------------------------------------------------->







# Times when the market is to be recorded
# Parses and sets actual time
@when('market state is recorded at')
def step_impl(context):

	# Gets number of columns by header
	n = context.table.headings
	global record_time
	record_time = {}
	# Add string represneting the calculation to its key
	for row in context.table:
		for value in n:
			record_time[str(value)] = row[value]

	# replace the string statments with
	parse_times(record_time)

	if(DUMP):
		target.write("----------------Updating Record Times----------------\n")
		for key in record_time:
			target.write(key + " : " + str(record_time[key]) +"\n")

@then('at {t} system is in initial state except V is {v}')
def step_impl(context, t, v):
	pass


@then('at {t} participant {p} has {k} {v}')
def step_impl(context, t, p, k, v):
	global subjects_list
	global record_time
	# subj_i = subj_index(p)

	time = record_time[t];


	# target_name = target_prefix + "Scenario" + str(scenario_index) + "/T" + str(scenario_index) + "_P" + str(p) + "_input.csv"
	# user_target = open(target_name, 'a')

	target_name2 = target_prefix + "Scenario" + str(scenario_index) + "/query.config"
	query_target = open(target_name2, 'a')

	if( k == "bid"):
		pass
	elif( k == "offer" ):
		pass
	elif( k == "profit"):
		timestamp = str(int(time)*1000000);
		query_target.write("timestamp:"+str(timestamp) + ",cumprofit_p" + p + ":" + v + "\n");
	elif ( k == "spread"):
		timestamp = str(int(time)*1000000);
		query_target.write("timestamp:"+str(timestamp) + ",spread_p" + p + ":" + v  + "\n");

		for i in range(0, subjects_num):
			target_name = target_prefix + "Scenario" + str(scenario_index) + "/T1_P" + str(i) + "_input.csv"
			user_target = open(target_name, 'a')
			if(int(i) == int(p)):
				print(str(subjects_num))
				# subjects_list[int(p)][str(k)] = v
				
				spread = int(v)
				user_target.write(str(record_time[t]) + ",SPREAD," + str(spread) + "\n")				
			else:
				user_target.write(str(record_time[t]) + ",OUT\n")		



@then('at {t} participants besides {p} have {k} {v}')
def step_impl(context, t, p, k, v):
	target_name2 = target_prefix + "Scenario" + str(scenario_index) + "/query.config"
	query_target = open(target_name2, 'a')
	global record_time

	time = record_time[t];

	for i in range(0, subjects_num):
		if(int(i) != int(p)):
		        timestamp = str(int(time)*1000000);
		        query_target.write("timestamp:"+str(timestamp) + ",cumprofit_p" + str(i) + ":" + v + "\n");


@then('at {t} all participants have {k} {v}')
def step_impl(context, t, k, v):
	# 1000000
	target.write("------------\n");

# @then('at {t} participant have {k} {v}')
# def step_impl(context, t, k, v):
# 	pass
