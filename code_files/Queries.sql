

CREATE TABLE top_25_countries AS SELECT a.*,
    b.Total_population,
    (Bovine_meat + Poultry_meat + Pigmeat + Mutton_Goat + Meat_Other) AS TOTAL,
    (Bovine_meat + Poultry_meat + Pigmeat + Mutton_Goat + Meat_Other) * b.Total_population AS Total_Meat_Consumption FROM
    EGS.`per-capita-meat-consumption-by-type-kilograms-per-year` a
        JOIN
    egs.`population_year_17` b ON a.Year = b.Year AND a.Entity = b.Entity
ORDER BY Year DESC , Total_Meat_Consumption DESC
LIMIT 25;

----------------------------------------------------------------------------

SELECT 
    *
FROM
    top_25_countries;

----------------------------------------------------------------------------

CREATE TABLE top_countries AS SELECT a.*,
    b.Total_population,
    (Bovine_meat + Poultry_meat + Pigmeat + Mutton_Goat + Meat_Other) AS TOTAL,
    (Bovine_meat + Poultry_meat + Pigmeat + Mutton_Goat + Meat_Other) * b.Total_population AS Total_Meat_Consumption FROM
    EGS.`per-capita-meat-consumption-by-type-kilograms-per-year` a
        JOIN
    egs.`population_year_17` b ON a.Year = b.Year AND a.Entity = b.Entity
ORDER BY Year DESC , Total_Meat_Consumption DESC;

----------------------------------------------------------------------------


SELECT 
    *
FROM
    top_countries;



----------------------------------------------------------------------------

CREATE TABLE top_25_countries_CO2
AS 
SELECT a.*, a.`Per capita CO2 emissions`*b.Total_population AS Total_CO2_emission, b.Total_population
FROM EGS.`co-emissions-per-capita` a,
EGS.population_total b
WHERE a.Year = b.Year
AND a.Entity = b.Entity
AND a.entity in (SELECT c.Entity from EGS.`top_25_countries` c);



----------------------------------------------------------------------------

CREATE TABLE total_meat_consumption_per_year_top_25 AS SELECT a.*,
    (a.Bovine_meat + a.Poultry_meat + a.Pigmeat + a.Mutton_Goat + a.Meat_Other) AS TOTAL_meat_consumed_per_capita,
    c.Total_population,
    (a.Bovine_meat + a.Poultry_meat + a.Pigmeat + a.Mutton_Goat + a.Meat_Other) * c.Total_population AS Total_Meat_Consumption FROM
    EGS.`per-capita-meat-consumption-by-type-kilograms-per-year` a,
    EGS.`population_total` c
WHERE
    a.Entity = c.Entity AND a.Year = c.Year
        AND a.Entity IN (SELECT 
            b.Entity
        FROM
            EGS.`top_25_countries` b);

----------------------------------------------------------------------------

ALTER TABLE EGS.total_meat_consumption_per_year_top_25 ADD COLUMN month VARCHAR(50);

ALTER TABLE EGS.total_meat_consumption_per_year_top_25 ADD COLUMN dates VARCHAR(100);


UPDATE EGS.total_meat_consumption_per_year_top_25 
SET 
    month = 'January';

UPDATE EGS.total_meat_consumption_per_year_top_25 
SET 
    dates = CONCAT(month, '-', Year);

----------------------------------------------------------------------------


CREATE TABLE EGS.top_25_meat_consumption AS SELECT Entity, Code, Year, month, dates, Total_Meat_Consumption FROM
    EGS.total_meat_consumption_per_year_top_25;


----------------------------------------------------------------------------


CREATE TABLE top_25_countries_CO2_vs_meat AS SELECT b.*,
    a.`Per capita CO2 emissions`,
    a.Total_CO2_emission FROM
    EGS.top_25_countries_CO2 a,
    EGS.total_meat_consumption_per_year_top_25 b
WHERE
    a.Year = b.Year AND a.Entity = b.Entity;

----------------------------------------------------------------------------

SELECT 
    *
FROM
    EGS.top_25_countries_CO2_vs_meat;

----------------------------------------------------------------------------




CREATE TABLE top_25_countries_land_use AS
SELECT (a.Bovine_meat * b.Bovine_meat + a.Meat_Other * b.Meat_Other + b.Mutton_Goat * a.Mutton_Goat + a.Pigmeat * b.Pigmeat + a.Poultry_meat * b.Poultry_meat) per_capita_land_use,
    (a.Bovine_meat * b.Bovine_meat + a.Meat_Other * b.Meat_Other + b.Mutton_Goat * a.Mutton_Goat + a.Pigmeat * b.Pigmeat + a.Poultry_meat * b.Poultry_meat)*b.Total_population Total_land_use,
    b.* FROM
    EGS.`land-use-protein-poore_mod` a,
    EGS.total_meat_consumption_per_year_top_25 b
