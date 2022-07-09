import warnings

import pandas as pd
from flask import Flask
# from sklearn.externals import joblib
import joblib
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
app = Flask(__name__)

model_dump1 = joblib.load(r'project\static\adminResources\Model\Model_CropProduction.sav')
model_dump2 = joblib.load(r'project\static\adminResources\Model\Model_CropPrice.sav')


class CropPrice_YieldPrediction:
    def dataPreprocessing(self, columnName, df):
        le = LabelEncoder()

        le.fit(df[columnName])

        df[columnName] = le.transform(df[columnName])

    def cropPrediction(self, districtName, predictionCrop, predictionYear, predictionArea,
                       predictionProduction):
        columnName1 = ['District', 'Crop', 'Year', 'Area', 'Production']
        columnValue1 = [districtName, predictionCrop, predictionYear, predictionArea,
                        predictionProduction]

        df1 = pd.DataFrame([columnValue1], columns=columnName1)

        self.dataPreprocessing('District', df1)
        self.dataPreprocessing('Crop', df1)

        X_test1 = df1.as_matrix()
        print(type(X_test1))

        prediction1 = model_dump1.predict(X_test1)
        print('predicted Yield>>>', prediction1)

        predicted_Yield = prediction1[0]
        columnName2 = ['District', 'Crop', 'Year', 'Area', 'Production', 'Yield']
        columnValue2 = [districtName, predictionCrop, predictionYear, predictionArea,
                        predictionProduction, predicted_Yield]

        df2 = pd.DataFrame([columnValue2], columns=columnName2)

        self.dataPreprocessing('District', df2)
        self.dataPreprocessing('Crop', df2)

        X_test2 = df2.as_matrix()
        print(type(X_test2))

        prediction2 = model_dump2.predict(X_test2)
        print('predicted cropPrice>>>', prediction2)

        predicted_Price = prediction2[0]

        return float(predicted_Yield), float(predicted_Price)
