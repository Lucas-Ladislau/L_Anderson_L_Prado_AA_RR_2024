import shlex
import subprocess
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.DEBUG, filename='run_exp_data.log', filemode='w', format='%(process)d - [%(asctime)s] : %(levelname)s -> %(message)s')

BINARY_PROGRAM = "./faz_algo"  # Nome do programa compilado
inputs = [5,500,1000,2000,5000,6000,7000,8000,9000,10000]  # Lista de valores de entrada
TIMES_RUN = 1
execution_times = []  # Lista para armazenar tempos de execução

def run_code():
    logging.debug(f'Running the program with each input {TIMES_RUN} times')
    for input_value in inputs:
        for count_time in range(TIMES_RUN):
            logging.debug(f"Running input: {input_value} - Time {count_time + 1}")
            cmd = shlex.split(f"{BINARY_PROGRAM} {input_value}")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate()

            # Verifica se houve erro durante a execução
            if process.returncode != 0 or stderr:
                logging.error(f"Error during run {count_time + 1} with input {input_value}: {stderr}")
            else:
                try:
                    run_time = float(stdout.strip())  # Pega o tempo de execução retornado pelo binário
                    logging.debug(f"Execution time for input {input_value} (run {count_time + 1}): {run_time} seconds")
                    execution_times.append((input_value, run_time))  # Armazena a entrada e o tempo de execução
                except ValueError:
                    logging.error(f"Invalid output for execution time: {stdout.strip()}")

def plot_execution_times():
    inputs = [entry[0] for entry in execution_times]
    times = [entry[1] for entry in execution_times]
    
    plt.figure(figsize=(10, 6))
    plt.plot(inputs, times, marker='o', label='Tempo de execução')
    plt.xlabel('N')
    plt.ylabel('Tempo de execução (segundos)')
    plt.title('Tempo de execução por N entradas')
    plt.legend()
    
    # Salva o gráfico em um arquivo PNG
    plt.savefig('execution_time_plot.png')
    print("O gráfico foi salvo como 'execution_time_plot.png'.")

def main():
    logging.debug('Experiment script executed')
    run_code()
    
    # Executa a plotagem sem logar as informações do gráfico
    logging.disable(logging.CRITICAL)
    plot_execution_times()
    logging.disable(logging.NOTSET)

if __name__ == "__main__":
    main()
