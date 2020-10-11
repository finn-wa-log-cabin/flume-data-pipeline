# Table Design

The table is modelled so that queries from the UI can be executed as efficiently as possible. I anticipate that the sensors will upload telemetry hourly, and that the charts in the UI will want the following data:

| Date Range | Granularity |
|------------|-------------|
| 1 week     | Hourly      |
| 1 month    | Daily       |
| 1 year     | Weekly      |

The [Azure table storage design guidelines](https://docs.microsoft.com/en-us/azure/storage/tables/table-storage-design-for-query) state that these are the most efficient queries:

- A Point Query is the most efficient lookup to use and is recommended to be used for high-volume lookups or lookups requiring lowest latency. Such a query can use the indexes to locate an individual entity very efficiently by specifying both the PartitionKey and RowKey values. For example: `$filter=(PartitionKey eq 'Sales') and (RowKey eq '2')`
- Second best is a Range Query that uses the PartitionKey and filters on a range of RowKey values to return more than one entity. The PartitionKey value identifies a specific partition, and the RowKey values identify a subset of the entities in that partition. For example: `$filter=PartitionKey eq 'Sales' and RowKey ge 'S' and RowKey lt 'T'`

I plan to insert data row-by-row into an hourly partition, and then use scheduled functions to aggregate the data into daily and weekly partitions.

## Table Model: water-tank-monitor-data

Each device will have a series of partitions, named using a compound key in the format `DeviceID_Granularity`.

### Partition 1: DeviceID_raw

The partition in which telemetry data is first inserted. It is called "Raw" instead of "Hourly" in case the upload rate ends up being different.

- Key format: Unix timestamp
- Value format: `{ depth: number }`

### Partition 2: DeviceID_daily

A function will run daily to populate this table from DeviceID_raw.

- Key format: date int (e.g. 20201011)
- Value format: ` { averageDepth: number }`

### Partition 3: DeviceID_weekly

A function will run weekly to populate this table from DeviceID_raw.

- Key format: date int (e.g. 20201011)
- Value format: ` { averageDepth: number }`