# How the current database tables are created.

```
CREATE TABLE BatteryData
(
    PkID_BatteryData INT IDENTITY PRIMARY KEY NOT NULL,
    SerialNumber NVARCHAR(50),
    DateCreated DATETIME DEFAULT SYSUTCDATETIME(),
    BatteryType NVARCHAR(50),
    Status NVARCHAR(50),
    PASS_SBS BIT, -- 1 if corresponding SBS passed the golden file tests, else 0
    PASS_Dataflash BIT -- 1 if corresponding Dataflash passed the golden file tests, else 0
);

CREATE TABLE BatteryDataLine_Dataflash
(
    PkID_BatteryDataLine_Dataflash INT IDENTITY PRIMARY KEY NOT NULL,
    FkID_BatteryData INT,
    CLASS NVARCHAR(50),
    SUBCLASS NVARCHAR(50),
    NAME NVARCHAR(50),
    TYPE NVARCHAR(10),
    MEASURED_VALUE NVARCHAR(100),
    UNIT NVARCHAR(40),
    PASS NVARCHAR(20), -- new column added for PASS status with Not applicable option (True/False/NA)
    FOREIGN KEY (FkID_BatteryData) REFERENCES BatteryData(PkID_BatteryData)
);

CREATE TABLE BatteryDataLine_SBS
(
    PkID_BatteryDataLine_SBS INT IDENTITY PRIMARY KEY NOT NULL,
    FkID_BatteryData INT,
    SBS_CMD NVARCHAR(10),
    NAME NVARCHAR(50),
    MEASURED_VALUE NVARCHAR(100),
    UNIT NVARCHAR(40),
    PASS NVARCHAR(20), -- new column added for PASS status with Not applicable option (True/False/NA)
    FOREIGN KEY (FkID_BatteryData) REFERENCES BatteryData(PkID_BatteryData)
);


CREATE TABLE GoldenFile_BQ4050_Dataflash_test
(
    PkID_GoldenFile_BQ4050_Dataflash_test INT IDENTITY PRIMARY KEY NOT NULL,
    CLASS NVARCHAR(50),
    SUBCLASS NVARCHAR(50),
    NAME NVARCHAR(50),
    CheckType NVARCHAR(10), -- EQUALITY or BOUNDARY
    ExactValue NVARCHAR(100), -- used for EQUALITY checks
    MinBoundary NVARCHAR(100), -- used for BOUNDARY checks
    MaxBoundary NVARCHAR(100), -- used for BOUNDARY checks
    UNIT NVARCHAR(40)
);

CREATE TABLE GoldenFile_BQ3060_Dataflash_test
(
    PkID_GoldenFile_BQ3060_Dataflash_test INT IDENTITY PRIMARY KEY NOT NULL,
    CLASS NVARCHAR(50),
    SUBCLASS NVARCHAR(50),
    NAME NVARCHAR(50),
    CheckType NVARCHAR(10), -- EQUALITY or BOUNDARY
    ExactValue NVARCHAR(100), -- used for EQUALITY checks
    MinBoundary NVARCHAR(100), -- used for BOUNDARY checks
    MaxBoundary NVARCHAR(100), -- used for BOUNDARY checks
    UNIT NVARCHAR(40)
);

CREATE TABLE GoldenFile_BQ78350_Dataflash_test
(
    PkID_GoldenFile_BQ78350_Dataflash_test INT IDENTITY PRIMARY KEY NOT NULL,
    CLASS NVARCHAR(50),
    SUBCLASS NVARCHAR(50),
    NAME NVARCHAR(50),
    CheckType NVARCHAR(10), -- EQUALITY or BOUNDARY
    ExactValue NVARCHAR(100), -- used for EQUALITY checks
    MinBoundary NVARCHAR(100), -- used for BOUNDARY checks
    MaxBoundary NVARCHAR(100), -- used for BOUNDARY checks
    UNIT NVARCHAR(40)
);

CREATE TABLE GoldenFile_BQ4050_SBS_test
(
    PkID_GoldenFile_BQ4050_SBS_test INT IDENTITY PRIMARY KEY NOT NULL,
    NAME NVARCHAR(50),
    CheckType NVARCHAR(10), -- EQUALITY or BOUNDARY
    ExactValue NVARCHAR(100), -- used for EQUALITY checks
    MinBoundary NVARCHAR(100), -- used for BOUNDARY checks
    MaxBoundary NVARCHAR(100), -- used for BOUNDARY checks
    UNIT NVARCHAR(40)
);

CREATE TABLE GoldenFile_BQ3060_SBS_test
(
    PkID_GoldenFile_BQ3060_SBS_test INT IDENTITY PRIMARY KEY NOT NULL,
    NAME NVARCHAR(50),
    CheckType NVARCHAR(10), -- EQUALITY or BOUNDARY
    ExactValue NVARCHAR(100), -- used for EQUALITY checks
    MinBoundary NVARCHAR(100), -- used for BOUNDARY checks
    MaxBoundary NVARCHAR(100), -- used for BOUNDARY checks
    UNIT NVARCHAR(40)
);

CREATE TABLE GoldenFile_BQ78350_SBS_test
(
    PkID_GoldenFile_BQ78350_SBS_test INT IDENTITY PRIMARY KEY NOT NULL,
    NAME NVARCHAR(50),
    CheckType NVARCHAR(10), -- EQUALITY or BOUNDARY
    ExactValue NVARCHAR(100), -- used for EQUALITY checks
    MinBoundary NVARCHAR(100), -- used for BOUNDARY checks
    MaxBoundary NVARCHAR(100), -- used for BOUNDARY checks
    UNIT NVARCHAR(40)
);
```



# How to insert data into the golden files

## dataflash

### Boundary values 
```
INSERT INTO GoldenFile_BQ4050_Dataflash_test (CLASS, SUBCLASS, NAME, CheckType, MinBoundary, MaxBoundary, UNIT)
VALUES ('Permanent Fail', 'SOT', 'Threshold', 'BOUNDARY', '3282', '3482', '0.1°K');
```
How to update:
```
--UPDATE GoldenFile_BQ4050_Dataflash_test 
--SET MinBoundary = '2000', MaxBoundary = '2500', UNIT = '0.1°K'
--WHERE CLASS = 'Permanent Fail' AND SUBCLASS = 'SOT' AND NAME = 'Threshold';
```
### Exact values
```
INSERT INTO GoldenFile_BQ4050_Dataflash_test (CLASS, SUBCLASS, NAME, CheckType, ExactValue, UNIT)
VALUES ('Settings', 'Permanent Failure', 'Enabled PF A', 'EQUALITY', '0x02', '0.1°K');
```

## SBS

### Boundary values 
```
INSERT INTO GoldenFile_BQ4050_SBS_test (NAME, CheckType, MinBoundary, MaxBoundary, UNIT)
VALUES ('Voltage', 'BOUNDARY', '3', '20', 'mV');
```

### Exact values
```
INSERT INTO GoldenFile_BQ4050_SBS_test (NAME, CheckType, ExactValue, UNIT)
VALUES ('Current', 'EQUALITY', '500', 'mA');
```