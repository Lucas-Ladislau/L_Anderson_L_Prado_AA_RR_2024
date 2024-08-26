import shlex
import subprocess
import logging
import matplotlib.pyplot as plt
import csv
import numpy as np
import os


logging.basicConfig(level=logging.DEBUG, filename=os.path.join('log', 'run_exp_data.log'), filemode='w', format='%(process)d - [%(asctime)s] : %(levelname)s -> %(message)s')

BINARY_PROGRAM = "./faz_algo" 
BINARY_PROGRAM_OPTIMIZED = "./faz_algo_otimizado"
inputs = [500, 1000,2000,2500,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000]
TIMES_RUN = 6
execution_data = []  # Lista para armazenar dados de execução (n, tempo, contador)

def run_code():
    logging.debug(f'Running the programs with each input {TIMES_RUN} times')
    for input_value in inputs:
        logging.debug(f"======================================INPUT: {input_value}==========================================")
        
        for program_name, program in [("Original Algorithm", BINARY_PROGRAM), ("Optimized Algorithm", BINARY_PROGRAM_OPTIMIZED)]:
            logging.debug(f"XXXXXXXXXXXXXXXXXXXXXXXXXXXXX<<< {program_name} >>>XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            logging.debug(f"Running input: {input_value} - Time 1 - {program_name}")

            times = []
            contador = 0
            
            for count_time in range(TIMES_RUN):
                logging.debug(f"------------------------------------{count_time + 1}°-----------------------------------------")
                cmd = shlex.split(f"{program} {input_value}")
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                stdout, stderr = process.communicate()

                # Verifica se houve erro durante a execução
                if process.returncode != 0 or stderr:
                    logging.error(f"Error during run {count_time + 1} with input {input_value} ({program_name}): {stderr}")
                else:
                    try:
                        # Extrair contador e tempo de execução da saída
                        lines = stdout.strip().split('\n')
                        contador = int(lines[0])
                        run_time = float(lines[1])
                        logging.debug(f"Execution time for input {input_value} (run {count_time + 1}): {run_time} seconds")
                        logging.debug(f"Counter for input {input_value} (run {count_time + 1}): {contador}")
                        logging.debug(f"------------------------------------------------------------------------------------\n")
                        times.append(run_time)
                    except ValueError:
                        logging.error(f"Invalid output for execution time or Counter: {stdout.strip()}")

            if times:
                time_average = sum(times) / len(times)
                execution_data.append((input_value, time_average, contador, program_name))  # Armazena n, tempo médio, contador médio e nome do programa

def plot_execution_times():
    # Separar os dados por algoritmo
    inputs_data = sorted(set(entry[0] for entry in execution_data))  # Obter entradas únicas e ordenadas
    times_original = []
    times_optimized = []

    # Criar dicionários para mapear inputs aos tempos
    times_dict_original = {entry[0]: entry[1] for entry in execution_data if entry[3] == "Original Algorithm"}
    times_dict_optimized = {entry[0]: entry[1] for entry in execution_data if entry[3] == "Optimized Algorithm"}

    # Preencher listas com tempos para cada entrada
    for input_value in inputs_data:
        times_original.append(times_dict_original.get(input_value, np.nan))
        times_optimized.append(times_dict_optimized.get(input_value, np.nan))

    # Calcular O() para os algoritmos
    coeficiente_original = times_original[-1] / (inputs_data[-1]**3) 
    coeficiente_optimized = times_optimized[-1] / (inputs_data[-1]**2) 
    
    on3_original = coeficiente_original * np.array(inputs_data)**3
    on2_optimized = coeficiente_optimized * np.array(inputs_data)**2

    plot_general_comparison(inputs_data,times_original, times_optimized, on3_original, on2_optimized)
    plot_o_cubic(inputs_data,times_original, on3_original)
    plot_o_quadratic(inputs_data, times_optimized, on2_optimized)

def plot_general_comparison(inputs_data,times_original, times_optimized, on3_original, on2_optimized):
    plt.figure(figsize=(12, 6))
    plt.plot(inputs_data, times_original, marker='o', label='Média tempo execução - Original')
    plt.plot(inputs_data, times_optimized, marker='o', label='Média tempo execução - Otimizado')
    plt.plot(inputs_data, on3_original, 'r--', label='O(n³)')
    plt.plot(inputs_data, on2_optimized, 'g--', label='O(n²)')
    plt.xlabel('N')
    plt.ylabel('Tempo de execução (segundos)')
    plt.title('Comparação de Tempo de Execução entre Algoritmo Original e Otimizado')
    plt.legend()
    plt.xlim(left=0, right=max(inputs_data) + 1000)
    plt.grid(True)
    
    # Salva o gráfico em um arquivo PNG
    plt.savefig(os.path.join('plot', 'execution_time_comparison_plot.png'))
    print("O gráfico foi salvo como 'execution_time_comparison_plot.png'.")

def plot_o_cubic(inputs_data,times_original, on3_original):
    plt.figure(figsize=(12, 6))
    plt.plot(inputs_data, times_original, marker='o', label='Média tempo execução')
    plt.plot(inputs_data, on3_original, 'r--', label='O(n³) - Original')
    plt.xlabel('N')
    plt.ylabel('Tempo de execução (segundos)')
    plt.title('Tempo de Execução do Algoritmo Original')
    plt.legend()
    plt.xlim(left=0, right=max(inputs_data) + 1000)
    plt.grid(True)
    
    # Salva o gráfico em um arquivo PNG
    plt.savefig(os.path.join('plot', 'execution_time_o_cubic.png'))
    print("O gráfico foi salvo como 'execution_time_o_cubic.png'.")

def plot_o_quadratic(inputs_data, times_optimized, on2_optimized):
    plt.figure(figsize=(12, 6))
    plt.plot(inputs_data, times_optimized, marker='o', label='Média tempo execução')
    plt.plot(inputs_data, on2_optimized, 'g--', label='O(n²)')
    plt.xlabel('N')
    plt.ylabel('Tempo de execução (segundos)')
    plt.title('Tempo de Execução do Algoritmo Otimizado')
    plt.legend()
    plt.xlim(left=0, right=max(inputs_data) + 1000)
    plt.grid(True)
    
    # Salva o gráfico em um arquivo PNG
    plt.savefig(os.path.join('plot', 'execution_time_o_quadratic.png'))
    print("O gráfico foi salvo como 'execution_time_o_quadratic.png'.")

def save_to_csv():
    with open('execution_times.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Input', 'Tempo Médio (segundos)', 'Contador Médio', 'Algoritmo'])
        for entry in execution_data:
            writer.writerow(entry)
    print("Os tempos médios foram salvos em 'execution_times.csv'.")

def main():
    logging.debug('Experiment script executed')
    run_code()
    
    # Executa a plotagem sem logar as informações do gráfico
    logging.disable(logging.CRITICAL)
    plot_execution_times()
    save_to_csv()
    logging.disable(logging.NOTSET)

if __name__ == "__main__":
    main()
