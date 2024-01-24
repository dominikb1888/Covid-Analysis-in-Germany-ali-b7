# COVID-19 Data Visualization in Germany (2020-2022)

## Description
This project aims to conduct a comprehensive analysis of the impact of the Covid-19 pandemic on Germany. Utilizing geographic and COVID-19 data sourced from the World Health Organization (WHO), the project attempts to offer an understanding of the virus' spread and its correlation with healthcare indicators. The primary objective is to analyze the relationship between total cases, population numbers, and death rates. By doing so, the project seeks to provide valuable insights into the effectiveness of healthcare systems across different regions in Germany in managing and mitigating the impact of future pandemics.

## Features


**City-Specific Insights**: Explore data for the 40 most populated cities in Germany, understanding the local impact of the pandemic.   
<img src="Images/graph2.png" width="300" height="200" alt="City-Specific Insights">

**Insights for each year**: Covid data visualization for covid cases throughout each year of the pandemic in the 40 most populated German cities.  
<img src="Images/graph1.png" width="300" height="200" alt="Insights for each year">

 
  

## Key User Groups: Public Health researchers

## Objective:
The primary goal of this project is to empower public health researchers with a comprehensive tool for understanding and analyzing the spread and impact of COVID-19 in Germany. By providing access to regional and city-specific data, the tool aids in the development, adjustment, and assessment of effective public health policies and strategies. Additionally, by identifying trends and correlations, researchers can strategically plan and implement public health interventions.

## Functionality:
**Data Comparison**: Enables users to efficiently compare COVID-19 data across different regions and cities within Germany. This comparative analysis is vital for identifying patterns, hotspots, and anomalies in virus transmission.  
**Impact Assessment**: Assists in evaluating the effectiveness of health measures and interventions by analyzing data trends over time.  

## Real-World Application:
**Resource Allocation for Policy Makers**: A health policy maker can utilize the interactive map feature to compare infection rates and death tolls across various states or cities. This information is crucial in identifying regions that require additional resources or adjustments in policy measures.  
**Research and Planning**: Researchers can leverage city-specific insights to investigate correlations between variables such as population density and virus spread. Such analysis is important for future urban planning and healthcare resource management.  

## User Benefit:
**Informed Decision Making**: The tool provides a user-friendly interface for accessing and interpreting complex data, leading to more informed and timely decision-making processes.  
**Strategic Planning**: Public health researchers can strategically plan and implement public health interventions by identifying trends and correlations.  

## Installation and Setup Instructions

### Running the Application in a Development Container Using GitHub Codespaces

1. **Open in GitHub Codespaces**:
   - Go to the GitHub repository: [https://github.com/ali-b7/Covid-Analysis-in-Germany.git].
   - Click on 'Code', then select 'Open with Codespaces'.
   - Choose 'New codespace' to create a new development environment.

2. **Automatic Setup**:
   - Once open in GitHub Codespaces, the development container will automatically set up the environment for you.

3. **Accessing the Application**:
   - Once the Codespace environment is ready and the application starts, go to the 'Ports' panel.
   - Find the port `8000` listed there.
   - Click on 'Open in Browser' next to port `8000`. This will open a new browser tab or window with the application running.

### Local Setup

1. **Clone the Repository**:
   - Run `git clone https://github.com/ali-b7/Covid-Analysis-in-Germany.git` in the terminal.
   - Navigate to the cloned directory.

2. **Install Dependencies**:
   - In the terminal, run `pip install -r requirements.txt`.

3. **Starting the Application**:
   - Run `uvicorn main:app --host 127.0.0.1 --port 8000 --reload` in the terminal.
   - The application will be available on `http://localhost:8080` or the specified port.

## Notes
This project is still a work in progress.

## Contact
For support, feedback, or contributions, feel free to contact me:

- Email: ali.badran@stud.th-deg.de

## License

This project is open source and available under the [MIT License](LICENSE).

