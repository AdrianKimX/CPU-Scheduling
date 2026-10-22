
from flask import Flask, render_template, request

app = Flask(__name__)


def calculate(processes, mode, quantum=2):
    jobs = [p.copy() for p in processes]
    remaining = {p["id"]: p["burst"] for p in jobs}
    chart = []
    time = 0

    if mode == "RR":
        queue = []
        pending = sorted(jobs, key=lambda p: (p["arrival"], p["order"]))
        index = 0

        while index < len(pending) or queue:
            if not queue:
                time = max(time, pending[index]["arrival"])

            while index < len(pending) and pending[index]["arrival"] <= time:
                queue.append(pending[index])
                index += 1

            p = queue.pop(0)
            start = time
            run = min(quantum, remaining[p["id"]])

            time += run
            remaining[p["id"]] -= run
            chart.append({
                "id": p["id"],
                "start": start,
                "end": time
            })

            while index < len(pending) and pending[index]["arrival"] <= time:
                queue.append(pending[index])
                index += 1

            if remaining[p["id"]] > 0:
                queue.append(p)

    else:
        completed = set()

        while len(completed) < len(jobs):
            ready = [
                p for p in jobs
                if p["id"] not in completed
                and p["arrival"] <= time
            ]

            if not ready:
                time = min(
                    p["arrival"] for p in jobs
                    if p["id"] not in completed
                )
                ready = [
                    p for p in jobs
                    if p["id"] not in completed
                    and p["arrival"] <= time
                ]

            if mode == "SJF":
                p = min(ready, key=lambda x: (x["burst"], x["order"]))
            elif mode == "Priority":
                p = min(ready, key=lambda x: (x["priority"], x["order"]))
            else:
                p = min(ready, key=lambda x: (x["arrival"], x["order"]))

            start = time
            time += remaining[p["id"]]

            chart.append({
                "id": p["id"],
                "start": start,
                "end": time
            })

            remaining[p["id"]] = 0
            completed.add(p["id"])

    completion = {}
    for entry in chart:
        completion[entry["id"]] = entry["end"]

    stats = []
    for p in sorted(jobs, key=lambda x: x["order"]):
        ct = completion[p["id"]]
        tt = ct - p["arrival"]
        wt = tt - p["burst"]

        stats.append({
            "id": p["id"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "priority": p["priority"],
            "completion": ct,
            "turnaround": tt,
            "waiting": wt
        })

    return {
        "mode": mode,
        "chart": chart,
        "stats": stats
    }


@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        try:
            arrivals = request.form.getlist("arrival")
            bursts = request.form.getlist("burst")
            priorities = request.form.getlist("priority")

            if not arrivals or not (
                len(arrivals) == len(bursts) == len(priorities)
            ):
                raise ValueError("Enter all process values.")

            processes = []

            for i, (a, b, pr) in enumerate(
                zip(arrivals, bursts, priorities)
            ):
                arrival = int(a)
                burst = int(b)
                priority = int(pr)

                if arrival < 0 or burst <= 0:
                    raise ValueError(
                        "Arrival must be non-negative and burst must be positive."
                    )

                processes.append({
                    "id": f"P{i + 1}",
                    "arrival": arrival,
                    "burst": burst,
                    "priority": priority,
                    "order": i
                })

            quantum = int(request.form.get("quantum", 2))
            if quantum <= 0:
                raise ValueError("Quantum must be positive.")

            for mode in ["FCFS", "SJF", "Priority", "RR"]:
                results.append(
                    calculate(processes, mode, quantum)
                )

        except ValueError as e:
            return render_template(
                "index.html", results=[], error=str(e)
            )

    return render_template(
        "index.html", results=results, error=None
    )


if __name__ == "__main__":
    app.run(debug=True)
