import random
import time

class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.failure_count = 0
        self.reincarnation_count = 0
        self.active = True

    def increase_failure_count(self):
        self.failure_count += 1

    def increase_reincarnation_count(self):
        self.reincarnation_count += 1
    
    def set_process_status (self, status):
        self.active = status

def initiate_election(processes):
    # Encontrar os processos que não falharam completamente
    active_processes = [process for process in processes if process.active]
    
    if not active_processes:
        # Todos os processos falharam completamente, não é possível eleger um líder
        return None
    
    # Encontrar o processo com o menor número de falhas e menor número de encarnações
    min_failures = min(process.failure_count for process in active_processes)
    candidate_processes = [process for process in active_processes if process.failure_count == min_failures]
    min_reincarnations = min(process.reincarnation_count for process in candidate_processes)
    elected_leader = min((process for process in candidate_processes if process.reincarnation_count == min_reincarnations), key=lambda x: x.process_id)
    return elected_leader

def simulate_failure(processes):
    # Simular uma falha de processo aleatória
    process_to_fail = random.choice(processes)
    process_to_fail.increase_failure_count()
    process_to_fail.increase_reincarnation_count()
    process_to_fail.set_process_status(False)
    print(f"Processo {process_to_fail.process_id} falhou! Número de encarnações: {process_to_fail.reincarnation_count}")
    return process_to_fail

# Verifica se é necessário executar uma nova eleição de processos
def is_new_election_needed (leader, processes):
    election_needed = False
    for process in processes:
        if (process.reincarnation_count < leader.reincarnation_count):
            election_needed = True
    return election_needed

# Simula a recuperação de processos em caso de falha
def process_recovery (processes):
    offline_processes = [process for process in processes if not(process.active)]
    if offline_processes != []:
        recovered_process = random.choice(offline_processes)
        print(f"O processo {recovered_process.process_id} se recuperou !")
        recovered_process.set_process_status(True)

def main():
    num_processes = 5
    failed_process = None
    processes = [Process(i) for i in range(num_processes)]
    
    # Iniciar eleição com o processo 0 como líder inicial
    current_leader = processes[0]
    
    # Simulação de execução
    while (True):
        # Simular falha de um processo com uma probabilidade de 20%
        if random.random() < 0.2:
            failed_process = simulate_failure(processes)

        # Simular a recuperação de um processo com uma probabilidade de 50%
        if random.random() < 0.5:
            process_recovery(processes)
        
        # Verificar se o líder falhou
        if failed_process != None and failed_process.process_id == current_leader.process_id:
            print(f"Líder atual (Processo {current_leader.process_id}) falhou! Iniciando nova eleição...")
            
            # Verificar se o líder atual é o melhor líder possível
            new_leader = initiate_election(processes)
            if new_leader is not None:
                current_leader = new_leader
                print(f"Novo líder eleito: Processo {current_leader.process_id}")
            else:
                print("Todos os processos falharam completamente. Não é possível eleger um líder.")
                break
        
        failed_process = None        
        # Aguardar um intervalo de tempo antes da próxima iteração
        time.sleep(1)

if __name__ == "__main__":
    main()
