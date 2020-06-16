COVID-19 Risk Prediciton Tool.


Create an environment to install and run tools. 
module load Python/3.6.6-foss-2018b 
module load Anaconda2/4.2.0
conda create --name env
source activate env
conda install plotly
pip install streamlit

Looks like streamlit package is not available for conda. I guess we're using it locally now.