WHERE
    1 = 1;

----------------------------------------------------------------------------

SELECT 
    *
FROM
    EGS.`land-use-protein-poore_mod`;

----------------------------------------------------------------------------



CREATE TABLE top_25_countries_fresh_water_use AS 
SELECT (a.Bovine_meat * b.Bovine_meat + b.Mutton_Goat * a.Mutton_Goat + a.Pigmeat * b.Pigmeat + a.Poultry_meat * b.Poultry_meat) per_capita_water_use,
    (a.Bovine_meat * b.Bovine_meat + a.Meat_Other * b.Meat_Other + b.Mutton_Goat * a.Mutton_Goat + a.Pigmeat * b.Pigmeat + a.Poultry_meat * b.Poultry_meat)*b.Total_population Total_water_use,
    b.* FROM
    EGS.`water-per-tonne-food_mod` a,
    EGS.total_meat_consumption_per_year_top_25 b
WHERE
    1 = 1;
    
----------------------------------------------------------------------------


SELECT 
    *
FROM
    EGS.`water-per-tonne-food_mod`;


----------------------------------------------------------------------------


--query to get top 10 countries


CREATE TABLE top_25_countries_CO2_land_water AS 
SELECT b.Entity,
    b.year,
    Total_CO2_emission,
    total_land_use,
    Total_water_use FROM
    EGS.top_25_countries_CO2 a,
    EGS.top_25_countries_fresh_water_use b,
    EGS.top_25_countries_land_use c
WHERE
    b.Entity = c.Entity
        AND a.Entity = b.Entity
        AND a.year = b.year
        AND b.year = c.year
        AND b.year > 2016
ORDER BY 3 DESC , 4 DESC , 5 DESC;

----------------------------------------------------------------------------


SELECT 
    Entity
FROM
    (SELECT 
        *
    FROM
        EGS.`per-capita-meat-consumption-by-type-kilograms-per-year`
    ORDER BY 3 DESC , 4 DESC , 5 DESC , 6 DESC , 7 DESC , 8 DESC) a;

----------------------------------------------------------------------------

SELECT 
    *
FROM
    EGS.`per-capita-meat-consumption-by-type-kilograms-per-year`
ORDER BY 3 DESC , 4 DESC , 5 DESC , 6 DESC , 7 DESC , 8 DESC;

----------------------------------------------------------------------------

SELECT 
    *,
    (Bovine_meat + Poultry_meat + Pigmeat + Mutton_Goat + Meat_Other) AS TOTAL
FROM
    EGS.`per-capita-meat-consumption-by-type-kilograms-per-year`
ORDER BY 3 DESC , 9 DESC;

----------------------------------------------------------------------------

SELECT 
    *
FROM
    top_25_countries
ORDER BY Total_Country_Pop DESC


----------------------------------------------------------------------------




SELECT a.Total_Meat_Consumption,b.Total_Meat_Consumption,
c.Total_Meat_Consumption,d.Total_Meat_Consumption,
a.dates,a.Entity,a.Total_Meat_Consumption,b.Year, b.Total_CO2_emission,
b.Total_population,c.Total_land_use,c.Year,d.Total_water_use
FROM EGS.`china predicted` a
LEFT JOIN EGS.top_25_countries_CO2_vs_meat b
ON Year(a.dates) = b.Year
and a.Entity = b.Entity
LEFT JOIN EGS.top_25_countries_land_use c
ON Year(a.dates) = c.Year
and a.Entity = c.Entity
LEFT JOIN EGS.top_25_countries_fresh_water_use d
ON Year(a.dates) = d.Year
and a.Entity = d.Entity;




----------------------------------------------------------------------------


CREATE TABLE top_25_countries_predictions
as
SELECT a.Entity,a.Year,a.Total_population,a.Total_Meat_Consumption Total_Meat_Consumption,
Total_water_use,Total_land_use,Total_CO2_emission
FROM EGS.top_25_countries_CO2_vs_meat a
INNER JOIN EGS.top_25_countries_land_use c
ON A.YEAR = c.Year
and a.Entity = c.Entity
INNER JOIN EGS.top_25_countries_fresh_water_use d
ON a.Year = d.Year
and a.Entity = d.Entity;


----------------------------------------------------------------------------

SELECT * FROM EGS.top_25_countries_predictions;



----------------------------------------------------------------------------



CREATE TABLE meat_type
as 
SELECT Entity,bovine_meat*Total_population Beef,poultry_meat*Total_population Chicken,
pigmeat*Total_population Pig, mutton_goat*Total_population Mutton, meat_other*Total_population Other,
Total_Meat_Consumption
 FROM EGS.total_meat_consumption_per_year_top_25
where year = 2017;

select * from meat_type;





