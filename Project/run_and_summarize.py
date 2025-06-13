"""
run_and_summarize.py

This orchestration script runs the OpenLane flow using config.json and then parses
key metrics from the output reports: area, power, timing, and other constraints.
It prints a clean summary to validate that the synthesized hardware meets the design
specifications and to support project documentation.
"""

import os
import subprocess
import time
import re

RUNS_DIR = "runs"
CONFIG_FILE = "config.json"
CLOCK_PERIOD_NS = 10.0  # Adjust if needed

def run_openlane():
    print("🚀 Launching OpenLane flow...")
    try:
        subprocess.run(["openlane", CONFIG_FILE], check=True)
    except subprocess.CalledProcessError:
        print("❌ OpenLane flow failed.")
        exit(1)

def find_latest_run():
    runs = sorted(
        [d for d in os.listdir(RUNS_DIR) if d.startswith("RUN_")],
        reverse=True
    )
    return os.path.join(RUNS_DIR, runs[0]) if runs else None

def extract_area(area_file):
    with open(area_file) as f:
        content = f.read()
        match = re.search(r"Total cell area\s*:\s*([\d.]+)", content)
        return float(match.group(1)) if match else None

def extract_power(power_file):
    with open(power_file) as f:
        for line in f:
            if "Total" in line and "mW" in line:
                return line.strip()
    return None

def extract_slack(timing_file):
    with open(timing_file) as f:
        content = f.read()
        wns = re.search(r"Worst slack.*?([-]?\d+\.\d+)", content)
        tns = re.search(r"Total slack.*?([-]?\d+\.\d+)", content)
        return (wns.group(1) if wns else None, tns.group(1) if tns else None)

def summarize_metrics(run_dir):
    print(f"\n📊 Summary for run: {run_dir}\n")
    area_file = os.path.join(run_dir, "reports", "synthesis", "area.rpt")
    power_file = os.path.join(run_dir, "reports", "signoff", "power.rpt")
    timing_file = os.path.join(run_dir, "reports", "signoff", "timing.rpt")

    if os.path.exists(area_file):
        area = extract_area(area_file)
        print(f"🧠 Total Cell Area: {area:.2f} µm²" if area else "❌ Area info missing.")
    else:
        print("❌ Area report not found.")

    if os.path.exists(power_file):
        power = extract_power(power_file)
        print(f"⚡ Power Report: {power}" if power else "❌ Power info missing.")
    else:
        print("❌ Power report not found.")

    if os.path.exists(timing_file):
        wns, tns = extract_slack(timing_file)
        print(f"⏱ Timing Slack:")
        print(f"   - WNS: {wns} ns" if wns else "   - WNS: ❌ Missing")
        print(f"   - TNS: {tns} ns" if tns else "   - TNS: ❌ Missing")
        if wns and float(wns) >= 0:
            print(f"   - ✅ Estimated Latency: {CLOCK_PERIOD_NS} ns")
    else:
        print("❌ Timing report not found.")

def main():
    run_openlane()
    run_dir = find_latest_run()
    if run_dir:
        summarize_metrics(run_dir)
    else:
        print("❌ Could not locate latest run directory.")

if __name__ == "__main__":
    main()
