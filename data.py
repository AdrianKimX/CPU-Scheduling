from flask import flask
def calculate(name, processes, mode, quantum=2):
    jobs = [p.copy() for p in processes]
    time = 0
    chart = []
    done = []

    while len(done) < len(jobs):
        ready = [
            p for p in jobs
            if p["id"]not in done and p["arrival"] <=
time            
        ]

        if not ready:
            time += 1
            continue

        if mode == "FCFS":
            p = min(ready, key=lambda x: x["arrival"])
        elif mode == "SJF":
            p = min(ready, key=lambda x: x["burst"])
        elif mode == "Priority":
             p = min(ready, key=lambda x: x["Priority"])
        else:
            p = ready[0]

        start = time

        if mode == "RR":
            run = min(quantum, p["burst"])
        else:
            run = p["burst"]

        time += run
        p["burst"] -= run
        chart.append(p["id"], start, time)

        if p["burst"] == 0:
            p["completion"] = time
            done.append(p["id"])

        elif mode == "RR":
            jobs.remove(p)
            jobs.append(p)

        print("\n , name")
        print("Gantt Chart")

        for item in chart:
            print("|",p[0], end=" ")
        print("|")

        print(chart[0][1], end=" ")
        for p in chart:
            print (p[2], end= " ")

        print("\n\nProcess\tCT\tTT\tWT")

        for p in sorted(jobs, key=lambda x: x["id"]):
            tt = p["completion"] - p["arrival"]
            wt = tt - next(
                x["burst"] for x in processes if x["id"] ==
    p["id"]
            )
            print(p["id"], "\t", p["completion"], "\t", tt,"\t", wt)

    processes = []

    n = int(input("Enter number of processes:"))

    for i in range(n):
        print("\nProcess P" + str(i + 1))

        arrival = int(input("Enter Arrival Time:"))
        burst = int(input("Enter Burst Time:"))
        priority = int(input("Enter Priority:"))

        processes.append({
            "id": "P" + str(i + 1),
            "arrival": arrival,
            "burst": burst,
            "original_burst": burst,
            "priority": priority,
            "order": i
        })

    quantum = int(input("\nEnter Time Quantum:"))

    calculate("FCFS", processes, "FCFS")
    calculate("SJF", processes, "SJF")
    calculate("Priority Scheduling", processes, "Priority")
    calculate("Round Robin", processes, "RR", quantum)

