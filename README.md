# Airline Flight Review and Visualization 
Date: 2025-03-31    
Authors: Andrew Jobe, Christian Ramos, Hussain Gardezi, Jeff Gielniak

Our team used two Kaggle datasets covering flight delay times and passenger reviews of different aspects of airline travel to create tools to allow a potential customer to pick the ideal flight for their needs.  Below are a summary of the tools:

- Day_of_Week.ipynb: Using the code in the Jupyter Notebook, the user is asked to input 3 days they are looking at for potential departure days.  The code then kicks them to an external Bar Chart showing delays for the major airlines for those 3 days

- Airlines_comparing_ratings.ipynb: Using the code in the Jupyter Notebook, the user inputs 3 Airlines and 3 Ratings categories they would like to compare and they are sent to an external Bar Chart displaying that comparison

- The Airline Reliability Dashboard (airline_reliability_plot.py) compares delay percentage vs. cancellation percentage by airline.  Users can filter by airline to focus on performance comparisons.  Quadrants visually segment airlines into high/low performance groups.

Run with: bokeh serve --show airline_reliability_plot.py

- The Airport Reliability Dashboard (airport_reliability_plot.py) compares average delay time vs. delay percentage by origin airport.  Includes dropdowns to filter by the airport and the number of top airports by traffic.  The circle size reflects the average delay length. Quadrants provide performance segmentation.

Run with: bokeh serve --show airport_reliability_plot.py

- This project analyzes airline ratings based on month, traveler type, and cabin class using an interactive dataset, providing insights to help travelers make informed booking decisions. The dataset, Analysis_complete.csv, was cleaned by checking for missing values and aggregating data by key attributes, including month, traveler type, cabin class, and airline name. The analysis identified the best-rated airlines per month, ranked overall airline performance, and examined how traveler type and cabin class influence ratings. Key findings indicate that January and July have the highest ratings, while December scores the lowest. Southwest Airlines consistently ranks as the best-rated airline, and business travelers in First Class provide the highest ratings. The visualization component includes an interactive Bokeh dashboard featuring a bar chart of monthly average ratings, with filters for traveler type, cabin class, and airline selection. Future steps involve analyzing how delays and cancellations impact ratings, comparing airfare trends with rating changes, and expanding the dashboard with additional insights and filters. My file name is flight_dashboard. After you run my code, in the terminal, you put this command bokeh serve --show flight_dashboard.py to activate the Bokeh dashboard. Also, make sure you correct the file path.

Summary of Input Datasets used:
1.https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018?select=2018.csv
CSV name in Resources folder in repository: 2018data.csv
*Took random 0.5% sample of data due to size of dataset

2. https://data.humdata.org/dataset/ourairports-usa
CSV name in Resources folder in repository: us-airports.csv

3. https://www.kaggle.com/datasets/joelljungstrom/128k-airline-reviews
CSV name in Resources folder in repository: AirlineReviews_ten_percent.csv
*Took random 10% sample of data due to size of dataset


CSV files we generated during coding/cleaning explanations:
IATA_airlines.csv - Airline codes table
IATA_airports.csv - Airport codes table
Main_flight_data.csv - 2018 flight data for 9 major airlines, flights originating in the US
Airline_reviews.csv - Average reviews of 9 major airlines
Analysis_Complete.csv - Our main dataset after merged in SQLAlchemy

We used 'Bokeh' as an additional Python library to enhance our visualizations
https://bokeh.org

We leveraged ChatGPT as a tool to help develop the framework for certain aspects of the project. It provided code snippets and examples for us to base our code structure off of.

# Ethical Considerations

While building this project, our team remained mindful of the ethical use and presentation of data. We recognize that flight delays and cancellations can result from a range of factors, including weather, air traffic control, infrastructure, and airline operations — many of which are outside an airline’s or airport’s direct control.

To avoid misleading interpretations:

- We removed outliers or obviously incomplete data (e.g., some airports show no cancellations). 
- We made assumptions (e.g., a threshold of 15 minutes for delay classification) transparent in our code.
- Visualizations include filters and interactivity so users can explore the data instead of relying on one static view.

We also acknowledge that travel experiences can vary greatly by traveler type, route, and season. Our project aims to inform, not prescribe and should be used alongside other tools when evaluating air travel options.

# Database Reasoning

For this project, we used SQLite with SQLAlchemy because it’s simple, efficient, and perfect for local development. It allowed us to quickly build and test relationships between flights, airlines, airports, and ratings without needing a complex database setup. We used pandas to clean and transform our 2018 airline dataset, then loaded everything into our database. SQLAlchemy helped us model the data clearly in Python, and we used an ERD to map out table relationships. This setup made it easy to run joined queries and analyze airline performance, delays, and more — all while keeping the project clean, scalable, and easy to maintain.
