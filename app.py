from flask import Flask ,render_template,jsonify,request,send_file
from src.exception import CustomException
from src.logger import logging
import os,sys

from src.pipeline.predict_pipeline import PredictionPipeline
from src.pipeline.train_pipeline import TraininingPipeline

app=Flask(__name__)

@app.route('/')

def home():
    return "Welcome to the Sensor Fault Detection application"

@app.route('/train')

def train_route():
    train_pipeline= TraininingPipeline()
    train_pipeline.run_pipeline()

    return "Training successful!!"

@app.route('/predict',methods=['POST','GET'])
def upload():
    try:
        if request.method=='POST':
            prediction_pipeline=PredictionPipeline(request)
            prediction_file_details=prediction_pipeline.run_pipeline()
            logging.info("prediction is complete.Downloading prediction file")
            return send_file(prediction_file_details.prediction_file_path,
                             download_name=prediction_file_details.prediction_file_name,
                             as_attachment=True)
        else:
            return render_template('upload_file.html')
        
    except Exception as e:
        raise CustomException(e,sys)
    
if __name__=="__main__":
    print("Your app is live at: http://127.0.0.1:5000")
    app.run(host="0.0.0.0",port=5000,debug=True)

