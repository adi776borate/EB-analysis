# Electoral Bond Analysis Website

This project aims to design a website with a fully integrated backend for analyzing electoral bond data. 
The website allows users to search, filter, and visualize electoral bond information such as purchases by individuals and companies, redemptions by political parties, donations given and received, and more.

##Web Design Features

**Features**
I have implmented following features in my website, you can access all these through index page.

   - A robust search functionality based on bond number  to quickly search for specific records.
   - A feature to show the number and total value of bonds purchased per year for a selected company/individual.
   - A feature to show the number and total value of bonds per year for a selected political party.
   - An option to select a political party from a drop-down/search, shows which companies have donated to it and what amount individually and combined.
   - An option to select a company from a drop-down/search, showcasing which parties they have donated and what amount individually and combined.
   - A feature to display a Pie chart depicting the total amount of donations to all parties.
   - A functionality to save displayed plots in PNG/JPEG format.
   - (*Bonus feature) to display line chart of how EB purchasing and redempting counts vary throughout the year.

**Plots**
   - Created and showcased plots using data fetched from the database, such as Pie charts, Bar charts, Line charts, etc.

## Folder Structure

- `main.py`: Backend code using Flask.
- `templates/`: Frontend HTML/CSS/JS files.
- `data/`: Folder containing input PDFs and output CSV files and a .ipynb file written to convert .pdf to .csv.
- `screenshot/`: Folder containing all the screenshots of UI in a pdf file
- `README.md`: Instructions for setting up the website locally and documenting the project.

## Instructions for Setting Up the Website Locally

1. Clone the GitHub repository: `git clone <https://github.com/adi776borate/EB-analysis.git>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Flask application: `python main.py`
4. Open a web browser and navigate to `http://localhost:5000` to access the website.

## Screenshots

All the screenshots of UI are captured and stored in thi

## Acknowledgements

- This project was completed as part of an assignment.
- The data used for analysis was provided as part of the assignment.
- ChartJS library was used for creating visualizations.
