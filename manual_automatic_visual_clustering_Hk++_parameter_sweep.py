#! /usr/local/bin/python3.6
import numpy, inspect, os, subprocess, csv

input_file_path=r'/home/lolech/Hk++/datasets/najlepsze_z_manual_wzgledem_EXTERNAL/GT_OLECH_013.csv'
output_folder_path=r'/home/lolech/Hk++/1/manual_automatic_OLECH_013_c2_k2_n70-100_r10-100/'
program_name=r'/home/lolech/Hk++/1/PruneAndPerformOCGMonLeaves.jar'
java_executable_path='/usr/bin/java' 
summary_file_name=r'measures.csv'

#pruning parameters
ocgm_jar_path = '/home/lolech/Hk++/1/hkplusplus.jar'
first_cut_height = 2 
last_cut_height = 2
cut_height_step = 1

#Hk++ parameters setup
method = '-lgmm'
use_verbose_mode = True
is_class_attribute_present = True
is_instance_name_attribute_present = False 
use_diagonal_matrix = True
generate_images = False

#number of repeats for each parameter setup
number_of_repeats = 10
#K - number of clusters
first_k_value=2
last_k_value=2
k_value_step=1
#S - dendrogram max size
first_s_value=2147483600
last_s_value=2147483600
s_value_step=1
#N - number of alg iterations
first_n_value=70
last_n_value=100
n_value_step=10
#R - number of alg repeats
first_r_value=10
last_r_value=100
r_value_step=10
#E - epsilon used in comparision with 0 (covariuance matrix det), in program thsi parameters is used as 10^-E
first_e_value=10
last_e_value=10
e_value_step=1
#L - little value used to make covariance matrix non singular, this value is added on diagonal of each covariance matrix until its determinant is greater than 0. This value is used as 10^-L
first_l_value=2
last_l_value=2
l_value_step=1
#W - maximum number of nodes
first_w_value=50
last_w_value=50
w_value_step=1
#Cf - static center covariance matrix scalling factor
first_cf_value=1.0
last_cf_value=1.0
cf_value_step=0.05
#Rf - static center responsibility scalling factor
first_rf_value=1.0
last_rf_value=1.0
rf_value_step=0.15

