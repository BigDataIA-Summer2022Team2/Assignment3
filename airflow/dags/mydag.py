import numpy
import tensorflow as tf
from keras.models import load_model
import os
from keras.applications.inception_v3 import preprocess_input
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

doc_md = """
### DAG
#### Purpose
This DAG takes all testing images and output the confusion matrix of the data.
"""
def matrix():
    abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    test_path = abs_path+"/test"
    model = load_model(abs_path + "/trained_model.h5")
    model.compile(optimizer="adam",loss='binary_crossentropy',metrics=['accuracy'])

    #Get Confusion Matrix
    test_generator = tf.keras.preprocessing.image.ImageDataGenerator()
    test_data_generator = test_generator.flow_from_directory(test_path,target_size=(256, 256),batch_size=50,shuffle=False)
    test_steps_per_epoch = numpy.math.ceil(test_data_generator.samples / test_data_generator.batch_size)
    predictions = model.predict(test_data_generator, steps=test_steps_per_epoch)

    predicted_classes = predictions.reshape(715,)
    #predicted_classes = numpy.argmax(predictions, axis=-1)
    predicted_classes = (predicted_classes > 0.5).astype("int32")
    true_classes = test_data_generator.classes
    class_labels = list(test_data_generator.class_indices.keys())
    matrix = confusion_matrix(true_classes, predicted_classes)
    # print('Classification Report')
    # print(classification_report(true_classes, predicted_classes, target_names=class_labels))
    print(matrix)

    # ax = sns.heatmap(matrix, annot=True, cmap='Blues')

    # ax.set_title('Confusion Matrix with labels\n\n')
    # ax.set_xlabel('\nPredicted Values')
    # ax.set_ylabel('Actual Values ')

    # ## Ticket labels - List must be in alphabetical order
    # ax.xaxis.set_ticklabels(['False','True'])
    # ax.yaxis.set_ticklabels(['False','True'])

    # ## Display the visualization of the Confusion Matrix.
    # plt.show()



with DAG("my_dag",start_date=datetime(2022, 1, 1),schedule_interval="@daily",catchup=False,) as dag:

    get_matrix = PythonOperator(
        task_id = 'get_matrix',
        python_callable=matrix
    )
    # Confusion_Matrix = PythonOperator(
    #     task_id="training_model_A",
    #     python_callable=test_model
    # )
    
        
