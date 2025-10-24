# Setup Instructions

## Getting Started with the Renewable Energy Portfolio Optimization Project

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.9 or higher** - [Download here](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Git** (optional, for version control) - [Download here](https://git-scm.com/)
- **Jupyter Notebook or JupyterLab** (will be installed with requirements)

### Step-by-Step Setup

#### 1. Extract the Project

If you received this as a ZIP file:
```bash
# Windows: Right-click and "Extract All"
# Mac: Double-click the ZIP file
# Linux: 
unzip renewable-portfolio-optimization.zip
cd renewable-portfolio-optimization
```

#### 2. Create a Virtual Environment (Highly Recommended)

**Why?** Virtual environments keep your project dependencies isolated from other Python projects.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command line, indicating the virtual environment is active.

#### 3. Install Dependencies

With your virtual environment activated:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take a few minutes as it downloads and installs all required packages.

**Note:** If you encounter issues with TensorFlow or other large packages, you can install a minimal version first:
```bash
pip install numpy pandas matplotlib seaborn scikit-learn statsmodels jupyter
```

Then install additional packages as needed.

#### 4. Download Initial Data

Run the data processing script to generate initial datasets:
```bash
python src/data_processing.py
```

This will create synthetic ERCOT data in the `data/raw/` and `data/processed/` directories.

**Expected output:**
```
Generating synthetic ERCOT DAM price data...
Saved to data/raw/ercot_dam_prices.csv
Generating synthetic ERCOT load data...
Saved to data/raw/ercot_load.csv
...
```

#### 5. Launch Jupyter Notebook

Start Jupyter to work with the analysis notebooks:
```bash
jupyter notebook
```

Or if you prefer JupyterLab:
```bash
jupyter lab
```

Your web browser will open with the Jupyter interface.

#### 6. Open the First Notebook

Navigate to `notebooks/` and open `01_data_exploration.ipynb` to begin your analysis!

### Project Structure Overview

```
renewable-portfolio-optimization/
├── README.md                 # Project overview and documentation
├── requirements.txt          # Python package dependencies
├── setup_instructions.md     # This file
├── .gitignore               # Git ignore rules
│
├── data/
│   ├── raw/                 # Raw data files (created by scripts)
│   │   ├── ercot_dam_prices.csv
│   │   ├── ercot_load.csv
│   │   ├── ercot_renewable_generation.csv
│   │   └── weather_data.csv
│   └── processed/           # Processed/merged datasets
│       └── merged_data.csv
│
├── notebooks/               # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_price_forecasting.ipynb (to be created)
│   ├── 03_generation_modeling.ipynb (to be created)
│   ├── 04_portfolio_optimization.ipynb (to be created)
│   └── 05_hedging_strategy.ipynb (to be created)
│
├── src/                     # Python source code
│   ├── __init__.py
│   ├── data_processing.py  # Data download and processing
│   ├── visualization.py    # Plotting utilities
│   ├── price_models.py     # Price forecasting (to be created)
│   ├── generation_models.py # Generation modeling (to be created)
│   ├── optimization.py     # Portfolio optimization (to be created)
│   └── hedging.py          # Hedging strategies (to be created)
│
├── tests/                   # Unit tests
│   └── __init__.py
│
└── results/                 # Analysis outputs
    ├── figures/             # Saved plots
    └── reports/             # Generated reports
```

### Development Workflow

1. **Data Collection** → Run `python src/data_processing.py`
2. **Exploratory Analysis** → Work through notebooks 01-05
3. **Model Development** → Create Python modules in `src/`
4. **Testing** → Write tests in `tests/`
5. **Documentation** → Update README and notebooks with findings

### Common Issues and Solutions

#### Issue: "pip not found"
**Solution:** Ensure Python is installed and in your PATH. Try `python -m pip` instead of just `pip`.

#### Issue: "jupyter not found"
**Solution:** Make sure you've activated your virtual environment and installed requirements.

#### Issue: Package installation fails
**Solution:** Try installing packages individually:
```bash
pip install numpy pandas matplotlib seaborn scikit-learn
pip install statsmodels jupyter ipykernel
```

#### Issue: Kernel not found in Jupyter
**Solution:** Register your virtual environment as a kernel:
```bash
python -m ipykernel install --user --name=renewable-opt --display-name="Python (Renewable Opt)"
```

#### Issue: ModuleNotFoundError in notebooks
**Solution:** Make sure:
1. Your virtual environment is activated
2. You're running Jupyter from the project root directory
3. The `src` directory is in your Python path (notebooks handle this automatically)

### Next Steps

Once setup is complete:

1. **Explore the Data** (Week 1)
   - Open `notebooks/01_data_exploration.ipynb`
   - Understand ERCOT price patterns
   - Analyze correlations
   
2. **Build Price Models** (Week 2)
   - Create GARCH volatility models
   - Implement ARIMA forecasting
   - Try XGBoost and LSTM
   
3. **Optimize Portfolio** (Week 3)
   - Model renewable generation
   - Implement Markowitz optimization
   - Calculate VaR
   
4. **Develop Hedging Strategy** (Week 4)
   - Design hedging rules
   - Backtest performance
   - Analyze P&L
   
5. **Polish & Document** (Week 5)
   - Create visualizations
   - Write up findings
   - Prepare for portfolio/interviews

### Getting Help

- **Python Documentation:** https://docs.python.org/3/
- **Pandas Documentation:** https://pandas.pydata.org/docs/
- **Jupyter Documentation:** https://jupyter.org/documentation
- **Project Issues:** Check the README or create an issue

### Tips for Success

1. **Work incrementally** - Complete one notebook before moving to the next
2. **Commit often** - Use Git to track your progress
3. **Document your work** - Add markdown cells explaining your reasoning
4. **Test your code** - Write unit tests for critical functions
5. **Ask questions** - If stuck, break the problem into smaller pieces

### Deactivating Virtual Environment

When you're done working:
```bash
deactivate
```

This returns you to your system's Python environment.

---

**Happy Coding!** 🚀

If you have questions about this project, contact:
- Email: berg.amalie@outlook.com
- LinkedIn: linkedin.com/in/amalie-berg
