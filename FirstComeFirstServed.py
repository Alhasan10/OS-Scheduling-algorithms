# Define each process in its own array
process_P1 = {'name': 'P1', 'arrival_time': 0, 'burst_time': 10, 'comes_back_after': 2, 'priority': 3, 'running_time': 0, 't_wait': 0, 'finish_time': 0, 'total_waiting': 0}
process_P2 = {'name': 'P2', 'arrival_time': 1, 'burst_time': 8, 'comes_back_after': 4, 'priority': 2, 'running_time': 0, 't_wait': 0, 'finish_time': 0, 'total_waiting': 0}
process_P3 = {'name': 'P3', 'arrival_time': 3, 'burst_time': 14, 'comes_back_after': 6, 'priority': 3, 'running_time': 0, 't_wait': 0, 'finish_time': 0, 'total_waiting': 0}
process_P4 = {'name': 'P4', 'arrival_time': 4, 'burst_time': 7, 'comes_back_after': 8, 'priority': 1, 'running_time': 0, 't_wait': 0, 'finish_time': 0, 'total_waiting': 0}
process_P5 = {'name': 'P5', 'arrival_time': 6, 'burst_time': 5, 'comes_back_after': 3, 'priority': 0, 'running_time': 0, 't_wait': 0, 'finish_time': 0, 'total_waiting': 0}
process_P6 = {'name': 'P6', 'arrival_time': 7, 'burst_time': 4, 'comes_back_after': 6, 'priority': 1, 'running_time': 0, 't_wait': 0, 'finish_time': 0, 'total_waiting': 0}
process_P7 = {'name': 'P7', 'arrival_time': 8, 'burst_time': 6, 'comes_back_after': 9, 'priority': 0, 'running_time': 0, 't_wait': 0, 'finish_time': 0, 'total_waiting': 0}

# Organize the processes in a list
processes = [process_P1, process_P2, process_P3, process_P4, process_P5, process_P6, process_P7]

# Sort processes based on arrival time
sorted_processes = sorted(processes, key=lambda x: x['arrival_time'])

ready_queue = []
waiting_queue = []
gantt_chart = []
cpu = None
waiting_time = 0

for time in range(201):

    for process in ready_queue:
        process['total_waiting'] += 1  # Increment total waiting time for each process in the ready queue

    if cpu:
        cpu['running_time'] += 1

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
            returned_process['t_wait'] = 0  # Reset running time for the returned process
            ready_queue.append(returned_process)

    # Check if the CPU is running a process
    if cpu:
        # Check if the process is done
        if cpu['running_time'] == cpu['burst_time'] or time == 200:
            cpu['running_time'] = 0
            completion_time = time
            waiting_queue.append(cpu)
            gantt_chart.append((cpu['name'], Started, completion_time))  # Include completion time
            gantt_chart.append(('|', completion_time, completion_time))
            cpu['finish_time'] = completion_time  # Update last execution time
            # Calculate waiting time for the process
            waiting_time += cpu['total_waiting']  # Update waiting time for the process
            cpu['total_waiting'] = 0  # Reset total waiting
            cpu = None  # Reset the CPU variable as it is now empty

    # Check if the CPU is empty and there are processes in the ready queue
    if not cpu and ready_queue:
        cpu = ready_queue.pop(0)
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


average_waiting_time = waiting_time / len(processes)
print(f"\nAverage Waiting Time: {average_waiting_time:.2f}")

# Calculate and display average turnaround time
turnaround_times = [process['finish_time'] - process['arrival_time'] for process in processes]
average_turnaround_time = sum(turnaround_times) / len(turnaround_times)
print(f"Average Turnaround Time: {average_turnaround_time:.2f}")
