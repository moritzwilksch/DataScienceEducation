#%%
import duckdb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import polars as pl
import seaborn as sns

df = pl.scan_parquet("data/fhvhv_2022-06.parquet")
taxi_zones = pl.scan_csv("data/taxi_zones.csv")

#%%
###################### Data Preprocessing ######################


def join_taxi_zone_names(data: pl.DataFrame, taxi_zones: pl.DataFrame) -> pl.DataFrame:
    """Join the names of the taxi zones"""
    return data.join(
        taxi_zones.select(pl.col("*").prefix("PU_")),
        left_on="PULocationID",
        right_on="PU_LocationID",
        how="left",
        suffix="_PU",
    )


def drop_columns(data: pl.DataFrame) -> pl.DataFrame:
    """Drop unused columns"""
    UNUSED = [
        "hvfhs_license_num",
        "dispatching_base_num",
        "originating_base_num",
        "access_a_ride_flag",
        "wav_request_flag",
        "wav_match_flag",
    ]
    return data.drop(UNUSED)


def fix_dtypes(data: pl.DataFrame) -> pl.DataFrame:
    """Fix categorical and datetime dtypes"""
    CATEGORICALS = [
        "shared_request_flag",
        "shared_match_flag",
        "PU_Borough",
        "PU_Zone",
        "PU_service_zone",
    ]

    data = data.with_columns(
        [
            pl.col(CATEGORICALS).cast(pl.Categorical),
            # (pl.col("trip_time") * 1000).cast(pl.Duration(time_unit="ms")),
        ]
    )
    return data


def feature_engineering(data: pl.DataFrame) -> pl.DataFrame:
    """Add some features"""
    return data.with_columns(
        [
            (pl.col("on_scene_datetime") - pl.col("request_datetime")).alias(
                "time_to_scene"
            ),
            (pl.col("trip_miles") / (pl.col("trip_time") / 60 / 60)).alias("avg_mph"),
        ]
    )


def remove_outliers(data: pl.DataFrame) -> pl.DataFrame:
    """Quantile-based outlier rm."""
    # Judgement call: we want to model the "normal" cab rides and ignore severe outliers – we will always underestimate them
    data = data.collect()
    len_pre = data.height

    data = data.filter(
        (pl.col("trip_miles") <= pl.col("trip_miles").quantile(0.999))
        & (pl.col("trip_time") <= pl.col("trip_time").quantile(0.999))
    )

    len_post = data.height
    print(
        f"Outlier removal: dropped {len_pre - len_post} rows ({(len_pre - len_post) / len_pre:.4%})"
    )
    return data.lazy()


clean: pd.DataFrame = (
    df.pipe(join_taxi_zone_names, taxi_zones)
    .pipe(drop_columns)
    .pipe(fix_dtypes)
    .pipe(feature_engineering)
    .pipe(remove_outliers)
    .collect()
).to_pandas()

#%%
plotdf = (
    (
        clean.groupby("PU_Zone")["time_to_scene"]
        .mean()
        .sort_values(ascending=False)
        .dt.total_seconds()
        / 60
    )
    .head(25)
    .sort_values()
)
plt.barh(y=plotdf.index, width=plotdf)

#%%

plt.hist(clean["trip_miles"], bins=100, log=False)

#%%
plotdf = clean.groupby(clean["pickup_datetime"].dt.date)["driver_pay"].mean()
fig, ax = plt.subplots(figsize=(15, 5))
# sns.lineplot(data=clean, x="pickup_datetime", y="driver_pay", ci=None, ax=ax)
plotdf.to_frame().plot(ax=ax )
