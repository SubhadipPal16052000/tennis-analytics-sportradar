
import subprocess
import sys
import time
from datetime import datetime

ETL_JOBS = [
    ("Competitions ETL", "fetch_competitions.py"),
    ("Complexes ETL", "fetch_complexes.py"),
    ("Rankings ETL", "fetch_ranking.py"),
]

def run_job(job_name, script_name):
    print("\n" + "=" * 60)
    print(f"▶ STARTING: {job_name}")
    print(f"▶ Script: {script_name}")
    print(f"▶ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    start_time = time.time()

    try:
        subprocess.run(
            [sys.executable, script_name],
            check=True
        )
        status = "SUCCESS"
    except subprocess.CalledProcessError as e:
        status = "FAILED"
        print(f"\n ERROR in {job_name}")
        print(e)
    finally:
        elapsed = round(time.time() - start_time, 2)
        print(f"\n Execution Time: {elapsed} seconds")
        print(f" STATUS: {status}")

    return status


def main():
    print("\n TENNIS ANALYTICS – ETL PIPELINE")
    print("=" * 60)

    pipeline_start = time.time()
    results = {}

    for job_name, script in ETL_JOBS:
        results[job_name] = run_job(job_name, script)

    print("\n" + "=" * 60)
    print(" ETL PIPELINE SUMMARY")
    print("=" * 60)

    for job, status in results.items():
        print(f"{job:<25} : {status}")

    total_time = round(time.time() - pipeline_start, 2)
    print("\n TOTAL PIPELINE TIME:", total_time, "seconds")

    if all(status == "SUCCESS" for status in results.values()):
        print("\n ALL ETL JOBS COMPLETED SUCCESSFULLY")
    else:
        print("\n PIPELINE COMPLETED WITH ERRORS – CHECK LOGS")

    print("=" * 60)


if __name__ == "__main__":
    main()
