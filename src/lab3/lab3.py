# ==========================================
# PART 1: BASIC STATISTICS (Slides 5-7)
# ==========================================

from pyspark import SparkConf, SparkContext
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.stat import Statistics
from pyspark.sql import SparkSession
from pyspark.mllib.random import RandomRDDs

#--- 1.1 Summary Statistics  ---
# Create a SparkConf and SparkContext
conf = SparkConf().setAppName("SummaryStatisticsExample")
sc = SparkContext(conf=conf)

# Create an RDD of vectors
data = [
    Vectors.dense([1.0, 2.0, 3.0]),
    Vectors.dense([4.0, 5.0, 6.0]),
    Vectors.dense([7.0, 8.0, 9.0])
]
rdd = sc.parallelize(data)

# Calculate summary statistics using colStats()
summary = Statistics.colStats(rdd)

# Print the summary statistics
print("Mean:", summary.mean())                # Mean of each column
print("Variance:", summary.variance())        # Variance of each column
print("Non-zero entries:", summary.numNonzeros()) # Number of non-zero entries

# Stop the SparkContext for this segment (usually handled by one session in a real script)
sc.stop()


#--- 1.2 Correlations  ---
spark = SparkSession.builder.appName("Correlation Example").getOrCreate()

# Create two RDDs representing two series of data
data1 = [1.0, 2.0, 3.0, 4.0, 5.0]
data2 = [2.0, 3.0, 4.0, 5.0, 6.0]

rdd1 = spark.sparkContext.parallelize(data1)
rdd2 = spark.sparkContext.parallelize(data2)

# Zip the two RDDs together into pairs
paired_rdd = rdd1.zip(rdd2)

# Calculate the correlation between the two series of data
correlation = Statistics.corr(paired_rdd, method="pearson")

# Print the correlation coefficient
print("Pearson Correlation Coefficient:", correlation)


#--- 1.3 Random Data Generation  ---
# Generate random data using RandomRDDs
num_samples = 1000  # Number of random data points
random_data = RandomRDDs.normalRDD(spark.sparkContext, num_samples)

# Show a sample of the generated random data
sample_data = random_data.take(3) 
print("Sample of Random Data:")
for value in sample_data:
    print(value)

# Stop the session to prepare for the next project
spark.stop()


# =========================================================
# PART 2: TITANIC PROJECT - NO PIPELINE (Slides 14-22)
# =========================================================

import os
import findspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, isnull, when, count
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

#--- 2.1 Environment Setup  ---
# (Note: Paths are specific to the Colab environment in the slides)
# os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
# path_to_spark = '/content/spark-3.4.1-bin-hadoop3'
# findspark.init(path_to_spark)

#--- 2.2 Initialize SparkSession  ---
spark = SparkSession.builder \
    .master("local") \
    .appName("Titanic data") \
    .getOrCreate()

#--- 2.3 Read Data  ---
# Replace path with your actual file path
df = spark.read \
    .format("csv") \
    .option("header", "true") \
    .load("/content/drive/MyDrive/big data course/titanic dataset/train.csv")

df.show(5)

#--- 2.4 Data Preprocessing  ---
# Selecting and casting columns
dataset = df.select(
    col('Survived').cast('float'),
    col('Pclass').cast('float'),
    col('Sex'),
    col('Age').cast('float'),
    col('Fare').cast('float'),
    col('Embarked')
)

# Removing null values
dataset = dataset.replace('?', None).dropna(how='any')

#--- 2.5 Categorical Conversion (StringIndexer)  ---
# Convert 'Sex' to numeric 'Gender'
dataset = StringIndexer(
    inputCol='Sex', 
    outputCol='Gender', 
    handleInvalid='keep'
).fit(dataset).transform(dataset)

# Convert 'Embarked' to numeric 'Boarded'
dataset = StringIndexer(
    inputCol='Embarked', 
    outputCol='Boarded', 
    handleInvalid='keep'
).fit(dataset).transform(dataset)

# Drop unnecessary columns
dataset = dataset.drop('Sex').drop('Embarked')

#--- 2.6 Feature Engineering (VectorAssembler)  ---
# Combine features into a single column named 'features'
require_featured = ['Pclass', 'Age', 'Fare', 'Gender', 'Boarded']
assembler = VectorAssembler(inputCols=require_featured, outputCol='features')
transformed_data = assembler.transform(dataset)
transformed_data.show(5)

#--- 2.7 Modeling  ---
# Split dataset into train (80%) and test (20%)
(training_data, test_data) = transformed_data.randomSplit([0.8, 0.2])
print("Number of train samples: " + str(training_data.count()))
print("Number of test samples: " + str(test_data.count()))

# Define Random Forest Classifier
rf = RandomForestClassifier(
    labelCol='Survived', 
    featuresCol='features', 
    maxDepth=5
)

# Train the model
model = rf.fit(training_data)

# Make predictions
predictions = model.transform(test_data)

#--- 2.8 Evaluation  ---
evaluator = MulticlassClassificationEvaluator(
    labelCol='Survived', 
    predictionCol='prediction', 
    metricName='accuracy'
)

# Accuracy
accuracy_train = evaluator.evaluate(model.transform(training_data))
print('Training Accuracy = ', accuracy_train)
accuracy_test = evaluator.evaluate(predictions)
print('Test Accuracy = ', accuracy_test)

spark.stop()


# =========================================================
# PART 3: TITANIC PROJECT - WITH PIPELINE (Slides 24-40)
# =========================================================

from pyspark.ml import Pipeline

# --- 3.1 Setup (Re-initializing for clarity) ---
spark = SparkSession.builder \
    .master("local") \
    .appName("Titanic data") \
    .getOrCreate()

#Read Data 
df = spark.read \
    .format("csv") \
    .option("header", "true") \
    .load("/content/drive/MyDrive/big data course/titanic dataset/train.csv")

#--- 3.2 Define Pipeline Stages  ---
# Split data
(train_df, test_df) = df.randomSplit([0.8, 0.2], 11)

# Stage 1 & 2: StringIndexers
Sex_indexer = StringIndexer(inputCol="Sex", outputCol="Gender")
Embarked_indexer = StringIndexer(inputCol="Embarked", outputCol="Boarded")

# Stage 3: VectorAssembler
inputCols = ['Pclass', 'Age', 'Fare', 'Gender', 'Boarded']
outputCol = "features"
vector_assembler = VectorAssembler(inputCols=inputCols, outputCol=outputCol)

# Stage 4: Estimator (Model)
dt_model = RandomForestClassifier(labelCol="Survived", featuresCol="features")

#--- 3.3 Execute Pipeline  ---
# Setup the pipeline
pipeline = Pipeline(stages=[Sex_indexer, Embarked_indexer, vector_assembler, dt_model])

# Fit the pipeline model on training data
final_pipeline = pipeline.fit(train_df)

# Predict on test data
test_predictions_from_pipeline = final_pipeline.transform(test_df)
test_predictions_from_pipeline.show(5, truncate=False)

spark.stop()