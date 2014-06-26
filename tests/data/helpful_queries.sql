

-- get results from last two simulations (i.e. modules)
select s."SimulationName", tsv."ValueDateTime", tsv."DataValue"
from "ODM2Core"."Results" as r
join "ODM2Core"."FeatureActions" fa on fa."FeatureActionID" = r."FeatureActionID"
join "ODM2Results"."TimeSeriesResultValues" tsv on tsv."ResultID" = r."ResultID"
join "ODM2Core"."Actions" a on a."ActionID" = fa."ActionID"
join "ODM2Simulation"."Simulations" s on s."ActionID" = a."ActionID"
where a."ActionID" in
(
	select s."ActionID"
	from "ODM2Simulation"."Simulations" s
	order by s."SimulationID" desc
	limit 2
)
order by s."SimulationID" asc
