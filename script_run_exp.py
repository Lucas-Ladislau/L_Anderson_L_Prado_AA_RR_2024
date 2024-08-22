#!/usr/bin/python3

from os import walk
import os
import shlex
import subprocess
import logging
import time
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.DEBUG, filename='run_exp_data.log', filemode='w', format='%(process)d - [%(asctime)s] : %(levelname)s -> %(message)s')

BINARY_PROGRAM = "./a.out"  # Nome do programa compilado
INPUTS_FILE = "inputs"
TIMES_RUN = 1
PATH_FILES_INPUT_LIST = []
execution_times = []  # Lista para armazenar tempos de execução

def list_files_input():
    for (dirpath, dirnames, filenames) in walk(INPUTS_FILE):
        for file in filenames:
            full_path = os.path.abspath(dirpath) + "/" + file
            PATH_FILES_INPUT_LIST.append(full_path)
    
    # Ordenar a lista de arquivos de entrada
    PATH_FILES_INPUT_LIST.sort()

def run_code():
    logging.debug(f'Running the program with each input {TIMES_RUN} times')
    for input_file in PATH_FILES_INPUT_LIST:
        if not os.path.exists(input_file):
            logging.error(f"Input file: {input_file} not found")            
        else:
            with open(input_file, 'r') as f:
                input_value = f.read().strip()  # Lê o valor do arquivo

            # Certifique-se de que o input_value é numérico e válido
            try:
                int(input_value)
            except ValueError:
                logging.error(f"Invalid input value: {input_value} in file {input_file}")
                continue

            for count_time in range(TIMES_RUN):
                logging.debug(f"Running input: {input_file} - Time {count_time + 1}")
                start_time = time.time()  # Início da medição de tempo
                cmd = shlex.split(f"{BINARY_PROGRAM} {input_value}")
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                stdout, stderr = process.communicate()
                end_time = time.time()  # Fim da medição de tempo

                # Verifica se houve erro durante a execução
                if process.returncode != 0 or stderr:
                    logging.error(f"Error during run {count_time + 1} with input {input_file}: {stderr}")
                else:
                    run_time = end_time - start_time

                    logging.debug(f"Execution time (run {count_time + 1}): {run_time} seconds")
                    logging.debug(f"Program output (run {count_time + 1}):")
                    logging.debug(stdout)

            execution_times.append((input_value, run_time))  # Armazena a entrada e o tempo de execucao

def plot_execution_times():
    inputs = [int(entry[0]) for entry in execution_times]
    times = [entry[1] for entry in execution_times]
    
    plt.figure(figsize=(10, 6))
    plt.plot(inputs, times, marker='o')
    plt.xlabel('N')
    plt.ylabel('Tempo de execução (seconds)')
    plt.title('Tempo de execução por N entradas')
    plt.grid(True)
    
    # Salva o gráfico em um arquivo PNG
    plt.savefig('execution_time_plot.png')
    print("O gráfico foi salvo como 'execution_time_plot.png'.")

def main():
    logging.debug('Experiment script executed')
    logging.debug('Listing input files to the program')
    list_files_input()
    run_code()
    
    # Executa a plotagem sem logar as informações do gráfico
    logging.disable(logging.CRITICAL)
    plot_execution_times()
    logging.disable(logging.NOTSET)

if __name__ == "__main__":
    main()