if __name__ == '__main__':
    number_of_cut_heights = int((last_cut_height - first_cut_height) / cut_height_step + 1)
    number_of_k_values = int((last_k_value - first_k_value) / k_value_step + 1)
    number_of_s_values = int((last_s_value - first_s_value) / s_value_step + 1)
    number_of_n_values = int((last_n_value - first_n_value) / n_value_step + 1)
    number_of_r_values = int((last_r_value - first_r_value) / r_value_step + 1)
    number_of_e_values = int((last_e_value - first_e_value) / e_value_step + 1)
    number_of_l_values = int((last_l_value - first_l_value) / l_value_step + 1)
    number_of_w_values = int((last_w_value - first_w_value) / w_value_step + 1)
    number_of_cf_values = int((last_cf_value - first_cf_value) / cf_value_step + 1)
    number_of_rf_values = int((last_rf_value - first_rf_value) / rf_value_step + 1)

    print('Number of CUT different values: ', number_of_cut_heights)
    print('Number of K different values: ', number_of_k_values)
    print('Number of S different values: ', number_of_s_values)
    print('Number of N different values: ', number_of_n_values)
    print('Number of R different values: ', number_of_r_values)
    print('Number of E different values: ', number_of_e_values)
    print('Number of L different values: ', number_of_l_values)
    print('Number of W different values: ', number_of_w_values)
    print('Number of Cf different values:', number_of_cf_values)
    print('Number of Rf different values:', number_of_rf_values)
    print('Number of iterations for each parameters set: ', number_of_repeats)

    
    verbose_mode = '-v' if use_verbose_mode else ''
    class_attribute = '-c' if is_class_attribute_present else ''
    instance_name = '-in' if is_instance_name_attribute_present else ''
    diagonal_matrix = '-dm' if use_diagonal_matrix else ''
    images = '-gi' if generate_images else ''

    total_number_of_experiments = number_of_cut_heights * number_of_k_values * number_of_s_values * number_of_n_values * number_of_r_values * number_of_e_values * number_of_l_values * number_of_w_values * number_of_cf_values * number_of_rf_values * number_of_repeats
    experiment_counter = 0

    for c in range(first_cut_height, last_cut_height + cut_height_step, cut_height_step):
        for k in range(first_k_value, last_k_value + k_value_step, k_value_step):
            for s in range(first_s_value, last_s_value + s_value_step, s_value_step):
                for w in range(first_w_value, last_w_value + w_value_step, w_value_step):
                    for n in range(first_n_value, last_n_value + n_value_step, n_value_step):
                        for r in range(first_r_value, last_r_value + r_value_step, r_value_step):
                            for e in range(first_e_value, last_e_value + e_value_step, e_value_step):
                                for l in range(first_l_value, last_l_value + l_value_step, l_value_step):
                                    for cf in numpy.arange(first_cf_value, last_cf_value + 0.0001, cf_value_step):
                                        for rf in numpy.arange(first_rf_value, last_rf_value + 0.0001, rf_value_step):
                                            for i in range(1, number_of_repeats + 1):
                                                experiment_counter = experiment_counter + 1
                                                print(experiment_counter, '/', total_number_of_experiments, 'i =', i, 'cut_height = ', c, 'k =', k, 's =', s, 'w =', w, 'n =', n, 'r =', r, 'e =', e, 'l = ', l, 'cf =', cf, 'rf =', rf)
                                                parameters = 'cut_'+str(c) + '_k'+str(k) + '_s'+str(s) + '_w'+str(w) + '_n'+str(n) + '_r'+str(r) + '_e'+str(e) + '_l'+str(l) + '_cf'+str(cf) + '_rf'+str(rf) + "_i"+str(i)
                                                experiment_name = os.path.splitext(os.path.basename(input_file_path))[0] + parameters
                                                
                                                program_output_folder_path = os.path.join(output_folder_path, experiment_name) 
                                                log_file_path = os.path.join(output_folder_path, 'log_' + experiment_name + '.txt')
                                                profiler_output_file_path = os.path.join(output_folder_path, 'log_' + experiment_name + '.hprof')
                                                
                                                os.makedirs(output_folder_path, exist_ok=True)
                                                
                                                with open(log_file_path, 'w') as log:
                                                    method_invocation = ['-mp', ocgm_jar_path, method, '-i', input_file_path, '-o', program_output_folder_path, '-k', str(k), '-n', str(n), '-r', str(r), '-s', str(s), '-l', str(l), '-e', str(e), '-w', str(w), verbose_mode, class_attribute, instance_name, diagonal_matrix, images]

                                                    program_invocation = ['-jar', program_name, '-ch', str(c)]

                                                    args = program_invocation + method_invocation
                                                    
                                                    if os.name == 'posix':
                                                        args.insert(0, 'java')
                                                    else:
                                                        args.insert(0, 'java.exe')

                                                    subprocess.run(args, stderr=subprocess.STDOUT, stdout=log, executable=java_executable_path)
                                                
                                                if i >= 1 and i == number_of_repeats:
                                                    number_of_lines = len(open(summary_file_name, 'r', newline='', encoding='utf-8').readlines())
                                                    
                                                    with open(summary_file_name, 'a', newline='', encoding='utf-8') as result_file:
                                                        writer = csv.writer(result_file, delimiter=';')
                                                        upper_bound_str = str(number_of_lines - number_of_repeats + 1)
                                                        number_of_lines_str = str(number_of_lines)

                                                        writer.writerow([''])
                                                        writer.writerow(['min', '=min(B' + upper_bound_str + ':B' + number_of_lines_str + ')', '=min(C' + upper_bound_str + ':C' + number_of_lines_str + ')', '=min(D' + upper_bound_str + ':D' + number_of_lines_str + ')', '=min(E' + upper_bound_str + ':E' + number_of_lines_str + ')', '=min(F' + upper_bound_str + ':F' + number_of_lines_str + ')', '=min(G' + upper_bound_str + ':G' + number_of_lines_str + ')', '=min(H' + upper_bound_str + ':H' + number_of_lines_str + ')', '=min(I' + upper_bound_str + ':I' + number_of_lines_str + ')', '=min(J' + upper_bound_str + ':J' + number_of_lines_str + ')', '=min(K' + upper_bound_str + ':K' + number_of_lines_str + ')', '=min(L' + upper_bound_str + ':L' + number_of_lines_str + ')', '=min(M' + upper_bound_str + ':M' + number_of_lines_str + ')', '=min(N' + upper_bound_str + ':N' + number_of_lines_str + ')', '=min(O' + upper_bound_str + ':O' + number_of_lines_str + ')', '=min(P' + upper_bound_str + ':P' + number_of_lines_str + ')', '=min(Q' + upper_bound_str + ':Q' + number_of_lines_str + ')', '=min(R' + upper_bound_str + ':R' + number_of_lines_str + ')', '=min(S' + upper_bound_str + ':S' + number_of_lines_str + ')', '=min(T' + upper_bound_str + ':T' + number_of_lines_str + ')', '=min(U' + upper_bound_str + ':U' + number_of_lines_str + ')', '=min(V' + upper_bound_str + ':V' + number_of_lines_str + ')', '=min(W' + upper_bound_str + ':W' + number_of_lines_str + ')', '=min(X' + upper_bound_str + ':X' + number_of_lines_str + ')', '=min(Y' + upper_bound_str + ':Y' + number_of_lines_str + ')', '=min(Z' + upper_bound_str + ':Z' + number_of_lines_str + ')', '=min(AA' + upper_bound_str + ':AA' + number_of_lines_str + ')', '=min(AB' + upper_bound_str + ':AB' + number_of_lines_str + ')', '=min(AC' + upper_bound_str + ':AC' + number_of_lines_str + ')', '=min(AD' + upper_bound_str + ':AD' + number_of_lines_str + ')', '=min(AE' + upper_bound_str + ':AE' + number_of_lines_str + ')', '=min(AF' + upper_bound_str + ':AF' + number_of_lines_str + ')', '=min(AG' + upper_bound_str + ':AG' + number_of_lines_str + ')', '=min(AH' + upper_bound_str + ':AH' + number_of_lines_str + ')', '=min(AI' + upper_bound_str + ':AI' + number_of_lines_str + ')', '=min(AJ' + upper_bound_str + ':AJ' + number_of_lines_str + ')', '=min(AK' + upper_bound_str + ':AK' + number_of_lines_str + ')', '=min(AL' + upper_bound_str + ':AL' + number_of_lines_str + ')', '=min(AM' + upper_bound_str + ':AM' + number_of_lines_str + ')', '=min(AN' + upper_bound_str + ':AN' + number_of_lines_str + ')', '=min(AO' + upper_bound_str + ':AO' + number_of_lines_str + ')'])

                                                        writer.writerow(['max', '=max(B' + upper_bound_str + ':B' + number_of_lines_str + ')', '=max(C' + upper_bound_str + ':C' + number_of_lines_str + ')', '=max(D' + upper_bound_str + ':D' + number_of_lines_str + ')', '=max(E' + upper_bound_str + ':E' + number_of_lines_str + ')', '=max(F' + upper_bound_str + ':F' + number_of_lines_str + ')', '=max(G' + upper_bound_str + ':G' + number_of_lines_str + ')', '=max(H' + upper_bound_str + ':H' + number_of_lines_str + ')', '=max(I' + upper_bound_str + ':I' + number_of_lines_str + ')', '=max(J' + upper_bound_str + ':J' + number_of_lines_str + ')', '=max(K' + upper_bound_str + ':K' + number_of_lines_str + ')', '=max(L' + upper_bound_str + ':L' + number_of_lines_str + ')', '=max(M' + upper_bound_str + ':M' + number_of_lines_str + ')', '=max(N' + upper_bound_str + ':N' + number_of_lines_str + ')', '=max(O' + upper_bound_str + ':O' + number_of_lines_str + ')', '=max(P' + upper_bound_str + ':P' + number_of_lines_str + ')', '=max(Q' + upper_bound_str + ':Q' + number_of_lines_str + ')', '=max(R' + upper_bound_str + ':R' + number_of_lines_str + ')', '=max(S' + upper_bound_str + ':S' + number_of_lines_str + ')', '=max(T' + upper_bound_str + ':T' + number_of_lines_str + ')', '=max(U' + upper_bound_str + ':U' + number_of_lines_str + ')', '=max(V' + upper_bound_str + ':V' + number_of_lines_str + ')', '=max(W' + upper_bound_str + ':W' + number_of_lines_str + ')', '=max(X' + upper_bound_str + ':X' + number_of_lines_str + ')', '=max(Y' + upper_bound_str + ':Y' + number_of_lines_str + ')', '=max(Z' + upper_bound_str + ':Z' + number_of_lines_str + ')', '=max(AA' + upper_bound_str + ':AA' + number_of_lines_str + ')', '=max(AB' + upper_bound_str + ':AB' + number_of_lines_str + ')', '=max(AC' + upper_bound_str + ':AC' + number_of_lines_str + ')', '=max(AD' + upper_bound_str + ':AD' + number_of_lines_str + ')', '=max(AE' + upper_bound_str + ':AE' + number_of_lines_str + ')', '=max(AF' + upper_bound_str + ':AF' + number_of_lines_str + ')', '=max(AG' + upper_bound_str + ':AG' + number_of_lines_str + ')', '=max(AH' + upper_bound_str + ':AH' + number_of_lines_str + ')', '=max(AI' + upper_bound_str + ':AI' + number_of_lines_str + ')', '=max(AJ' + upper_bound_str + ':AJ' + number_of_lines_str + ')', '=max(AK' + upper_bound_str + ':AK' + number_of_lines_str + ')', '=max(AL' + upper_bound_str + ':AL' + number_of_lines_str + ')', '=max(AM' + upper_bound_str + ':AM' + number_of_lines_str + ')', '=max(AN' + upper_bound_str + ':AN' + number_of_lines_str + ')', '=max(AO' + upper_bound_str + ':AO' + number_of_lines_str + ')'])

                                                        writer.writerow(['average', '=average(B' + upper_bound_str + ':B' + number_of_lines_str + ')', '=average(C' + upper_bound_str + ':C' + number_of_lines_str + ')', '=average(D' + upper_bound_str + ':D' + number_of_lines_str + ')', '=average(E' + upper_bound_str + ':E' + number_of_lines_str + ')', '=average(F' + upper_bound_str + ':F' + number_of_lines_str + ')', '=average(G' + upper_bound_str + ':G' + number_of_lines_str + ')', '=average(H' + upper_bound_str + ':H' + number_of_lines_str + ')', '=average(I' + upper_bound_str + ':I' + number_of_lines_str + ')', '=average(J' + upper_bound_str + ':J' + number_of_lines_str + ')', '=average(K' + upper_bound_str + ':K' + number_of_lines_str + ')', '=average(L' + upper_bound_str + ':L' + number_of_lines_str + ')', '=average(M' + upper_bound_str + ':M' + number_of_lines_str + ')', '=average(N' + upper_bound_str + ':N' + number_of_lines_str + ')', '=average(O' + upper_bound_str + ':O' + number_of_lines_str + ')', '=average(P' + upper_bound_str + ':P' + number_of_lines_str + ')', '=average(Q' + upper_bound_str + ':Q' + number_of_lines_str + ')', '=average(R' + upper_bound_str + ':R' + number_of_lines_str + ')', '=average(S' + upper_bound_str + ':S' + number_of_lines_str + ')', '=average(T' + upper_bound_str + ':T' + number_of_lines_str + ')', '=average(U' + upper_bound_str + ':U' + number_of_lines_str + ')', '=average(V' + upper_bound_str + ':V' + number_of_lines_str + ')', '=average(W' + upper_bound_str + ':W' + number_of_lines_str + ')', '=average(X' + upper_bound_str + ':X' + number_of_lines_str + ')', '=average(Y' + upper_bound_str + ':Y' + number_of_lines_str + ')', '=average(Z' + upper_bound_str + ':Z' + number_of_lines_str + ')', '=average(AA' + upper_bound_str + ':AA' + number_of_lines_str + ')', '=average(AB' + upper_bound_str + ':AB' + number_of_lines_str + ')', '=average(AC' + upper_bound_str + ':AC' + number_of_lines_str + ')', '=average(AD' + upper_bound_str + ':AD' + number_of_lines_str + ')', '=average(AE' + upper_bound_str + ':AE' + number_of_lines_str + ')', '=average(AF' + upper_bound_str + ':AF' + number_of_lines_str + ')', '=average(AG' + upper_bound_str + ':AG' + number_of_lines_str + ')', '=average(AH' + upper_bound_str + ':AH' + number_of_lines_str + ')', '=average(AI' + upper_bound_str + ':AI' + number_of_lines_str + ')', '=average(AJ' + upper_bound_str + ':AJ' + number_of_lines_str + ')', '=average(AK' + upper_bound_str + ':AK' + number_of_lines_str + ')', '=average(AL' + upper_bound_str + ':AL' + number_of_lines_str + ')', '=average(AM' + upper_bound_str + ':AM' + number_of_lines_str + ')', '=average(AN' + upper_bound_str + ':AN' + number_of_lines_str + ')', '=average(AO' + upper_bound_str + ':AO' + number_of_lines_str + ')'])

                                                        writer.writerow(['stdev', '=stdev(B' + upper_bound_str + ':B' + number_of_lines_str + ')', '=stdev(C' + upper_bound_str + ':C' + number_of_lines_str + ')', '=stdev(D' + upper_bound_str + ':D' + number_of_lines_str + ')', '=stdev(E' + upper_bound_str + ':E' + number_of_lines_str + ')', '=stdev(F' + upper_bound_str + ':F' + number_of_lines_str + ')', '=stdev(G' + upper_bound_str + ':G' + number_of_lines_str + ')', '=stdev(H' + upper_bound_str + ':H' + number_of_lines_str + ')', '=stdev(I' + upper_bound_str + ':I' + number_of_lines_str + ')', '=stdev(J' + upper_bound_str + ':J' + number_of_lines_str + ')', '=stdev(K' + upper_bound_str + ':K' + number_of_lines_str + ')', '=stdev(L' + upper_bound_str + ':L' + number_of_lines_str + ')', '=stdev(M' + upper_bound_str + ':M' + number_of_lines_str + ')', '=stdev(N' + upper_bound_str + ':N' + number_of_lines_str + ')', '=stdev(O' + upper_bound_str + ':O' + number_of_lines_str + ')', '=stdev(P' + upper_bound_str + ':P' + number_of_lines_str + ')', '=stdev(Q' + upper_bound_str + ':Q' + number_of_lines_str + ')', '=stdev(R' + upper_bound_str + ':R' + number_of_lines_str + ')', '=stdev(S' + upper_bound_str + ':S' + number_of_lines_str + ')', '=stdev(T' + upper_bound_str + ':T' + number_of_lines_str + ')', '=stdev(U' + upper_bound_str + ':U' + number_of_lines_str + ')', '=stdev(V' + upper_bound_str + ':V' + number_of_lines_str + ')', '=stdev(W' + upper_bound_str + ':W' + number_of_lines_str + ')', '=stdev(X' + upper_bound_str + ':X' + number_of_lines_str + ')', '=stdev(Y' + upper_bound_str + ':Y' + number_of_lines_str + ')', '=stdev(Z' + upper_bound_str + ':Z' + number_of_lines_str + ')', '=stdev(AA' + upper_bound_str + ':AA' + number_of_lines_str + ')', '=stdev(AB' + upper_bound_str + ':AB' + number_of_lines_str + ')', '=stdev(AC' + upper_bound_str + ':AC' + number_of_lines_str + ')', '=stdev(AD' + upper_bound_str + ':AD' + number_of_lines_str + ')', '=stdev(AE' + upper_bound_str + ':AE' + number_of_lines_str + ')', '=stdev(AF' + upper_bound_str + ':AF' + number_of_lines_str + ')', '=stdev(AG' + upper_bound_str + ':AG' + number_of_lines_str + ')', '=stdev(AH' + upper_bound_str + ':AH' + number_of_lines_str + ')', '=stdev(AI' + upper_bound_str + ':AI' + number_of_lines_str + ')', '=stdev(AJ' + upper_bound_str + ':AJ' + number_of_lines_str + ')', '=stdev(AK' + upper_bound_str + ':AK' + number_of_lines_str + ')', '=stdev(AL' + upper_bound_str + ':AL' + number_of_lines_str + ')', '=stdev(AM' + upper_bound_str + ':AM' + number_of_lines_str + ')', '=stdev(AN' + upper_bound_str + ':AN' + number_of_lines_str + ')', '=stdev(AO' + upper_bound_str + ':AO' + number_of_lines_str + ')'])

