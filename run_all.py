
import subprocess
import sys

print("=" * 60)
print("Freight Rate Prediction Pipeline")
print("=" * 60)

# Step 1: Install requirements
print("\nStep 1: Installing requirements...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Step 2: Train model and make predictions
print("\nStep 2: Training model and making predictions...")
subprocess.run([sys.executable, "train_model.py"])

# Step 3: Run scorer
print("\nStep 3: Running scorer...")
subprocess.run([sys.executable, "score.py", "--predictions", "validation_predictions.csv", "--december-predictions", "december-chart-inputs.csv"])

print("\n" + "=" * 60)
print("Pipeline complete!")
print("=" * 60)
print("\nGenerated files:")
print("- validation_predictions.csv (12,000 predictions)")
print("- december-chart-inputs.csv (31 predictions)")
print("- scorer_results/candidate_december.png (December chart)")
print("\nDocumentation:")
print("- README.md (project documentation)")
print("- ASSESSMENT_REPORT.md (detailed methodology)")
print("- train_model.py (training code)")
print("- score.py (scorer and chart generator)")
