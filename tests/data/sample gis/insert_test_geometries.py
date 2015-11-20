__author__ = 'tonycastronova'


from osgeo import ogr


test_geoms = ['sample_points_nad83.shp','sample_poly_nad83.shp']
test_codes = ['points_nad83', 'poly_nad83']

# OnOpen the shapefile
driver = ogr.GetDriverByName('ESRI Shapefile')


insert = 'INSERT INTO "ODM2Core"."SamplingFeatures" ("SamplingFeatureTypeCV","SamplingFeatureCode","FeatureGeometry") values \n'
code = 0
for test in test_geoms:
    dataset = driver.Open(test)

    layer = dataset.GetLayer()
    spatialRef = layer.GetSpatialRef()

    geoms = []
    for i in xrange(0,layer.GetFeatureCount()):
        feature = layer.GetNextFeature()
        geom = feature.GetGeometryRef()

        # convert into shapely geometry
        geoms.append(geom.ExportToWkt())




    for i in range(0, len(geoms)):
        insert += '(\'geom\',\'%s\',ST_GeomFromText(\'%s\')),\n' %(test_codes[code] +'_'+ str(i), geoms[i])

    code += 1


print '\n' + 60*'-'
print 'Run the following SQL command to insert the test geometries:'
print 60*'-'
print insert[:-2]+';'



