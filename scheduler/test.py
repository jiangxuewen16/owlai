import json

from hdfs import Client, InsecureClient
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import happybase
from pyspark.sql.types import StructType, IntegerType, StringType

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


@app.route("/hdfs")
def hdfs():
    input_uri = "mongodb://data-cloud-develop:123456@192.168.18.243:27017/hq_data_cloud"
    # spark_conf = SparkConf().setAppName("hdfs").setMaster("spark://t3.dev:7077").set("spark.mongodb.input.uri", input_uri) \
    # .set('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.3') \
    spark_session = SparkSession.builder.master("spark://t3.dev:7077").appName("hdfs") \
        .config("spark.mongodb.input.uri", input_uri) \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.4.1') \
        .getOrCreate()

    pipeline = "[{'$match': {'u_id': 1}}]"
    result = spark_session.read.format('com.mongodb.spark.sql.DefaultSource').option("collection", "c_area").load()
    collect = result.collect()
    sc = spark_session.sparkContext

    data = sc.parallelize(collect).filter(lambda x: x['area_type'] == "1").map(lambda x: {x['area_id']: x['area_name']})
    data.repartition(1).saveAsTextFile("hdfs://t3.dev:9000/huiqu/common/area.txt")

    result = data.collect()
    spark_session.stop()
    return {"data": result}
    # print(type(collect))
    # result.show()


@app.route("/data")
def get_data():
    client = Client("http://t3.dev:50070", "hadoop")
    # client = InsecureClient(url="http://t3.dev:50070", user="hadoop", root="/")
    print(client.list("/huiqu/common/area.txt"))
    with client.read("/huiqu/common/area.txt/part-00000") as read:
        # print(read.read().decode('utf8'))
        return {"data": read.read().decode('utf8')}


@app.route("/hbase")
def hbase():
    host = 't3.dev'
    # table name
    table = 'test'
    # 建立spark连接
    spark = SparkSession.builder.master("spark://t3.dev:7077").appName("test") \
        .getOrCreate()

    connection = happybase.Connection(host)
    table = connection.table(table)

    # table.put(b'1234', {b'family:qual1': b'value1',
    #                        b'family:qual2': b'value2'})
    table.batch()

    row = table.row('1234')
    print(row)
    print(row[b'uname:'])

