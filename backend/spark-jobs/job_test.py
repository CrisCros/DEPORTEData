# Job Test — Verifica que spark-submit conecta al cluster.
# Calcula Pi con Monte Carlo. No necesita S3 ni RDS.

import random
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DEPORTEData_Test_Connection").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

sc = spark.sparkContext
NUM_SAMPLES = 1_000_000

def inside(p):
    x, y = random.random(), random.random()
    return x * x + y * y < 1

count = sc.parallelize(range(NUM_SAMPLES)).filter(inside).count()
pi_estimate = 4.0 * count / NUM_SAMPLES

print(f"Workers usados: {sc.defaultParallelism}")
print(f"Pi = {pi_estimate}")

spark.stop()
