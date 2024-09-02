# Define each process in its own array
process_P1 = {'name': 'P1', 'arrival_time': 0, 'burst_time': 10, 'comes_back_after': 2, 'priority': 3, 'running_time': 0, 't_wait': 0, 'decremented': 0, 'finish_time': 0, 'total_waiting': 0}
process_P2 = {'name': 'P2', 'arrival_time': 1, 'burst_time': 8, 'comes_back_after': 4, 'priority': 2, 'running_time': 0, 't_wait': 0, 'decremented': 0, 'finish_time': 0, 'total_waiting': 0}
process_P3 = {'name': 'P3', 'arrival_time': 3, 'burst_time': 14, 'comes_back_after': 6, 'priority': 3, 'running_time': 0, 't_wait': 0, 'decremented': 0, 'finish_time': 0, 'total_waiting': 0}
process_P4 = {'name': 'P4', 'arrival_time': 4, 'burst_time': 7, 'comes_back_after': 8, 'priority': 1, 'running_time': 0, 't_wait': 0, 'decremented': 0, 'finish_time': 0, 'total_waiting': 0}
process_P5 = {'name': 'P5', 'arrival_time': 6, 'burst_time': 5, 'comes_back_after': 3, 'priority': 0, 'running_time': 0, 't_wait': 0, 'decremented': 0, 'finish_time': 0, 'total_waiting': 0}
process_P6 = {'name': 'P6', 'arrival_time': 7, 'burst_time': 4, 'comes_back_after': 6, 'priority': 1, 'running_time': 0, 't_wait': 0, 'decremented': 0, 'finish_time': 0, 'total_waiting': 0}
process_P7 = {'name': 'P7', 'arrival_time': 8, 'burst_time': 6, 'comes_back_after': 9, 'priority': 2, 'running_time': 0, 't_wait': 0, 'decremented': 0, 'finish_time': 0, 'total_waiting': 0}

# Organize the processes in a list
processes = [process_P1, process_P2, process_P3, process_P4, process_P5, process_P6, process_P7]

ready_queue = []
waiting_queue = []
gantt_chart = []
cpu = []
waiting_time = 0

# Counter to keep track of the time each process has spent in the ready queue
time_in_ready_queue = {process['name']: 0 for process in processes}


for time in range(201):

    for process in ready_queue:
        process['total_waiting'] += 1  # Increment total waiting time for each process in the ready queue

    if cpu:
        cpu['running_time'] += 1

    # Decrement priority after 5 time units in the ready queue
    for process in ready_queue:
        time_in_ready_queue[process['name']] += 1
        if time_in_ready_queue[process['name']] == 5:
            if process['decremented'] + process['priority'] > 0:
                process['decremented'] -= 1

            time_in_ready_queue[process['name']] = 0

    # Check if processes have arrived
    for process in processes:
        if process['arrival_time'] == time:
            ready_queue.append(process)

    wait_temp = waiting_queue.copy()
    # Check if processes in waiting queue can come back
    for returned_process in wait_temp:
        returned_process['t_wait'] += 1
        if returned_process['t_wait'] == returned_process['comes_back_after']:
            waiting_queue.remove(returned_process)
            returned_process['t_wait'] = 0 # Reset running time for the returned process
            returned_process['decremented'] = 0
            ready_queue.append(returned_process)


    if ready_queue:
        min_queue = min(ready_queue, key=lambda process: process['priority'] + process['decremented'])

    # Check if the CPU is running a process
    if cpu:
        # Check if the process is done
        if cpu['running_time'] == cpu['burst_time'] or time == 200:
            cpu['running_time'] = 0
            completion_time = time
            cpu['finish_time'] = completion_time  # Update finish time
            waiting_queue.append(cpu)
            gantt_chart.append((cpu['name'], Started, time))
            gantt_chart.append(('|', time, time))
            # Calculate waiting time for the process
            waiting_time += cpu['total_waiting']  # Update waiting time for the process
            cpu['total_waiting'] = 0  # Reset total waiting
            cpu = []  # Reset the CPU variable as it is now empty

    # Check if the CPU is empty and there are processes in the ready queue
    if min_queue and not cpu:
        cpu = min_queue
        ready_queue.remove(min_queue)
        time_in_ready_queue[cpu['name']] = 0
        Started = time


# Display Gantt chart
print("\nGantt Chart:")
for entry in gantt_chart:
    symbol, start, end = entry
    if symbol == '|':
        print(symbol, end=" ")
    else:
        print(f"{symbol} {start}->{end}", end=" ")
print()


completed_processes = [process for process in processes if process['finish_time'] > 0]
average_waiting_time = waiting_time / len(completed_processes)
print(f"\nAverage Waiting Time: {average_waiting_time:.2f}")

# Calculate and display average turnaround time
completed_processes = [process for process in processes if process['finish_time'] > 0]
turnaround_times = [process['finish_time'] - process['arrival_time'] for process in completed_processes]
average_turnaround_time = sum(turnaround_times) / len(turnaround_times)
print(f"Average Turnaround Time: {average_turnaround_time:.2f}")
