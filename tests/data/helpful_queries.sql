

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




select tsrv."ValueDateTime",tsrv."DataValue", v."VariableCode", u."UnitsName"
from "ODM2Simulation"."Simulations" as s
join "ODM2Core"."Actions" a on a."ActionID" = s."ActionID"
join "ODM2Core"."FeatureActions" fa on fa."ActionID" = a."ActionID"
join "ODM2Core"."Results" r on r."FeatureActionID" = fa."FeatureActionID"
join "ODM2Core"."Variables" v on v."VariableID" = r."VariableID"
join "ODM2Core"."Units" u on u."UnitsID" = r."UnitsID"
join "ODM2Results"."TimeSeriesResultValues" tsrv on tsrv."ResultID" = r."ResultID"
where s."SimulationName" = 'SWMM' and r."ResultID" = 159;