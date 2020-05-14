from pyspark.mllib.tree import DecisionTree
from pyspark.sql import SparkSession

from app import app
from core import utils, config

from core import dbengine


@app.route('/')
def hello_world():
    print(dir(dbengine))
    return {"name": config.get_config("APP_NAME"), "age": 12}

@app.route('/mongo')
def spark():
    input_uri = "mongodb://nlp_admin:123456@127.0.0.1:27017/nlp"
    output_uri = "mongodb://nlp_admin:123456@127.0.0.1:27017/nlp"

    spark_session = SparkSession.builder.master("local").appName("mongo-test") \
        .config("spark.mongodb.input.uri", input_uri) \
        .config("spark.mongodb.output.uri", output_uri) \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.3') \
        .getOrCreate()

    pipeline = "[{'$match': {'u_id': 1}}]"
    # pipeline = "[{'$project': {'_id': -1}},{'$match': {'u_id': 1}}]"
    result = spark_session.read.format('com.mongodb.spark.sql.DefaultSource').option("collection", "nlp_user").option(
        "pipeline", pipeline).load()

    collect = result.collect()
    print(collect)
    # DecisionTree.trainClassifier(data=collect, numClasses=2, categoricalFeaturesInfo={0: 3})

    result.show()
    spark.stop()