import subprocess

print("\nStarting AI Sales Intelligence Pipeline...\n")

scripts = [
    "llm_analysis/generate_insights.py",
    "llm_analysis/forecast_engine.py",
    "llm_analysis/anomaly_detection.py",
    "llm_analysis/report_generator.py"
]

for script in scripts:
    print(f"\nRunning {script}...\n")
    subprocess.run(["python", script])

print("\nPipeline Completed Successfully.\n")
print("Check the outputs folder for generated results.")