#                                                    writer.writerow([''])
#                                                    writer.writerow(['short', '=average(C' + upper_bound_str + ':C' + number_of_lines_str + ')', '=stdev(C' + upper_bound_str + ':C' + number_of_lines_str + ')', '=average(D' + upper_bound_str + ':D' + number_of_lines_str + ')', '=stdev(D' + upper_bound_str + ':D' + number_of_lines_str + ')', '=average(E' + upper_bound_str + ':E' + number_of_lines_str + ')', '=stdev(E' + upper_bound_str + ':E' + number_of_lines_str + ')', '=average(F' + upper_bound_str + ':F' + number_of_lines_str + ')', '=stdev(F' + upper_bound_str + ':F' + number_of_lines_str + ')', '=average(G' + upper_bound_str + ':G' + number_of_lines_str + ')', '=stdev(G' + upper_bound_str + ':G' + number_of_lines_str + ')', '=average(H' + upper_bound_str + ':H' + number_of_lines_str + ')', '=stdev(H' + upper_bound_str + ':H' + number_of_lines_str + ')', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'skrot', '=average(C' + upper_bound_str + ':C' + number_of_lines_str + ')', '=stdev(C' + upper_bound_str + ':C' + number_of_lines_str + ')', '=average(D' + upper_bound_str + ':D' + number_of_lines_str + ')', '=stdev(D' + upper_bound_str + ':D' + number_of_lines_str + ')', '=average(E' + upper_bound_str + ':E' + number_of_lines_str + ')', '=stdev(E' + upper_bound_str + ':E' + number_of_lines_str + ')', '=average(F' + upper_bound_str + ':F' + number_of_lines_str + ')', '=stdev(F' + upper_bound_str + ':F' + number_of_lines_str + ')', '=average(G' + upper_bound_str + ':G' + number_of_lines_str + ')', '=stdev(G' + upper_bound_str + ':G' + number_of_lines_str + ')', '=average(H' + upper_bound_str + ':H' + number_of_lines_str + ')', '=stdev(H' + upper_bound_str + ':H' + number_of_lines_str + ')'])
                                                        writer.writerow([''])
                                                        writer.writerow([''])

