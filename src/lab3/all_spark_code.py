

from pyspark.sql import SparkSession

# Start SparkSession

spark = SparkSession.builder 
.master("local[*]") 
.appName("Unified-MLlib-Project") 
.getOrCreate()

# ============================================================

# 2. BASIC STATISTICS EXAMPLES (colStats, corr, random data)

# ============================================================

from pyspark import SparkConf, SparkContext
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.stat import Statistics
from pyspark.mllib.random import RandomRDDs

sc = spark.sparkContext

# --- Summary Statistics ---

summary_rdd = sc.parallelize([
Vectors.dense([1.0, 2.0, 3.0]),
Vectors.dense([4.9, 5.0, 6.9]),
Vectors.dense([7.9, 8.8, 9.0])
])

summary = Statistics.colStats(summary_rdd)
print("Summary Statistics")
print("Mean:", summary.mean())
print("Variance:", summary.variance())
print("Non-zero entries:", summary.numNonzeros())

# --- Correlation ---

corr_rdd1 = sc.parallelize([1.0, 2.0, 3.9, 4.8, 5.9])
corr_rdd2 = sc.parallelize([2.0, 2.0, 4.0, 5.0, 6.0])
correlation = Statistics.corr(corr_rdd1.zip(corr_rdd2))
print("Correlation:", correlation)

# --- Random Data ---

random_data = RandomRDDs.normalRDD(sc, 1000)
print("Random sample:", random_data.take(3))

# ============================================================

# 3. TITANIC ML WITHOUT PIPELINE

# ============================================================

# Load Titanic dataset (adjust path)

df = (spark.read.format("csv")
.option("header", "true")
.load("/content/titanic/train.csv"))

from pyspark.sql.functions import col

dataset = df.select(
col("Survived").cast("float"),
col("Pclass").cast("float"),
col("Sex"),
col("Age").cast("float"),
col("Fare").cast("float"),
col("Embarked")
)

# Remove null values

from pyspark.sql.functions import isnull, when, count
dataset = dataset.replace("?", None).dropna()

# StringIndexer transformations

from pyspark.ml.feature import StringIndexer
dataset = StringIndexer(inputCol="Sex", outputCol="Gender", handleInvalid="keep").fit(dataset).transform(dataset)
dataset = StringIndexer(inputCol="Embarked", outputCol="Boarded", handleInvalid="keep").fit(dataset).transform(dataset)

# Drop old columns

dataset = dataset.drop("Sex", "Embarked")

# Create features vector

from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
inputCols=["Pclass", "Age", "Fare", "Gender", "Boarded"],
outputCol="features"
)

data = assembler.transform(dataset)

# Train-test split

train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)

# Train Random Forest (no pipeline)

from pyspark.ml.classification import RandomForestClassifier

rf = RandomForestClassifier(
labelCol="Survived",
featuresCol="features",
maxDepth=5
)

rf_model = rf.fit(train_data)
rf_predictions = rf_model.transform(test_data)

# Evaluate

from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(
labelCol="Survived",
predictionCol="prediction",
metricName="accuracy"
)

print("Titanic Accuracy (No Pipeline):", evaluator.evaluate(rf_predictions))

# ============================================================

# 4. TITANIC WITH PIPELINE

# ============================================================

from pyspark.ml import Pipeline

SEX_indexer = StringIndexer(inputCol="Sex", outputCol="Gender")
EMB_indexer = StringIndexer(inputCol="Embarked", outputCol="Boarded")

pipeline_assembler = VectorAssembler(
inputCols=["Pclass", "Age", "Fare", "Gender", "Boarded"],
outputCol="features"
)

pipeline_rf = RandomForestClassifier(
labelCol="Survived",
featuresCol="features"
)

pipeline = Pipeline(stages=[
SEX_indexer,
EMB_indexer,
pipeline_assembler,
pipeline_rf
])

pipeline_model = pipeline.fit(df.dropna())
pipeline_predictions = pipeline_model.transform(df.dropna())

print("Pipeline Predictions:")
pipeline_predictions.show(5)

# ============================================================

# 5. DEEP LEARNING PIPELINES (sparkdl)

# ============================================================


from sparkdl import readImages, DeepImageFeaturizer

# Example path for images

# image_df = readImages("/content/images")

# deep_featurizer = DeepImageFeaturizer(

# inputCol="image",

# outputCol="features",

# modelName="InceptionV3"

# )

# from pyspark.ml.classification import LogisticRegression

# lr = LogisticRegression(labelCol="label")

# deep_pipeline = Pipeline(stages=[deep_featurizer, lr])

# deep_model = deep_pipeline.fit(train_image_df)