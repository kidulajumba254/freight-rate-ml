# Loom Video Script - Freight Rate Prediction Assessment

**Time: 2-3 minutes**
**Camera: ON**

---

## Introduction (0:00-0:20)

"Hi, I'm [Your Name], and today I'll walk you through my freight rate prediction assessment. The goal was to predict freight rates for trucking loads using machine learning, specifically to predict rates for 12,000 validation loads and generate a December 2025 forecast chart."

---

## Data Overview (0:20-0:40)

"I worked with 48,000 labeled training samples containing load characteristics like pickup/delivery locations, distance, weight, equipment type, market index, and quote signal. The target variable was the posted rate for each load."

"For data cleaning, I handled 300 missing weight values and 374 missing market index values by filling them with their respective medians. This ensured no data loss while maintaining statistical integrity."

---

## Data Splitting Strategy (0:40-1:00)

"I used an 80-20 random split for initial evaluation, but I also implemented a chronological (time-based) split to better simulate the actual forecasting task."

"The random split gave us an MAE of 113.79 and R² of 0.8680. However, I recognize this is optimistic for real-world forecasting. The chronological split—training on earlier data and validating on later data—gave an MAE of 122.23 and R² of 0.8262, which is a more realistic proxy for the November-December prediction period."

---

## Feature Engineering (1:00-1:20)

"I engineered several features from the data:"
- "Temporal features: year, month, day, day of week, day of year, and week of year"
- "Weight per mile: to normalize weight by distance"
- "Equipment type: one-hot encoded as Dry Van, Flatbed, and Reefer"

"I want to note that some features like distance categories and weight categories were computed for analysis but not included in the final model to keep it focused on the most predictive features."

---

## Model Selection (1:20-1:40)

"I tested two models: Random Forest and Gradient Boosting Regressor. Gradient Boosting performed better with an MAE of 113.79 compared to Random Forest's 132.24 on the random split."

"I selected Gradient Boosting because it handles non-linear relationships well, which is important for freight rate prediction, and it showed better generalization across the validation sets."

---

## Feature Importance (1:40-2:00)

"The feature importance analysis revealed that distance is by far the most important factor, accounting for 97.5% of the model's predictions. This aligns with industry knowledge that longer hauls have significantly higher rates."

"Equipment type contributed about 0.8%, and weight and market index each contributed around 0.4%. This suggests that distance is the primary driver, but equipment type does play a secondary role."

---

## December Chart (2:00-2:20)

"For the December chart predictions, I generated predicted rates for a fixed route from Lexington to Fort Wayne, 360 miles, Dry Van, 32,000 pounds for each day in December 2025."

[Show the chart]
"The chart shows the predicted rates varying by day, reflecting the temporal patterns the model learned from the training data. The rates cluster around $860, with slight variations based on the day of the week and other temporal features."

---

## Limitations (2:20-2:40)

"There are several limitations to acknowledge:"
- "The random split is optimistic compared to the chronological split"
- "Distance dominates at 97.5%, suggesting opportunity for improvement with more diverse features"
- "Pickup and delivery cities could be better utilized with geospatial features"
- "Equipment type has low importance, which might need more data"

"Future improvements could include geospatial features, seasonal modeling, and external data like fuel prices or economic indicators."

---

## Conclusion (2:40-3:00)

"In summary, the Gradient Boosting model achieved strong predictive power with an R² of 0.8680 on the random split and 0.8262 on the more realistic chronological split. The model successfully generated predictions for all 12,000 validation loads and the December 2025 chart."

"The assessment highlights the importance of using time-based validation for forecasting tasks and provides a solid foundation for freight rate prediction. Thank you for watching."

---

## Key Points to Emphasize

✅ **80-20 random split vs chronological split** - explain why both matter
✅ **Gradient Boosting outperformed Random Forest** - show the metrics
✅ **Distance is 97.5% important** - key insight
✅ **December chart shows temporal patterns** - point to the chart
✅ **Limitations acknowledged** - shows critical thinking
✅ **Model explains 82.6-86.8% of variance** - strong performance

---

## Tips for Recording

1. **Camera on** as required
2. **Screen share** to show:
   - The December chart (scorer_results/candidate_december.png)
   - Feature importance table
   - Model performance metrics
3. **Speak clearly and at a moderate pace**
4. **Keep it under 3 minutes** - this script is timed for 2:40
5. **Be conversational** - don't just read the script
6. **Highlight the chart** when you show it

---

## Optional Visual Aids to Show During Video

1. **ASSESSMENT_REPORT.md** - scroll through sections
2. **scorer_results/candidate_december.png** - December chart
3. **train_model.py** - show feature engineering code
4. **Feature importance output** - from terminal run
5. **validation_predictions.csv** - show format

---

## Quick Reference for Spontaneous Speaking

If you want to speak more naturally:

**Instead of reading word-for-word:**
- "The data had some missing values" → "I had to handle about 300 missing weights and almost 400 missing market indices"
- "The model achieved strong performance" → "The Gradient Boosting model explains about 87% of the variance in freight rates"
- "Distance is the most important feature" → "Distance is overwhelmingly important—nearly 98% of the prediction comes from distance alone"

**Natural transitions:**
- "Moving on to..." / "Next, let's talk about..."
- "What's interesting here is..."
- "The key takeaway is..."
- "This makes sense because..."

---

## Practice Tips

1. **Time yourself** - read through once to check timing
2. **Mark key points** - note where to show the chart
3. **Pause for emphasis** - especially on metrics and limitations
4. **Be honest about limitations** - this shows maturity
5. **End strong** - reiterate the main achievement

Good luck with your recording! 🎥
