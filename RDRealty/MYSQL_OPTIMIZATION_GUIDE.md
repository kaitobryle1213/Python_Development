# MySQL Optimization Guide for High Volume Data (>50,000 records)

To ensure optimal performance for the RDRealty application as the dataset grows beyond 50,000 records, the following MySQL server configurations are recommended. These settings should be added to your MySQL configuration file (typically `my.cnf` on Linux or `my.ini` on Windows).

## Key Configuration Settings

### 1. InnoDB Buffer Pool Size
This is the most critical setting for InnoDB performance. It determines how much data and indexes are cached in memory.
*   **Recommendation**: Set to **70-80% of available physical RAM** on a dedicated database server.
*   **Example (for a server with 4GB RAM)**:
    ```ini
    [mysqld]
    innodb_buffer_pool_size = 3G
    ```

### 2. InnoDB Log File Size
Larger log files allow for more write operations to be buffered before flushing to disk, which improves write performance (e.g., during bulk imports).
*   **Recommendation**: 25% of buffer pool size or at least **512M**.
*   **Example**:
    ```ini
    innodb_log_file_size = 512M
    ```

### 3. Max Connections
Ensure the server can handle concurrent connections from the web application.
*   **Recommendation**: Depends on traffic, but **200-500** is usually sufficient for mid-sized apps.
*   **Example**:
    ```ini
    max_connections = 300
    ```

### 4. Query Cache (MySQL < 8.0)
If you are using an older version of MySQL (5.7 or older), query cache can help. Note: It is removed in MySQL 8.0.
*   **Recommendation**: Disable it for high-concurrency write workloads, but for read-heavy apps, a small cache helps.
*   **Example**:
    ```ini
    query_cache_type = 1
    query_cache_size = 64M
    ```

### 5. Temporary Tables
Increase the size of in-memory temporary tables to avoid writing to disk during complex sort/group operations.
*   **Example**:
    ```ini
    tmp_table_size = 64M
    max_heap_table_size = 64M
    ```

## Application-Level Optimizations Applied

We have already applied the following optimizations to the Django application:

1.  **Database Indexing**:
    *   Added indexes to frequently filtered fields: `loc_province`, `loc_city`, `loc_barangay`, `oi_fullname`, `date_added`, `title_classification`, `title_status`.
    *   This speeds up search and filtering significantly.

2.  **Pagination**:
    *   Implemented pagination (20 items per page) on the Property List view.
    *   This prevents loading all 50,000+ records into memory at once, drastically reducing server load and page load time.

3.  **Query Optimization**:
    *   Used `prefetch_related` to eliminate N+1 query problems when fetching related data (Owners, Local Info).
    *   This reduces the number of database round-trips from thousands (one per property) to just a few.

## Maintenance Commands

Run these periodically to optimize table storage:
```sql
OPTIMIZE TABLE rdrealty_app_property;
OPTIMIZE TABLE rdrealty_local_information;
OPTIMIZE TABLE rdrealty_owner_information;
```
