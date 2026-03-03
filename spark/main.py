from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("Pagila PySpark Docker") \
    .getOrCreate()
\
spark.sparkContext.setLogLevel("ERROR")

def read_table(table_name):
    return spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://db:5432/postgres") \
        .option("dbtable", table_name) \
        .option("user", "postgres") \
        .option("password", "123456") \
        .option("driver", "org.postgresql.Driver") \
        .load()

df_actor = read_table("actor")
df_film = read_table("film")
df_film_actor = read_table("film_actor")
df_category = read_table("category")
df_film_category = read_table("film_category")
df_rental = read_table("rental")
df_inventory = read_table("inventory")
df_payment = read_table("payment")
df_city = read_table("city")
df_address = read_table("address")
df_customer = read_table("customer")


print("\nTask 1")
q1 = df_category.join(df_film_category, "category_id") \
    .groupBy("name") \
    .agg(F.count("film_id").alias("films_count")) \
    .orderBy(F.col("films_count").desc())
q1.show()

print("Task 2")
q2 = df_rental.join(df_inventory, "inventory_id") \
    .join(df_film_actor, "film_id") \
    .join(df_actor, "actor_id") \
    .groupBy("actor_id", "first_name", "last_name") \
    .agg(F.count("rental_id").alias("rental_count")) \
    .orderBy(F.col("rental_count").desc()) \
    .limit(10)
q2.show()

print("Task 3")
q3 = df_payment.join(df_rental, "rental_id") \
    .join(df_inventory, "inventory_id") \
    .join(df_film_category, "film_id") \
    .join(df_category, "category_id") \
    .groupBy("name") \
    .agg(F.sum("amount").alias("total_sales")) \
    .orderBy(F.col("total_sales").desc()) \
    .limit(1)
q3.show()

print("Task 4")
q4 = df_film.join(df_inventory, "film_id", "left_anti") \
    .select("title")
q4.show(truncate=False)

print("Task 5")
df_children_stats = df_actor.join(df_film_actor, "actor_id") \
    .join(df_film_category, "film_id") \
    .join(df_category, "category_id") \
    .filter(F.col("name") == "Children") \
    .groupBy("actor_id", "first_name", "last_name") \
    .agg(F.count("film_id").alias("films_count"))

window_spec = Window.orderBy(F.col("films_count").desc())

q5 = df_children_stats \
    .withColumn("rank", F.dense_rank().over(window_spec)) \
    .filter(F.col("rank") <= 3) \
    .select("first_name", "last_name", "films_count", "rank")
q5.show()

print("Task 6")
q6 = df_city.join(df_address, "city_id") \
    .join(df_customer, "address_id") \
    .groupBy("city") \
    .agg(
        F.sum(F.when(F.col("active") == 1, 1).otherwise(0)).alias("active_customers"),
        F.sum(F.when(F.col("active") == 0, 1).otherwise(0)).alias("inactive_customers")
    ) \
    .orderBy(F.col("inactive_customers").desc())
q6.show()

print("Task 7")
base_df = df_city.join(df_address, "city_id") \
    .join(df_customer, "address_id") \
    .join(df_rental, "customer_id") \
    .join(df_inventory, "inventory_id") \
    .join(df_film_category, "film_id") \
    .join(df_category, "category_id") \
    .filter((F.col("city").rlike("^a|^A")) | (F.col("city").contains("-"))) \
    .withColumn("hours", (F.col("return_date").cast("long") - F.col("rental_date").cast("long")) / 3600)

df_starts_a = base_df.filter(F.col("city").rlike("^a|^A")) \
    .groupBy("name") \
    .agg(F.round(F.sum("hours"), 2).alias("total_hours")) \
    .orderBy(F.col("total_hours").desc()) \
    .limit(1)

df_has_hyphen = base_df.filter(F.col("city").contains("-")) \
    .groupBy("name") \
    .agg(F.round(F.sum("hours"), 2).alias("total_hours")) \
    .orderBy(F.col("total_hours").desc()) \
    .limit(1)

q7 = df_starts_a.union(df_has_hyphen)
q7.show()

spark.stop()