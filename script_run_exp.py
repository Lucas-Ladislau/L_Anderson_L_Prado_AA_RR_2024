import shlex
import subprocess
import logging
import matplotlib.pyplot as plt
import csv
import numpy as np
import os

logging.basicConfig(level=logging.DEBUG, filename=os.path.join('log', 'run_exp_data.log'), filemode='w', format='%(process)d - [%(asctime)s] : %(levelname)s -> %(message)s')

BINARY_PROGRAM = "./faz_algo"  # Nome do programa compilado
inputs = [100, 500, 1000,2000,2500,3000,4000,5000,6000,7000,8000]
TIMES_RUN = 6
execution_data = []  # Lista para armazenar dados de execução (n, tempo, contador)

def run_code():
    logging.debug(f'Running the program with each input {TIMES_RUN} times')
    for input_value in inputs:
        logging.debug(f"==================================INPUT: {input_value}=======================================")
        times = []
        contador = 0
        for count_time in range(TIMES_RUN):
            logging.debug(f"------------------------------------{count_time + 1}°-----------------------------------------")
            logging.debug(f"Running input: {input_value} - Time {count_time + 1}")
            cmd = shlex.split(f"{BINARY_PROGRAM} {input_value}")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate()

            # Verifica se houve erro durante a execução
            if process.returncode != 0 or stderr:
                logging.error(f"Error during run {count_time + 1} with input {input_value}: {stderr}")
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
        logging.debug(f"==================================END INPUT: {input_value}======================================\n")
        if times:
            time_average = sum(times) / len(times)
            execution_data.append((input_value, time_average, contador))  # Armazena n, tempo médio e contador médio

def plot_execution_times():
    inputs = [entry[0] for entry in execution_data]
    times = [entry[1] for entry in execution_data]

    # Calcular O(n^3)
    coeficiente = times[-1] / (inputs[-1]**3)  # Ajustar coeficiente com base no último valor
    on3 = coeficiente * np.array(inputs)**3
    
    plt.figure(figsize=(10, 6))
    plt.plot(inputs, times, marker='o', label='Média do tempo de execução')
    plt.plot(inputs, on3, 'r--', label='O(n³)')
    plt.xlabel('N')
    plt.ylabel('Tempo de execução (segundos)')
    plt.title('Tempo de execução por N entradas')
    plt.legend()
    plt.xlim(left=0, right=9000)
    plt.grid(True)
    
    # Salva o gráfico em um arquivo PNG
    plt.savefig(os.path.join('plot', 'execution_time_plot.png'))
    print("O gráfico foi salvo como 'execution_time_plot.png'.")

def save_to_csv():
    with open('execution_times.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Input', 'Tempo Médio (segundos)', 'Contador Médio'])
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