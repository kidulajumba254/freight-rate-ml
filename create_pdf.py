"""
Convert assessment report to PDF with December chart
"""

import markdown
from weasyprint import HTML

# Read the markdown report
with open('ASSESSMENT_REPORT.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML
html_content = markdown.markdown(md_content)

# Add CSS styling
html_with_style = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1 {{ color: #333; border-bottom: 2px solid #064A56; padding-bottom: 10px; }}
        h2 {{ color: #444; margin-top: 30px; }}
        h3 {{ color: #555; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f5f5f5; }}
        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        .december-chart {{
            text-align: center;
            margin: 30px 0;
        }}
        .december-chart img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    {html_content}
    <div class="december-chart">
        <h2>December 2025 Predicted Load Rate Chart</h2>
        <img src="scorer_results/candidate_december.png" alt="December 2025 Predicted Load Rate Chart">
        <p><em>Figure: Predicted freight rates for Lexington to Fort Wayne route (360 miles, Dry Van, 32,000 lbs) in December 2025</em></p>
    </div>
</body>
</html>
"""

# Generate PDF
HTML(string=html_with_style).write_pdf('ASSESSMENT_REPORT.pdf')

print("PDF generated: ASSESSMENT_REPORT.pdf")
